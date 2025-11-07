#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug helper: inspect registry v5 paths, PROJECT_ROOT resolution, and list missing vs present files.
"""

from pathlib import Path
import importlib.util
import yaml
import sys

def load_refresh_module():
    spec = importlib.util.spec_from_file_location("refresh", "scripts/refresh_registry_v5.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main() -> int:
    mod = load_refresh_module()
    print("PROJECT_ROOT:", mod.PROJECT_ROOT)

    reg_path = Path("docs/_registry/registry_v1.1_v5.yaml").resolve()
    print("Registry path:", reg_path, "exists=", reg_path.exists())
    if not reg_path.exists():
        print("Registry file not found, abort.", file=sys.stderr)
        return 2

    reg = yaml.safe_load(reg_path.read_text(encoding="utf-8"))
    missing, present = [], []
    for lin in reg.get("lineages", []):
        versions = lin.get("versions", []) or []
        for ver in versions:
            if not isinstance(ver, dict):
                continue
            p = ver.get("file_path")
            if not isinstance(p, str):
                continue
            ap = (mod.PROJECT_ROOT / p).resolve()
            (present if ap.exists() else missing).append((p, ap))

    print("present_count=", len(present), "missing_count=", len(missing))
    print("Sample missing (up to 30):")
    for p, ap in missing[:30]:
        print("-", p, "->", ap)

    # Explicit checks
    checks = [
        "docs/03-architecture/decisions/ADR-0001-repo-driven-by-docs-first-v2.md",
        "docs/03-architecture/rfcs/RFC-001-choix-stack-initiale-v2.md",
        "reports/validation/SSOT_V1_1_ALIGN_PHASE2_CODEX.md",
        "docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_ALIGN_PLAN.md",
    ]
    for p in checks:
        ap = (mod.PROJECT_ROOT / p).resolve()
        print("check:", p, "exists=", ap.exists(), "->", ap)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
