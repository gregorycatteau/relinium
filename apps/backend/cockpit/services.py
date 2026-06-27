from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from types import ModuleType
from typing import Any

from django.conf import settings


SSOT_ROOT: Path = settings.SSOT_ROOT
REPO_ROOT: Path = settings.REPO_ROOT
VALIDATOR_PATH = SSOT_ROOT / "core" / "scripts" / "validate_documents.py"
KNOWN_FINDINGS_PATH = SSOT_ROOT / "core" / "validation" / "known_findings.json"
PROTECTED_PREFIXES = ("personal_vault/", "vault_index/", "users/user_template/")


def load_validator() -> ModuleType:
    module_name = "relinium_core_validate_documents"
    if module_name in sys.modules:
        return sys.modules[module_name]

    spec = importlib.util.spec_from_file_location(module_name, VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator from {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def relative_to_ssot(path: Path) -> str:
    return path.resolve().relative_to(SSOT_ROOT.resolve()).as_posix()


def is_safe_relative_path(value: str) -> bool:
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts


def is_exposed_ssot_path(value: str | None) -> bool:
    if not value or not is_safe_relative_path(value):
        return False
    normalized = Path(value).as_posix()
    return not normalized.startswith(PROTECTED_PREFIXES)


def json_response_data() -> dict[str, Any]:
    return {
        "ssot_root": "ssot-root",
        "baseline_path": "core/validation/known_findings.json",
        "validator_path": "core/scripts/validate_documents.py",
    }


def serialize_finding(finding: Any) -> dict[str, Any]:
    data = asdict(finding)
    data["formatted"] = finding.format()
    if data.get("location"):
        data["location"] = data["location"].replace(str(SSOT_ROOT), "ssot-root")
    data["formatted"] = data["formatted"].replace(str(SSOT_ROOT), "ssot-root")
    return data


def collect_validation() -> dict[str, Any]:
    validator = load_validator()
    streams = validator.discover_event_streams(SSOT_ROOT)

    strict_findings = []
    for stream in streams:
        strict_findings.extend(validator.validate_event_stream(SSOT_ROOT, stream))
    if not streams:
        strict_findings.append(
            validator.Finding("ERROR", "ssot-root", "EVENT_STREAMS_NOT_FOUND", "no event streams found")
        )

    baseline_entries, baseline_errors = validator.load_baseline(KNOWN_FINDINGS_PATH)
    baseline_findings = [*strict_findings, *baseline_errors]
    matched_baseline_count = 0
    if not baseline_errors:
        baseline_findings, matched_baseline_count = validator.apply_baseline(baseline_findings, baseline_entries)

    return {
        "strict": {
            "status": "pass" if not strict_findings else "failed",
            "finding_count": len(strict_findings),
            "findings": [serialize_finding(item) for item in strict_findings],
        },
        "with_baseline": {
            "status": "pass" if not baseline_findings else "failed",
            "finding_count": len(baseline_findings),
            "matched_baseline_count": matched_baseline_count,
            "findings": [serialize_finding(item) for item in baseline_findings],
        },
        "known_findings": load_known_findings(),
    }


def load_known_findings() -> dict[str, Any]:
    if not KNOWN_FINDINGS_PATH.exists():
        return {"path": "core/validation/known_findings.json", "count": 0, "findings": []}
    data = json.loads(KNOWN_FINDINGS_PATH.read_text(encoding="utf-8"))
    findings = data.get("findings", []) if isinstance(data, dict) else []
    return {
        "path": "core/validation/known_findings.json",
        "count": len(findings) if isinstance(findings, list) else 0,
        "findings": findings if isinstance(findings, list) else [],
    }


def collect_streams() -> list[dict[str, Any]]:
    streams: list[dict[str, Any]] = []
    streams_root = SSOT_ROOT / "event_kernel" / "streams"
    if not streams_root.exists():
        return streams

    for stream_file in sorted(streams_root.glob("*/events_raw.ndjson")):
        rel = relative_to_ssot(stream_file)
        events = parse_event_file(stream_file)
        kinds = Counter(event.get("kind", "unknown") for event in events)
        streams.append(
            {
                "path": rel,
                "tenant": stream_file.parent.name,
                "event_count": len(events),
                "kinds": dict(sorted(kinds.items())),
                "last_event": events[-1] if events else None,
            }
        )
    return streams


def parse_event_file(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with path.open("rb") as handle:
        for line_number, raw_line in enumerate(handle, 1):
            stripped = raw_line.strip()
            if not stripped or stripped.startswith(b"#"):
                continue
            try:
                event = json.loads(stripped.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            if not isinstance(event, dict):
                continue
            event["line"] = line_number
            event["stream_path"] = relative_to_ssot(path)
            event["raw_line_sha256"] = load_validator().sha256_bytes(raw_line)
            if not is_exposed_ssot_path(event.get("path")):
                event.pop("path", None)
            events.append(event)
    return events


def collect_events() -> dict[str, Any]:
    validation = collect_validation()
    strict_by_line = {
        (item.get("stream_path"), item.get("line_number")): item
        for item in validation["strict"]["findings"]
        if item.get("stream_path") and item.get("line_number")
    }
    known_by_line = {
        (item.get("stream_path"), item.get("line")): item
        for item in validation["known_findings"]["findings"]
        if item.get("stream_path") and item.get("line")
    }

    events: list[dict[str, Any]] = []
    for stream in collect_streams():
        stream_path = SSOT_ROOT / stream["path"]
        for event in parse_event_file(stream_path):
            key = (event["stream_path"], event["line"])
            event["validation"] = classify_event_validation(event, strict_by_line.get(key), known_by_line.get(key))
            events.append(event)

    events.sort(key=lambda item: (item.get("timestamp", ""), item.get("id", "")), reverse=True)
    return {"count": len(events), "events": events}


def classify_event_validation(
    event: dict[str, Any],
    strict_finding: dict[str, Any] | None,
    known_finding: dict[str, Any] | None,
) -> dict[str, Any]:
    if strict_finding and known_finding:
        return {"status": "baseline", "finding": strict_finding, "known_finding": known_finding}
    if strict_finding:
        return {"status": "anomaly", "finding": strict_finding}

    target = event.get("path")
    declared_hash = event.get("hash_sha256")
    if target and is_exposed_ssot_path(target) and isinstance(declared_hash, str):
        target_path = SSOT_ROOT / target
        if target_path.exists() and target_path.is_file():
            actual_hash = load_validator().sha256_file(target_path)
            if actual_hash == declared_hash:
                return {"status": "hash_ok", "actual_hash": actual_hash}
            return {"status": "anomaly", "actual_hash": actual_hash}
    return {"status": "unchecked"}


def collect_documents() -> dict[str, Any]:
    documents: dict[str, dict[str, Any]] = {}
    validator = load_validator()
    for stream in collect_streams():
        for event in parse_event_file(SSOT_ROOT / stream["path"]):
            target = event.get("path")
            if not is_exposed_ssot_path(target):
                continue
            assert isinstance(target, str)
            target_path = SSOT_ROOT / target
            exists = target_path.exists() and target_path.is_file()
            actual_hash = validator.sha256_file(target_path) if exists else None
            declared_hash = event.get("hash_sha256") if isinstance(event.get("hash_sha256"), str) else None
            documents[target] = {
                "path": target,
                "exists": exists,
                "declared_hash": declared_hash,
                "actual_hash": actual_hash,
                "hash_status": "ok" if actual_hash and actual_hash == declared_hash else "anomaly",
                "referenced_by": event.get("id"),
                "event_line": event.get("line"),
                "stream_path": event.get("stream_path"),
            }
    ordered = [documents[key] for key in sorted(documents)]
    return {"count": len(ordered), "documents": ordered}


def collect_summary() -> dict[str, Any]:
    validation = collect_validation()
    streams = collect_streams()
    events_data = collect_events()
    known = validation["known_findings"]

    roadmap = [
        {"label": "Core rules", "progress": 85, "status": "substantial"},
        {"label": "Event kernel", "progress": 65, "status": "prototype"},
        {"label": "Registry", "progress": 15, "status": "stub"},
        {"label": "Canon documents", "progress": 10, "status": "empty"},
        {"label": "Policies", "progress": 35, "status": "partial"},
        {"label": "Tools", "progress": 25, "status": "minimal validator"},
        {"label": "Front cockpit", "progress": 30, "status": "first dashboard"},
    ]

    return {
        **json_response_data(),
        "validation": {
            "strict_status": validation["strict"]["status"],
            "with_baseline_status": validation["with_baseline"]["status"],
            "strict_finding_count": validation["strict"]["finding_count"],
            "known_finding_count": known["count"],
            "matched_baseline_count": validation["with_baseline"]["matched_baseline_count"],
        },
        "counts": {
            "streams": len(streams),
            "events": events_data["count"],
            "documents": collect_documents()["count"],
        },
        "roadmap": roadmap,
    }
