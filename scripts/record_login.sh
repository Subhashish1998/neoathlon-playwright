#!/usr/bin/env bash
# Log in manually in the opened browser, then close it. Session is saved to auth/state.json
# BASE_URL and LOGIN_PATH are read from .env.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
[ -f "$ROOT/.env" ] || { echo ".env not found. Copy .env.example to .env and fill it in." >&2; exit 1; }
get_env() { grep -E "^\s*$1\s*=" "$ROOT/.env" | head -1 | cut -d= -f2- | tr -d '\r' | xargs || true; }
BASE_URL="$(get_env BASE_URL | sed 's:/*$::')"
[ -n "$BASE_URL" ] || { echo "BASE_URL missing in .env" >&2; exit 1; }
LOGIN_PATH="${1:-$(get_env LOGIN_PATH)}"; LOGIN_PATH="${LOGIN_PATH:-/auth}"
mkdir -p "$ROOT/auth"
playwright codegen --save-storage "$ROOT/auth/state.json" "${BASE_URL}${LOGIN_PATH}"
