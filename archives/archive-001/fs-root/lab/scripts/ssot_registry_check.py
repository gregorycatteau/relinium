#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSOT v1.1 - Registry Check (triple-check - étape 2)
Objectifs:
  - Vérifier la couverture du registre v1.1 vs fichiers normatifs (détecter les manques)
  - Vérifier la cohérence basique: id_root, id, status, file_path, previous_hash format
  - Lecture seule par défaut, adapté au CI (--ci)

Usage:
  python scripts/ssot_registry_check.py [--ci] [--registry-file PATH] [--scan-roots DIR ...]
"""

import argparse
import re
import hashlib
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

try:
    import yaml
except Exception:
    print("❌ PyYAML est requis: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

def guess_project_root() -> Path:
    """
    Détecte le vrai root du dépôt en priorisant le répertoire qui contient
    le registre v1.1 (docs/_registry/registry_v1.1.yaml). Évite de confondre
    avec un sous-dossier (ex: lab/) qui possède aussi 'scripts'.
    """
    candidates = [
        # Prioriser le repo root (un niveau au-dessus de 'scripts')
        Path(__file__).resolve().parents[2],
        # Ensuite le parent direct (utile si structure différente)
        Path(__file__).resolve().parents[1],
        # Puis CWD et son parent (exécutions depuis sous-dossiers)
        Path.cwd(),
        Path.cwd().parent,
    ]

    # 1) Chercher un candidat qui contient explicitement le registre v1.1
    for c in candidates:
        try:
            if (c / "docs/_registry/registry_v1.1.yaml").exists():
                return c
        except Exception:
            continue

    # 2) Fallback: répertoire qui a 'docs' et 'scripts'
    for c in candidates:
        try:
            if (c / "docs").exists() and (c / "scripts").exists():
                return c
        except Exception:
            continue

    # 3) Dernier recours: le repo root supposé (parents[2]) sinon parents[1]
    p2 = Path(__file__).resolve().parents[2]
    if (p2 / "docs").exists():
        return p2
    return Path(__file__).resolve().parents[1]

PROJECT_ROOT = guess_project_root()
DEFAULT_REGISTRY_FILE = PROJECT_ROOT / "docs/_registry/registry_v1.1.yaml"
DEFAULT_SCAN_ROOTS = [
    PROJECT_ROOT / "docs/03-architecture/decisions",
    PROJECT_ROOT / "docs/03-architecture/rfcs",
    PROJECT_ROOT / "docs/03-architecture/observations",
    PROJECT_ROOT / "docs/observatory",
    PROJECT_ROOT / "docs/sprints",
    PROJECT_ROOT / "reports",
]

ID_ROOT_RE = re.compile(r"^(ADR|RFC|OBS|POC|SPRINT|SPRINT_DOC)-\d{4}$")
ID_RE = re.compile(r"^(ADR|RFC|OBS|POC|SPRINT|SPRINT_DOC)-\d{4}(-v\d+)?$")
SHA256_RE = re.compile(r"^sha256:[a-f0-9]{64}$")

def parse_yaml_file(path: Path) -> Optional[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Erreur YAML: {path}: {e}", file=sys.stderr)
        return None

def calculate_sha256_file(path: Path) -> Optional[str]:
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for block in iter(lambda: f.read(65536), b""):
                h.update(block)
        return f"sha256:{h.hexdigest()}"
    except Exception:
        return None

def list_normative_files(roots: Iterable[Path]) -> List[Path]:
    out: List[Path] = []
    for root in roots:
        if root.exists():
            out.extend(sorted(root.rglob("*.md")))
    return out

def extract_id_from_filename(p: Path) -> Optional[str]:
    """
    Essaie d'extraire l'ID documentaire à partir du nom de fichier, ex:
      ADR-0001-repo-driven-by-docs-first.md      -> ADR-0001
      ADR-0001-repo-driven-by-docs-first-v2.md   -> ADR-0001-v2
      RFC-001-xxx.md                             -> RFC-001
      RFC-001-xxx-v2.md                          -> RFC-001-v2
    """
    name = p.name
    m = re.match(r"^(ADR|RFC|OBS|POC|SPRINT_DOC)-(\d{4})(?:-.*?)(?:-v(\d+))?\.md$", name)
    if not m:
        # autre pattern possible: "RFC-001.md" (rare)
        m2 = re.match(r"^(ADR|RFC|OBS|POC|SPRINT_DOC)-(\d{4})(-v(\d+))?\.md$", name)
        if m2:
            if m2.group(4):
                return f"{m2.group(1)}-{m2.group(2)}-v{m2.group(4)}"
            else:
                return f"{m2.group(1)}-{m2.group(2)}"
        return None
    type_part, num_part, vpart = m.group(1), m.group(2), m.group(3)
    if vpart:
        return f"{type_part}-{num_part}-v{vpart}"
    return f"{type_part}-{num_part}"

def id_root_of(doc_id: str) -> Optional[str]:
    if not ID_RE.match(doc_id):
        return None
    return doc_id.split("-v")[0] if "-v" in doc_id else doc_id

def build_registry_index(
    reg: Dict[str, Any]
) -> Tuple[Set[str], Set[str], Dict[str, Path], Set[Path], Set[Path]]:
    """
    Construit des index:
      - all_ids_in_versions: tous les 'id' présents dans lineages[].versions[]
      - all_id_roots: tous les id_root
      - path_by_id: map id -> file_path absolu (dernière occurrence)
      - pending_paths: ensemble des file_path listés dans pending_migration
      - registered_paths: ensemble de tous les file_path référencés dans lineages
    """
    all_ids: Set[str] = set()
    all_roots: Set[str] = set()
    path_by_id: Dict[str, Path] = {}
    pending_paths: Set[Path] = set()
    registered_paths: Set[Path] = set()

    lineages = reg.get("lineages", [])
    if isinstance(lineages, list):
        for lin in lineages:
            root = lin.get("id_root")
            if isinstance(root, str):
                all_roots.add(root)
            versions = lin.get("versions", [])
            if isinstance(versions, list):
                for ver in versions:
                    vid = ver.get("id")
                    fp = ver.get("file_path")
                    if isinstance(vid, str):
                        all_ids.add(vid)
                        if isinstance(fp, str):
                            abs_fp = (PROJECT_ROOT / fp).resolve()
                            path_by_id[vid] = abs_fp
                            registered_paths.add(abs_fp)

    pending = reg.get("pending_migration", [])
    if isinstance(pending, list):
        for p in pending:
            fp = p.get("file_path")
            if isinstance(fp, str):
                pending_paths.add((PROJECT_ROOT / fp).resolve())

    return all_ids, all_roots, path_by_id, pending_paths, registered_paths

def check_registry_structure(reg: Dict[str, Any], quiet: bool=False, strict: bool=False) -> Tuple[int, int]:
    """
    Contrôles structurels minimaux:
      - id_root pattern
      - id pattern, cohérence avec id_root
      - file_path présent et fichier existant
      - previous_hash format si présent
    Retourne (warn_count, err_count)
    """
    warn = err = 0
    lineages = reg.get("lineages", [])
    if not isinstance(lineages, list):
        print("❌ 'lineages' manquant ou invalide dans le registre", file=sys.stderr)
        return (warn, err + 1)

    for lin in lineages:
        id_root_val = lin.get("id_root")
        if not isinstance(id_root_val, str) or not ID_ROOT_RE.match(id_root_val):
            print(f"❌ [REG-ROOT] id_root invalide: {id_root_val}")
            err += 1

        versions = lin.get("versions", [])
        if not isinstance(versions, list) or not versions:
            print(f"⚠️  [REG-VERSIONS] Aucune version listée pour {id_root_val}")
            warn += 1
            continue

        for ver in versions:
            vid = ver.get("id")
            vstatus = ver.get("status")
            vpath = ver.get("file_path")
            vprev = ver.get("previous_hash")

            if not isinstance(vid, str) or not ID_RE.match(vid):
                print(f"❌ [REG-ID] id invalide: {vid} (id_root={id_root_val})")
                err += 1
            else:
                # cohérence id_root
                root_of_id = id_root_of(vid)
                if root_of_id != id_root_val:
                    print(f"❌ [REG-IDROOT] incohérence id/id_root: id={vid} id_root={id_root_val}")
                    err += 1

            if not isinstance(vpath, str) or not vpath.strip():
                print(f"❌ [REG-PATH] file_path manquant pour id={vid}")
                err += 1
            else:
                abs_path = (PROJECT_ROOT / vpath).resolve()
                if not abs_path.exists():
                    print(f"❌ [REG-PATH-MISSING] Fichier inexistant: {abs_path}")
                    err += 1
                # Validation du hash (si présent)
                vhash = ver.get("hash")
                if isinstance(vhash, str):
                    if vhash.endswith("(to_be_calculated)"):
                        if strict:
                            print(f"❌ [REG-HASH-PLACEHOLDER] id={vid} path={abs_path} hash='{vhash}'")
                            err += 1
                    elif SHA256_RE.match(vhash):
                        actual = calculate_sha256_file(abs_path)
                        if actual is None:
                            print(f"⚠️  [REG-HASH-CALC-FAIL] id={vid} path={abs_path}")
                            warn += 1
                        elif actual != vhash:
                            print(f"❌ [REG-HASH-DIVERGENCE] id={vid} path={abs_path}")
                            if not quiet:
                                print(f"    attendu: {vhash}")
                                print(f"    calculé: {actual}")
                            err += 1
                    else:
                        print(f"❌ [REG-HASH-FORMAT] id={vid} hash invalide: {vhash}")
                        err += 1
                else:
                    if strict:
                        print(f"❌ [REG-HASH-MISSING] id={vid} path={abs_path}")
                        err += 1
                    else:
                        print(f"⚠️  [REG-HASH-MISSING] id={vid} path={abs_path}")
                        warn += 1

            if vprev is not None and (not isinstance(vprev, str) or not SHA256_RE.match(vprev)):
                print(f"❌ [REG-PREVIOUS] previous_hash invalide pour id={vid}: {vprev}")
                err += 1

            # status: on vérifie juste présence (les valeurs fines diffèrent selon type/locale)
            if vstatus is None:
                print(f"⚠️  [REG-STATUS] status manquant pour id={vid}")
                warn += 1

    return warn, err

def check_pending_migration(reg: Dict[str, Any], quiet: bool=False, strict: bool=False) -> Tuple[int, int]:
    """
    Vérifie pending_migration:
      - 'file_path' existe
      - 'hash' présent, format sha256:..., cohérent avec le fichier
      - 'status' présent
    Retourne (warn_count, err_count)
    """
    warn = err = 0
    pending = reg.get("pending_migration", [])
    if not isinstance(pending, list):
        return warn, err

    for item in pending:
        if not isinstance(item, dict):
            continue
        pid = item.get("id")
        ppath = item.get("file_path")
        phash = item.get("hash")
        pstatus = item.get("status")

        if not isinstance(ppath, str) or not ppath.strip():
            print(f"❌ [PEND-PATH] file_path manquant pour id={pid}")
            err += 1
            continue

        abs_path = (PROJECT_ROOT / ppath).resolve()
        if not abs_path.exists():
            print(f"❌ [PEND-PATH-MISSING] Fichier inexistant: {abs_path} (id={pid})")
            err += 1

        # status requis
        if not isinstance(pstatus, str) or not pstatus.strip():
            if strict:
                print(f"❌ [PEND-STATUS-MISSING] id={pid} path={abs_path}")
                err += 1
            else:
                print(f"⚠️  [PEND-STATUS-MISSING] id={pid} path={abs_path}")
                warn += 1

        # hash requis
        if not isinstance(phash, str) or not SHA256_RE.match(phash):
            if strict:
                print(f"❌ [PEND-HASH-MISSING_OR_INVALID] id={pid} path={abs_path} hash='{phash}'")
                err += 1
            else:
                print(f"⚠️  [PEND-HASH-MISSING_OR_INVALID] id={pid} path={abs_path} hash='{phash}'")
                warn += 1
        else:
            actual = calculate_sha256_file(abs_path)
            if actual is None:
                print(f"⚠️  [PEND-HASH-CALC-FAIL] id={pid} path={abs_path}")
                warn += 1
            elif actual != phash:
                print(f"❌ [PEND-HASH-DIVERGENCE] id={pid} path={abs_path}")
                if not quiet:
                    print(f"    attendu: {phash}")
                    print(f"    calculé: {actual}")
                err += 1

    return warn, err

def check_registry_coverage(reg: Dict[str, Any], scan_roots: Iterable[Path], quiet: bool=False) -> Tuple[int, int]:
    """
    Vérifie la couverture:
      - Chaque fichier normatif trouvé sous scan_roots est présent soit dans lineages.versions,
        soit dans pending_migration.
    Retourne (warn_count, err_count)
    """
    warn = err = 0
    all_ids, all_roots, path_by_id, pending_paths, registered_paths = build_registry_index(reg)

    normative_files = list_normative_files(scan_roots)
    known_paths: Set[Path] = registered_paths | pending_paths

    # chemins normalisés vers absolus
    missing_in_registry: List[Path] = []
    for f in normative_files:
        if f.resolve() not in known_paths:
            missing_in_registry.append(f)

    if missing_in_registry:
        print("❌ [REG-COVERAGE] Fichiers normatifs non couverts par le registre ou pending_migration:")
        for f in missing_in_registry:
            print(f"    - {f}")
        err += len(missing_in_registry)
    else:
        if not quiet:
            print("✅ [REG-COVERAGE] Couverture registre OK sur les répertoires scannés")

    return warn, err

def check_required_entries(reg: Dict[str, Any], quiet: bool=False, strict: bool=False) -> Tuple[int, int]:
    """
    Vérifie la présence explicite d'entrées requises:
      - RFC-004 (alignment protocol) dans le registre (lineages/versions.file_path) ou pending_migration
      - OBS-0001..0003 dans le registre ou pending_migration
    Retourne (warn_count, err_count)
    """
    warn = err = 0

    # Indexer file_paths et ids connus
    file_paths: Set[Path] = set()
    ids_present: Set[str] = set()

    lineages = reg.get("lineages", [])
    if isinstance(lineages, list):
        for lin in lineages:
            root = lin.get("id_root")
            if isinstance(root, str):
                ids_present.add(root)
            versions = lin.get("versions", [])
            if isinstance(versions, list):
                for ver in versions:
                    vid = ver.get("id")
                    if isinstance(vid, str):
                        ids_present.add(vid)
                    vpath = ver.get("file_path")
                    if isinstance(vpath, str):
                        file_paths.add((PROJECT_ROOT / vpath).resolve())

    pending = reg.get("pending_migration", [])
    if isinstance(pending, list):
        for it in pending:
            pid = it.get("id")
            if isinstance(pid, str):
                ids_present.add(pid)
            ppath = it.get("file_path")
            if isinstance(ppath, str):
                file_paths.add((PROJECT_ROOT / ppath).resolve())

    # 1) RFC-004: vérifier via file_path (tolérant sur pattern d'ID)
    rfc004_path = (PROJECT_ROOT / "docs/03-architecture/rfcs/RFC-004-alignment-protocol.md").resolve()
    if rfc004_path not in file_paths:
        msg = f"[REQ] RFC-004 manquant dans le registre/pending_migration (path={rfc004_path})"
        if strict:
            print(f"❌ {msg}")
            err += 1
        else:
            print(f"⚠️  {msg}")
            warn += 1

    # 2) OBS-0001..0003: vérifier via IDs (présents en pending_migration ou lineages)
    required_obs = ["OBS-0001", "OBS-0002", "OBS-0003"]
    for rid in required_obs:
        if rid not in ids_present:
            msg = f"[REQ] {rid} manquant dans le registre/pending_migration"
            if strict:
                print(f"❌ {msg}")
                err += 1
            else:
                print(f"⚠️  {msg}")
                warn += 1

    return warn, err

def main() -> int:
    parser = argparse.ArgumentParser(description="SSOT v1.1 Registry Check")
    parser.add_argument("--ci", action="store_true", help="Mode CI (sortie plus concise)")
    parser.add_argument("--strict", action="store_true", help="Active les contrôles bloquants (auto en --ci)")
    parser.add_argument("--registry-file", type=str, default=str(DEFAULT_REGISTRY_FILE), help="Chemin du registre v1.1")
    parser.add_argument("--scan-roots", nargs="*", default=[str(p) for p in DEFAULT_SCAN_ROOTS], help="Racines à scanner pour couverture")
    args = parser.parse_args()

    quiet = bool(args.ci)
    strict = bool(getattr(args, "strict", False) or getattr(args, "ci", False))

    registry_path = Path(args.registry_file)
    reg = parse_yaml_file(registry_path)
    if reg is None:
        print(f"❌ Impossible de lire le registre: {registry_path}", file=sys.stderr)
        return 2

    if not quiet:
        print(f"🔎 Vérification structure du registre: {registry_path.relative_to(PROJECT_ROOT)}")
    w1, e1 = check_registry_structure(reg, quiet=quiet, strict=strict)

    if not quiet:
        print(f"📚 Vérification couverture vs fichiers: {', '.join([str(Path(r).relative_to(PROJECT_ROOT)) for r in args.scan_roots])}")
    w2, e2 = check_registry_coverage(reg, scan_roots=[Path(r) for r in args.scan_roots], quiet=quiet)

    # Vérifications spécifiques pending_migration
    if not quiet:
        print(f"🧩 Vérification pending_migration (hash/status/cohérence)")
    w3, e3 = check_pending_migration(reg, quiet=quiet, strict=strict)

    # Vérifications d'existence: RFC-004 et OBS-0001..0003
    if not quiet:
        print(f"🧷 Vérification des entrées requises (RFC-004, OBS-0001..0003)")
    w4, e4 = check_required_entries(reg, quiet=quiet, strict=strict)

    total_w = w1 + w2 + w3 + w4
    total_e = e1 + e2 + e3 + e4

    if not quiet:
        print("—" * 80)
        print(f"Récapitulatif: warnings={total_w}, errors={total_e}")

    # Codes de sortie:
    #  - 0: OK
    #  - 1: écarts mineurs (warnings uniquement)
    #  - 2: écarts critiques (bloquant CI)
    crit_errors = total_e + (total_w if strict else 0)
    if crit_errors > 0:
        return 2
    elif total_w > 0:
        return 1
    else:
        return 0

if __name__ == "__main__":
    sys.exit(main())
