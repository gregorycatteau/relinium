#!/usr/bin/env python3
"""
Script de validation automatique des métadonnées frontmatter.
Vérifie la conformité de tous les documents Markdown avec le schéma JSON canonique.

Usage:
    python3 scripts/validate_frontmatter.py

Exit codes:
    0 - Tous les documents sont valides
    1 - Au moins un document invalide ou erreur d'exécution
"""

import json
import sys
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import yaml

try:
    from jsonschema import validate, ValidationError, Draft7Validator
except ImportError:
    print("❌ Erreur: Le module 'jsonschema' est requis.")
    print("   Installation: pip install jsonschema")
    sys.exit(1)


class FrontmatterValidator:
    """Validateur de frontmatter pour documents Relinium."""
    
    def __init__(self, schema_path: str, docs_root: str = "docs"):
        self.schema_path = Path(schema_path)
        self.docs_root = Path(docs_root)
        self.schema = self._load_schema()
        self.validator = Draft7Validator(self.schema)
        self.results = []
        
    def _load_schema(self) -> dict:
        """Charge le schéma JSON canonique."""
        if not self.schema_path.exists():
            raise FileNotFoundError(f"Schéma introuvable: {self.schema_path}")
        
        with open(self.schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _extract_frontmatter(self, content: str) -> Optional[Dict]:
        """Extrait le frontmatter YAML d'un document Markdown."""
        # Recherche du bloc YAML frontmatter entre --- ... ---
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(pattern, content, re.DOTALL)
        
        if not match:
            return None
        
        frontmatter_text = match.group(1)
        try:
            return yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as e:
            raise ValueError(f"YAML invalide: {e}")
    
    def _find_markdown_files(self) -> List[Path]:
        """Trouve tous les fichiers Markdown dans docs/."""
        md_files = []
        for path in self.docs_root.rglob("*.md"):
            # Exclure certains répertoires/fichiers si nécessaire
            if any(part.startswith('.') for part in path.parts):
                continue
            md_files.append(path)
        return sorted(md_files)
    
    def validate_file(self, file_path: Path) -> Tuple[bool, Optional[str]]:
        """
        Valide un fichier Markdown.
        
        Returns:
            (is_valid, error_message)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extraction du frontmatter
            frontmatter = self._extract_frontmatter(content)
            
            if frontmatter is None:
                return False, "Pas de frontmatter YAML trouvé"
            
            # Validation contre le schéma
            errors = list(self.validator.iter_errors(frontmatter))
            
            if errors:
                error_msgs = []
                for error in errors[:3]:  # Limiter à 3 erreurs par fichier
                    path = ".".join(str(p) for p in error.path) if error.path else "root"
                    error_msgs.append(f"  • {path}: {error.message}")
                return False, "\n".join(error_msgs)
            
            return True, None
            
        except Exception as e:
            return False, f"Erreur: {str(e)}"
    
    def validate_all(self) -> Dict:
        """
        Valide tous les fichiers Markdown.
        
        Returns:
            Dictionnaire avec les statistiques de validation
        """
        print(f"🔍 Validation des frontmatter dans {self.docs_root}/")
        print(f"📋 Schéma: {self.schema_path}")
        print(f"📅 Date: {datetime.now().isoformat()}\n")
        
        files = self._find_markdown_files()
        
        if not files:
            print("⚠️  Aucun fichier Markdown trouvé.\n")
            return {
                'total': 0,
                'valid': 0,
                'invalid': 0,
                'files': []
            }
        
        print(f"📂 {len(files)} fichiers à analyser\n")
        print("=" * 80)
        
        for file_path in files:
            is_valid, error_msg = self.validate_file(file_path)
            # Utiliser le chemin absolu puis le rendre relatif proprement
            try:
                relative_path = file_path.relative_to(Path.cwd())
            except ValueError:
                # Si relative_to échoue, utiliser le chemin absolu résolu
                relative_path = file_path.resolve().relative_to(Path.cwd().resolve())
            
            result = {
                'path': str(relative_path),
                'valid': is_valid,
                'error': error_msg
            }
            self.results.append(result)
            
            # Affichage du résultat
            status = "✅ VALIDE" if is_valid else "❌ INVALIDE"
            print(f"{status:12} {relative_path}")
            if error_msg:
                print(f"             {error_msg}\n")
        
        print("=" * 80)
        
        # Statistiques
        valid_count = sum(1 for r in self.results if r['valid'])
        invalid_count = len(self.results) - valid_count
        
        stats = {
            'total': len(self.results),
            'valid': valid_count,
            'invalid': invalid_count,
            'files': self.results
        }
        
        print(f"\n📊 RÉSUMÉ:")
        print(f"   Total    : {stats['total']} fichiers")
        print(f"   Valides  : {stats['valid']} ✅")
        print(f"   Invalides: {stats['invalid']} ❌")
        
        if invalid_count == 0:
            print(f"\n🎉 SUCCÈS: Tous les documents sont conformes au schéma v1.0!\n")
        else:
            print(f"\n⚠️  ÉCHEC: {invalid_count} document(s) non conforme(s).\n")
        
        return stats
    
    def generate_log(self, output_path: str):
        """Génère un fichier log de validation."""
        log_path = Path(output_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("VALIDATION LOG - FRONTMATTER RELINIUM\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Date d'exécution: {datetime.now().isoformat()}\n")
            f.write(f"Schéma utilisé  : {self.schema_path}\n")
            f.write(f"Répertoire scanné: {self.docs_root}\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("RÉSULTATS PAR FICHIER\n")
            f.write("-" * 80 + "\n\n")
            
            for result in self.results:
                status = "VALIDE" if result['valid'] else "INVALIDE"
                f.write(f"[{status}] {result['path']}\n")
                if result['error']:
                    f.write(f"  Erreur: {result['error']}\n")
                f.write("\n")
            
            f.write("-" * 80 + "\n")
            f.write("STATISTIQUES\n")
            f.write("-" * 80 + "\n")
            valid_count = sum(1 for r in self.results if r['valid'])
            f.write(f"Total de fichiers analysés: {len(self.results)}\n")
            f.write(f"Fichiers valides         : {valid_count}\n")
            f.write(f"Fichiers invalides       : {len(self.results) - valid_count}\n")
            f.write(f"Taux de conformité       : {valid_count/len(self.results)*100:.1f}%\n")
        
        print(f"📝 Log enregistré: {log_path}\n")


def main():
    """Point d'entrée principal du script."""
    # Chemins relatifs au répertoire racine du projet
    schema_path = "docs/01-genesis/document_schema_v1.1.json"
    docs_root = "docs"
    log_output = "docs/sprints/SSOT-v1.0/02-evidence/S3_VALIDATION_LOG.txt"
    
    try:
        # Création du validateur
        validator = FrontmatterValidator(schema_path, docs_root)
        
        # Validation de tous les fichiers
        start_time = datetime.now()
        stats = validator.validate_all()
        duration = (datetime.now() - start_time).total_seconds()
        
        print(f"⏱️  Durée d'exécution: {duration:.2f}s")
        
        # Génération du log
        validator.generate_log(log_output)
        
        # Code de sortie
        if stats['invalid'] > 0:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except FileNotFoundError as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
