# Relinium Cockpit Apps

Application layer for the Relinium SSOT.

The SSOT filesystem under `ssot-root/` remains the source of truth. The Django
backend reads it and exposes JSON and GraphQL endpoints. The Nuxt frontend
renders a local cockpit for operational inspection.

## Architecture

Relinium separates two layers:

- `ssot-root/` is the governance layer: rules, schemas, policies, invariants,
  contracts, and canonical append-only events.
- PostgreSQL is the operational black box: real application storage, future
  business data, projections, validation results, jobs, audit logs, snapshots,
  and workflow state.

Django is the orchestrator between both layers. Any future write to PostgreSQL
must be validated against SSOT rules before it is accepted. PostgreSQL must not
become a copy of vault content or a replacement source of truth for canonical
SSOT files.

## Backend

Requirements:

- Python 3
- Django 4.2+
- PostgreSQL for database-backed operation
- `psycopg` v3

Install:

```bash
cd apps/backend
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

### Environment

Copy `.env.example` values into your local environment. The development
PostgreSQL URL is:

```bash
export RELINIUM_DATABASE_MODE=db
export DATABASE_URL=postgresql://relinium_app:relinium_app_dev@127.0.0.1:5432/relinium_app
```

For inspection-only operation without database writes, omit `DATABASE_URL` or
set:

```bash
export RELINIUM_DATABASE_MODE=readonly
```

This mode keeps REST and GraphQL inspection working from `ssot-root/`, but it
does not run migrations or database-backed workflows. There is no SQLite
fallback.

### Auth/IAM

Relinium Phase 1 uses `django.contrib.auth` as the identity foundation and the
`accounts` app for organizations, profiles, memberships, RBAC permissions,
access requests and redacted auth audit events.

Authentication modes:

```bash
export RELINIUM_AUTH_MODE=disabled
export RELINIUM_DEV_AUTH_ENABLED=false
export RELINIUM_DEV_USER_EMAIL=dev@relinium.local
export RELINIUM_DEV_USER_NAME="Relinium Dev"
export RELINIUM_DEV_USER_ROLE=owner
export RELINIUM_DEFAULT_ORG="Relinium Local"
export RELINIUM_MFA_REQUIRED_DEFAULT=false
export RELINIUM_SESSION_COOKIE_SECURE=false
export RELINIUM_CSRF_COOKIE_SECURE=false
export RELINIUM_GRAPHQL_INTROSPECTION_ENABLED=true
```

`RELINIUM_AUTH_MODE=dev` is only effective when
`RELINIUM_DEV_AUTH_ENABLED=true`. This is intentionally explicit. No developer
identity is created implicitly.

OAuth/OIDC is prepared but not implemented in Phase 1. Future providers should
cover Microsoft Entra ID, Google Workspace and generic OIDC. Relinium must not
store professional passwords, OAuth access tokens or OAuth refresh tokens.
The prepared OIDC environment variables are `OIDC_PROVIDER_NAME`,
`OIDC_CLIENT_ID`, `OIDC_CLIENT_SECRET`, `OIDC_DISCOVERY_URL` and
`OIDC_REDIRECT_URI`. Empty values mean `authStatus.providerConfigured=false`;
the frontend must not present the organization login as active.

MFA is prepared through profile and organization policy fields. TOTP must be
implemented later with a proven library such as `django-otp` or
`django-two-factor-auth`; no custom TOTP implementation is allowed.
`authStatus.mfaProviderStatus` remains `planned` in Phase 1.

RBAC permissions are centralized in `apps/backend/accounts/permissions.py`.
Sensitive GraphQL mutations now require an authenticated user, an active
organization membership and the matching permission.
GraphQL auth guards are centralized in `apps/backend/accounts/graphql_security.py`.

Production hardening variables:

- `DJANGO_DEBUG=false`
- `DJANGO_ALLOWED_HOSTS=<strict host list>`
- `RELINIUM_SESSION_COOKIE_SECURE=true`
- `RELINIUM_CSRF_COOKIE_SECURE=true`
- `RELINIUM_CORS_ALLOWED_ORIGINS=<strict origin list>`
- `RELINIUM_GRAPHQL_INTROSPECTION_ENABLED=false`
- `RELINIUM_GRAPHQL_MAX_REQUEST_BYTES=1048576`

`RELINIUM_GRAPHQL_INTROSPECTION_ENABLED` defaults to `true` in debug mode and
`false` when `DJANGO_DEBUG=false`. When disabled, `/graphql` rejects
introspection requests containing `__schema` or `__type` with a generic client
message. `RELINIUM_GRAPHQL_MAX_REQUEST_BYTES` limits POST request bodies before
GraphQL execution.

### Local PostgreSQL

Start local PostgreSQL:

```bash
cd apps/backend
docker compose up -d postgres
```

If `127.0.0.1:5432` is already used by another local PostgreSQL, keep that
service untouched and start Relinium on another local port:

```bash
cd apps/backend
RELINIUM_POSTGRES_PORT=5433 docker compose up -d postgres
export DATABASE_URL=postgresql://relinium_app:relinium_app_dev@127.0.0.1:5433/relinium_app
```

The local service uses:

- database: `relinium_app`
- user: `relinium_app`
- password: `relinium_app_dev`
- host: `127.0.0.1`
- port: `5432`

### Django commands

```bash
cd apps/backend
python3 manage.py check
python3 manage.py makemigrations --check --dry-run
python3 manage.py migrate
python3 manage.py runserver 127.0.0.1:8000
```

Endpoints:

- `GET /api/health`
- `GET /api/ssot/summary`
- `GET /api/events/streams`
- `GET /api/events`
- `GET /api/validation/status`
- `GET /api/validation/known-findings`
- `GET|POST /graphql`

The validation endpoint uses:

```bash
python3 ssot-root/core/scripts/validate_documents.py
python3 ssot-root/core/scripts/validate_documents.py --baseline ssot-root/core/validation/known_findings.json
```

internally by importing the validator module and applying the same validation
logic in process.

REST is kept temporarily while GraphQL is introduced in parallel.

### GraphQL

Initial read-only queries:

- `health`
- `ssotSummary`
- `eventStreams`
- `events(limit: 50, offset: 0)`
- `validationStatus`
- `knownFindings`
- `documents(limit: 50, offset: 0)`
- `roadmapStatus`

`events` and `documents` are limited to 200 items per request. Resolvers call
the existing cockpit services instead of reading arbitrary paths.

Example:

```graphql
query {
  health {
    status
    ssotRoot
  }
}
```

### Relinium Anti-Scam

`scam_trace` adds the Relinium Anti-Scam business line. It is PostgreSQL-backed
and exposed through GraphQL for the operator cockpit.

GraphQL queries:

- `scamCases`
- `scamCase(id)`
- `scamCaseTimeline(caseId)`
- `scamCaseIndicators(caseId)`
- `scamCaseReports(caseId)`
- `scamCaseCorrelations(caseId)`
- `scamQuestionnaireTemplate`

GraphQL mutations:

- `createScamCase`
- `addScamArtifact`
- `answerScamQuestion`
- `generateScamReports`
- `markReportReviewed`

MVP scope:

- create a minimized anti-scam case;
- paste limited EML, SMS, call note, URL, bank record or victim statement text;
- compute SHA-256 on the backend;
- extract passive indicators without visiting suspicious URLs;
- answer the guided questionnaire;
- derive a probative timeline;
- generate Markdown reports for victim, authorities, bank and technical review;
- correlate cases on shared indicators.

### Source Registry

`source_registry` is the enterprise onboarding registry for data sources that
Relinium may observe later. It is PostgreSQL-backed and exposed through GraphQL.

GraphQL queries:

- `dataSources`
- `dataSource(id)`

GraphQL mutations:

- `createDataSource`
- `updateDataSource`
- `markDataSourceReady`
- `disableDataSource`

MVP scope:

- declare a source as local folder, network share/NAS, server/VPS, cloud/GED, or
  other;
- store a label, non-secret locator reference, status, read-only rules,
  exclusions, and redacted notes;
- compute a SHA-256 hash of the locator reference;
- expose only `locatorDisplay` and `locatorHash` in source lists, never the raw
  locator reference;
- record redacted audit events;
- keep source records read-only and avoid launching scans automatically.

Secrets are explicitly out of scope for v0.1. Do not store passwords, API keys,
OAuth tokens, cookies, or bearer tokens in source records. Future credentials
must use encrypted backend storage with rotation, access audit, and
operator/admin separation.
Locators containing URI userinfo or markers such as `password=`, `token=`,
`api_key=`, `secret=` or `Bearer` are rejected.

Future scanner integration is prepared but not executed by the backend yet:

```bash
relinium-cartography-scan --root <source> --mode presence --out <snapshot.ndjson>
```

Security limits:

- no automatic click or remote content fetch;
- no binary-heavy storage in PostgreSQL for this milestone;
- no cleartext secrets;
- no automatic submission to Signal Spam, 33700, Phishing Initiative, 17Cyber,
  THESEE/PHAROS, police/gendarmerie or banks;
- human validation is mandatory before any external transmission.

### Security limits

- No SQLite fallback.
- No password-based GraphQL login.
- No implicit development user.
- No OAuth token storage.
- No custom MFA implementation.
- No arbitrary filesystem path input.
- No exposure of `personal_vault`, `vault_index`, or `users/user_template`.
- No vault content in PostgreSQL.
- No secrets in logs, audit records, or redacted message fields.
- Existing SSOT REST and inspection GraphQL remain read-only; `scam_trace`
  exposes controlled business mutations backed by PostgreSQL.
- Future GraphQL production exposure must add authentication and query
  depth/complexity controls.

## Frontend

Requirements:

- Node.js 20+
- npm

Install and run:

```bash
cd apps/frontend
npm install
NUXT_PUBLIC_API_BASE=http://127.0.0.1:8000 npm run dev
```

Open:

- Backend: `http://127.0.0.1:8000/api/health`
- GraphQL: `http://127.0.0.1:8000/graphql`
- Frontend: `http://localhost:3000`
- Anti-Scam: `http://localhost:3000/anti-scam`

The frontend reads only the Django API URL from `NUXT_PUBLIC_API_BASE`.
The cockpit still consumes REST in this milestone. A later step should migrate
the Nuxt data layer to GraphQL while preserving the existing TypeScript view
contracts.

## Go agents

Relinium keeps Go binaries under `apps/go/` so several defensive agents can
share internal packages without mixing responsibilities.

Current structure:

```text
apps/go/
  cmd/
    relinium-cartography-scan/
    relinium-evidence-hash/
  internal/
    cartography/
    evidence/
    fsutil/
    hashing/
    ndjson/
    seal/
```

Planned later:

```text
apps/go/cmd/relinium-motion-detector/
apps/go/internal/motion/
apps/go/internal/connectors/
```

### Cartographie documentaire

`relinium-cartography-scan` photographs a document tree without importing or
copying files into Relinium. It produces sealed NDJSON observations that can be
ingested later by Django/PostgreSQL.

Example:

```bash
cd apps/go
go run ./cmd/relinium-cartography-scan \
  --root /path/to/authorized/tree \
  --mode presence \
  --out /tmp/relinium-snapshot.ndjson
```

Fingerprint mode reads only the first and last configured blocks of regular
files:

```bash
go run ./cmd/relinium-cartography-scan \
  --root /path/to/authorized/tree \
  --mode fingerprint \
  --fingerprint-block-size 262144 \
  --exclude .git \
  --out /tmp/relinium-snapshot-fingerprint.ndjson
```

The scanner:

- is read-only;
- does not follow symlinks by default;
- writes relative paths only;
- never writes raw file content;
- emits `snapshot_started`, `observation`, `scan_error`, and
  `snapshot_sealed` events.

### Evidence hash tool

`relinium-evidence-hash` computes a full SHA-256 over one local regular file and
emits one NDJSON custody observation. It never modifies the artifact and never
uploads data.

Example:

```bash
cd apps/go
go run ./cmd/relinium-evidence-hash \
  --path /path/to/authorized/artifact.eml \
  --out /tmp/relinium-artifact-hash.ndjson
```

Output record fields:

- `record_type`
- `artifact_sha256`
- `size_bytes`
- `observed_at_utc`
- `relative_or_redacted_name`
- `tool_version`

### Detecteur de mouvement documentaire

The motion detector is not implemented yet. It will be a separate binary
because detecting who changed what requires more than filesystem events:
filesystem watcher data must be correlated with OS, NAS, cloud, GED, session,
IP, and audit logs when those sources are authorized and available.
