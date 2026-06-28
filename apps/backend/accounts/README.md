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

## Parcours d'acces

Le frontend expose `/connexion` comme hub d'acces avec trois chemins:

- utilisateur existant: connexion par identite organisationnelle quand OIDC
  sera raccorde;
- creation compte entreprise: preparation d'une demande d'ouverture
  d'organisation via `/creation-compte`;
- acces administrateur: preparation d'une demande renforcee via `/admin-acces`.

Ces parcours ne creent pas de mot de passe Relinium et ne collectent pas de
secret. La mutation `requestAccess` peut etre reutilisee pour enregistrer une
demande redigee et contextualisee, mais elle ne valide pas automatiquement une
organisation, un responsable ou un role administrateur.

Le KYC organisationnel reste futur. Les etapes attendues sont la verification
email professionnel, la verification telephone, le controle du domaine ou site
officiel, le controle justificatif et une validation humaine. Aucun upload de
justificatif n'est stocke en v0.1.

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
OIDC_PROVIDER_NAME=
OIDC_CLIENT_ID=
OIDC_CLIENT_SECRET=
OIDC_DISCOVERY_URL=
OIDC_REDIRECT_URI=
```

`RELINIUM_AUTH_MODE` accepte:

- `disabled`: aucune identite applicative automatique;
- `dev`: mode local explicite;
- `oidc`: reserve au raccordement OAuth/OIDC futur.

Le mode dev ne s'active que si `RELINIUM_AUTH_MODE=dev` et
`RELINIUM_DEV_AUTH_ENABLED=true`. Sans ces deux signaux, aucune identite
fallback n'est creee.

`authStatus` expose `providerConfigured` et `providerName` pour signaler si un
provider OIDC est réellement configure. Phase 1 ne fournit pas de callback OIDC
et ne doit donc afficher aucune connexion organisationnelle comme fonctionnelle
tant que ce raccordement n'est pas ajoute.

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

Les guards GraphQL sont centralises dans `accounts.graphql_security`:

- `require_authenticated`;
- `require_permission`;
- `current_request_user`;
- `current_organization_or_error`;
- `safe_graphql_error`.

Le durcissement de transport GraphQL est applique par
`relinium_api.graphql_view.ReliniumGraphQLView`. En production
(`DJANGO_DEBUG=false`), `RELINIUM_GRAPHQL_INTROSPECTION_ENABLED` doit rester
absent ou valoir `false`: les requetes contenant `__schema` ou `__type` sont
refusees avec le message generique `GraphQL introspection is disabled.`. Les
requêtes applicatives normales restent autorisees. La taille des corps POST est
limitee par `RELINIUM_GRAPHQL_MAX_REQUEST_BYTES` (`1048576` par defaut).

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
En Phase 1, `authStatus.mfaProviderStatus` vaut `planned`; une politique
organisationnelle `mfa_policy=required` rend `mfaRequired` visible sans activer
de verification TOTP factice.
