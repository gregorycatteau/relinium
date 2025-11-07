#!/usr/bin/env bash
# Bench léger standardisé pour POCs Relinium.
# Usage: ./scripts/bench_light.sh http://localhost:PORT/documents?page=1&size=20

set -euo pipefail

URL=${1:-"http://localhost:8000/documents?page=1&size=20"}
REQS=${REQS:-1000}
CONCURRENCY=${CONCURRENCY:-20}

echo "Bench léger sur ${URL} : ${REQS} requêtes, concurrence ${CONCURRENCY}..."
if command -v hey >/dev/null 2>&1; then
  hey -n "${REQS}" -c "${CONCURRENCY}" "${URL}"
else
  echo "⚠️ Outil 'hey' non installé. Merci de l'installer ou d'adapter ce script."
fi
