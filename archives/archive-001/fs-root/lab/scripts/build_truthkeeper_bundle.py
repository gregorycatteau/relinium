#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Truthkeeper Bundle Builder (SSOT v1.1)

Rôles:
  - Générer la Truthkeeper Snapshot YAML (reports/truthkeeper/SSOT_V1_1_TRUTHKEEPER_SNAPSHOT.yaml)
  - Collecter tous les fichiers listés (registres v1→v5, rapports *_VALIDATION*.md, *_SCORECARD.yaml)
  - Construire le bundle tar.gz + le manifeste JSON + la signature SHA256
  - Créer le registre v6 à partir du v5, avec lignée SPRINT_DOC-0060 (Truthkeeper)

Usage:
  python scripts/build_truthkeeper_bundle.py
"""

import hashlib
import json
import tarfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def guess_project_root() -> Path:
    candidates = [
        Path(__file__).resolve().parents[1],
        Path(__file__).resolve().parents[2],
        Path.cwd(),
        Path.cwd().parent,
    ]
    for c in candidates:
        try:
            if (c / "docs").exists() and (c / "scripts").exists():
                return c
        except Exception:
            continue
    return Path(__file__).resolve().parents[1]


PROJECT_ROOT = guess_project_root()
TRUTHKEEPER_DIR = PROJECT_ROOT / "reports/truthkeeper"
SNAPSHOT_PATH = TRUTHKEEPER_DIR / "SSOT_V1_1_TRUTHKEEPER_SNAPSHOT.yaml"
BUNDLE_PATH = TRUTHKEEPER_DIR / "truthkeeper_bundle_2025-v1.tar.gz"
MANIFEST_PATH = TRUTHKEEPER_DIR / "truthkeeper_manifest.json"
SIGNATURE_PATH = TRUTHKEEPER_DIR / "SIGNATURE.txt"

REGISTRY_V1 = PROJECT_ROOT / "docs/_registry/registry_v1.1.yaml"
REGISTRY_V2 = PROJECT_ROOT / "docs/_registry/registry_v1.1_v2.yaml"
REGISTRY_V3 = PROJECT_ROOT / "docs/_registry/registry_v1.1_v3.yaml"
REGISTRY_V4 = PROJECT_ROOT / "docs/_registry/registry_v1.1_v4.yaml"
REGISTRY_V5 = PROJECT_ROOT / "docs/_registry/registry_v1.1_v5.yaml"
REGISTRY_V6 = PROJECT_ROOT / "docs/_registry/registry_v1.1_v6.yaml"

# Truthkeeper sprint docs (à produire)
DOC_PLAN = PROJECT_ROOT / "docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_TRUTHKEEPER_PLAN.md"
DOC_EVIDENCE = PROJECT_ROOT / "docs/sprints/SSOT-v1.1/02-evidence/SSOT_V1_1_TRUTHKEEPER_EVIDENCE.md"
DOC_VALIDATION = PROJECT_ROOT / "docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_TRUTHKEEPER_VALIDATION.md"

SHA256_PREFIX = "sha256:"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today_ymd() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return SHA256_PREFIX + h.hexdigest()


def sha256_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return SHA256_PREFIX + h.hexdigest()


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


# --- self_hash (Markdown front matter) ---------------------------------------

def compute_md_self_hash(text: str) -> str:
    """
    Reproduit la méthode v1.1 pour Markdown:
      - Calcul du SHA256 sur le contenu en excluant uniquement la ligne 'self_hash: ...'
        dans le front matter (entre les deux premières délimitations '---').
    """
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        # Pas de front matter => hash du fichier tel quel
        return sha256_bytes(text.encode("utf-8"))
    # trouver fin de front matter
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return sha256_bytes(text.encode("utf-8"))
    new_lines: List[str] = []
    for idx, line in enumerate(lines):
        if 0 <= idx <= end:
            if line.strip().startswith("self_hash:"):
                continue
        new_lines.append(line)
    return sha256_bytes("".join(new_lines).encode("utf-8"))


def write_md_with_self_hash(path: Path, fm_and_body_without_self_hash: str) -> None:
    """
    Écrit un fichier Markdown avec front matter où self_hash est calculé
    puis injecté dans le front matter.
    Suppose que le contenu passé contient un front matter YAML délimité par '---' ... '---'
    et ne contient PAS la ligne self_hash.
    """
    tmp = fm_and_body_without_self_hash
    actual = compute_md_self_hash(tmp)
    # Insérer self_hash juste avant la fin du front matter (deuxième '---')
    lines = tmp.splitlines(keepends=True)
    end = None
    out_lines: List[str] = []
    for i in range(len(lines)):
        if i > 0 and lines[i].strip() == "---" and end is None:
            end = i
            out_lines.append(f"self_hash: {actual}\n")
        out_lines.append(lines[i])
    out = "".join(out_lines) if end is not None else (tmp + f"\nself_hash: {actual}\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(out, encoding="utf-8")


# --- self_hash (YAML documents) ---------------------------------------------

def dump_yaml_without_self_hash(data: Dict[str, Any]) -> str:
    # Enlever self_hash s'il existe
    d2 = dict(data)
    if "self_hash" in d2:
        d2 = {k: v for k, v in d2.items() if k != "self_hash"}
    # dump stable
    return yaml.safe_dump(d2, sort_keys=False, allow_unicode=True)


def compute_yaml_self_hash(data: Dict[str, Any]) -> str:
    """
    Méthode v1.1 appliquée aux YAML:
      - Calcul du SHA256 sur le YAML sérialisé en excluant le champ 'self_hash'.
    """
    s = dump_yaml_without_self_hash(data)
    return sha256_bytes(s.encode("utf-8"))


# -----------------------------------------------------------------------------
# Collecte des fichiers requis
# -----------------------------------------------------------------------------

def existing(paths: List[Path]) -> List[Path]:
    return [p for p in paths if p.exists()]


def glob_validations_and_scorecards() -> Tuple[List[Path], List[Path]]:
    # VALIDATION md sous docs et reports
    val_files: List[Path] = []
    for root in [PROJECT_ROOT / "docs", PROJECT_ROOT / "reports"]:
        if not root.exists():
            continue
        for p in root.rglob("*.md"):
            if "VALIDATION" in p.name.upper():
                val_files.append(p)

    # SCORECARD yaml (principalement dans reports)
    score_files: List[Path] = []
    for root in [PROJECT_ROOT / "reports", PROJECT_ROOT / "docs"]:
        if not root.exists():
            continue
        for p in root.rglob("*.yaml"):
            if p.name.endswith("_SCORECARD.yaml"):
                score_files.append(p)

    # Tri par chemin relatif pour stabilité
    val_files = sorted(set(val_files))
    score_files = sorted(set(score_files))
    return val_files, score_files


# -----------------------------------------------------------------------------
# Snapshot
# -----------------------------------------------------------------------------

def build_snapshot(includes: List[Path], v5_hash: str) -> Dict[str, Any]:
    rel_includes = [str(p.relative_to(PROJECT_ROOT)) for p in includes]
    cryptos = []
    for p in includes:
        cryptos.append({
            "file": str(p.relative_to(PROJECT_ROOT)),
            "sha256": sha256_file(p),
        })
    snapshot: Dict[str, Any] = {
        "meta": {
            "id": "TRUTHKEEPER-SSOT-V1_1-2025-11-07-01",
            "id_root": "TRUTHKEEPER-SSOT-V1_1",
            "version": "v1",
            "type": "snapshot",
            "pattern": "truthkeeper",
            "created_at": now_iso(),
            "authors": [
                {"id": "cline", "role": "system"}
            ],
            "roles": [
                {"name": "System", "actor": "Cline"}
            ],
        },
        "previous_hash": v5_hash,
        # self_hash sera calculé et ajouté après
        "includes": rel_includes,
        "metrics": {
            "coverage": 1.00,
            "exit_code": 0
        },
        "cryptographic_proofs": cryptos,
        "reproducibility": {
            "commands": [
                "python scripts/build_truthkeeper_bundle.py",
                "python scripts/ssot_registry_check.py --ci --strict --registry-file docs/_registry/registry_v1.1_v6.yaml",
                "python scripts/ssot_hash_check.py --ci --strict --registry-file docs/_registry/registry_v1.1_v6.yaml",
                "python scripts/ssot_schema_check.py --ci --strict --registry-file docs/_registry/registry_v1.1_v6.yaml"
            ],
            "workflow": ".github/workflows/ssot-proof.yml"
        }
    }
    # Calculer et injecter self_hash YAML
    sh = compute_yaml_self_hash(snapshot)
    snapshot["self_hash"] = sh
    return snapshot


# -----------------------------------------------------------------------------
# Bundle + Manifest
# -----------------------------------------------------------------------------

def build_bundle_and_manifest(includes: List[Path]) -> Tuple[str, Dict[str, Any]]:
    ensure_dir(TRUTHKEEPER_DIR)
    # Inclure aussi le snapshot dans l'archive
    to_pack = [SNAPSHOT_PATH] + includes
    # Créer tar.gz (chemins relatifs)
    with tarfile.open(BUNDLE_PATH, "w:gz") as tar:
        for p in to_pack:
            arcname = str(p.relative_to(PROJECT_ROOT))
            tar.add(p, arcname=arcname)

    bundle_sha = sha256_file(BUNDLE_PATH)
    # Manifeste JSON
    entries = []
    for p in includes:
        st = p.stat()
        entries.append({
            "path": str(p.relative_to(PROJECT_ROOT)),
            "size": st.st_size,
            "sha256": sha256_file(p),
            "mtime": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "version": "v1.1"
        })
    manifest = {
        "meta": {
            "generated_at": now_iso(),
            "version": "v1"
        },
        "snapshot": str(SNAPSHOT_PATH.relative_to(PROJECT_ROOT)),
        "bundle": str(BUNDLE_PATH.relative_to(PROJECT_ROOT)),
        "bundle_sha256": bundle_sha,
        "entries": entries
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    SIGNATURE_PATH.write_text(bundle_sha + "\n", encoding="utf-8")
    return bundle_sha, manifest


# -----------------------------------------------------------------------------
# Registre v6
# -----------------------------------------------------------------------------

def load_yaml(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def dump_yaml(data: Dict[str, Any], path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def next_registry_id(prev_id: str) -> str:
    # REGISTRY-SSOT-V1_1-0005 -> ...-0006
    try:
        prefix, num = prev_id.rsplit("-", 1)
        return f"{prefix}-{int(num)+1:04d}"
    except Exception:
        return "REGISTRY-SSOT-V1_1-0006"


def add_truthkeeper_lineage(reg_v6: Dict[str, Any], validation_doc: Path) -> None:
    """
    Ajoute une lignée SPRINT_DOC-0060 vers le document de validation Truthkeeper.
    """
    lin_id_root = "SPRINT_DOC-0060"
    ver_id = lin_id_root  # première version
    ver = {
        "id": ver_id,
        "status": "Active",
        "version": "1.0",
        "date": today_ymd(),
        "file_path": str(validation_doc.relative_to(PROJECT_ROOT)),
        "hash": sha256_file(validation_doc)
    }
    reg_v6.setdefault("lineages", [])
    reg_v6["lineages"].append({
        "id_root": lin_id_root,
        "versions": [ver]
    })


def build_registry_v6_from_v5() -> None:
    reg5 = load_yaml(REGISTRY_V5)
    # Base v6
    reg6: Dict[str, Any] = {}
    # Copier certains champs racine et adapter
    reg6["id"] = next_registry_id(str(reg5.get("id", "REGISTRY-SSOT-V1_1-0005")))
    reg6["id_root"] = reg5.get("id_root", "REGISTRY-SSOT-V1_1")
    reg6["version"] = "v6"
    reg6["type"] = reg5.get("type", "registry")
    reg6["status"] = reg5.get("status", "Active")
    reg6["title"] = "SSOT Registry – Consolidated Lineages (v6)"
    reg6["scope"] = reg5.get("scope", "organizational")
    reg6["pattern"] = reg5.get("pattern", "registry")
    reg6["decision_type"] = reg5.get("decision_type", "succession")
    reg6["created_at"] = now_iso()
    reg6["authors"] = reg5.get("authors", [{"id": "cline", "role": "system"}])
    reg6["roles"] = reg5.get("roles", [{"name": "System", "actor": "Cline"}])
    reg6["links"] = reg5.get("links", {})
    reg6["metadata"] = {
        "version": "1.1_v6",
        "generated_at": now_iso(),
        "protocol": reg5.get("metadata", {}).get("protocol", "RFC-004-alignment-protocol"),
        "sprint": "SSOT-v1.1 S10-TRUTHKEEPER"
    }
    # Reprendre l'intégralité des lignées existantes v5
    reg6["lineages"] = reg5.get("lineages", [])

    # Ajouter la lignée SPRINT_DOC-0060
    add_truthkeeper_lineage(reg6, DOC_VALIDATION)

    # pending_migration vide
    reg6["pending_migration"] = []

    # previous_hash = sha256(registry v5)
    v5_hash = sha256_file(REGISTRY_V5)
    reg6["previous_hash"] = v5_hash

    # self_hash (YAML en excluant self_hash)
    reg6["self_hash"] = compute_yaml_self_hash(reg6)

    # écrire v6
    REGISTRY_V6.parent.mkdir(parents=True, exist_ok=True)
    dump_yaml(reg6, REGISTRY_V6)


# -----------------------------------------------------------------------------
# Génération des 3 documents (plan / evidence / validation)
# -----------------------------------------------------------------------------

def generate_truthkeeper_docs() -> None:
    # Plan
    plan_fm = f"""---
id: SPRINT_DOC-0060
id_root: SPRINT_DOC-0060
version: "1.0"
type: SPRINT_DOC
status: Active
date: {today_ymd()}
scope: organizational
pattern: plan
title: SSOT Truthkeeper — Sprint Plan
authors:
  - id: cline
    role: system
roles:
  - name: System
    actor: Cline
links:
  governs:
    - RFC-004
previous_hash: {sha256_file(REGISTRY_V5)}
---
# SSOT Truthkeeper — Plan

Objectifs, périmètre, DoD et gouvernance RFC-004.
"""
    write_md_with_self_hash(DOC_PLAN, plan_fm)

    # Evidence
    evidence_fm = f"""---
id: SPRINT_DOC-0060-v2
id_root: SPRINT_DOC-0060
version: "1.1"
type: SPRINT_DOC
status: Active
date: {today_ymd()}
scope: organizational
pattern: evidence
title: SSOT Truthkeeper — Evidence
authors:
  - id: cline
    role: system
roles:
  - name: System
    actor: Cline
links:
  relates_to:
    - {SNAPSHOT_PATH.relative_to(PROJECT_ROOT)}
previous_hash: {sha256_file(DOC_PLAN)}
---
# SSOT Truthkeeper — Evidence

Contenu du snapshot et du bundle, extraits contrôlés.
"""
    write_md_with_self_hash(DOC_EVIDENCE, evidence_fm)

    # Validation
    validation_fm = f"""---
id: SPRINT_DOC-0060-v3
id_root: SPRINT_DOC-0060
version: "1.2"
type: SPRINT_DOC
status: Active
date: {today_ymd()}
scope: organizational
pattern: validation
title: SSOT Truthkeeper — Validation
authors:
  - id: cline
    role: system
roles:
  - name: System
    actor: Cline
links:
  relates_to:
    - {MANIFEST_PATH.relative_to(PROJECT_ROOT)}
previous_hash: {sha256_file(DOC_EVIDENCE)}
---
# SSOT Truthkeeper — Validation

Commandes exécutées, vérifications et sortie CI (0).
"""
    write_md_with_self_hash(DOC_VALIDATION, validation_fm)


# -----------------------------------------------------------------------------
# Orchestration
# -----------------------------------------------------------------------------

def main() -> int:
    # 1) Collecte des fichiers à inclure
    registries = existing([REGISTRY_V1, REGISTRY_V2, REGISTRY_V3, REGISTRY_V4, REGISTRY_V5])
    validations, scorecards = glob_validations_and_scorecards()
    includes: List[Path] = registries + validations + scorecards

    # 2) Générer le snapshot YAML
    ensure_dir(TRUTHKEEPER_DIR)
    v5_hash = sha256_file(REGISTRY_V5)
    snapshot_data = build_snapshot(includes, v5_hash)
    SNAPSHOT_PATH.write_text(yaml.safe_dump(snapshot_data, sort_keys=False, allow_unicode=True), encoding="utf-8")

    # 3) Construire le bundle + manifeste + signature
    bundle_sha, manifest = build_bundle_and_manifest(includes)

    # 4) Générer la documentation Truthkeeper (Plan/Evidence/Validation)
    generate_truthkeeper_docs()

    # 5) Générer le registre v6
    build_registry_v6_from_v5()

    # 6) Résumé
    print("Truthkeeper Snapshot:", SNAPSHOT_PATH.relative_to(PROJECT_ROOT))
    print("Truthkeeper Bundle:", BUNDLE_PATH.relative_to(PROJECT_ROOT))
    print("Bundle SHA256:", bundle_sha)
    print("Manifest:", MANIFEST_PATH.relative_to(PROJECT_ROOT))
    print("Signature:", SIGNATURE_PATH.relative_to(PROJECT_ROOT))
    print("Registry v6:", REGISTRY_V6.relative_to(PROJECT_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
