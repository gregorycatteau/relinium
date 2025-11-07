#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSOT v1.1 - Hash Check (triple-check - étape 1)
Objectifs:
  - Vérifier la cohérence des self_hash dans les documents Markdown (front matter v1.1)
  - Vérifier la cohérence du manifeste des hashs SSOT v1.1 (SSOT_V1_1_HASHES.yaml)
  - Lecture seule par défaut (aucune écriture sans drapeau explicite), adapté au CI (--ci)

Usage:
  python scripts/ssot_hash_check.py [--ci] [--hashes-file PATH] [--roots DIR ...]
  python scripts/ssot_hash_check.py --print-self-hash FILE
  python scripts/ssot_hash_check.py --write-self-hash FILE   # Utilisation locale uniquement (pas en CI)

Notes:
  - L'algorithme du self_hash consiste à recalculer le SHA256 du fichier complet
    en excluant uniquement la ligne 'self_hash: ...' située dans le front matter.
  - Le script retourne un code non nul s'il détecte au moins une divergence (self_hash, manifeste v1.1).
"""

import argparse
import hashlib
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Set

try:
    import yaml
except Exception as e:
    print("❌ PyYAML est requis: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

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
DEFAULT_HASHES_FILE = PROJECT_ROOT / "docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_HASHES.yaml"
DEFAULT_ROOTS = [
    PROJECT_ROOT / "docs",
    PROJECT_ROOT / "reports",
]
DEFAULT_REGISTRY_FILE = PROJECT_ROOT / "docs/_registry/registry_v1.1_v5.yaml"

SHA256_PREFIX = "sha256:"
SELF_HASH_KEY = "self_hash"

SELF_HASH_LINE_RE = re.compile(r"^\s*self_hash\s*:\s*(.+?)\s*$")
FRONTMATTER_DELIM = re.compile(r"^---\s*$")

# -----------------------------------------------------------------------------
# Utils
# -----------------------------------------------------------------------------

def calculate_sha256_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return SHA256_PREFIX + h.hexdigest()

def calculate_sha256_file(path: Path) -> str:
    if not path.exists():
        return "FILE_NOT_FOUND"
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for block in iter(lambda: f.read(65536), b""):
                h.update(block)
        return SHA256_PREFIX + h.hexdigest()
    except Exception as e:
        return f"ERROR: {e}"

def read_text(path: Path) -> Optional[str]:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return None

def extract_frontmatter_lines(lines: List[str]) -> Tuple[int, int]:
    """
    Retourne l'intervalle [start_idx, end_idx] (inclusifs) des lignes du front matter
    délimitées par les deux premiers '---' en début de fichier.
    Si front matter absent, retourne (-1, -1).
    """
    if not lines:
        return (-1, -1)
    if not FRONTMATTER_DELIM.match(lines[0]):
        return (-1, -1)
    # chercher la prochaine ligne '---'
    for i in range(1, len(lines)):
        if FRONTMATTER_DELIM.match(lines[i]):
            return (0, i)
    return (-1, -1)

def compute_self_hash_from_text(text: str) -> str:
    """
    Calcule le self_hash en excluant uniquement la ligne 'self_hash: ...'
    du front matter (entre les deux premières lignes ---).
    """
    # On travaille sur les lignes avec leur fin (préserve LF/CRLF tel que lu)
    lines = text.splitlines(keepends=True)
    start, end = extract_frontmatter_lines(lines)
    if start == -1:
        # Pas de front matter; le self_hash est défini alors qu'il n'y a pas de FM.
        data = text.encode("utf-8")
        return calculate_sha256_bytes(data)

    new_lines = []
    for idx, line in enumerate(lines):
        if start <= idx <= end:
            # Dans la section front matter: exclure la ligne self_hash
            if SELF_HASH_LINE_RE.match(line):
                continue
        new_lines.append(line)

    data = "".join(new_lines).encode("utf-8")
    return calculate_sha256_bytes(data)

def parse_yaml_file(path: Path) -> Optional[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Erreur YAML: {path}: {e}")
        return None

def collect_superseded_original_paths(registry_path: Path) -> Set[Path]:
    """
    Extrait, depuis le registre v1.1, les chemins des documents originaux (sans suffixe -vN)
    dont le statut est 'Superseded'. Ces fichiers ne doivent pas être modifiés (gouvernance),
    donc on les ignore dans le contrôle self_hash (pas d'avertissements bloquants en strict).
    """
    result: Set[Path] = set()
    data = parse_yaml_file(registry_path)
    if not isinstance(data, dict):
        return result

    lineages = data.get("lineages", [])
    for lin in lineages or []:
        versions = lin.get("versions", []) if isinstance(lin, dict) else []
        for v in versions:
            if not isinstance(v, dict):
                continue
            vid = str(v.get("id", ""))
            status = str(v.get("status", ""))
            fpath = v.get("file_path")
            if not fpath or not isinstance(fpath, str):
                continue
            # Original si pas de suffixe '-vN'
            is_original = not re.search(r"-v\d+\b", vid)
            if is_original and status == "Superseded":
                abs_path = (PROJECT_ROOT / fpath).resolve()
                result.add(abs_path)
    return result

def iter_markdown_files(roots: List[Path]) -> List[Path]:
    out: List[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*.md"):
            # Exclure éventuellement certains dossiers techniques si besoin
            out.append(p)
    return out

def find_self_hash_in_frontmatter(text: str) -> Optional[str]:
    lines = text.splitlines(keepends=False)
    start, end = extract_frontmatter_lines([l + "\n" for l in lines])  # réutilise helper
    if start == -1:
        return None
    for i in range(start, end + 1):
        m = SELF_HASH_LINE_RE.match(lines[i])
        if m:
            return m.group(1).strip()
    return None

# -----------------------------------------------------------------------------
# Checks
# -----------------------------------------------------------------------------

def check_markdown_self_hash(files: List[Path], quiet: bool=False) -> Tuple[int, int, int]:
    """
    Retourne (ok_count, warn_count, err_count)
      - ok    : self_hash présent et valide
      - warn  : self_hash absent (non bloquant)
      - err   : self_hash présent mais invalide
    """
    ok = warn = err = 0
    for fp in files:
        txt = read_text(fp)
        if txt is None:
            print(f"❌ [READ] {fp}")
            err += 1
            continue

        declared = find_self_hash_in_frontmatter(txt)
        if declared is None:
            # self_hash absent -> on log en avertissement pour l'instant
            if not quiet:
                print(f"⚠️  [SELF_HASH-MISSING] {fp}")
            warn += 1
            continue

        # Placeholder explicite interdit en mode strict (et signalé comme erreur)
        if isinstance(declared, str) and declared.endswith("(to_be_calculated)"):
            print(f"❌ [SELF_HASH-PLACEHOLDER] {fp}")
            err += 1
            continue

        actual = compute_self_hash_from_text(txt)
        if declared == actual:
            if not quiet:
                print(f"✅ [SELF_HASH-OK] {fp}")
            ok += 1
        else:
            print(f"❌ [SELF_HASH-DIVERGENCE] {fp}")
            if not quiet:
                print(f"    déclaré: {declared}")
                print(f"    calculé: {actual}")
            err += 1
    return ok, warn, err

def _collect_hash_entries(node: Any, entries: List[Tuple[Path, str, str]]) -> None:
    """
    Collecte récursivement les tuples (path, expected_hash, context) à partir
    d'une structure YAML hétérogène. On considère 'file' + 'hash' comme une entrée valable.
    """
    if isinstance(node, dict):
        # Si c'est un noeud document avec 'file' et 'hash'
        if "file" in node and "hash" in node:
            file_path = (PROJECT_ROOT / node["file"]).resolve()
            h = node["hash"]
            ctx = ""
            # Essayons d'extraire un contexte humainement lisible (id, key parent, etc.)
            # On ne veut pas être fragile, donc minimal.
            if "created_at" in node:
                ctx = f"created_at={node['created_at']}"
            entries.append((file_path, str(h), ctx))
        else:
            # Sinon descente récursive
            for k, v in node.items():
                _collect_hash_entries(v, entries)
    elif isinstance(node, list):
        for it in node:
            _collect_hash_entries(it, entries)
    else:
        # scalaires
        return

def check_hash_manifest(manifest_path: Path, quiet: bool=False, strict: bool=False) -> Tuple[int, int, int]:
    """
    Vérifie le manifeste SSOT_V1_1_HASHES.yaml:
      - pour toute entrée avec hash 'sha256:...' (ni 'to_be_calculated'), recalcul et comparaison
    Retourne (ok_count, skip_count, err_count)
    """
    data = parse_yaml_file(manifest_path)
    if data is None:
        print(f"❌ Impossible de lire {manifest_path}")
        return (0, 0, 1)

    entries: List[Tuple[Path, str, str]] = []
    _collect_hash_entries(data, entries)

    ok = skip = err = 0
    for (path, expected, ctx) in entries:
        if not expected.startswith(SHA256_PREFIX) or expected.endswith("(to_be_calculated)"):
            if strict:
                print(f"❌ [HASH-PLACEHOLDER] {path} hash='{expected}' {f'({ctx})' if ctx else ''}")
                err += 1
            else:
                if not quiet:
                    print(f"⏭️  [SKIP] {path} hash='{expected}' {f'({ctx})' if ctx else ''}")
                skip += 1
            continue

        actual = calculate_sha256_file(path)
        if actual == "FILE_NOT_FOUND":
            print(f"❌ [HASH-FILE-NOT-FOUND] {path}")
            err += 1
        elif actual.startswith("ERROR:"):
            print(f"❌ [HASH-ERROR] {path} -> {actual}")
            err += 1
        elif actual == expected:
            if not quiet:
                print(f"✅ [HASH-OK] {path}")
            ok += 1
        else:
            print(f"❌ [HASH-DIVERGENCE] {path}")
            if not quiet:
                print(f"    attendu: {expected}")
                print(f"    calculé: {actual}")
                if ctx:
                    print(f"    contexte: {ctx}")
            err += 1

    return ok, skip, err

# -----------------------------------------------------------------------------
# Actions utilitaires locales (hors CI)
# -----------------------------------------------------------------------------

def print_self_hash(file_path: Path) -> int:
    txt = read_text(file_path)
    if txt is None:
        print(f"❌ Lecture impossible: {file_path}", file=sys.stderr)
        return 2
    actual = compute_self_hash_from_text(txt)
    print(actual)
    return 0

def write_self_hash(file_path: Path) -> int:
    """
    Ecrit (ou met à jour) la ligne self_hash dans le front matter.
    Utilisation locale uniquement. Ne pas activer en CI.
    """
    txt = read_text(file_path)
    if txt is None:
        print(f"❌ Lecture impossible: {file_path}", file=sys.stderr)
        return 2

    actual = compute_self_hash_from_text(txt)
    lines = txt.splitlines(keepends=True)
    start, end = extract_frontmatter_lines(lines)
    if start == -1:
        print(f"❌ Front matter introuvable: {file_path}", file=sys.stderr)
        return 3

    replaced = False
    new_lines: List[str] = []
    for idx, line in enumerate(lines):
        if start <= idx <= end and SELF_HASH_LINE_RE.match(line):
            new_lines.append(f"self_hash: {actual}\n")
            replaced = True
        else:
            new_lines.append(line)

    if not replaced:
        # insérer avant la fermeture du front matter (ligne '---' fin)
        insert_at = end  # avant la deuxième ligne '---'
        new_lines = new_lines[:insert_at] + [f"self_hash: {actual}\n"] + new_lines[insert_at:]

    try:
        file_path.write_text("".join(new_lines), encoding="utf-8")
        print(f"✍️  self_hash écrit: {file_path} -> {actual}")
        return 0
    except Exception as e:
        print(f"❌ Ecriture impossible: {file_path}: {e}", file=sys.stderr)
        return 4

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="SSOT v1.1 Hash Check (self_hash + manifeste hashes)")
    parser.add_argument("--ci", action="store_true", help="Mode CI (sortie plus concise)")
    parser.add_argument("--strict", action="store_true", help="Active les contrôles bloquants (auto en --ci)")
    parser.add_argument("--hashes-file", type=str, default=str(DEFAULT_HASHES_FILE), help="Chemin du manifeste de hashs v1.1")
    parser.add_argument("--roots", nargs="*", default=[str(p) for p in DEFAULT_ROOTS], help="Racines à scanner pour les Markdown (self_hash)")
    parser.add_argument("--print-self-hash", dest="print_self_hash", type=str, default=None, help="Calcule et affiche le self_hash d'un fichier Markdown")
    parser.add_argument("--write-self-hash", dest="write_self_hash", type=str, default=None, help="Ecrit/Met à jour le self_hash (usage local uniquement - pas en CI)")
    parser.add_argument("--registry-file", type=str, default=str(DEFAULT_REGISTRY_FILE), help="Chemin du registre v1.1 (pour ignorer les originaux 'Superseded')")
    args = parser.parse_args()
    strict = bool(getattr(args, "strict", False) or getattr(args, "ci", False))

    if args.print_self_hash:
        return print_self_hash(Path(args.print_self_hash).resolve())

    if args.write_self_hash:
        if args.ci:
            print("❌ --write-self-hash ne doit pas être utilisé en CI", file=sys.stderr)
            return 2
        return write_self_hash(Path(args.write_self_hash).resolve())

    quiet = bool(args.ci)

    # 1) Vérification self_hash
    md_files = iter_markdown_files([Path(p) for p in args.roots])

    # Charger registre pour ignorer les originaux 'Superseded' (gouvernance)
    skip_set: Set[Path] = set()
    try:
        reg_path = Path(getattr(args, "registry_file", str(DEFAULT_REGISTRY_FILE)))
        if reg_path.exists():
            skip_set = collect_superseded_original_paths(reg_path)
    except Exception:
        skip_set = set()

    if skip_set:
        before = len(md_files)
        md_files = [p for p in md_files if p.resolve() not in skip_set]
        if not quiet:
            print(f"⏭️  Ignorés (originaux Superseded via registre): {before - len(md_files)}")

    if not quiet:
        print(f"🔍 Vérification self_hash sur {len(md_files)} fichier(s) Markdown...")
    ok_sh, warn_sh, err_sh = check_markdown_self_hash(md_files, quiet=quiet)
    if not quiet:
        print(f"    ✅ valides: {ok_sh} | ⚠️  absents: {warn_sh} | ❌ divergences: {err_sh}")

    # 2) Vérification manifeste v1.1
    hashes_file = Path(args.hashes_file)
    if hashes_file.exists():
        if not quiet:
            try:
                rel = hashes_file.relative_to(PROJECT_ROOT)
            except Exception:
                rel = hashes_file
            print(f"🔐 Vérification du manifeste: {rel}")
        ok_m, skip_m, err_m = check_hash_manifest(hashes_file, quiet=quiet, strict=strict)
        if not quiet:
            print(f"    ✅ ok: {ok_m} | ⏭️  ignorés: {skip_m} | ❌ divergences: {err_m}")
    else:
        try:
            rel = hashes_file.relative_to(PROJECT_ROOT)
        except Exception:
            rel = hashes_file
        print(f"⚠️  Manifeste inexistant (skip): {rel}")
        ok_m = skip_m = 0
        err_m = 0

    # Politique de retour: échec si divergences détectées
    if not quiet:
        print("—" * 80)
        print(f"Récapitulatif: self_hash_err={err_sh}, manifest_err={err_m}, warnings={warn_sh}, manifest_skip={skip_m}")
    # Codes de sortie:
    #  - 0: OK
    #  - 2: écarts critiques (bloquant CI)
    # Politique Phase 3: seules les divergences (err) sont bloquantes; les warnings n'impactent pas le code retour.
    crit_errors = err_sh + err_m
    if crit_errors > 0:
        return 2
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
