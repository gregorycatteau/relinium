#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSOT v1.1 - Schema Check (triple-check - étape 3)
Objectifs:
  - Vérifier la conformité minimale du front matter v1.1 sur un sous-ensemble de fichiers
  - Règles essentielles:
      * Champs requis: id, type, status, date (formats/patterns)
      * Cohérence id/type (préfixe)
      * Status conforme aux statuts autorisés par type (depuis le schéma v1.1)
      * links.supersedes => previous_hash requis et format sha256:...
      * 'author' ET 'roles.author' ne doivent pas coexister
      * Dates non futures (format YYYY-MM-DD)
  - Lecture seule, sortie concise en mode CI (--ci), code de sortie non nul si erreurs

Usage:
  python scripts/ssot_schema_check.py [--ci]
  python scripts/ssot_schema_check.py --targets DIR [DIR ...]
  python scripts/ssot_schema_check.py --schema docs/01-genesis/document_schema_v1.1.yaml

Notes:
  - Par défaut, ne scanne PAS docs/sprints/** pour éviter les faux positifs sur des types spécifiques de sprint.
  - Pour élargir la couverture, utilisez --targets explicitement.
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml
except Exception:
    print("❌ PyYAML est requis: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

def guess_project_root() -> Path:
    """
    Détecte le root du dépôt en priorisant la présence du registre v1.1
    pour éviter toute exécution depuis un sous-dossier (ex: lab/).
    """
    candidates = [
        Path(__file__).resolve().parents[2],
        Path(__file__).resolve().parents[1],
        Path.cwd(),
        Path.cwd().parent,
    ]
    for c in candidates:
        try:
            if (c / "docs/_registry/registry_v1.1.yaml").exists():
                return c
        except Exception:
            continue
    for c in candidates:
        try:
            if (c / "docs").exists() and (c / "scripts").exists():
                return c
        except Exception:
            continue
    p2 = Path(__file__).resolve().parents[2]
    if (p2 / "docs").exists():
        return p2
    return Path(__file__).resolve().parents[1]

PROJECT_ROOT = guess_project_root()
DEFAULT_SCHEMA_PATH = PROJECT_ROOT / "docs/01-genesis/document_schema_v1.1.yaml"
DEFAULT_TARGETS = [
    PROJECT_ROOT / "docs/03-architecture/decisions",
    PROJECT_ROOT / "docs/03-architecture/rfcs",
    PROJECT_ROOT / "docs/03-architecture/observations",
]

ID_RE = re.compile(r"^(ADR|RFC|OBS|POC|SPRINT_DOC)-\d{4}(-v\d+)?$")
ID_ROOT_RE = re.compile(r"^(ADR|RFC|OBS|POC|SPRINT_DOC)-\d{4}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SHA256_RE = re.compile(r"^sha256:[a-f0-9]{64}$")
VERSION_RE = re.compile(r"^\d+\.\d+(?:\.\d+)?$")

FRONTMATTER_DELIM = re.compile(r"^---\s*$")

def read_text(path: Path) -> Optional[str]:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return None

def extract_frontmatter_blocks(text: str) -> Tuple[Optional[str], Optional[int], Optional[int]]:
    """
    Extrait le bloc front matter YAML sous forme de texte, et retourne aussi (start_idx, end_idx) de lignes (inclusifs).
    Retourne (None, None, None) si absent.
    """
    lines = text.splitlines(keepends=True)
    if not lines:
        return None, None, None
    if not FRONTMATTER_DELIM.match(lines[0]):
        return None, None, None
    for i in range(1, len(lines)):
        if FRONTMATTER_DELIM.match(lines[i]):
            block = "".join(lines[1:i])  # sans les délimiteurs
            return block, 0, i
    return None, None, None

def parse_yaml_block(yaml_text: str) -> Optional[Dict[str, Any]]:
    try:
        return yaml.safe_load(yaml_text) if yaml_text is not None else None
    except Exception as e:
        return None

def list_markdown_files(targets: List[Path]) -> List[Path]:
    out: List[Path] = []
    for t in targets:
        if not t.exists():
            continue
        out.extend(sorted(t.rglob("*.md")))
    return out

def load_schema(schema_path: Path) -> Optional[Dict[str, Any]]:
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Erreur de lecture du schéma: {schema_path}: {e}", file=sys.stderr)
        return None

def allowed_status_by_type(schema: Dict[str, Any]) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}
    st = schema.get("statuts_by_type", {})
    if isinstance(st, dict):
        for typ, obj in st.items():
            allowed = []
            for item in obj.get("allowed_statuts", []):
                val = item.get("value")
                if isinstance(val, str):
                    allowed.append(val)
            if allowed:
                out[typ] = allowed
    return out

def enum_list_from_schema(schema: Dict[str, Any], field_key: str) -> List[str]:
    """
    Récupère la liste des valeurs autorisées pour un champ énuméré
    depuis new_fields_v1_1.<field_key>.enum dans le schéma v1.1.
    """
    try:
        new_fields = schema.get("new_fields_v1_1", {})
        field = new_fields.get(field_key, {})
        enums = field.get("enum", [])
        return [str(x) for x in enums if isinstance(x, str)]
    except Exception:
        return []

def validate_date(date_str: str) -> Tuple[bool, Optional[str]]:
    if not DATE_RE.match(date_str):
        return False, "format_invalide"
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except Exception:
        return False, "date_non_parseable"
    now = datetime.now(timezone.utc)
    if dt > now:
        return False, "date_future"
    return True, None

def find_in(obj: Dict[str, Any], dotted: str) -> Any:
    cur: Any = obj
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur

def check_document_frontmatter(
    fm: Dict[str, Any],
    status_map: Dict[str, List[str]],
    schema: Dict[str, Any],
    strict: bool=False,
) -> List[str]:
    """
    Retourne une liste d'erreurs textuelles pour ce front matter.
    """
    errors: List[str] = []

    # Champs requis
    id_val = fm.get("id")
    typ = fm.get("type")
    status = fm.get("status")
    date_val = fm.get("date")

    if not isinstance(id_val, str) or not ID_RE.match(id_val):
        errors.append("id_invalide")
    if not isinstance(typ, str):
        errors.append("type_manquant_ou_invalide")
    if not isinstance(status, str):
        errors.append("status_manquant_ou_invalide")
    if not isinstance(date_val, str):
        errors.append("date_manquante_ou_invalide")

    # id/type cohérence (préfixe)
    if isinstance(id_val, str) and isinstance(typ, str):
        prefix = id_val.split("-")[0]
        if prefix != typ:
            # Cas particuliers: certains dépôts nomment type=ADR mais id "ADR-..." OK.
            # On exige l'égalité stricte pour ADR/RFC/OBS/POC/SPRINT_DOC
            errors.append("type_id_prefix_incoherent")

    # status autorisé par type (si possible)
    if isinstance(typ, str) and isinstance(status, str):
        allowed = status_map.get(typ)
        if isinstance(allowed, list) and allowed and status not in allowed:
            errors.append("status_non_autorise_pour_type")

    # Date format et futur
    if isinstance(date_val, str):
        ok, why = validate_date(date_val)
        if not ok:
            errors.append(f"date_invalide:{why}")

    # Succession: links.supersedes => previous_hash requis
    supersedes = find_in(fm, "links.supersedes")
    previous_hash = fm.get("previous_hash")
    if supersedes is not None:
        if not isinstance(previous_hash, str) or not SHA256_RE.match(previous_hash):
            errors.append("previous_hash_requis_ou_invalide_si_supersedes")

    # author et roles.author ne doivent pas coexister
    has_author_simple = "author" in fm
    roles = fm.get("roles")
    has_roles_author = False
    if isinstance(roles, dict) and "author" in roles:
        has_roles_author = True
    if has_author_simple and has_roles_author:
        errors.append("author_et_roles.author_coexistent")

    # Contrôles additionnels S8-STRICT
    # version
    ver = fm.get("version")
    if strict:
        if not isinstance(ver, str) or not VERSION_RE.match(ver):
            errors.append("version_manquante_ou_invalide")
    else:
        if ver is not None and (not isinstance(ver, str) or not VERSION_RE.match(ver)):
            errors.append("version_invalide")

    # id_root
    id_root = fm.get("id_root")
    if strict:
        if not isinstance(id_root, str) or not ID_ROOT_RE.match(id_root):
            errors.append("id_root_manquant_ou_invalide")
    else:
        if id_root is not None and (not isinstance(id_root, str) or not ID_ROOT_RE.match(id_root)):
            errors.append("id_root_invalide")

    # scope / pattern (énumérations depuis le schéma)
    allowed_scope = enum_list_from_schema(schema, "scope")
    allowed_pattern = enum_list_from_schema(schema, "pattern")
    sc = fm.get("scope")
    pt = fm.get("pattern")

    if strict:
        if not isinstance(sc, str) or (allowed_scope and sc not in allowed_scope):
            errors.append("scope_manquant_ou_invalide")
        if not isinstance(pt, str) or (allowed_pattern and pt not in allowed_pattern):
            errors.append("pattern_manquant_ou_invalide")
    else:
        if sc is not None and (not isinstance(sc, str) or (allowed_scope and sc not in allowed_scope)):
            errors.append("scope_invalide")
        if pt is not None and (not isinstance(pt, str) or (allowed_pattern and pt not in allowed_pattern)):
            errors.append("pattern_invalide")

    # decision_type (principalement pour ADR)
    allowed_decision_type = enum_list_from_schema(schema, "decision_type")
    dt = fm.get("decision_type")
    if isinstance(typ, str) and typ == "ADR":
        if strict:
            if not isinstance(dt, str) or (allowed_decision_type and dt not in allowed_decision_type):
                errors.append("decision_type_manquant_ou_invalide_pour_ADR")
        else:
            if dt is not None and (not isinstance(dt, str) or (allowed_decision_type and dt not in allowed_decision_type)):
                errors.append("decision_type_invalide_pour_ADR")
    else:
        # Si non-ADR et présent, valider le format si disponible
        if dt is not None and (not isinstance(dt, str) or (allowed_decision_type and dt not in allowed_decision_type)):
            errors.append("decision_type_invalide")

    # Validation structurelle de roles.* si présent (non requis en strict s'il est absent)
    if roles is not None:
        if not isinstance(roles, dict):
            errors.append("roles_invalide")
        else:
            # roles.author: liste d'objets {name, email?}
            if "author" in roles:
                auth = roles.get("author")
                if not isinstance(auth, list) or any(not isinstance(x, dict) or "name" not in x or not isinstance(x.get("name"), str) for x in auth):
                    errors.append("roles.author_invalide")
            # roles.reviewers: liste d'objets {name, reviewed_at?}
            if "reviewers" in roles:
                revs = roles.get("reviewers")
                if not isinstance(revs, list) or any(not isinstance(x, dict) or "name" not in x or not isinstance(x.get("name"), str) for x in revs):
                    errors.append("roles.reviewers_invalide")
            # roles.guardian: objet {name}
            if "guardian" in roles:
                g = roles.get("guardian")
                if not isinstance(g, dict) or "name" not in g or not isinstance(g.get("name"), str):
                    errors.append("roles.guardian_invalide")
            # roles.approved_by: liste d'objets {name, approved_at?}
            if "approved_by" in roles:
                appr = roles.get("approved_by")
                if not isinstance(appr, list) or any(not isinstance(x, dict) or "name" not in x or not isinstance(x.get("name"), str) for x in appr):
                    errors.append("roles.approved_by_invalide")

    return errors

def main() -> int:
    parser = argparse.ArgumentParser(description="SSOT v1.1 Schema Check")
    parser.add_argument("--ci", action="store_true", help="Mode CI (sortie plus concise)")
    parser.add_argument("--strict", action="store_true", help="Active les contrôles bloquants (auto en --ci)")
    parser.add_argument("--schema", type=str, default=str(DEFAULT_SCHEMA_PATH), help="Chemin vers document_schema_v1.1.yaml")
    parser.add_argument("--targets", nargs="*", default=[str(p) for p in DEFAULT_TARGETS], help="Répertoires à scanner (Markdown)")
    parser.add_argument("--registry-file", type=str, default=str(PROJECT_ROOT / "docs/_registry/registry_v1.1_v5.yaml"), help="Chemin du registre v1.1 (permet d'exempter les originaux Superseded)")
    args = parser.parse_args()
    strict = bool(getattr(args, "strict", False) or getattr(args, "ci", False))

    quiet = bool(args.ci)

    schema = load_schema(Path(args.schema))
    if schema is None:
        print(f"❌ Schéma introuvable ou illisible: {args.schema}", file=sys.stderr)
        return 2

    status_map = allowed_status_by_type(schema)

    # Construire la liste des chemins à exempter (originaux Superseded dans le registre)
    skip_paths: Set[Path] = set()
    try:
        reg_path = Path(getattr(args, "registry_file", "")).resolve()
        if reg_path.exists():
            with open(reg_path, "r", encoding="utf-8") as f:
                reg_data = yaml.safe_load(f)
            if isinstance(reg_data, dict):
                for lin in reg_data.get("lineages", []) or []:
                    versions = lin.get("versions", []) or []
                    for ver in versions:
                        if not isinstance(ver, dict):
                            continue
                        vstatus = ver.get("status")
                        vpath = ver.get("file_path")
                        if isinstance(vstatus, str) and isinstance(vpath, str) and vstatus.strip().lower() == "superseded":
                            abs_vpath = (PROJECT_ROOT / vpath).resolve()
                            skip_paths.add(abs_vpath)
    except Exception:
        # Tolérant: si le registre n'est pas lisible, on n'exempte rien
        skip_paths = set()

    md_files = list_markdown_files([Path(t) for t in args.targets])
    if not quiet:
        rel_items = []
        for t in args.targets:
            p = Path(t).resolve()
            try:
                rel_items.append(str(p.relative_to(PROJECT_ROOT)))
            except Exception:
                rel_items.append(str(p))
        rel_targets = ", ".join(rel_items)
        print(f"🔍 Validation front matter v1.1 sur {len(md_files)} fichier(s) dans: {rel_targets}")

    total_ok = 0
    total_err = 0

    for fp in md_files:
        abs_fp = fp.resolve()
        if abs_fp in skip_paths:
            if not quiet:
                print(f"⏭️  [SCHEMA-SKIP-SUPERSEDED] {fp}")
            continue
        txt = read_text(fp)
        if txt is None:
            print(f"❌ [READ] {fp}")
            total_err += 1
            continue

        block, start, end = extract_frontmatter_blocks(txt)
        if block is None:
            # Pas de front matter => non conforme v1.1
            print(f"❌ [FM-ABSENT] {fp}")
            total_err += 1
            continue

        fm = parse_yaml_block(block)
        if not isinstance(fm, dict):
            print(f"❌ [FM-NON-PARSEABLE] {fp}")
            total_err += 1
            continue

        errs = check_document_frontmatter(fm, status_map, schema, strict)
        if errs:
            print(f"❌ [SCHEMA] {fp}")
            if not quiet:
                for e in errs:
                    print(f"    - {e}")
            total_err += 1
        else:
            if not quiet:
                print(f"✅ [SCHEMA-OK] {fp}")
            total_ok += 1

    if not quiet:
        print("—" * 80)
        print(f"Récapitulatif: ok={total_ok}, errors={total_err}")

    if total_err > 0:
        return 2 if strict else 1
    else:
        return 0

if __name__ == "__main__":
    sys.exit(main())
