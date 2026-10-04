#!/usr/bin/env bash
# Record a new test with codegen. BASE_URL is read from .env.
# Usage: ./scripts/record.sh <test_name> [url_path]
#   ./scripts/record.sh signup /signup   ->  tests/recorded/test_signup.py
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NAME="${1:?test name required}"; URL_PATH="${2:-/}"
[ -f "$ROOT/.env" ] || { echo ".env not found. Copy .env.example to .env and fill it in." >&2; exit 1; }
BASE_URL="$(grep -E '^\s*BASE_URL\s*=' "$ROOT/.env" | head -1 | cut -d= -f2- | tr -d '\r' | xargs | sed 's:/*$::')"
[ -n "$BASE_URL" ] || { echo "BASE_URL missing in .env" >&2; exit 1; }
OUT="$ROOT/tests/recorded/test_${NAME}.py"
ARGS=(codegen --target python-pytest --viewport-size "1440,900" -o "$OUT")
[ -f "$ROOT/auth/state.json" ] && ARGS+=(--load-storage "$ROOT/auth/state.json")
echo "Recording to $OUT"
playwright "${ARGS[@]}" "${BASE_URL}${URL_PATH}"
python "$ROOT/scripts/clean_recording.py" "$OUT"
