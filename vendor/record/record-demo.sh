#!/usr/bin/env bash
# record-demo.sh -- Leather-flavoured wrapper around record.sh.

set -euo pipefail

SCRIPT_PATH="${BASH_SOURCE[0]:-$0}"
SCRIPT_DIR="$(cd -- "$(dirname -- "${SCRIPT_PATH}")" &> /dev/null && pwd)"
GP_SCRIPT="${SCRIPT_DIR}/record.sh"

if [[ ! -x "${GP_SCRIPT}" ]]; then
  echo "error: missing executable helper: ${GP_SCRIPT}" >&2
  exit 1
fi

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" || "${1:-}" == "help" ]]; then
  cat <<'EOF'
Usage:
  ./record-demo.sh DIR [CMD ...]
  ./record-demo.sh --help

Leather-focused wrapper around ./record.sh.
It preserves the older LEATHER_RECORD_* environment variables and defaults
the prompt + render theme to the Leather palette.
EOF
  exit 0
fi

# Preserve the older Leather-specific env knobs by translating them to the
# general-purpose recorder's settings only when the generic name is unset.
if [[ "${RECORD_ENV_FILE+x}" == "x" && "${LEATHER_RECORD_ENV_FILE+x}" != "x" ]]; then
  export RECORD_ENV_FILE="${LEATHER_RECORD_ENV_FILE}"
fi
if [[ "${RECORD_FONT_SIZE+x}" == "x" && "${LEATHER_RECORD_FONT_SIZE+x}" != "x" ]]; then
  export RECORD_FONT_SIZE="${LEATHER_RECORD_FONT_SIZE}"
fi
if [[ "${RECORD_COLS+x}" == "x" && "${LEATHER_RECORD_COLS+x}" != "x" ]]; then
  export RECORD_COLS="${LEATHER_RECORD_COLS}"
fi
if [[ "${RECORD_ROWS+x}" == "x" && "${LEATHER_RECORD_ROWS+x}" != "x" ]]; then
  export RECORD_ROWS="${LEATHER_RECORD_ROWS}"
fi
if [[ "${RECORD_SELECT+x}" == "x" && "${LEATHER_RECORD_SELECT+x}" != "x" ]]; then
  export RECORD_SELECT="${LEATHER_RECORD_SELECT}"
fi
if [[ "${RECORD_IDLE_LIMIT+x}" == "x" && "${LEATHER_RECORD_IDLE_LIMIT+x}" != "x" ]]; then
  export RECORD_IDLE_LIMIT="${LEATHER_RECORD_IDLE_LIMIT}"
fi
if [[ "${RECORD_LAST_FRAME_DURATION+x}" == "x" && "${LEATHER_RECORD_LAST_FRAME_DURATION+x}" != "x" ]]; then
  export RECORD_LAST_FRAME_DURATION="${LEATHER_RECORD_LAST_FRAME_DURATION}"
fi
if [[ "${RECORD_LINE_DELAY+x}" == "x" && "${LEATHER_RECORD_LINE_DELAY+x}" != "x" ]]; then
  export RECORD_LINE_DELAY="${LEATHER_RECORD_LINE_DELAY}"
fi
if [[ "${RECORD_LINE_CHUNK+x}" == "x" && "${LEATHER_RECORD_LINE_CHUNK+x}" != "x" ]]; then
  export RECORD_LINE_CHUNK="${LEATHER_RECORD_LINE_CHUNK}"
fi
if [[ "${RECORD_SOURCE_ZSHRC+x}" == "x" && "${LEATHER_RECORD_SOURCE_ZSHRC+x}" != "x" ]]; then
  export RECORD_SOURCE_ZSHRC="${LEATHER_RECORD_SOURCE_ZSHRC}"
fi

export RECORD_PROMPT_LABEL="${RECORD_PROMPT_LABEL:-leather}"
export RECORD_PROMPT_COLOR="${RECORD_PROMPT_COLOR:-#af5fff}"
export RECORD_AGG_THEME="${RECORD_AGG_THEME:-232323,e8e6e3,26242c,ff6b7a,10a889,d9b86c,35b8f0,8b5cf6,38d0c8,e8e6e3,6e6a76,ff8490,22c7a5,f0d58a,54c7ff,a78bfa,6be8df,ffffff}"
export RECORD_TEXT_FONTS="${RECORD_TEXT_FONTS:-Monaco,Consolas,Menlo,Bitstream Vera Sans Mono,DejaVu Sans Mono,Liberation Mono}"

exec "${GP_SCRIPT}" "$@"
