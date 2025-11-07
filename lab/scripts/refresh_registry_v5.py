#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refresh hashes in docs/_registry/registry_v1.1_v5.yaml and add missing entries.

Actions:
- Recompute sha256 for every lineages[].versions[].file_path and update the 'hash' field.
- Ensure coverage by adding a lineage for reports/validation/SSOT_V1_1_ALIGN_PHASE2_CODEX.md
  if it is missing (assign next available SPRINT_DOC-XXXX id).

Usage:
  python3 scripts/refresh_registry_v5.py [--registry docs/_registry/registry_v1.1_v5.yaml]
"""

import argparse
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

def guess_project_root() -> Path:
    candidates = [
        Path(__file__).resolve().parents[1],
        Path(__file__).resolve().parents[2],
        Path.cwd(),
        Path.cwd().parent,
    ]
    # Prefer a directory that contains the canonical registry file(s)
    for c in candidates:
        try:
            if (c / "docs/_registry/registry_v1.1.yaml").exists() or (c / "docs/_registry/registry_v1.1_v5.yaml").exists():
                return c
        except Exception:
            continue
    # Fallback: directory that has both docs and scripts
    for c in candidates:
        try:
            if (c / "docs").exists() and (c / "scripts").exists():
                return c
        except Exception:
            continue
    # Last resort: parent of this script
    return Path(__file__).resolve().parents[1]

PROJECT_ROOT = guess_project_root()
DEFAULT_REGISTRY = PROJECT_ROOT / "docs/_registry/registry_v1.1_v5.yaml"

TARGET_MISSING_PATH = "reports/validation/SSOT_V1_1_ALIGN_PHASE2_CODEX.md"

def calculate_sha256_file(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return "sha256:" + h.hexdigest()

def load_yaml(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def dump_yaml(data: Dict[str, Any], path: Path) -> None:
    # Preserve key order (Python 3.7+ preserves insertion order in dict)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

def get_next_sprint_doc_id(lineages: List[Dict[str, Any]]) -> str:
    max_num = 0
    for lin in lineages:
        root = lin.get("id_root")
        if isinstance(root, str) and root.startswith("SPRINT_DOC-"):
            try:
                num = int(root.split("-")[1])
                if num > max_num:
                    max_num = num
            except Exception:
                continue
    return f"SPRINT_DOC-{max_num + 1:04d}"

def lineage_contains_file(lineage: Dict[str, Any], file_rel: str) -> bool:
    versions = lineage.get("versions", [])
    if not isinstance(versions, list):
        return False
    for ver in versions:
        if isinstance(ver, dict) and ver.get("file_path") == file_rel:
            return True
    return False

def registry_has_file(reg: Dict[str, Any], file_rel: str) -> bool:
    for lin in reg.get("lineages", []):
        if not isinstance(lin, dict):
            continue
        if lineage_contains_file(lin, file_rel):
            return True
    return False

def add_phase2_codex_lineage_if_missing(reg: Dict[str, Any]) -> bool:
    """
    Add a new lineage for ALIGN_PHASE2_CODEX if missing.
    Returns True if modified.
    """
    if registry_has_file(reg, TARGET_MISSING_PATH):
        return False

    file_abs = (PROJECT_ROOT / TARGET_MISSING_PATH).resolve()
    file_hash = calculate_sha256_file(file_abs)
    if file_hash is None:
        # File absent, do not add
        return False

    new_root = get_next_sprint_doc_id(reg.get("lineages", []))
    # Minimal required fields for registry_check:
    # id_root, versions -> [{ id, status, version, date, file_path, hash }]
    new_lineage = {
        "id_root": new_root,
        "versions": [
            {
                "id": new_root,
                "status": "Active",
                "version": "1.0",
                "date": "2025-11-07",
                "file_path": TARGET_MISSING_PATH,
                "hash": file_hash,
            }
        ],
    }
    reg.setdefault("lineages", []).append(new_lineage)
    return True

def refresh_hashes(reg: Dict[str, Any]) -> Tuple[int, int]:
    """
    Recompute and update hashes. Returns (updated_count, missing_files)
    """
    updated = 0
    missing = 0
    for lin in reg.get("lineages", []):
        if not isinstance(lin, dict):
            continue
        versions = lin.get("versions", [])
        if not isinstance(versions, list):
            continue
        for ver in versions:
            if not isinstance(ver, dict):
                continue
            fp = ver.get("file_path")
            if not isinstance(fp, str) or not fp.strip():
                continue
            abs_path = (PROJECT_ROOT / fp).resolve()
            h = calculate_sha256_file(abs_path)
            if h is None:
                missing += 1
                continue
            if ver.get("hash") != h:
                ver["hash"] = h
                updated += 1
    return updated, missing

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", type=str, default=str(DEFAULT_REGISTRY))
    args = ap.parse_args()

    reg_path = Path(args.registry).resolve()
    reg = load_yaml(reg_path)

    changed = False

    # 1) Refresh all hashes
    upd, miss = refresh_hashes(reg)
    if upd > 0:
        changed = True
        print(f"Updated hash fields: {upd}")
    if miss > 0:
        print(f"Warning: missing files encountered: {miss}")

    # 2) Add Phase2 Codex lineage if missing
    if add_phase2_codex_lineage_if_missing(reg):
        changed = True
        print(f"Added lineage for missing file: {TARGET_MISSING_PATH}")

    if changed:
        dump_yaml(reg, reg_path)
        print(f"Wrote updated registry: {reg_path}")
    else:
        print("Registry already up-to-date.")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
