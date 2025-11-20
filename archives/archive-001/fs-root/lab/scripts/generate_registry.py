#!/usr/bin/env python3
"""
Script de génération du registre documentaire Relinium (SSOT v1.0)

Ce script parcourt récursivement le répertoire docs/ pour extraire tous
les frontmatters YAML valides, calculer leurs hashes SHA256 et générer
un registre global de tous les documents.

Auteur: Équipe Relinium Genesis
Version: 1.0.0
Date: 2025-05-11
"""

import os
import re
import sys
import yaml
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import defaultdict


# Dossiers à ignorer lors du parcours
EXCLUDED_DIRS = {
    '_registry',
    '_templates',
    'sprints',
    '.github',
    '__pycache__',
    '.git',
    'node_modules',
    'venv',
    '.venv'
}

# Types de documents valides selon le schéma
VALID_DOC_TYPES = ['ADR', 'RFC', 'OBS', 'POC', 'SPRINT_DOC']


def extract_frontmatter(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Extrait le frontmatter YAML d'un fichier Markdown.
    
    Args:
        file_path: Chemin vers le fichier à analyser
        
    Returns:
        Dictionnaire contenant les métadonnées ou None si invalide
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Recherche du frontmatter YAML entre --- et ---
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return None
        
        frontmatter_text = match.group(1)
        frontmatter = yaml.safe_load(frontmatter_text)
        
        # Validation basique des champs requis
        required_fields = ['id', 'type', 'status', 'date']
        if not all(field in frontmatter for field in required_fields):
            return None
        
        # Validation du type
        if frontmatter.get('type') not in VALID_DOC_TYPES:
            return None
        
        return frontmatter
        
    except Exception as e:
        print(f"⚠️  Erreur lors de l'extraction du frontmatter de {file_path}: {e}", file=sys.stderr)
        return None


def calculate_file_hash(file_path: Path) -> str:
    """
    Calcule le hash SHA256 du contenu d'un fichier.
    
    Args:
        file_path: Chemin vers le fichier
        
    Returns:
        Hash SHA256 en hexadécimal
    """
    sha256_hash = hashlib.sha256()
    
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    
    return sha256_hash.hexdigest()


def scan_documents(docs_dir: Path) -> List[Dict[str, Any]]:
    """
    Parcourt récursivement le répertoire docs/ et collecte les métadonnées.
    
    Args:
        docs_dir: Répertoire racine à scanner
        
    Returns:
        Liste des documents avec leurs métadonnées
    """
    documents = []
    
    for root, dirs, files in os.walk(docs_dir):
        # Filtrer les répertoires à exclure
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        
        for file in files:
            if not file.endswith('.md'):
                continue
            
            file_path = Path(root) / file
            relative_path = file_path.relative_to(docs_dir.parent)
            
            frontmatter = extract_frontmatter(file_path)
            if frontmatter is None:
                continue
            
            # Calcul du hash du fichier
            file_hash = calculate_file_hash(file_path)
            
            # Construction de l'entrée du document
            doc_entry = {
                'id': frontmatter['id'],
                'type': frontmatter['type'],
                'status': frontmatter['status'],
                'date': frontmatter['date'],
                'file_path': str(relative_path),
                'hash': file_hash
            }
            
            # Ajout des champs optionnels
            if 'author' in frontmatter:
                doc_entry['author'] = frontmatter['author']
            if 'version' in frontmatter:
                doc_entry['version'] = frontmatter['version']
            if 'tags' in frontmatter:
                doc_entry['tags'] = frontmatter['tags']
            if 'links' in frontmatter:
                doc_entry['links'] = frontmatter['links']
            
            documents.append(doc_entry)
    
    return documents


def detect_duplicates(documents: List[Dict[str, Any]]) -> List[str]:
    """
    Détecte les IDs de documents en double.
    
    Args:
        documents: Liste des documents
        
    Returns:
        Liste des IDs dupliqués
    """
    id_counts = defaultdict(int)
    for doc in documents:
        id_counts[doc['id']] += 1
    
    return [doc_id for doc_id, count in id_counts.items() if count > 1]


def build_citation_graph(documents: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """
    Construit un graphe simplifié des relations de citation.
    
    Args:
        documents: Liste des documents
        
    Returns:
        Dictionnaire représentant le graphe de citations
    """
    graph = {}
    
    for doc in documents:
        doc_id = doc['id']
        links = doc.get('links', {})
        
        # Relations sortantes (ce document cite...)
        cites = links.get('cites', [])
        cited_by = links.get('cited_by', [])
        
        if cites or cited_by:
            graph[doc_id] = {
                'cites': cites,
                'cited_by': cited_by
            }
    
    return graph


def generate_registry(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Génère la structure complète du registre.
    
    Args:
        documents: Liste des documents collectés
        
    Returns:
        Registre structuré avec métadonnées et statistiques
    """
    # Tri des documents par ID
    sorted_docs = sorted(documents, key=lambda x: x['id'])
    
    # Statistiques par type
    type_stats = defaultdict(int)
    status_stats = defaultdict(int)
    
    for doc in documents:
        type_stats[doc['type']] += 1
        status_stats[doc['status']] += 1
    
    # Construction du registre
    registry = {
        'metadata': {
            'version': '1.0.0',
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'generator': 'scripts/generate_registry.py',
            'schema': 'docs/01-genesis/document_schema_v1.json'
        },
        'summary': {
            'total_documents': len(documents),
            'by_type': dict(type_stats),
            'by_status': dict(status_stats)
        },
        'documents': sorted_docs
    }
    
    return registry


def save_registry(registry: Dict[str, Any], output_path: Path) -> None:
    """
    Sauvegarde le registre au format YAML.
    
    Args:
        registry: Structure du registre
        output_path: Chemin de sortie
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(
            registry,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=120
        )


def main():
    """Point d'entrée principal du script."""
    print("🔍 Génération du registre documentaire Relinium (SSOT v1.0)")
    print("=" * 70)
    
    # Chemins
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_dir = project_root / 'docs'
    output_path = docs_dir / '_registry' / 'registry.yaml'
    
    # Vérification de l'existence du répertoire docs
    if not docs_dir.exists():
        print(f"❌ Erreur: Le répertoire {docs_dir} n'existe pas", file=sys.stderr)
        sys.exit(1)
    
    # Scan des documents
    print(f"\n📂 Scan du répertoire: {docs_dir}")
    documents = scan_documents(docs_dir)
    print(f"✅ {len(documents)} documents valides détectés")
    
    # Détection des doublons
    print("\n🔍 Vérification des doublons...")
    duplicates = detect_duplicates(documents)
    if duplicates:
        print(f"⚠️  ATTENTION: {len(duplicates)} IDs en double détectés:")
        for dup_id in duplicates:
            print(f"   - {dup_id}")
        print("\n❌ Le registre ne peut pas être généré avec des doublons.")
        sys.exit(1)
    else:
        print("✅ Aucun doublon détecté")
    
    # Construction du graphe de citations
    print("\n🔗 Construction du graphe de relations...")
    citation_graph = build_citation_graph(documents)
    print(f"✅ {len(citation_graph)} documents avec relations détectées")
    
    # Génération du registre
    print("\n📝 Génération du registre...")
    registry = generate_registry(documents)
    
    # Sauvegarde
    print(f"💾 Sauvegarde dans: {output_path}")
    save_registry(registry, output_path)
    
    # Calcul du hash du registre
    registry_hash = calculate_file_hash(output_path)
    
    # Affichage du résumé
    print("\n" + "=" * 70)
    print("✅ REGISTRE GÉNÉRÉ AVEC SUCCÈS")
    print("=" * 70)
    print(f"\n📊 Statistiques:")
    print(f"   • Total de documents: {registry['summary']['total_documents']}")
    print(f"   • Par type:")
    for doc_type, count in sorted(registry['summary']['by_type'].items()):
        print(f"     - {doc_type}: {count}")
    print(f"   • Par statut:")
    for status, count in sorted(registry['summary']['by_status'].items()):
        print(f"     - {status}: {count}")
    print(f"\n🔐 Hash SHA256 du registre:")
    print(f"   {registry_hash}")
    print(f"\n📁 Fichier généré:")
    print(f"   {output_path}")
    print()


if __name__ == '__main__':
    main()
