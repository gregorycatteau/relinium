#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compose le registre v1.1_v4 à partir de v3, en promouvant toutes les entrées pending_migration
vers des lignées actives, et en scellant le registre avec previous_hash (sha256 du v3)
et self_hash (sha256 du v4 en excluant la ligne self_hash).

- Aucun fichier existant n'est modifié.
- Produit:
  * docs/_registry/registry_v1.1_v4.yaml
  * docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_ALIGN_PHASE2_VALIDATION.md
"""

import hashlib
import re
from copy import deepcopy
from datetime import datetime, date
from pathlib import Path
from typing import Dict, Any, List, Set, Tuple, Optional

try:
    import yaml
except Exception:
    raise SystemExit("PyYAML est requis: pip install pyyaml")

ROOT = Path.cwd()
V3_PATH = ROOT / "docs/_registry/registry_v1.1_v3.yaml"
V4_PATH = ROOT / "docs/_registry/registry_v1.1_v4.yaml"
VALIDATION_PATH = ROOT / "docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_ALIGN_PHASE2_VALIDATION.md"
PHASE2_INCLUDE = [
    "docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_ALIGN_PHASE2_PLAN.md",
    "docs/sprints/SSOT-v1.1/02-evidence/SSOT_V1_1_ALIGN_PHASE2_EVIDENCE.md",
]

SHA256_RE = re.compile(r"^sha256:[a-f0-9]{64}$")
ID_ROOT_RE = re.compile(r"^(ADR|RFC|OBS|POC|SPRINT_DOC)-\d{4}$")
ID_RE = re.compile(r"^(ADR|RFC|OBS|POC|SPRINT_DOC)-\d{4}(-v\d+)?$")

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return "sha256:" + h.hexdigest()

def compute_self_hash_excluding_line(text: str) -> str:
    # Exclure exactement la ligne commençant par self_hash:
    kept: List[str] = []
    for ln in text.splitlines(keepends=True):
        if re.match(r'^\s*self_hash\s*:', ln):
            continue
        kept.append(ln)
    data = "".join(kept).encode("utf-8")
    h = hashlib.sha256()
    h.update(data)
    return "sha256:" + h.hexdigest()

def load_yaml(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def dump_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

def normalize_idroot_from_pending_id(candidate: Optional[str]) -> Optional[str]:
    """
    Si l'ID pending est déjà de la forme RFC-0004, OBS-0001, ADR-0001, on normalise.
    Sinon None -> on créera un SPRINT_DOC-xxxx.
    """
    if not isinstance(candidate, str):
        return None
    m = re.match(r"^(ADR|RFC|OBS)-0*(\d{1,4})$", candidate)
    if not m:
        return None
    return f"{m.group(1)}-{int(m.group(2)):04d}"

def collect_covered_paths(lineages: List[Dict[str, Any]]) -> Set[str]:
    covered: Set[str] = set()
    for lin in lineages or []:
        for ver in lin.get("versions", []) or []:
            fp = ver.get("file_path")
            if isinstance(fp, str):
                covered.add(str((ROOT / fp).resolve()))
    return covered

def next_sprint_doc_index(lineages: List[Dict[str, Any]]) -> int:
    mx = 0
    for lin in lineages or []:
        rid = lin.get("id_root") or ""
        m = re.match(r"^SPRINT_DOC-(\d{4})$", rid)
        if m:
            try:
                mx = max(mx, int(m.group(1)))
            except Exception:
                pass
    return mx + 1

def ensure_lineage_for_path(lineages4: List[Dict[str, Any]], rel_path: str) -> bool:
    """
    Garantit qu'un fichier rel_path est couvert par une lignée (SPRINT_DOC).
    - N'ajoute rien si déjà couvert.
    - Ajoute une lignée SPRINT_DOC-XXXX v1.0 Active sinon.
    Retourne True si une lignée a été ajoutée.
    """
    if not isinstance(rel_path, str) or not rel_path.strip():
        return False
    abs_path = (ROOT / rel_path).resolve()
    if not abs_path.exists():
        return False

    covered = collect_covered_paths(lineages4)
    if str(abs_path) in covered:
        return False

    # Assigner un nouvel id_root SPRINT_DOC-XXXX
    nxt = next_sprint_doc_index(lineages4)
    id_root = f"SPRINT_DOC-{nxt:04d}"
    ver_id = id_root
    ver_version = "1.0"
    vhash = sha256_file(abs_path)

    lineage = {
        "id_root": id_root,
        "versions": [
            {
                "id": ver_id,
                "status": "Active",
                "version": ver_version,
                "date": date.today().isoformat(),
                "file_path": rel_path,
                "hash": vhash,
            }
        ],
    }
    lineages4.append(lineage)
    return True

def promote_pending(reg3: Dict[str, Any], lineages4: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], int]:
    """
    Promeut toutes les entrées pending_migration en lignées actives.
    - Conserve RFC/OBS/ADR si l'id pending est normalisable
    - Sinon affecte un nouvel id_root SPRINT_DOC-XXXX
    - version: 1.0.0 pour ADR/RFC/OBS, sinon 1.0
    - status: Active
    - previous_hash: absent (v1)
    - évite les doublons par file_path déjà couvert
    """
    pending = reg3.get("pending_migration", []) or []
    covered_paths = collect_covered_paths(lineages4)
    added: List[Dict[str, Any]] = []
    nxt = next_sprint_doc_index(lineages4)

    for it in pending:
        fp_rel = it.get("file_path")
        if not isinstance(fp_rel, str) or not fp_rel.strip():
            continue
        abs_path = (ROOT / fp_rel).resolve()
        if not abs_path.exists():
            continue
        if str(abs_path) in covered_paths:
            # déjà couvert dans une lignée existante
            continue

        actual_hash = sha256_file(abs_path)

        candidate = it.get("id")
        id_root = normalize_idroot_from_pending_id(candidate)
        if id_root is None:
            # Créer une lignée SPRINT_DOC-xxxx
            id_root = f"SPRINT_DOC-{nxt:04d}"
            nxt += 1

        # id de version initiale = id_root
        ver_id = id_root
        ver_version = "1.0.0" if id_root.startswith(("ADR", "RFC", "OBS")) else "1.0"

        lineage = {
            "id_root": id_root,
            "versions": [
                {
                    "id": ver_id,
                    "status": "Active",
                    "version": ver_version,
                    "date": date.today().isoformat(),
                    "file_path": fp_rel,
                    "hash": actual_hash,
                    # pas de previous_hash pour une v1
                }
            ],
        }
        lineages4.append(lineage)
        added.append(lineage)
        covered_paths.add(str(abs_path))

    return added, len(pending)

def build_v4() -> Tuple[Dict[str, Any], List[Dict[str, Any]], int]:
    reg3 = load_yaml(V3_PATH)

    # 1) Préparer v4: copier metadata et lineages, vider pending_migration
    reg4: Dict[str, Any] = {}

    # Ajouter front matter v1.1 (sans blocs ---, pour rester compatible avec v3)
    now_iso = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    reg4["id"] = "REGISTRY-SSOT-V1_1-0004"
    reg4["id_root"] = "REGISTRY-SSOT-V1_1"
    reg4["version"] = "v4"
    reg4["type"] = "registry"
    reg4["status"] = "Active"
    reg4["title"] = "SSOT Registry – Consolidated Lineages (v4)"
    reg4["scope"] = "organizational"
    reg4["pattern"] = "registry"
    reg4["decision_type"] = "succession"
    reg4["created_at"] = now_iso
    reg4["authors"] = [{"id": "cline", "role": "system"}]
    reg4["roles"] = [{"name": "System", "actor": "Cline"}]
    reg4["links"] = {
        "relates_to": [
            "VAL-STRICT-SSOT-V1_1-0001",
            "VAL-ALIGN-PHASE2-SSOT-V1_1-0001",
        ],
        "evidence": [
            "docs/_registry/registry_v1.1_v3.yaml",
            "docs/sprints/SSOT-v1.1/01-plan/SSOT_V1_1_ALIGN_PHASE2_PLAN.md",
            "docs/sprints/SSOT-v1.1/02-evidence/SSOT_V1_1_ALIGN_PHASE2_EVIDENCE.md",
        ],
    }

    # Metadata selon v3 (structure conservée)
    reg4["metadata"] = deepcopy(reg3.get("metadata", {})) or {}
    reg4["metadata"]["version"] = "1.1_v4"
    reg4["metadata"]["generated_at"] = now_iso
    reg4["metadata"]["protocol"] = reg4["metadata"].get("protocol", "RFC-004-alignment-protocol")
    reg4["metadata"]["sprint"] = "SSOT-v1.1 S9-ALIGN P2-bis"

    # Copier lignes v3 telles quelles
    lineages4 = deepcopy(reg3.get("lineages", [])) or []
    reg4["lineages"] = lineages4

    # Promouvoir pending
    added_lineages, v3_pending_count = promote_pending(reg3, lineages4)

    # Vider pending dans v4
    reg4["pending_migration"] = []

    # Couverture obligatoire Phase2 (plan + evidence)
    for rel in PHASE2_INCLUDE:
        ensure_lineage_for_path(lineages4, rel)

    # previous_hash = sha256(v3)
    reg4["previous_hash"] = sha256_file(V3_PATH)
    # self_hash placeholder
    reg4["self_hash"] = "sha256:(to_be_calculated)"

    return reg4, added_lineages, v3_pending_count

def main() -> int:
    V4_PATH.parent.mkdir(parents=True, exist_ok=True)

    reg4, added_lineages, v3_pending_count = build_v4()

    # Ecrire v4 (premier dump)
    dump_yaml(V4_PATH, reg4)

    # Calculer le self_hash réel du v4 (exclusion de la ligne self_hash:)
    txt = V4_PATH.read_text(encoding="utf-8")
    actual_self = compute_self_hash_excluding_line(txt)
    txt_updated = re.sub(r'^self_hash\s*:\s*.*$', f"self_hash: {actual_self}", txt, flags=re.MULTILINE)
    V4_PATH.write_text(txt_updated, encoding="utf-8")

    # Préparer le rapport de validation
    v3_reg = load_yaml(V3_PATH)
    v3_lineages_cnt = len(v3_reg.get("lineages", []) or [])
    v4_reg = load_yaml(V4_PATH)
    v4_lineages_cnt = len(v4_reg.get("lineages", []) or [])
    v4_pending_cnt = len(v4_reg.get("pending_migration", []) or [])

    # Prévisualisation des ajouts (limité)
    added_preview: List[str] = []
    for lin in added_lineages[:30]:
        idr = lin.get("id_root")
        ver = lin.get("versions", [{}])[0]
        fp = ver.get("file_path")
        h = ver.get("hash")
        added_preview.append(f"- {idr} -> {fp} ({h})")

    # Génération validation MD (front matter simple + contenu)
    VALIDATION_PATH.parent.mkdir(parents=True, exist_ok=True)
    md_lines: List[str] = []
    md_lines.append("---\n")
    md_lines.append('id: "SSOT_V1_1_ALIGN_PHASE2_VALIDATION"\n')
    md_lines.append('type: "sprint_doc"\n')
    md_lines.append('pattern: "validation"\n')
    md_lines.append('title: "SSOT v1.1 – Validation Phase 2-bis (v4 registry)"\n')
    md_lines.append(f'created_at: "{datetime.utcnow().replace(microsecond=0).isoformat()}Z"\n')
    md_lines.append("authors:\n")
    md_lines.append('  - id: "cline"\n')
    md_lines.append('    role: "system"\n')
    md_lines.append("self_hash: sha256:(to_be_calculated)\n")
    md_lines.append("---\n\n")

    md_lines.append("# SSOT v1.1 – Validation Phase 2-bis\n\n")
    md_lines.append("## Résumé\n")
    md_lines.append(f"- previous_hash (v3): {v4_reg.get('previous_hash')}\n")
    md_lines.append(f"- self_hash (v4): to_be_computed_below\n\n")

    md_lines.append("## Comparatif v3 vs v4\n")
    md_lines.append(f"- Lignées v3: {v3_lineages_cnt}\n")
    md_lines.append(f"- Lignées v4: {v4_lineages_cnt} (Δ={v4_lineages_cnt - v3_lineages_cnt}, ajouts={len(added_lineages)})\n")
    md_lines.append(f"- pending_migration v3: {v3_pending_count}\n")
    md_lines.append(f"- pending_migration v4: {v4_pending_cnt}\n\n")

    md_lines.append("## Lignées promues (extrait)\n")
    md_lines.extend([ln + "\n" for ln in added_preview])
    md_lines.append("\n")

    md_lines.append("## Commandes exécutées\n")
    md_lines.append("```bash\n")
    md_lines.append("python scripts/build_registry_v1_1_v4.py\n")
    md_lines.append("python scripts/ssot_registry_check.py --ci --strict --registry-file docs/_registry/registry_v1.1_v4.yaml\n")
    md_lines.append("```\n")

    VALIDATION_PATH.write_text("".join(md_lines), encoding="utf-8")

    # self_hash MD: exclusion ligne self_hash: dans le bloc front matter
    md_txt = VALIDATION_PATH.read_text(encoding="utf-8")
    md_self = compute_self_hash_excluding_line(md_txt)
    md_txt2 = re.sub(r'^self_hash\s*:\s*.*$', f"self_hash: {md_self}", md_txt, flags=re.MULTILINE)
    VALIDATION_PATH.write_text(md_txt2, encoding="utf-8")

    # Inclure la validation Phase2 dans le registre v4 et recalculer le self_hash
    v4_reg2 = load_yaml(V4_PATH)
    lineages2 = v4_reg2.get("lineages", []) or []
    added_validation = ensure_lineage_for_path(lineages2, str(VALIDATION_PATH.relative_to(ROOT)))
    if added_validation:
        v4_reg2["lineages"] = lineages2
        v4_reg2["pending_migration"] = []
        # Conserver previous_hash, réinitialiser self_hash puis recalculer
        v4_reg2["self_hash"] = "sha256:(to_be_calculated)"
        dump_yaml(V4_PATH, v4_reg2)
        txt2 = V4_PATH.read_text(encoding="utf-8")
        actual_self2 = compute_self_hash_excluding_line(txt2)
        txt2_updated = re.sub(r'^self_hash\s*:\s*.*$', f"self_hash: {actual_self2}", txt2, flags=re.MULTILINE)
        V4_PATH.write_text(txt2_updated, encoding="utf-8")
        actual_self = actual_self2

    print("v4 registry generated:", V4_PATH)
    print("validation doc generated:", VALIDATION_PATH)
    print("self_hash(v4):", actual_self)
    print("previous_hash(v3):", v4_reg.get("previous_hash"))
    print("added_lineages:", len(added_lineages))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
