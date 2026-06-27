#!/usr/bin/env python3
"""Minimal Relinium SSOT validator.

This v0.1 validator intentionally starts with the Event Kernel because it is
the current audit backbone: every targeted file event must parse, point inside
ssot-root, and match the declared SHA-256.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REQUIRED_EVENT_FIELDS = {
    "id": str,
    "kind": str,
    "event_type": str,
    "timestamp": str,
    "tenant_id": str,
    "actor_human": str,
    "actor_agent": str,
    "hash_sha256": str,
    "genesis": bool,
    "comment": str,
}

ALLOWED_EVENT_KINDS = {
    "schema_event",
    "crypto_event",
    "policy_event",
    "ingestion_event",
    "evidence_event",
    "analysis_event",
}

EVENT_ID_RE = re.compile(r"^[A-Z0-9-]+$")
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
UTC_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


@dataclass(frozen=True)
class Finding:
    severity: str
    location: str
    code: str
    message: str
    stream_path: str | None = None
    line_number: int | None = None
    event_id: str | None = None
    raw_line_sha256: str | None = None

    def format(self) -> str:
        return f"{self.severity}: {self.location}: {self.message}"


@dataclass(frozen=True)
class BaselineEntry:
    stream_path: str
    line: int
    code: str
    event_id: str | None
    message_fragment: str
    raw_line_sha256: str

    def matches(self, finding: Finding) -> bool:
        return (
            finding.stream_path == self.stream_path
            and finding.line_number == self.line
            and finding.code == self.code
            and finding.event_id == self.event_id
            and finding.raw_line_sha256 == self.raw_line_sha256
            and self.message_fragment in finding.message
        )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_safe_relative_path(value: str) -> bool:
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def rel_path(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def line_finding(
    ssot_root: Path,
    stream: Path,
    line_number: int,
    raw_line: bytes,
    code: str,
    message: str,
    event_id: str | None = None,
) -> Finding:
    stream_path = rel_path(stream, ssot_root)
    return Finding(
        "ERROR",
        f"{stream}:{line_number}",
        code,
        message,
        stream_path=stream_path,
        line_number=line_number,
        event_id=event_id,
        raw_line_sha256=sha256_bytes(raw_line),
    )


def validate_event_stream(ssot_root: Path, stream: Path) -> Iterable[Finding]:
    if not stream.exists():
        yield Finding("ERROR", str(stream), "EVENT_STREAM_MISSING", "event stream does not exist")
        return

    seen_ids: set[str] = set()

    with stream.open("rb") as handle:
        for line_number, raw_line in enumerate(handle, 1):
            try:
                decoded_line = raw_line.decode("utf-8")
            except UnicodeDecodeError as exc:
                yield line_finding(
                    ssot_root,
                    stream,
                    line_number,
                    raw_line,
                    "EVENT_LINE_INVALID_UTF8",
                    f"line is not valid UTF-8: {exc.reason}",
                )
                continue

            line = decoded_line.strip()

            if not line or line.startswith("#"):
                continue

            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                yield line_finding(
                    ssot_root,
                    stream,
                    line_number,
                    raw_line,
                    "EVENT_JSON_INVALID",
                    f"invalid JSON: {exc.msg}",
                )
                continue

            if not isinstance(event, dict):
                yield line_finding(
                    ssot_root,
                    stream,
                    line_number,
                    raw_line,
                    "EVENT_NOT_OBJECT",
                    "event must be a JSON object",
                )
                continue

            event_id = event.get("id") if isinstance(event.get("id"), str) else None

            for field, expected_type in REQUIRED_EVENT_FIELDS.items():
                if field not in event:
                    yield line_finding(
                        ssot_root,
                        stream,
                        line_number,
                        raw_line,
                        "EVENT_REQUIRED_FIELD_MISSING",
                        f"missing required field {field!r}",
                        event_id,
                    )
                    continue
                if not isinstance(event[field], expected_type):
                    yield line_finding(
                        ssot_root,
                        stream,
                        line_number,
                        raw_line,
                        "EVENT_REQUIRED_FIELD_TYPE",
                        f"field {field!r} has invalid type",
                        event_id,
                    )

            if isinstance(event_id, str):
                if not EVENT_ID_RE.fullmatch(event_id):
                    yield line_finding(
                        ssot_root,
                        stream,
                        line_number,
                        raw_line,
                        "EVENT_ID_FORMAT",
                        f"invalid event id {event_id!r}",
                        event_id,
                    )
                if event_id in seen_ids:
                    yield line_finding(
                        ssot_root,
                        stream,
                        line_number,
                        raw_line,
                        "EVENT_ID_DUPLICATE",
                        f"duplicate event id {event_id!r}",
                        event_id,
                    )
                seen_ids.add(event_id)

            kind = event.get("kind")
            if isinstance(kind, str) and kind not in ALLOWED_EVENT_KINDS:
                yield line_finding(
                    ssot_root,
                    stream,
                    line_number,
                    raw_line,
                    "EVENT_KIND_INVALID",
                    f"invalid event kind {kind!r}",
                    event_id,
                )

            timestamp = event.get("timestamp")
            if isinstance(timestamp, str) and not UTC_TIMESTAMP_RE.fullmatch(timestamp):
                yield line_finding(
                    ssot_root,
                    stream,
                    line_number,
                    raw_line,
                    "EVENT_TIMESTAMP_FORMAT",
                    "timestamp must be UTC RFC3339 without fractional seconds",
                    event_id,
                )

            declared_hash = event.get("hash_sha256")
            if isinstance(declared_hash, str) and not SHA256_RE.fullmatch(declared_hash):
                yield line_finding(
                    ssot_root,
                    stream,
                    line_number,
                    raw_line,
                    "EVENT_HASH_SHA256_FORMAT",
                    "hash_sha256 must be 64 lowercase hex characters",
                    event_id,
                )

            target = event.get("path")
            if target is None:
                continue
            if not isinstance(target, str):
                yield line_finding(
                    ssot_root,
                    stream,
                    line_number,
                    raw_line,
                    "EVENT_PATH_TYPE",
                    "path must be a string when present",
                    event_id,
                )
                continue
            if not is_safe_relative_path(target):
                yield line_finding(
                    ssot_root,
                    stream,
                    line_number,
                    raw_line,
                    "EVENT_PATH_UNSAFE",
                    f"unsafe path {target!r}",
                    event_id,
                )
                continue

            target_path = ssot_root / target
            if not target_path.exists():
                yield line_finding(
                    ssot_root,
                    stream,
                    line_number,
                    raw_line,
                    "EVENT_TARGET_MISSING",
                    f"target file does not exist: {target}",
                    event_id,
                )
                continue
            if not target_path.is_file():
                yield line_finding(
                    ssot_root,
                    stream,
                    line_number,
                    raw_line,
                    "EVENT_TARGET_NOT_FILE",
                    f"target path is not a file: {target}",
                    event_id,
                )
                continue
            if isinstance(declared_hash, str) and SHA256_RE.fullmatch(declared_hash):
                actual_hash = sha256_file(target_path)
                if actual_hash != declared_hash:
                    yield line_finding(
                        ssot_root,
                        stream,
                        line_number,
                        raw_line,
                        "EVENT_TARGET_HASH_MISMATCH",
                        f"hash mismatch for {target}: declared {declared_hash}, actual {actual_hash}",
                        event_id,
                    )


def discover_event_streams(ssot_root: Path) -> list[Path]:
    streams_dir = ssot_root / "event_kernel" / "streams"
    if not streams_dir.exists():
        return []
    return sorted(streams_dir.glob("*/events_raw.ndjson"))


def load_baseline(path: Path) -> tuple[list[BaselineEntry], list[Finding]]:
    errors: list[Finding] = []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [], [Finding("ERROR", str(path), "BASELINE_MISSING", "baseline file does not exist")]
    except json.JSONDecodeError as exc:
        return [], [Finding("ERROR", str(path), "BASELINE_JSON_INVALID", f"invalid baseline JSON: {exc.msg}")]

    if not isinstance(data, dict):
        return [], [Finding("ERROR", str(path), "BASELINE_INVALID", "baseline must be a JSON object")]

    raw_findings = data.get("findings")
    if not isinstance(raw_findings, list):
        return [], [Finding("ERROR", str(path), "BASELINE_INVALID", "baseline findings must be a list")]

    entries: list[BaselineEntry] = []
    for index, item in enumerate(raw_findings, 1):
        location = f"{path}:findings[{index}]"
        if not isinstance(item, dict):
            errors.append(Finding("ERROR", location, "BASELINE_INVALID", "baseline entry must be an object"))
            continue

        stream_path = item.get("stream_path")
        line = item.get("line")
        code = item.get("code")
        event_id = item.get("event_id")
        message_fragment = item.get("message_fragment")
        raw_line_sha256 = item.get("raw_line_sha256")

        if not isinstance(stream_path, str) or not is_safe_relative_path(stream_path):
            errors.append(Finding("ERROR", location, "BASELINE_INVALID", "stream_path must be a safe relative path"))
            continue
        if not isinstance(line, int) or line < 1:
            errors.append(Finding("ERROR", location, "BASELINE_INVALID", "line must be a positive integer"))
            continue
        if not isinstance(code, str) or not code:
            errors.append(Finding("ERROR", location, "BASELINE_INVALID", "code must be a non-empty string"))
            continue
        if event_id is not None and not isinstance(event_id, str):
            errors.append(Finding("ERROR", location, "BASELINE_INVALID", "event_id must be a string or null"))
            continue
        if not isinstance(message_fragment, str) or not message_fragment:
            errors.append(Finding("ERROR", location, "BASELINE_INVALID", "message_fragment must be a non-empty string"))
            continue
        if not isinstance(raw_line_sha256, str) or not SHA256_RE.fullmatch(raw_line_sha256):
            errors.append(Finding("ERROR", location, "BASELINE_INVALID", "raw_line_sha256 must be 64 lowercase hex characters"))
            continue

        entries.append(
            BaselineEntry(
                stream_path=stream_path,
                line=line,
                code=code,
                event_id=event_id,
                message_fragment=message_fragment,
                raw_line_sha256=raw_line_sha256,
            )
        )

    return entries, errors


def apply_baseline(findings: list[Finding], baseline: list[BaselineEntry]) -> tuple[list[Finding], int]:
    unmatched_findings: list[Finding] = []
    matched_baseline_indexes: set[int] = set()

    for finding in findings:
        match_index = next(
            (
                index
                for index, entry in enumerate(baseline)
                if index not in matched_baseline_indexes and entry.matches(finding)
            ),
            None,
        )
        if match_index is None:
            unmatched_findings.append(finding)
        else:
            matched_baseline_indexes.add(match_index)

    for index, entry in enumerate(baseline):
        if index in matched_baseline_indexes:
            continue
        unmatched_findings.append(
            Finding(
                "ERROR",
                f"{entry.stream_path}:{entry.line}",
                "BASELINE_STALE",
                f"baseline entry no longer matches an active finding: {entry.code}",
            )
        )

    return unmatched_findings, len(matched_baseline_indexes)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate minimal Relinium SSOT invariants.")
    parser.add_argument(
        "--ssot-root",
        default=Path(__file__).resolve().parents[2],
        type=Path,
        help="Path to ssot-root. Defaults to the repository ssot-root.",
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        help="Path to a strict known-findings baseline JSON file.",
    )
    args = parser.parse_args(argv)

    ssot_root = args.ssot_root.resolve()
    findings: list[Finding] = []

    if not ssot_root.exists():
        findings.append(Finding("ERROR", str(ssot_root), "SSOT_ROOT_MISSING", "ssot-root does not exist"))
    elif not ssot_root.is_dir():
        findings.append(Finding("ERROR", str(ssot_root), "SSOT_ROOT_NOT_DIRECTORY", "ssot-root is not a directory"))
    else:
        streams = discover_event_streams(ssot_root)
        if not streams:
            findings.append(Finding("ERROR", str(ssot_root), "EVENT_STREAMS_NOT_FOUND", "no event streams found"))
        for stream in streams:
            findings.extend(validate_event_stream(ssot_root, stream))

    matched_baseline_count = 0
    if args.baseline:
        baseline_path = args.baseline
        if not baseline_path.is_absolute():
            baseline_path = (Path.cwd() / baseline_path).resolve()
        baseline, baseline_errors = load_baseline(baseline_path)
        findings.extend(baseline_errors)
        if not baseline_errors:
            findings, matched_baseline_count = apply_baseline(findings, baseline)

    if findings:
        for finding in findings:
            print(finding.format(), file=sys.stderr)
        print(f"Validation failed: {len(findings)} finding(s).", file=sys.stderr)
        return 1

    if args.baseline:
        print(f"Validation passed: minimal SSOT checks succeeded ({matched_baseline_count} baseline finding(s) accepted).")
        return 0

    print("Validation passed: minimal SSOT checks succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
