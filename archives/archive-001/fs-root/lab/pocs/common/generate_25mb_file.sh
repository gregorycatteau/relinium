#!/usr/bin/env bash
# Génère un fichier binaire de ~25 Mo pour tests d'upload.

set -euo pipefail

TARGET_FILE=${1:-"upload_25mb.bin"}

echo "Génération de $TARGET_FILE (~25 MiB)..."
head -c 26214400 /dev/urandom > "$TARGET_FILE"
echo "OK."
