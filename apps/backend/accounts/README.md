# Relinium Accounts

`accounts` porte la fondation Auth/IAM de Relinium.

## Portee Phase 1

- socle `django.contrib.auth`;
- organisations;
- profils utilisateurs;
- memberships organisationnels;
- roles RBAC;
- permissions metier centrales;
- demandes d'acces;
- audit d'authentification redige;
- preparation OAuth/OIDC et MFA.

Phase 1 n'implemente pas de provider OAuth reel, pas de mot de passe applicatif
Relinium, pas de TOTP, pas de WebAuthn et pas de stockage de token OAuth.

## Modes d'authentification

Variables:

```bash
RELINIUM_AUTH_MODE=disabled
RELINIUM_DEV_AUTH_ENABLED=false
RELINIUM_DEV_USER_EMAIL=dev@relinium.local
RELINIUM_DEV_USER_NAME="Relinium Dev"
RELINIUM_DEV_USER_ROLE=owner
RELINIUM_DEFAULT_ORG="Relinium Local"
RELINIUM_MFA_REQUIRED_DEFAULT=false
```

`RELINIUM_AUTH_MODE` accepte:

- `disabled`: aucune identite applicative automatique;
- `dev`: mode local explicite;
- `oidc`: reserve au raccordement OAuth/OIDC futur.

Le mode dev ne s'active que si `RELINIUM_AUTH_MODE=dev` et
`RELINIUM_DEV_AUTH_ENABLED=true`. Sans ces deux signaux, aucune identite
fallback n'est creee.

## RBAC

Roles:

- `owner`;
- `admin`;
- `analyst`;
- `operator`;
- `viewer`.

Permissions initiales:

- `source:create`
- `source:read`
- `source:update`
- `source:disable`
- `scan:prepare`
- `scan:run`
- `event:read`
- `scam_case:create`
- `scam_case:read`
- `scam_case:update`
- `report:generate`
- `report:review`
- `admin:manage_members`
- `admin:manage_security`

Les helpers dans `accounts.permissions` sont le point d'entree unique pour les
resolvers GraphQL et les futurs services applicatifs.

## Secrets

Ne jamais stocker:

- mot de passe professionnel;
- access token OAuth;
- refresh token OAuth;
- secret TOTP en clair;
- recovery code en clair.

Les champs d'audit restent rediges. Les IP sont hashees et les user-agents sont
tronques.

## OIDC futur

Les providers cibles sont:

- Microsoft Entra ID;
- Google Workspace;
- OIDC generique.

Le callback OIDC devra lier une identite externe a `OAuthIdentity` sans stocker
de token brut.

## MFA futur

TOTP devra passer par une librairie eprouvee comme `django-otp` ou
`django-two-factor-auth`. Aucun pseudo-TOTP maison ne doit etre ajoute.
