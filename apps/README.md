# Relinium Cockpit Apps

Minimal read-only application layer for the Relinium SSOT.

The SSOT filesystem under `ssot-root/` remains the source of truth. The Django
backend reads it and exposes JSON endpoints. The Nuxt frontend renders a local
cockpit for operational inspection.

## Backend

Requirements:

- Python 3
- Django 4.2+

Run:

```bash
cd apps/backend
python3 manage.py runserver 127.0.0.1:8000
```

Endpoints:

- `GET /api/health`
- `GET /api/ssot/summary`
- `GET /api/events/streams`
- `GET /api/events`
- `GET /api/validation/status`
- `GET /api/validation/known-findings`

The validation endpoint uses:

```bash
python3 ssot-root/core/scripts/validate_documents.py
python3 ssot-root/core/scripts/validate_documents.py --baseline ssot-root/core/validation/known_findings.json
```

internally by importing the validator module and applying the same validation
logic in process.

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
- Frontend: `http://localhost:3000`

The frontend reads only the Django API URL from `NUXT_PUBLIC_API_BASE`.
