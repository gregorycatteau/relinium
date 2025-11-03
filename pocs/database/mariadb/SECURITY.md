# SECURITY – [À REMPLACER : nom du candidat]

## 1. Validation & sanitization
- Bibliothèques / mécanismes utilisés :
- Endpoints couverts :
- Comportement sur JSON malformé / types erronés :

## 2. Contrôles de sécurité
### Rate limiting
- Présent sur /auth/login ? [Oui/Non]
- Paramètres (req/min/IP) :
- Implémentation :

### AuthN / AuthZ
- Mode auth : [sessions / JWT / OIDC / autre]
- Rôles implémentés : [viewer/editor/admin]
- Vérification accès document "private" par viewer → 403 ? [Oui/Non]

### Uploads
- Limite de taille :
- Contrôle du type de fichier ? :
- Gestion des erreurs (fichier trop gros) :

## 3. Headers de sécurité
- X-Content-Type-Options :
- Referrer-Policy :
- X-Frame-Options ou CSP frame-ancestors :
- Content-Security-Policy (si applicable) :

## 4. Logs & observabilité
- Format logs : [texte / JSON]
- Infos loggées : [correlation-id, user-id, endpoint, status, latence]
- Erreurs critiques loggées ? :
- Journaux d'accès disponibles ? :

## 5. Tests "hacker mindset"
- Bruteforce doux /auth/login (20 tentatives) : résultat :
- Injection JSON malformé : résultat :
- Accès document private en viewer : résultat :
- Upload overflow (> max autorisé) : résultat :

## 6. Dépendances & vulnérabilités
- Outils de scan (pip-audit / npm audit / cargo audit / govulncheck / autre) :
- Vulnérabilités critiques détectées ? :
- Actions de mitigation :

## 7. Conclusion sécurité
- Niveau global : [OK / A renforcer / KO]
- Points critiques :
- Recommandations :

