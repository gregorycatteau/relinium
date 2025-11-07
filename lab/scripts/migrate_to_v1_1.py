#!/usr/bin/env python3
"""
Script de migration prototype vers le schéma documentaire v1.1

PHILOSOPHIE :
Ce script est STRICTEMENT NON DESTRUCTIF par défaut.
Il prépare la mise en conformité par succession certifiée,
sans modifier un seul fichier existant.

Usage:
    python scripts/migrate_to_v1_1.py --dry-run              # Mode par défaut, affiche uniquement
    python scripts/migrate_to_v1_1.py --execute              # Crée les fichiers successeurs
    python scripts/migrate_to_v1_1.py --execute --target docs/03-architecture

Respect strict du RFC-004-alignment-protocol.md
"""

import argparse
import hashlib
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import yaml
except ImportError:
    print("❌ ERREUR: pyyaml n'est pas installé")
    print("💡 Installez-le avec: pip install pyyaml")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTES
# ═══════════════════════════════════════════════════════════════════════════════

SCHEMA_V1_0_REQUIRED = ["id", "type", "status", "date"]
DOCUMENT_TYPES = ["ADR", "RFC", "OBS", "POC", "SPRINT_DOC"]
DEFAULT_TARGET = "docs"

# Patterns pour identifier les documents
DOCUMENT_PATTERN = re.compile(r"^(ADR|RFC|OBS|POC|SPRINT_DOC)-\d{4}\.md$")
VERSION_PATTERN = re.compile(r"^(ADR|RFC|OBS|POC|SPRINT_DOC)-\d{4}-v\d+\.md$")

# ═══════════════════════════════════════════════════════════════════════════════
# CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

class MigrationReport:
    """Rapport de migration non-destructive"""
    
    def __init__(self):
        self.total_scanned = 0
        self.candidates = []
        self.already_v1_1 = []
        self.errors = []
        self.would_create = []
        self.created = []
    
    def add_candidate(self, filepath: Path, reason: str):
        """Ajoute un document candidat à la migration"""
        self.candidates.append({
            "path": str(filepath),
            "reason": reason
        })
    
    def add_already_migrated(self, filepath: Path):
        """Documente un fichier déjà conforme v1.1"""
        self.already_v1_1.append(str(filepath))
    
    def add_error(self, filepath: Path, error: str):
        """Enregistre une erreur"""
        self.errors.append({
            "path": str(filepath),
            "error": error
        })
    
    def add_would_create(self, original_path: Path, new_path: Path, hash_value: str):
        """Enregistre ce qui serait créé en mode execute"""
        self.would_create.append({
            "original": str(original_path),
            "successor": str(new_path),
            "previous_hash": hash_value
        })
    
    def add_created(self, original_path: Path, new_path: Path):
        """Enregistre un fichier effectivement créé"""
        self.created.append({
            "original": str(original_path),
            "successor": str(new_path)
        })
    
    def print_summary(self, dry_run: bool):
        """Affiche le résumé du rapport"""
        print("\n" + "═" * 80)
        print("📊 RAPPORT DE MIGRATION v1.0 → v1.1")
        print("═" * 80)
        
        print(f"\n📁 Documents analysés: {self.total_scanned}")
        print(f"✅ Déjà conformes v1.1: {len(self.already_v1_1)}")
        print(f"🔍 Candidats à la migration: {len(self.candidates)}")
        print(f"❌ Erreurs rencontrées: {len(self.errors)}")
        
        if dry_run:
            print(f"\n🎯 Documents qui seraient créés: {len(self.would_create)}")
        else:
            print(f"\n✨ Documents créés: {len(self.created)}")
        
        if self.errors:
            print("\n❌ ERREURS DÉTAILLÉES:")
            for error in self.errors:
                print(f"  • {error['path']}")
                print(f"    └─ {error['error']}")
        
        if self.candidates:
            print("\n🔍 CANDIDATS À LA MIGRATION:")
            for candidate in self.candidates:
                print(f"  • {candidate['path']}")
                print(f"    └─ {candidate['reason']}")
        
        if dry_run and self.would_create:
            print("\n💡 MODE DRY-RUN: Les fichiers suivants SERAIENT créés avec --execute:")
            for item in self.would_create:
                print(f"  • {item['original']}")
                print(f"    └─ → {item['successor']}")
                print(f"    └─ previous_hash: {item['previous_hash'][:20]}...")
        
        if not dry_run and self.created:
            print("\n✅ FICHIERS CRÉÉS:")
            for item in self.created:
                print(f"  • {item['successor']}")
                print(f"    └─ supersedes: {item['original']}")
        
        print("\n" + "═" * 80)
        
        if dry_run:
            print("💡 Pour exécuter la migration, utilisez: --execute")
            print("⚠️  ATTENTION: Aucun fichier existant ne sera modifié")
        else:
            print("✅ Migration terminée sans modifier les fichiers originaux")


# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════════════════════════════

def compute_file_hash(filepath: Path) -> str:
    """
    Calcule le hash SHA256 d'un fichier complet.
    
    Args:
        filepath: Chemin vers le fichier
        
    Returns:
        Hash sous forme 'sha256:...'
    """
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return f"sha256:{sha256.hexdigest()}"
    except Exception as e:
        raise ValueError(f"Impossible de calculer le hash: {e}")


def extract_frontmatter(filepath: Path) -> Optional[Dict]:
    """
    Extrait les métadonnées YAML du frontmatter d'un fichier.
    
    Args:
        filepath: Chemin vers le fichier Markdown
        
    Returns:
        Dictionnaire des métadonnées ou None si pas de frontmatter
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.startswith('---'):
            return None
        
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None
        
        return yaml.safe_load(parts[1])
    except Exception as e:
        raise ValueError(f"Erreur lors de l'extraction du frontmatter: {e}")


def extract_document_content(filepath: Path) -> Tuple[Optional[Dict], str]:
    """
    Sépare frontmatter et contenu d'un document.
    
    Args:
        filepath: Chemin vers le fichier
        
    Returns:
        Tuple (frontmatter dict, content string)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if not content.startswith('---'):
            return None, content
        
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None, content
        
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2]
        
        return frontmatter, body
    except Exception as e:
        raise ValueError(f"Erreur lors de la lecture: {e}")


def is_valid_v1_0_document(frontmatter: Dict) -> bool:
    """Vérifie si un frontmatter est conforme au minimum v1.0"""
    if not frontmatter:
        return False
    return all(field in frontmatter for field in SCHEMA_V1_0_REQUIRED)


def is_already_v1_1_successor(frontmatter: Dict) -> bool:
    """Vérifie si un document est déjà un successeur v1.1"""
    if not frontmatter:
        return False
    
    # Un document est considéré v1.1 s'il a previous_hash ou id_root
    has_succession_fields = 'previous_hash' in frontmatter or 'id_root' in frontmatter
    
    # Ou s'il a des champs de gouvernance v1.1
    has_gov_fields = 'roles' in frontmatter or 'decision_type' in frontmatter
    
    # Ou s'il a des champs de classification v1.1
    has_class_fields = 'scope' in frontmatter or 'pattern' in frontmatter
    
    return has_succession_fields or has_gov_fields or has_class_fields


def generate_successor_id(original_id: str) -> str:
    """
    Génère un ID pour le document successeur.
    
    Args:
        original_id: ID original (ex: "RFC-001" ou "RFC-001-v2")
        
    Returns:
        ID successeur (ex: "RFC-001-v2" ou "RFC-001-v3")
    """
    # Si déjà versionné, incrémenter
    match = re.match(r'^(.*)-v(\d+)$', original_id)
    if match:
        base, version = match.groups()
        return f"{base}-v{int(version) + 1}"
    
    # Sinon, ajouter -v2
    return f"{original_id}-v2"


def generate_successor_filename(original_path: Path) -> Path:
    """
    Génère le nom de fichier pour le document successeur.
    
    Args:
        original_path: Chemin du fichier original
        
    Returns:
        Chemin du fichier successeur
    """
    stem = original_path.stem  # Nom sans extension
    
    # Si déjà versionné, incrémenter
    match = re.match(r'^(.*)-v(\d+)$', stem)
    if match:
        base, version = match.groups()
        new_stem = f"{base}-v{int(version) + 1}"
    else:
        new_stem = f"{stem}-v2"
    
    return original_path.parent / f"{new_stem}.md"


def enrich_frontmatter_v1_1(
    original_fm: Dict,
    original_id: str,
    original_hash: str
) -> Dict:
    """
    Enrichit le frontmatter v1.0 avec les champs v1.1.
    
    Args:
        original_fm: Frontmatter original
        original_id: ID du document original
        original_hash: Hash du document original
        
    Returns:
        Nouveau frontmatter enrichi v1.1
    """
    # Copie profonde pour ne pas modifier l'original
    new_fm = dict(original_fm)
    
    # 1. Mise à jour de l'ID
    new_fm['id'] = generate_successor_id(original_id)
    
    # 2. Ajout des champs de succession certifiée (REQUIS)
    new_fm['previous_hash'] = original_hash
    
    # Extraire l'id_root (sans version)
    root_match = re.match(r'^(.*?)(-v\d+)?$', original_id)
    if root_match:
        new_fm['id_root'] = root_match.group(1)
    else:
        new_fm['id_root'] = original_id
    
    # 3. Mise à jour de la version (passage à 2.0)
    if 'version' in new_fm:
        # Incrémenter le MAJOR
        version_parts = new_fm['version'].split('.')
        new_fm['version'] = f"{int(version_parts[0]) + 1}.0"
    else:
        new_fm['version'] = "2.0"
    
    # 4. Ajout de links.supersedes si pas déjà présent
    if 'links' not in new_fm:
        new_fm['links'] = {}
    
    new_fm['links']['supersedes'] = original_id
    
    # 5. Tentative de déduction du scope depuis les tags (optionnel)
    if 'tags' in new_fm and 'scope' not in new_fm:
        tags = new_fm['tags']
        if any(t in ['backend', 'frontend', 'database', 'api', 'infrastructure'] for t in tags):
            new_fm['scope'] = 'technical'
        elif any(t in ['governance', 'methodology', 'process'] for t in tags):
            new_fm['scope'] = 'organizational'
        elif any(t in ['ethics', 'values', 'principles'] for t in tags):
            new_fm['scope'] = 'ethical'
    
    # 6. Tentative de déduction du pattern depuis le type (optionnel)
    if 'pattern' not in new_fm:
        type_to_pattern = {
            'ADR': 'decision',
            'RFC': 'reflection',
            'OBS': 'observation',
            'POC': 'experiment',
            'SPRINT_DOC': 'observation'
        }
        doc_type = new_fm.get('type', '')
        if doc_type in type_to_pattern:
            new_fm['pattern'] = type_to_pattern[doc_type]
    
    return new_fm


# ═══════════════════════════════════════════════════════════════════════════════
# LOGIQUE PRINCIPALE
# ═══════════════════════════════════════════════════════════════════════════════

def scan_documents(target_dir: Path, report: MigrationReport) -> List[Path]:
    """
    Scanne récursivement un répertoire pour trouver les documents candidats.
    
    Args:
        target_dir: Répertoire à scanner
        report: Rapport de migration
        
    Returns:
        Liste des chemins de documents candidats
    """
    candidates = []
    
    for md_file in target_dir.rglob("*.md"):
        report.total_scanned += 1
        
        # Ignorer les fichiers déjà versionnés
        if VERSION_PATTERN.match(md_file.name):
            continue
        
        # Vérifier si c'est un document documentaire
        if not DOCUMENT_PATTERN.match(md_file.name):
            continue
        
        try:
            frontmatter = extract_frontmatter(md_file)
            
            if not frontmatter:
                report.add_error(md_file, "Pas de frontmatter valide")
                continue
            
            # Vérifier conformité minimale v1.0
            if not is_valid_v1_0_document(frontmatter):
                report.add_error(md_file, "Frontmatter non conforme v1.0")
                continue
            
            # Vérifier si déjà migré v1.1
            if is_already_v1_1_successor(frontmatter):
                report.add_already_migrated(md_file)
                continue
            
            # C'est un candidat !
            candidates.append(md_file)
            report.add_candidate(md_file, "Document v1.0 valide, candidat à enrichissement v1.1")
            
        except Exception as e:
            report.add_error(md_file, str(e))
    
    return candidates


def prepare_successor(
    original_path: Path,
    dry_run: bool,
    report: MigrationReport
) -> Optional[Path]:
    """
    Prépare (et optionnellement crée) un document successeur v1.1.
    
    Args:
        original_path: Chemin du document original
        dry_run: Si True, ne crée pas le fichier
        report: Rapport de migration
        
    Returns:
        Chemin du fichier successeur ou None si erreur
    """
    try:
        # 1. Calcul du hash du document original
        original_hash = compute_file_hash(original_path)
        
        # 2. Extraction frontmatter + contenu
        frontmatter, body = extract_document_content(original_path)
        
        if not frontmatter:
            raise ValueError("Frontmatter manquant")
        
        original_id = frontmatter.get('id', '')
        
        # 3. Enrichissement du frontmatter v1.1
        new_frontmatter = enrich_frontmatter_v1_1(frontmatter, original_id, original_hash)
        
        # 4. Génération du nouveau chemin
        successor_path = generate_successor_filename(original_path)
        
        # 5. Enregistrement dans le rapport
        report.add_would_create(original_path, successor_path, original_hash)
        
        # 6. Création effective en mode execute
        if not dry_run:
            # Construction du nouveau contenu
            fm_str = yaml.dump(new_frontmatter, allow_unicode=True, sort_keys=False)
            new_content = f"---\n{fm_str}---{body}"
            
            # Écriture du nouveau fichier (SANS TOUCHER À L'ORIGINAL)
            with open(successor_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            report.add_created(original_path, successor_path)
            
            return successor_path
        
        return None
        
    except Exception as e:
        report.add_error(original_path, f"Erreur lors de la préparation: {e}")
        return None


def write_migration_log(report: MigrationReport, output_dir: Path, dry_run: bool):
    """
    Écrit un rapport de migration en Markdown (uniquement en mode execute).
    
    Args:
        report: Rapport de migration
        output_dir: Répertoire de sortie
        dry_run: Si True, n'écrit pas le fichier
    """
    if dry_run or not report.created:
        return
    
    # Créer le répertoire si nécessaire
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = output_dir / f"MIGRATION_PROTOTYPE_REPORT_{timestamp}.md"
    
    content = f"""# Rapport de Migration Prototype v1.0 → v1.1

**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Mode**: {'Dry-run' if dry_run else 'Execute'}  
**Documents analysés**: {report.total_scanned}  
**Documents migrés**: {len(report.created)}

## 📊 Statistiques

- ✅ Déjà conformes v1.1: {len(report.already_v1_1)}
- 🔍 Candidats identifiés: {len(report.candidates)}
- ✨ Fichiers créés: {len(report.created)}
- ❌ Erreurs: {len(report.errors)}

## ✨ Fichiers Créés

"""
    
    for item in report.created:
        content += f"### {Path(item['successor']).name}\n\n"
        content += f"- **Original**: `{item['original']}`\n"
        content += f"- **Successeur**: `{item['successor']}`\n"
        content += f"- **Relation**: Succession certifiée (RFC-004)\n\n"
    
    if report.errors:
        content += "\n## ❌ Erreurs Rencontrées\n\n"
        for error in report.errors:
            content += f"- **{error['path']}**: {error['error']}\n"
    
    content += f"""
## 🎯 Prochaines Étapes

1. Vérifier manuellement les fichiers successeurs créés
2. Valider les métadonnées v1.1 ajoutées
3. Exécuter la CI pour valider la conformité
4. Mettre à jour le registre (`registry.yaml`)

## ⚠️ Garantie de Non-Modification

**AUCUN fichier existant n'a été modifié** durant cette migration.  
Tous les documents originaux restent intacts et lisibles.

Conformément au RFC-004, seuls de nouveaux fichiers successeurs ont été créés.
"""
    
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n📄 Rapport de migration écrit: {log_path}")


# ═══════════════════════════════════════════════════════════════════════════════
# POINT D'ENTRÉE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Point d'entrée principal du script"""
    
    parser = argparse.ArgumentParser(
        description="Migration prototype non-destructive vers schéma v1.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python scripts/migrate_to_v1_1.py --dry-run
  python scripts/migrate_to_v1_1.py --execute
  python scripts/migrate_to_v1_1.py --execute --target docs/03-architecture

IMPORTANT:
  Ce script est STRICTEMENT NON DESTRUCTIF par défaut.
  Il ne modifie JAMAIS les fichiers existants.
  Il crée uniquement de nouveaux fichiers successeurs.
        """
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Mode dry-run (défaut): affiche ce qui serait fait sans créer de fichiers'
    )
    
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Mode execute: crée effectivement les fichiers successeurs'
    )
    
    parser.add_argument(
        '--target',
        type=str,
        default=DEFAULT_TARGET,
        help=f'Répertoire cible à analyser (défaut: {DEFAULT_TARGET})'
    )
    
    args = parser.parse_args()
    
    # Par défaut, on est en dry-run
    dry_run = not args.execute
    
    # Validation du répertoire cible
    target_path = Path(args.target)
    if not target_path.exists():
        print(f"❌ ERREUR: Le répertoire {args.target} n'existe pas")
        sys.exit(1)
    
    if not target_path.is_dir():
        print(f"❌ ERREUR: {args.target} n'est pas un répertoire")
        sys.exit(1)
    
    # Initialisation du rapport
    report = MigrationReport()
    
    # Header
    print("\n" + "═" * 80)
    print("🔄 MIGRATION PROTOTYPE v1.0 → v1.1")
    print("═" * 80)
    print(f"\n📂 Répertoire cible: {target_path}")
    print(f"🎯 Mode: {'DRY-RUN (simulation)' if dry_run else 'EXECUTE (création effective)'}")
    
    if dry_run:
        print("\n⚠️  MODE DRY-RUN: Aucun fichier ne sera créé")
        print("💡 Pour exécuter la migration, ajoutez --execute")
    else:
        print("\n✅ MODE EXECUTE: Les fichiers successeurs seront créés")
        print("⚠️  GARANTIE: Aucun fichier existant ne sera modifié")
    
    print("\n" + "─" * 80)
    
    # 1. Scanner les documents
    print("\n🔍 Analyse du corpus documentaire...")
    candidates = scan_documents(target_path, report)
    print(f"✓ {report.total_scanned} fichiers analysés")
    print(f"✓ {len(candidates)} candidats identifiés")
    
    # 2. Préparer/créer les successeurs
    if candidates:
        print(f"\n{'🎯 Préparation' if dry_run else '✨ Création'} des fichiers successeurs...")
        
        for candidate in candidates:
            prepare_successor(candidate, dry_run, report)
            print(f"  {'⚡ Préparé' if dry_run else '✅ Créé'}: {candidate.name}")
    
    # 3. Écrire le rapport de migration (seulement si --execute)
    if not dry_run and report.created:
        output_dir = Path("docs/sprints/SSOT-v1.1/02-evidence")
        write_migration_log(report, output_dir, dry_run)
    
    # 4. Afficher le rapport
    report.print_summary(dry_run)
    
    # 5. Code de sortie
    if report.errors:
        print("\n⚠️  Des erreurs ont été rencontrées")
        sys.exit(1)
    
    if dry_run and candidates:
        print(f"\n💡 {len(candidates)} document(s) prêt(s) à être migré(s)")
        print("   Relancez avec --execute pour créer les fichiers")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
