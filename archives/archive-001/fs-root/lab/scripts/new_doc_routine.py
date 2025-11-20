#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Routine d'assistance pour la création/mise à jour des documents normatifs.

Étapes principales :
  1. Génère/actualise le front matter (sans/avec self_hash).
  2. Conserve ou injecte le corps du document (template optionnel).
  3. Calcule le self_hash (logique partagée avec ssot_hash_check.py).
  4. Met à jour le registre v1.1 (création ou rafraîchissement d'une version).
  5. Exécute les validations locales (validate_frontmatter + make docs-check).
  6. Commit automatique des fichiers mis à jour (sauf --skip-commit).
"""

from __future__ import annotations

import argparse
import hashlib
import io
import subprocess
import sys
from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.scalarstring import DoubleQuotedScalarString as DQ

SCRIPT_DIR = Path(__file__).resolve().parent


def guess_repo_root() -> Path:
    candidates = [SCRIPT_DIR] + list(SCRIPT_DIR.parents) + [Path.cwd()] + list(Path.cwd().parents)
    visited = set()
    for candidate in candidates:
        candidate = candidate.resolve()
        if candidate in visited:
            continue
        visited.add(candidate)
        if (candidate / ".git").exists():
            return candidate
        docs_registry = candidate / "docs/_registry/registry_v1.1.yaml"
        if docs_registry.exists():
            return candidate
    return SCRIPT_DIR.parent


REPO_ROOT = guess_repo_root()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from ssot_hash_check import compute_self_hash_from_text  # type: ignore  # noqa: E402

DEFAULT_REGISTRY_PATH = REPO_ROOT / "docs/_registry/registry_v1.1.yaml"
DEFAULT_HASH_MANIFEST_PATH = (
    REPO_ROOT / "docs/sprints/SSOT-v1.1/03-validation/SSOT_V1_1_HASHES.yaml"
)
FRONTMATTER_FIELDS_ORDER = [
    "id",
    "type",
    "status",
    "date",
    "author",
    "version",
    "title",
    "scope",
    "pattern",
    "tags",
    "links",
]


@dataclass
class RoutineConfig:
    path: Path
    id: str
    id_root: str
    doc_type: str
    status: str
    date: str
    version: str
    author: str
    tags: List[str]
    links: OrderedDict[str, List[str]]
    body_template: Optional[Path]
    overwrite_body: bool
    registry_path: Path
    doc_title: Optional[str]
    lineage_title: Optional[str]
    scope: Optional[str]
    pattern: Optional[str]
    commit_message: str
    skip_validations: bool
    skip_commit: bool
    extra_frontmatter: Dict[str, str]
    links_delimiter: str
    previous_hash: Optional[str]
    hash_manifest_path: Path


def parse_args() -> RoutineConfig:
    parser = argparse.ArgumentParser(
        description="Automatise la création/mise à jour d'un document SSOT + registre."
    )
    parser.add_argument("--path", required=True, help="Chemin du document (relatif au repo).")
    parser.add_argument("--id", required=True, help="Identifiant documentaire (ex: SPRINT-0002).")
    parser.add_argument("--id-root", dest="id_root", help="id_root pour le registre (défaut=id).")
    parser.add_argument("--type", dest="doc_type", required=True, help="Type documentaire (SPRINT, OBS, ...).")
    parser.add_argument("--status", required=True, help='Statut (ex: "En cours", "Active").')
    parser.add_argument("--date", help="Date ISO (YYYY-MM-DD). Défaut: aujourd'hui si non fournie.")
    parser.add_argument("--version", required=True, help="Version sémantique (ex: 1.0.0).")
    parser.add_argument("--author", required=True, help="Auteur à consigner dans le front matter.")
    parser.add_argument("--tags", help="Liste de tags séparés par des virgules.")
    parser.add_argument(
        "--links",
        help=(
            "Liens séparés par des virgules. Forme avancée: cle:val1,val2;autre_cle:val3."
            " Sans cle explicite, --links-key est utilisé."
        ),
    )
    parser.add_argument(
        "--links-key",
        default="cites",
        help="Clé par défaut pour les liens (si --links n'indique pas de cle explicite).",
    )
    parser.add_argument(
        "--links-delimiter",
        default=";",
        help="Délimiteur entre groupes de liens dans --links (défaut: ';').",
    )
    parser.add_argument("--body-template", help="Fichier Markdown à utiliser comme corps initial.")
    parser.add_argument(
        "--overwrite-body",
        action="store_true",
        help="Remplace explicitement le corps existant par le template fourni.",
    )
    parser.add_argument(
        "--registry",
        default=str(DEFAULT_REGISTRY_PATH),
        help="Chemin du registre v1.1 à mettre à jour.",
    )
    parser.add_argument(
        "--hash-manifest",
        default=str(DEFAULT_HASH_MANIFEST_PATH),
        help="Chemin du manifeste SSOT_V1_1_HASHES.yaml à synchroniser.",
    )
    parser.add_argument("--title", dest="doc_title", help="Champ title à ajouter dans le front matter.")
    parser.add_argument(
        "--lineage-title",
        help="Titre à stocker dans le registre (défaut: --title ou premier H1 du document).",
    )
    parser.add_argument("--scope", help="Champ scope à propager dans le registre.")
    parser.add_argument("--pattern", help="Champ pattern à propager dans le registre.")
    parser.add_argument(
        "--commit-message",
        help="Message de commit automatique. Défaut: docs(<ID>): update via new_doc_routine.",
    )
    parser.add_argument("--skip-validations", action="store_true", help="N'exécute pas les validations.")
    parser.add_argument("--skip-commit", action="store_true", help="N'effectue pas de commit automatique.")
    parser.add_argument(
        "--extra-frontmatter",
        action="append",
        default=[],
        help="Clé=valeur additionnelle à injecter dans le front matter (répétable).",
    )
    parser.add_argument(
        "--previous-hash",
        help="Valeur à stocker dans previous_hash pour la version du registre (optionnel).",
    )

    args = parser.parse_args()

    target_path = Path(args.path)
    if not target_path.is_absolute():
        target_path = (REPO_ROOT / target_path).resolve()

    registry_path = Path(args.registry)
    if not registry_path.is_absolute():
        registry_path = (REPO_ROOT / registry_path).resolve()

    manifest_path = Path(args.hash_manifest)
    if not manifest_path.is_absolute():
        manifest_path = (REPO_ROOT / manifest_path).resolve()

    body_template = None
    if args.body_template:
        body_template = Path(args.body_template)
        if not body_template.is_absolute():
            body_template = (REPO_ROOT / body_template).resolve()
        if not body_template.exists():
            parser.error(f"Template introuvable: {body_template}")

    tags = parse_tags(args.tags)
    links = parse_links(args.links, args.links_key, args.links_delimiter)

    extra = {}
    for item in args.extra_frontmatter:
        if "=" not in item:
            parser.error(f"Format invalide pour --extra-frontmatter: {item}")
        key, value = item.split("=", 1)
        extra[key.strip()] = value.strip()

    resolved_date = args.date or datetime.utcnow().date().isoformat()
    commit_message = args.commit_message or f"docs({args.id}): update via new_doc_routine"

    return RoutineConfig(
        path=target_path,
        id=args.id,
        id_root=args.id_root or args.id,
        doc_type=args.doc_type,
        status=args.status,
        date=resolved_date,
        version=args.version,
        author=args.author,
        tags=tags,
        links=links,
        body_template=body_template,
        overwrite_body=args.overwrite_body,
        registry_path=registry_path,
        doc_title=args.doc_title,
        lineage_title=args.lineage_title,
        scope=args.scope,
        pattern=args.pattern,
        commit_message=commit_message,
        skip_validations=args.skip_validations,
        skip_commit=args.skip_commit,
        extra_frontmatter=extra,
        links_delimiter=args.links_delimiter,
        previous_hash=args.previous_hash,
        hash_manifest_path=manifest_path,
    )


def parse_tags(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def parse_links(raw: Optional[str], default_key: str, delimiter: str) -> OrderedDict[str, List[str]]:
    result: OrderedDict[str, List[str]] = OrderedDict()
    if not raw:
        return result
    chunks = [chunk.strip() for chunk in raw.split(delimiter) if chunk.strip()]
    for chunk in chunks:
        if ":" in chunk:
            key, values = chunk.split(":", 1)
        else:
            key, values = default_key, chunk
        key = key.strip()
        items = [value.strip() for value in values.split(",") if value.strip()]
        if not items:
            continue
        result[key] = items
    return result


def read_file_sections(path: Path) -> Tuple[Optional[str], str]:
    if not path.exists():
        return None, ""
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None, content
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            front = "".join(lines[1:idx])
            body = "".join(lines[idx + 1 :])
            return front, body
    return None, content


def load_frontmatter_dict(fragment: Optional[str]) -> Dict[str, object]:
    if not fragment:
        return {}
    data = yaml.safe_load(fragment) or {}
    if not isinstance(data, dict):
        raise ValueError("Front matter existant invalide (attendu: mapping YAML).")
    return dict(data)


def make_flow_sequence(values: List[str]) -> CommentedSeq:
    seq = CommentedSeq([DQ(str(v)) for v in values])
    seq.fa.set_flow_style()
    return seq


def render_frontmatter(metadata: Dict[str, object], self_hash: Optional[str]) -> str:
    fm = CommentedMap()
    processed: set[str] = set()
    yaml_emitter = YAML()
    yaml_emitter.preserve_quotes = True
    yaml_emitter.width = 120
    yaml_emitter.indent(sequence=4, offset=2)

    for key in FRONTMATTER_FIELDS_ORDER:
        if key not in metadata:
            continue
        value = metadata[key]
        if key == "tags":
            seq = make_flow_sequence(list(value or []))
            fm[key] = seq
        elif key == "links":
            links_map = CommentedMap()
            if isinstance(value, dict):
                for link_key, items in value.items():
                    links_map[link_key] = make_flow_sequence(list(items))
            else:
                links_map.fa.set_flow_style()
            if not links_map:
                links_map.fa.set_flow_style()
            fm[key] = links_map
        else:
            fm[key] = DQ(str(value))
        processed.add(key)

    for key, value in metadata.items():
        if key in processed or key == "self_hash":
            continue
        if isinstance(value, list):
            fm[key] = make_flow_sequence([str(v) for v in value])
        elif isinstance(value, dict):
            nested = CommentedMap()
            for sub_key, sub_value in value.items():
                nested[sub_key] = DQ(str(sub_value))
            fm[key] = nested
        else:
            fm[key] = DQ(str(value))
        processed.add(key)

    if self_hash:
        fm["self_hash"] = str(self_hash)

    buffer = io.StringIO()
    yaml_emitter.dump(fm, buffer)
    payload = buffer.getvalue().strip()
    return f"---\n{payload}\n---\n"


def ensure_metadata(config: RoutineConfig, existing: Dict[str, object]) -> Dict[str, object]:
    meta = dict(existing)
    meta["id"] = config.id
    meta["type"] = config.doc_type
    meta["status"] = config.status
    meta["date"] = config.date
    meta["author"] = config.author
    meta["version"] = config.version
    if config.doc_title:
        meta["title"] = config.doc_title
    if config.tags:
        meta["tags"] = config.tags
    else:
        meta.setdefault("tags", [])
    if config.links:
        meta["links"] = config.links
    else:
        meta.setdefault("links", OrderedDict())
    for key, value in config.extra_frontmatter.items():
        meta[key] = value
    meta.pop("self_hash", None)
    return meta


def infer_title_from_body(body: str) -> Optional[str]:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            stripped = stripped.lstrip("#").strip()
            if stripped:
                return stripped
    return None


def compute_file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return f"sha256:{h.hexdigest()}"


def update_hash_manifest(manifest_path: Path, target_rel_path: str, new_hash: str) -> bool:
    if not manifest_path.exists():
        print(f"⚠️  Manifeste introuvable, skip: {manifest_path}")
        return False

    yaml_handler = YAML()
    yaml_handler.preserve_quotes = True
    try:
        with manifest_path.open("r", encoding="utf-8") as stream:
            data = yaml_handler.load(stream)
    except Exception as exc:
        print(f"⚠️  Lecture manifeste impossible ({manifest_path}): {exc}")
        return False

    updated = False

    def _walk(node: object) -> None:
        nonlocal updated
        if isinstance(node, dict):
            file_value = node.get("file")
            if isinstance(file_value, str):
                normalized = file_value.replace("\\", "/")
                if normalized == target_rel_path:
                    node["hash"] = DQ(new_hash)
                    updated = True
            for value in node.values():
                _walk(value)
        elif isinstance(node, list):
            for item in node:
                _walk(item)

    _walk(data)

    if not updated:
        rel_manifest = manifest_path.relative_to(REPO_ROOT)
        print(f"⚠️  Aucune entrée contenant '{target_rel_path}' dans {rel_manifest}")
        return False

    with manifest_path.open("w", encoding="utf-8") as stream:
        yaml_handler.dump(data, stream)
    print(f"✅ Manifeste mis à jour: {manifest_path.relative_to(REPO_ROOT)}")
    return True


def update_registry_entry(
    config: RoutineConfig,
    doc_rel_path: Path,
    doc_hash: str,
    self_hash: str,
    tags: List[str],
    lineage_title: Optional[str],
) -> None:
    yaml_loader = YAML()
    yaml_loader.preserve_quotes = True
    yaml_loader.width = 160
    registry_path = config.registry_path

    if registry_path.exists():
        with registry_path.open("r", encoding="utf-8") as stream:
            registry_data = yaml_loader.load(stream) or CommentedMap()
    else:
        registry_data = CommentedMap()

    if not isinstance(registry_data, CommentedMap):
        raise ValueError("Le registre v1.1 n'est pas un mapping YAML valide.")

    lineages = registry_data.get("lineages")
    if lineages is None:
        lineages = CommentedSeq()
        registry_data["lineages"] = lineages

    lineage_node = None
    for entry in lineages:
        if isinstance(entry, dict) and str(entry.get("id_root")) == config.id_root:
            lineage_node = entry
            break

    if lineage_node is None:
        lineage_node = CommentedMap()
        lineage_node["id_root"] = config.id_root
        lineages.append(lineage_node)

    if lineage_title:
        lineage_node["title"] = DQ(lineage_title)
    if config.scope:
        lineage_node["scope"] = DQ(config.scope)
    if config.pattern:
        lineage_node["pattern"] = DQ(config.pattern)

    versions = lineage_node.get("versions")
    if versions is None:
        versions = CommentedSeq()
        lineage_node["versions"] = versions

    version_node = None
    for candidate in versions:
        if isinstance(candidate, dict) and str(candidate.get("id")) == config.id:
            version_node = candidate
            break

    if version_node is None:
        version_node = CommentedMap()
        versions.append(version_node)

    version_node["id"] = DQ(config.id)
    version_node["type"] = DQ(config.doc_type)
    version_node["status"] = DQ(config.status)
    version_node["version"] = DQ(config.version)
    version_node["date"] = DQ(config.date)
    version_node["file_path"] = DQ(str(doc_rel_path).replace("\\", "/"))
    if tags:
        version_node["tags"] = make_flow_sequence(tags)
    else:
        version_node["tags"] = make_flow_sequence([])
    version_node["hash"] = doc_hash
    version_node["self_hash"] = self_hash
    version_node["author"] = DQ(config.author)
    if config.previous_hash:
        version_node["previous_hash"] = config.previous_hash

    with registry_path.open("w", encoding="utf-8") as stream:
        yaml_loader.dump(registry_data, stream)


def run_command(command: List[str], cwd: Path, description: str) -> None:
    print(f"→ {description}: {' '.join(command)}")
    result = subprocess.run(command, cwd=str(cwd))
    if result.returncode != 0:
        raise RuntimeError(f"Échec de la commande ({description}). Code: {result.returncode}")


def git_add_and_commit(paths: List[Path], message: str) -> None:
    tracked = [str(path) for path in paths]
    if not tracked:
        return
    run_command(["git", "add", *tracked], REPO_ROOT, "Mise en staging")
    diff_check = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=str(REPO_ROOT))
    if diff_check.returncode == 0:
        print("⚠️  Aucun changement à committer (les fichiers étaient déjà à jour).")
        subprocess.run(["git", "reset"], cwd=str(REPO_ROOT))
        return
    run_command(["git", "commit", "-m", message], REPO_ROOT, "Commit automatique")


def main() -> None:
    config = parse_args()
    config.path.parent.mkdir(parents=True, exist_ok=True)

    frontmatter_raw, existing_body = read_file_sections(config.path)
    metadata = ensure_metadata(config, load_frontmatter_dict(frontmatter_raw))

    if not existing_body.strip() or config.overwrite_body:
        if config.body_template:
            body_content = config.body_template.read_text(encoding="utf-8")
        else:
            body_content = f"# {config.id}\n\n*(Documentation à compléter.)*\n"
    else:
        body_content = existing_body

    metadata["tags"] = config.tags or metadata.get("tags", [])
    if not isinstance(metadata["tags"], list):
        metadata["tags"] = parse_tags(str(metadata["tags"]))

    if config.links:
        links_payload: OrderedDict[str, List[str]] = config.links
    else:
        existing_links = metadata.get("links", OrderedDict())
        if isinstance(existing_links, dict):
            links_payload = OrderedDict()
            for key, value in existing_links.items():
                if isinstance(value, str):
                    links_payload[key] = [value]
                elif isinstance(value, list):
                    links_payload[key] = [str(v) for v in value if str(v).strip()]
        else:
            links_payload = OrderedDict()
    metadata["links"] = links_payload

    metadata.update(config.extra_frontmatter)

    fm_without_hash = render_frontmatter(metadata, self_hash=None)
    needs_newline = body_content.startswith("\n")
    combined_preview = fm_without_hash + ("" if needs_newline else "\n") + body_content
    if not combined_preview.endswith("\n"):
        combined_preview += "\n"

    self_hash_value = compute_self_hash_from_text(combined_preview)
    final_frontmatter = render_frontmatter(metadata, self_hash=self_hash_value)
    final_content = final_frontmatter + ("" if body_content.startswith("\n") else "\n") + body_content
    if not final_content.endswith("\n"):
        final_content += "\n"

    config.path.write_text(final_content, encoding="utf-8")
    print(f"✅ Document mis à jour: {config.path.relative_to(REPO_ROOT)}")

    try:
        doc_rel_path = config.path.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise ValueError("Le fichier ciblé doit appartenir au dépôt Git.") from exc

    file_hash = compute_file_hash(config.path)

    lineage_title = (
        config.lineage_title
        or config.doc_title
        or metadata.get("title")
        or infer_title_from_body(body_content)
    )

    update_registry_entry(
        config=config,
        doc_rel_path=doc_rel_path,
        doc_hash=file_hash,
        self_hash=self_hash_value,
        tags=list(metadata.get("tags", [])),
        lineage_title=lineage_title if isinstance(lineage_title, str) else None,
    )
    print(f"✅ Registre mis à jour: {config.registry_path.relative_to(REPO_ROOT)}")

    registry_rel = str(config.registry_path.relative_to(REPO_ROOT)).replace("\\", "/")
    registry_hash = compute_file_hash(config.registry_path)
    manifest_touched = update_hash_manifest(
        manifest_path=config.hash_manifest_path,
        target_rel_path=registry_rel,
        new_hash=registry_hash,
    )

    if not config.skip_validations:
        run_command(["python", "scripts/validate_frontmatter.py"], REPO_ROOT, "Validation front matter")
        run_command(["make", "docs-check"], REPO_ROOT, "Cible docs-check")

    if not config.skip_commit:
        tracked_paths = [config.path, config.registry_path]
        if manifest_touched:
            tracked_paths.append(config.hash_manifest_path)
        git_add_and_commit(tracked_paths, config.commit_message)
    else:
        print("ℹ️  Commit automatique désactivé (--skip-commit).")

    print("🎯 Routine terminée sans divergence.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover - point d'entrée CLI
        print(f"❌ Routine interrompue: {exc}", file=sys.stderr)
        sys.exit(1)
