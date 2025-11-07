#!/usr/bin/env python3
"""
SSOT v1.0 - Script d'audit cryptographique
Vérifie l'intégrité de tous les livrables par comparaison des hashes SHA256
"""

import hashlib
import yaml
import os
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Any

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

PROJECT_ROOT = Path(__file__).parent.parent
HASHES_FILE = PROJECT_ROOT / "docs/sprints/SSOT-v1.0/03-validation/SSOT_V1_HASHES.yaml"
REPORT_FILE = PROJECT_ROOT / "docs/sprints/SSOT-v1.0/02-evidence/S5_HASH_VERIFICATION_REPORT.txt"

# ═══════════════════════════════════════════════════════════════════════════════
# FONCTIONS UTILITAIRES
# ═══════════════════════════════════════════════════════════════════════════════

def calculate_sha256(file_path: Path) -> str:
    """Calcule le hash SHA256 d'un fichier."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            # Lecture par blocs de 64KB pour gérer les gros fichiers
            for byte_block in iter(lambda: f.read(65536), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return "FILE_NOT_FOUND"
    except Exception as e:
        return f"ERROR: {str(e)}"

def load_hashes_registry() -> Dict[str, Any]:
    """Charge le registre des hashes."""
    try:
        with open(HASHES_FILE, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Erreur lors de la lecture du registre des hashes: {e}")
        sys.exit(1)

def extract_deliverables(registry: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extrait tous les livrables du registre."""
    deliverables = []
    
    # S1 deliverables
    if 's1_deliverables' in registry:
        for item in registry['s1_deliverables']:
            if 'path' in item and 'hash' in item:
                deliverables.append({
                    'sprint': 'S1',
                    'name': item.get('name', 'Unknown'),
                    'path': item['path'],
                    'expected_hash': item['hash'],
                    'type': item.get('type', 'unknown')
                })
    
    # S2 deliverables
    if 's2_deliverables' in registry:
        for item in registry['s2_deliverables']:
            if 'path' in item and 'hash' in item:
                deliverables.append({
                    'sprint': 'S2',
                    'name': item.get('name', 'Unknown'),
                    'path': item['path'],
                    'expected_hash': item['hash'],
                    'type': item.get('type', 'unknown')
                })
    
    # S3 deliverables
    if 's3_deliverables' in registry:
        for item in registry['s3_deliverables']:
            if 'path' in item and 'hash' in item:
                deliverables.append({
                    'sprint': 'S3',
                    'name': item.get('name', 'Unknown'),
                    'path': item['path'],
                    'expected_hash': item['hash'],
                    'type': item.get('type', 'unknown')
                })
    
    # S4 deliverables
    if 's4_deliverables' in registry:
        for item in registry['s4_deliverables']:
            if 'path' in item and 'hash' in item:
                deliverables.append({
                    'sprint': 'S4',
                    'name': item.get('name', 'Unknown'),
                    'path': item['path'],
                    'expected_hash': item['hash'],
                    'type': item.get('type', 'unknown')
                })
    
    return deliverables

def verify_deliverables(deliverables: List[Dict[str, Any]]) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Vérifie tous les livrables.
    
    Returns:
        Tuple de (validés, divergents, fichiers manquants)
    """
    valid = []
    divergent = []
    missing = []
    
    for deliverable in deliverables:
        # Ignorer les fichiers avec des hashes spéciaux
        expected_hash = deliverable['expected_hash']
        if expected_hash in ['pending', 'self_reference', 'pending_hash']:
            continue
        
        file_path = PROJECT_ROOT / deliverable['path']
        actual_hash = calculate_sha256(file_path)
        
        if actual_hash == "FILE_NOT_FOUND":
            missing.append({
                **deliverable,
                'actual_hash': 'FILE_NOT_FOUND'
            })
        elif actual_hash.startswith("ERROR"):
            divergent.append({
                **deliverable,
                'actual_hash': actual_hash
            })
        elif actual_hash == expected_hash:
            valid.append({
                **deliverable,
                'actual_hash': actual_hash
            })
        else:
            divergent.append({
                **deliverable,
                'actual_hash': actual_hash
            })
    
    return valid, divergent, missing

def calculate_corpus_hash(valid_deliverables: List[Dict]) -> str:
    """
    Calcule le hash global du corpus en concaténant tous les hashes triés.
    """
    # Extraire tous les hashes et les trier
    hashes = sorted([d['expected_hash'] for d in valid_deliverables])
    
    # Concaténer et hasher
    concatenated = ''.join(hashes)
    corpus_hash = hashlib.sha256(concatenated.encode()).hexdigest()
    
    return corpus_hash

def generate_report(valid: List[Dict], divergent: List[Dict], missing: List[Dict], 
                   corpus_hash: str, execution_time: float) -> str:
    """Génère le rapport de vérification."""
    
    report_lines = [
        "═" * 80,
        "SSOT v1.0 - RAPPORT DE VÉRIFICATION DES HASHES",
        "═" * 80,
        "",
        f"Date de génération : {datetime.now(timezone.utc).isoformat()}",
        f"Fichier source : {HASHES_FILE.relative_to(PROJECT_ROOT)}",
        f"Temps d'exécution : {execution_time:.3f} secondes",
        "",
        "─" * 80,
        "RÉSUMÉ",
        "─" * 80,
        "",
        f"Total de fichiers audités  : {len(valid) + len(divergent) + len(missing)}",
        f"✅ Hashes valides           : {len(valid)}",
        f"❌ Hashes divergents        : {len(divergent)}",
        f"⚠️  Fichiers manquants      : {len(missing)}",
        "",
        f"🔐 Hash global du corpus   : {corpus_hash}",
        "",
    ]
    
    # Section des fichiers valides
    if valid:
        report_lines.extend([
            "─" * 80,
            "FICHIERS VALIDES",
            "─" * 80,
            ""
        ])
        
        by_sprint = {}
        for item in valid:
            sprint = item['sprint']
            if sprint not in by_sprint:
                by_sprint[sprint] = []
            by_sprint[sprint].append(item)
        
        for sprint in sorted(by_sprint.keys()):
            report_lines.append(f"## {sprint} - {len(by_sprint[sprint])} fichier(s)")
            report_lines.append("")
            for item in by_sprint[sprint]:
                report_lines.extend([
                    f"  Nom   : {item['name']}",
                    f"  Path  : {item['path']}",
                    f"  Hash  : {item['expected_hash']}",
                    f"  Type  : {item['type']}",
                    f"  ✅ VALIDE",
                    ""
                ])
    
    # Section des divergences
    if divergent:
        report_lines.extend([
            "─" * 80,
            "⚠️  DIVERGENCES DÉTECTÉES",
            "─" * 80,
            ""
        ])
        
        for item in divergent:
            report_lines.extend([
                f"  Nom          : {item['name']}",
                f"  Path         : {item['path']}",
                f"  Hash attendu : {item['expected_hash']}",
                f"  Hash actuel  : {item['actual_hash']}",
                f"  ❌ DIVERGENCE",
                ""
            ])
    
    # Section des fichiers manquants
    if missing:
        report_lines.extend([
            "─" * 80,
            "⚠️  FICHIERS MANQUANTS",
            "─" * 80,
            ""
        ])
        
        for item in missing:
            report_lines.extend([
                f"  Nom  : {item['name']}",
                f"  Path : {item['path']}",
                f"  ⚠️  FICHIER NON TROUVÉ",
                ""
            ])
    
    # Conclusion
    report_lines.extend([
        "─" * 80,
        "CONCLUSION",
        "─" * 80,
        ""
    ])
    
    if not divergent and not missing:
        report_lines.extend([
            "✅ AUDIT RÉUSSI",
            "",
            "Tous les fichiers du SSOT v1.0 ont été vérifiés avec succès.",
            "Aucune divergence cryptographique détectée.",
            "Le corpus est certifié complet et intègre.",
            ""
        ])
    else:
        report_lines.extend([
            "❌ AUDIT ÉCHOUÉ",
            "",
            f"Nombre de divergences : {len(divergent)}",
            f"Nombre de fichiers manquants : {len(missing)}",
            "",
            "Action requise : Vérifier les fichiers signalés ci-dessus.",
            ""
        ])
    
    report_lines.extend([
        "═" * 80,
        "Fin du rapport",
        "═" * 80
    ])
    
    return '\n'.join(report_lines)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Point d'entrée principal."""
    print("🔍 Démarrage de l'audit cryptographique SSOT v1.0...")
    print(f"📂 Répertoire projet : {PROJECT_ROOT}")
    print(f"📄 Registre des hashes : {HASHES_FILE.relative_to(PROJECT_ROOT)}")
    print()
    
    start_time = datetime.now()
    
    # Charger le registre
    print("📖 Chargement du registre des hashes...")
    registry = load_hashes_registry()
    
    # Extraire les livrables
    print("📋 Extraction des livrables...")
    deliverables = extract_deliverables(registry)
    print(f"   → {len(deliverables)} fichiers à vérifier")
    print()
    
    # Vérifier les hashes
    print("🔐 Vérification des hashes SHA256...")
    valid, divergent, missing = verify_deliverables(deliverables)
    
    # Calculer le hash global du corpus
    print("🧮 Calcul du hash global du corpus...")
    corpus_hash = calculate_corpus_hash(valid)
    
    # Mesurer le temps d'exécution
    execution_time = (datetime.now() - start_time).total_seconds()
    
    # Générer le rapport
    print("📝 Génération du rapport...")
    report = generate_report(valid, divergent, missing, corpus_hash, execution_time)
    
    # Sauvegarder le rapport
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Rapport généré : {REPORT_FILE.relative_to(PROJECT_ROOT)}")
    print()
    
    # Afficher le résumé
    print("─" * 80)
    print("RÉSUMÉ DE L'AUDIT")
    print("─" * 80)
    print(f"✅ Fichiers valides    : {len(valid)}")
    print(f"❌ Divergences         : {len(divergent)}")
    print(f"⚠️  Fichiers manquants : {len(missing)}")
    print(f"🔐 Hash corpus         : {corpus_hash}")
    print(f"⏱️  Temps d'exécution   : {execution_time:.3f}s")
    print()
    
    if divergent or missing:
        print("❌ AUDIT ÉCHOUÉ - Des anomalies ont été détectées")
        return 1
    else:
        print("✅ AUDIT RÉUSSI - Intégrité du SSOT v1.0 confirmée")
        return 0

if __name__ == "__main__":
    sys.exit(main())
