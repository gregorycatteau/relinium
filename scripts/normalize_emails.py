#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Normalize all email addresses in the repository to a single official address.

- Scans only text files with specific extensions
- Excludes typical build/cache/vendor/.git directories
- Replaces all emails with the target email (default: contact@pixelprowlers.io)
- Generates a markdown report summarizing changes
- Dry-run by default; use --write to apply changes

Usage:
  Dry run (no changes, generate report):
    python3 scripts/normalize_emails.py --report docs/06-ops/email-normalization-report.md

  Apply changes + report:
    python3 scripts/normalize_emails.py --write --report docs/06-ops/email-normalization-report.md
"""

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Exclusions and filters
EXCLUDED_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".cache",
    ".next",
    ".nuxt",
    "coverage",
    ".idea",
    ".vscode",
}

INCLUDED_EXTS = {
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    ".json",
    ".py",
    ".ts",
    ".js",
    ".sh",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
}

# Email regex (case-insensitive), fairly standard
EMAIL_REGEX = re.compile(
    r"(?i)\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)


def is_excluded_dir(dirpath: Path) -> bool:
    """
    Returns True if any path segment matches an excluded directory name.
    """
    for part in dirpath.parts:
        if part in EXCLUDED_DIRS:
            return True
    return False


def should_process_file(path: Path) -> bool:
    """
    Returns True if the file has an allowed extension and is not in an excluded dir.
    """
    if not path.is_file():
        return False
    if path.suffix.lower() not in INCLUDED_EXTS:
        return False
    if is_excluded_dir(path.parent):
        return False
    return True


def read_text_utf8_strict(path: Path) -> Tuple[bool, str]:
    """
    Read file as strict UTF-8. If decoding fails, return (False, reason).
    """
    try:
        # Read as binary and decode strictly to avoid altering encodings
        data = path.read_bytes()
        text = data.decode("utf-8", errors="strict")
        return True, text
    except Exception as e:
        return False, f"decode_error: {e!r}"


def write_text_utf8(path: Path, text: str) -> None:
    """
    Write text back as UTF-8 bytes (preserves content newlines as-is).
    """
    path.write_bytes(text.encode("utf-8"))


def normalize_file_emails(
    path: Path, target_email: str, do_write: bool
) -> Dict[str, int]:
    """
    Normalize emails in a single file.
    Returns a dict with:
      - matches: number of email matches found (including those already equal to target)
      - replacements: number of effective content-modifying replacements done (0 if content identical)
    """
    ok, content = read_text_utf8_strict(path)
    if not ok:
        return {"matches": 0, "replacements": 0}

    # Count matches first (including those identical to target)
    matches = len(list(EMAIL_REGEX.finditer(content)))

    if matches == 0:
        return {"matches": 0, "replacements": 0}

    # Perform replacement
    new_content, subn = EMAIL_REGEX.subn(target_email, content)

    # If content is identical, effective replacements are zero (idempotent)
    effective_replacements = 0 if new_content == content else subn

    if do_write and effective_replacements > 0:
        write_text_utf8(path, new_content)

    return {"matches": matches, "replacements": effective_replacements}


def walk_repository(root: Path) -> List[Path]:
    """
    Yield files to process from root respecting exclusions and extensions.
    """
    files: List[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        # Prune excluded dirs in-place for performance
        dirnames[:] = [d for d in dirnames if (current / d).name not in EXCLUDED_DIRS]

        # Skip entire subtree if current path already excluded by ancestor
        if is_excluded_dir(current):
            continue

        for fname in filenames:
            fpath = current / fname
            if should_process_file(fpath):
                files.append(fpath)
    return files


def generate_markdown_report(
    report_path: Path,
    target_email: str,
    summary: Dict[str, int],
    file_changes: List[Tuple[Path, Dict[str, int]]],
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
    exts = ", ".join(sorted(INCLUDED_EXTS))
    excluded = ", ".join(sorted(EXCLUDED_DIRS))

    lines: List[str] = []
    lines.append("# Email Normalization Report")
    lines.append("")
    lines.append(f"- Date: {now}")
    lines.append(f"- Cible normalisation: `{target_email}`")
    lines.append("")
    lines.append("## Paramètres")
    lines.append(f"- Extensions traitées: {exts}")
    lines.append(f"- Répertoires exclus: {excluded}")
    lines.append("")
    lines.append("## Synthèse")
    lines.append(f"- Fichiers inspectés: {summary.get('files_inspected', 0)}")
    lines.append(f"- Fichiers modifiés: {summary.get('files_modified', 0)}")
    lines.append(f"- Emails détectés (total): {summary.get('matches_total', 0)}")
    lines.append(f"- Remplacements effectués (total): {summary.get('replacements_total', 0)}")
    lines.append("")
    lines.append("## Détails par fichier (uniquement ceux modifiés)")
    if summary.get("files_modified", 0) == 0:
        lines.append("_Aucun fichier modifié. Le dépôt est déjà normalisé._")
    else:
        lines.append("")
        for path, stats in file_changes:
            if stats.get("replacements", 0) > 0:
                lines.append(f"- `{path.as_posix()}`: {stats['replacements']} remplacement(s)")
    lines.append("")
    lines.append("> Rapport généré automatiquement par `scripts/normalize_emails.py`.")

    write_text_utf8(report_path, "\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize all emails in repository.")
    parser.add_argument("--root", default=".", help="Root directory to scan (default: .)")
    parser.add_argument(
        "--target",
        default="contact@pixelprowlers.io",
        help="Target email to normalize to (default: contact@pixelprowlers.io)",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Apply changes to files (default: dry-run)",
    )
    parser.add_argument(
        "--report",
        default="docs/06-ops/email-normalization-report.md",
        help="Path to write markdown report (default: docs/06-ops/email-normalization-report.md)",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    report_path = Path(args.report)

    files = walk_repository(root)

    matches_total = 0
    replacements_total = 0
    files_modified = 0
    file_changes: List[Tuple[Path, Dict[str, int]]] = []

    for f in files:
        stats = normalize_file_emails(f, args.target, args.write)
        matches_total += stats["matches"]
        if stats["replacements"] > 0:
            replacements_total += stats["replacements"]
            files_modified += 1
            file_changes.append((f.relative_to(root), stats))

    summary = {
        "files_inspected": len(files),
        "files_modified": files_modified,
        "matches_total": matches_total,
        "replacements_total": replacements_total,
        "target_email": args.target,
        "write_mode": bool(args.write),
        "report_path": report_path.as_posix(),
    }

    # Generate report
    generate_markdown_report(report_path if report_path.is_absolute() else root / report_path, args.target, summary, file_changes)

    # Print JSON summary to stdout for automation
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
