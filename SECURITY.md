# Politique de sécurité

Relinium prend la sécurité au sérieux. Ce document décrit nos pratiques et comment signaler une vulnérabilité.

## Principes de sécurité

### Security-by-Design

La sécurité est intégrée dès la conception :
- **Modèle de menaces** : identifié avant toute implémentation
- **Principe du moindre privilège** : accès minimum nécessaire
- **Défense en profondeur** : plusieurs couches de sécurité
- **Traçabilité** : tous les changements sont documentés et auditables

### Données sensibles

- ❌ **Aucun secret dans le dépôt** (tokens, mots de passe, clés API, certificats)
- ✅ Variables d'environnement (`.env`) pour la configuration
- ✅ Secrets gérés via gestionnaires dédiés (GitHub Secrets, Vault, etc.)
- ✅ `.gitignore` configuré pour exclure les fichiers sensibles

### Dépendances

- Justification de chaque dépendance ajoutée
- Revue régulière des vulnérabilités connues
- Mises à jour de sécurité prioritaires
- Audit des dépendances tierces

## Signaler une vulnérabilité

### Process de divulgation responsable

Si vous découvrez une faille de sécurité :

1. **NE PAS** créer d'issue publique
2. **NE PAS** divulguer publiquement avant correction
3. **Envoyer un rapport** par l'un de ces canaux :
   - Email chiffré : **security [at] relinium.io** (clé PGP disponible sur demande)
   - GitHub Security Advisories (onglet Security du dépôt)
   - Issue privée de type **Security vulnerability** (si disponible)

### Informations à inclure

Pour un traitement efficace, fournir :
- Description détaillée de la vulnérabilité
- Impact potentiel et scénarios d'exploitation
- Preuve de concept (PoC) si possible
- Versions affectées
- Suggestions de mitigation (optionnel)

### Délais de réponse

- **Accusé de réception** : sous 48h
- **Évaluation initiale** : sous 7 jours
- **Correctif** : selon la criticité (1 à 30 jours)
- **Divulgation publique** : après correction et délai de déploiement

### Reconnaissance

Les chercheurs en sécurité qui signalent des vulnérabilités de manière responsable seront :
- Crédités publiquement (sauf demande contraire)
- Mentionnés dans les notes de version
- Ajoutés à un hall of fame (à venir)

## Pratiques recommandées pour les contributeurs

### Développement sécurisé

- Activer la **2FA sur GitHub** (obligatoire pour les mainteneurs)
- Signer les commits (`git commit -S`)
- Ne jamais commiter de secrets ou credentials
- Valider les entrées utilisateur
- Échapper les sorties pour prévenir les injections
- Utiliser HTTPS pour toutes les communications

### Configuration Git

```bash
# Signature obligatoire des commits
git config --global commit.gpgsign true
git config --global tag.gpgSign true

# Protection contre les commits accidentels de secrets
# Installer git-secrets ou équivalent
git secrets --install
git secrets --register-aws
```

### Vérifications avant commit

- [ ] Aucun secret dans le code
- [ ] Dépendances justifiées et à jour
- [ ] Tests de sécurité passants
- [ ] Documentation de sécurité mise à jour
- [ ] ADR créée pour tout changement impactant la sécurité

## Versions supportées

| Version | Support | Correctifs de sécurité |
|---------|---------|------------------------|
| main    | ✅ Oui  | Immédiat              |
| dev     | ⚠️ Limité | Selon criticité       |
| < 1.0   | ❌ Non  | Non supporté          |

Une fois la version 1.0 publiée, seules les versions majeures récentes recevront des correctifs.

## Modèle de menaces

Le modèle de menaces complet est documenté dans :
- `docs/04-risk/threat_model.md`
- `docs/04-risk/risk_register.md`

### Menaces principales identifiées

1. **Injection de code malveillant** via dépendances
2. **Divulgation de secrets** dans le dépôt
3. **Attaques par déni de service** (DoS/DDoS)
4. **Compromission de comptes** contributeurs
5. **Manipulation de la supply chain**

Mitigations détaillées dans la documentation.

## Incidents de sécurité

### En cas d'incident confirmé

1. **Évaluation** : criticité et impact
2. **Containment** : isolement du problème
3. **Correction** : développement du patch
4. **Communication** : notification des utilisateurs
5. **Post-mortem** : analyse et amélioration

### Historique des incidents

Aucun incident de sécurité signalé à ce jour.

Les futurs incidents seront documentés de manière transparente (après résolution) dans `docs/06-ops/incidents/`.

## Compliance et audit

- Commits signés recommandés (obligatoires pour les mainteneurs)
- Logs d'accès conservés (GitHub audit log)
- Revues de sécurité régulières planifiées
- Audit externe envisagé pour la version 1.0

## Ressources additionnelles

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Guide de sécurité GitHub](https://docs.github.com/en/code-security)

## Contact

- **Email sécurité** : security [at] relinium.io
- **Email général** : contact [at] relinium.io
- **GitHub Issues** : pour les questions non sensibles

---

**La sécurité est l'affaire de tous. Merci de contribuer à un projet robuste et fiable.**
