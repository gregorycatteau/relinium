# RFC-auth-iam-relinium-v0.1

## Objet

Cette RFC decrit la fondation Auth/IAM de Relinium v0.1.

Elle documente une approche progressive:

- socle Django auth;
- organisations et memberships;
- RBAC metier;
- audit d'authentification redige;
- preparation OAuth/OIDC;
- preparation MFA.

## Principes

1. Zero trust par defaut.
2. Moindre privilege.
3. Pas de mot de passe professionnel stocke par Relinium.
4. Pas de token OAuth brut en base.
5. Pas de pseudo-MFA maison.
6. Mutations GraphQL sensibles protegees par permission.
7. Separation explicite des modes local, dev et production.

## Phase 1

Phase 1 ajoute une app `accounts` cote backend:

- `Organization`;
- `UserProfile`;
- `OrganizationMembership`;
- `OAuthIdentity`;
- `AccessRequest`;
- `AuthAuditEvent`.

Les roles initiaux sont:

- `owner`;
- `admin`;
- `analyst`;
- `operator`;
- `viewer`.

Les permissions metier initiales couvrent:

- SourceRegistry;
- preparation scan;
- lecture evenements;
- dossiers Anti-Scam;
- generation et revue de rapports;
- administration membres et securite.

## Mode developpement

Le mode developpement est strictement explicite:

- `RELINIUM_AUTH_MODE=dev`;
- `RELINIUM_DEV_AUTH_ENABLED=true`.

Sans ces deux variables, aucune identite de developpement n'est creee.

## OAuth/OIDC futur

Les providers cibles sont:

- Microsoft Entra ID;
- Google Workspace;
- OIDC generique.

Le callback futur devra creer ou lier un `User` Django et une `OAuthIdentity`
sans stocker d'access token ni de refresh token brut.

## MFA futur

La strategie MFA cible:

- politique MFA par organisation;
- statut utilisateur `mfa_required`, `mfa_enrolled`, `last_mfa_at`;
- TOTP via librairie eprouvee;
- recovery codes hashes;
- WebAuthn/passkeys dans une phase ulterieure.

## Limites v0.1

Phase 1 ne fournit pas encore:

- provider OIDC reel;
- TOTP;
- WebAuthn;
- gestion avancee des sessions;
- rate limiting applicatif;
- limitation de complexite GraphQL.

Ces sujets doivent etre traites avant exposition production.
