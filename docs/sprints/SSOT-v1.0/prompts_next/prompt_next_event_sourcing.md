# Prompt Next : Event Sourcing Documentaire (Phase 3+)

Ce prompt sera utilisé si un besoin d'audit forensique émerge (> 2000 documents).

---

## 📋 PROMPT POUR CLINE

```
Mission : Implémenter Event Sourcing documentaire pour audit trail complet

Contexte :
- SSOT Phase 1 et 2 déployées et opérationnelles
- Corpus > 2000 documents
- Besoin d'audit forensique identifié
- Reconstruction temporelle d'états passés nécessaire

Objectif :
Implémenter un système append-only log de tous les événements documentaires.

Architecture :

1. Event Log
   - docs/_meta/event-log.jsonl (JSON Lines, append-only)
   - Événements : DocumentCreated, StatusChanged, DocumentCited, etc.
   - Timestamp précis, auteur, métadonnées changement

2. Registry actuel maintenu
   - docs/_registry/registry.yaml (état actuel)
   - Régénérable depuis event-log
   - Vue "current state"

3. Event Store
   - Tous les événements préservés
   - Jamais de suppression
   - Compression périodique (archives)

4. Reconstruction d'état
   - Script replay_events.py
   - Reconstruire état à date T
   - Audit forensique complet

Événements à modéliser :
- DocumentCreated(id, type, author, timestamp)
- DocumentModified(id, fields_changed, timestamp)
- StatusChanged(id, from, to, timestamp)
- DocumentCited(source, target, timestamp)
- DocumentSuperseded(old, new, timestamp)

Livrables :
- docs/_meta/event-log.jsonl
- lab/scripts/event_store.py (append events)
- lab/scripts/replay_events.py (reconstruct state)
- .github/workflows/event-logging.yml
- docs/07-contrib/event-sourcing-guide.md

Avantages :
- Inviolabilité forte (append-only)
- Audit trail complet
- Time-travel possible
- Reconstruction d'états historiques

Contraintes :
- Event log peut devenir volumineux (compression nécessaire)
- Reconstruction nécessite replay (cache requis)
- Complexité conceptuelle (documentation essentielle)

Durée estimée : 3-4 semaines

Basé sur :
- SSOT_METADATA_EXPLORATION.md (Approche G.3 - score 32/44)
- Hypothèse 10.1 : Living Registry avec Event Sourcing léger
```

---

**Utiliser uniquement si besoin audit forensique avéré**
