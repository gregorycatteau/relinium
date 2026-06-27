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

Security limits:

- no automatic click or remote content fetch;
- no binary-heavy storage in PostgreSQL for this milestone;
- no cleartext secrets;
- no automatic submission to Signal Spam, 33700, Phishing Initiative, 17Cyber,
  THESEE/PHAROS, police/gendarmerie or banks;
- human validation is mandatory before any external transmission.

### Security limits

- No SQLite fallback.
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
