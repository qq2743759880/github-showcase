#!/usr/bin/env bash
# record.sh -- record a terminal demo for any project directory and render a
# GIF from the resulting asciinema cast.

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./record.sh [options] DIR [CMD ...]
  ./record.sh --help

Examples:
  ./record.sh .
  ./record.sh ~/src/my-app npm test
  ./record.sh ../other-repo --env NODE_ENV=production make demo
  ./record.sh . --title "release demo" --basename release-demo leather run --pretty demo.agent.md

Options:
  -h, --help                  Show this help text.
  --print-config              Print the resolved recording configuration and exit.
  --env KEY=VALUE             Export a variable inside the recorded shell. Repeatable.
  --env-file PATH             Load env defaults from PATH before recording.
  --no-env-file               Skip automatic .env loading.
  --title TEXT                Override the asciinema title.
  --demo-name TEXT            Override the summary label shown before recording.
  --label TEXT                Override the scrubbed working-directory label.
  --basename NAME             Override the output file basename.
  --out-dir DIR               Write cast and gif outputs to DIR.
  --prompt-label TEXT         Prompt prefix shown in the recorded shell.
  --prompt-color HEX          Prompt color, e.g. #af5fff.
  --font-size PT              agg font size. Default: 22
  --cols N                    Terminal columns. Default: 160
  --rows N                    Terminal rows. Default: 30
  --select RANGE              agg --select range. Default: 0.2..
  --idle-time-limit SEC       asciinema / agg idle time limit. Default: 1.5
  --last-frame-duration SEC   Pause at the end of the gif loop. Default: 3
  --line-delay SEC            Add delay after each rendered line chunk. Default: 0
  --line-chunk N              Lines per pacing chunk. Default: 1
  --source-zshrc              Source the operator's .zshrc before applying recorder overrides.

Environment:
  RECORD_ENV_FILE             Default env file path. Default: <project-root>/.env
  RECORD_OUT_DIR              Output directory. Default: <project-root>/recordings
  RECORD_OUT_BASENAME         Output basename without extension. Default: timestamp
  RECORD_TITLE                Asciinema title. Default: <project-name> demo
  RECORD_DEMO_NAME            Banner label. Default: demo
  RECORD_WORKDIR_LABEL        Scrubbed path label shown in output
  RECORD_PROMPT_LABEL         Prompt label. Default: <project-name>
  RECORD_PROMPT_COLOR         Prompt color. Default: #af5fff
  RECORD_FONT_SIZE            agg font size
  RECORD_COLS                 Terminal columns
  RECORD_ROWS                 Terminal rows
  RECORD_SELECT               agg --select range
  RECORD_IDLE_LIMIT           asciinema / agg idle time limit
  RECORD_LAST_FRAME_DURATION  End-of-loop gif pause
  RECORD_LINE_DELAY           Delay inserted after each line chunk
  RECORD_LINE_CHUNK           Lines per pacing chunk
  RECORD_SOURCE_ZSHRC         1 to source the user's .zshrc first
  RECORD_AGG_THEME            Custom agg theme triplets
  RECORD_TEXT_FONTS           Comma-separated font family list for agg

Outputs:
  <out-dir>/<basename>.cast
  <out-dir>/<basename>.gif
EOF
}

die() {
  echo "error: $*" >&2
  exit 1
}

require_tool() {
  command -v "$1" >/dev/null 2>&1 || MISSING_TOOLS+=("$1")
}

TARGET_DIR=""
TARGET_ENV=()
TARGET_CMD_ARGS=()
MISSING_TOOLS=()
CALLER_DIR="$(pwd)"
PRINT_CONFIG=0
SKIP_ENV_FILE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help|help)
      usage
      exit 0
      ;;
    --print-config)
      PRINT_CONFIG=1
      shift
      ;;
    --env)
      [[ $# -ge 2 ]] || die "--env requires KEY=VALUE"
      [[ "$2" =~ ^[A-Za-z_][A-Za-z0-9_]*= ]] || die "--env argument must be KEY=VALUE, got: $2"
      TARGET_ENV+=("$2")
      shift 2
      ;;
    --env-file)
      [[ $# -ge 2 ]] || die "--env-file requires a path"
      export RECORD_ENV_FILE="$2"
      shift 2
      ;;
    --no-env-file)
      SKIP_ENV_FILE=1
      shift
      ;;
    --title)
      [[ $# -ge 2 ]] || die "--title requires a value"
      export RECORD_TITLE="$2"
      shift 2
      ;;
    --demo-name)
      [[ $# -ge 2 ]] || die "--demo-name requires a value"
      export RECORD_DEMO_NAME="$2"
      shift 2
      ;;
    --label)
      [[ $# -ge 2 ]] || die "--label requires a value"
      export RECORD_WORKDIR_LABEL="$2"
      shift 2
      ;;
    --basename)
      [[ $# -ge 2 ]] || die "--basename requires a value"
      export RECORD_OUT_BASENAME="$2"
      shift 2
      ;;
    --out-dir)
      [[ $# -ge 2 ]] || die "--out-dir requires a path"
      export RECORD_OUT_DIR="$2"
      shift 2
      ;;
    --prompt-label)
      [[ $# -ge 2 ]] || die "--prompt-label requires a value"
      export RECORD_PROMPT_LABEL="$2"
      shift 2
      ;;
    --prompt-color)
      [[ $# -ge 2 ]] || die "--prompt-color requires a value"
      export RECORD_PROMPT_COLOR="$2"
      shift 2
      ;;
    --font-size)
      [[ $# -ge 2 ]] || die "--font-size requires a value"
      export RECORD_FONT_SIZE="$2"
      shift 2
      ;;
    --cols)
      [[ $# -ge 2 ]] || die "--cols requires a value"
      export RECORD_COLS="$2"
      shift 2
      ;;
    --rows)
      [[ $# -ge 2 ]] || die "--rows requires a value"
      export RECORD_ROWS="$2"
      shift 2
      ;;
    --select)
      [[ $# -ge 2 ]] || die "--select requires a value"
      export RECORD_SELECT="$2"
      shift 2
      ;;
    --idle-time-limit)
      [[ $# -ge 2 ]] || die "--idle-time-limit requires a value"
      export RECORD_IDLE_LIMIT="$2"
      shift 2
      ;;
    --last-frame-duration)
      [[ $# -ge 2 ]] || die "--last-frame-duration requires a value"
      export RECORD_LAST_FRAME_DURATION="$2"
      shift 2
      ;;
    --line-delay)
      [[ $# -ge 2 ]] || die "--line-delay requires a value"
      export RECORD_LINE_DELAY="$2"
      shift 2
      ;;
    --line-chunk)
      [[ $# -ge 2 ]] || die "--line-chunk requires a value"
      export RECORD_LINE_CHUNK="$2"
      shift 2
      ;;
    --source-zshrc)
      export RECORD_SOURCE_ZSHRC=1
      shift
      ;;
    --)
      shift
      TARGET_CMD_ARGS+=("$@")
      break
      ;;
    -*)
      die "unknown option: $1"
      ;;
    *)
      if [[ -z "${TARGET_DIR}" ]]; then
        TARGET_DIR="$1"
      else
        TARGET_CMD_ARGS+=("$1")
      fi
      shift
      ;;
  esac
done

[[ -n "${TARGET_DIR}" ]] || {
  usage >&2
  exit 2
}

# --print-config is a pure resolver — it must work on a box (or CI runner)
# that has neither recorder tool installed, so the check moves below it.
if (( PRINT_CONFIG == 0 )); then
  require_tool asciinema
  require_tool agg
  if (( ${#MISSING_TOOLS[@]} > 0 )); then
    die "missing tools: ${MISSING_TOOLS[*]}"
  fi
fi

if [[ "${TARGET_DIR}" == /* ]]; then
  WORK_DIR="${TARGET_DIR}"
else
  WORK_DIR="${CALLER_DIR}/${TARGET_DIR}"
fi
[[ -d "${WORK_DIR}" ]] || die "directory does not exist: ${WORK_DIR}"

WORK_DIR="$(cd "${WORK_DIR}" && pwd)"
PROJECT_ROOT="$(git -C "${WORK_DIR}" rev-parse --show-toplevel 2>/dev/null || printf '%s\n' "${WORK_DIR}")"
PROJECT_NAME="$(basename -- "${PROJECT_ROOT}")"
PROJECT_LABEL="${PROJECT_NAME}"
WDIR_LABEL="$(realpath --relative-to="${PROJECT_ROOT}" "${WORK_DIR}" 2>/dev/null || basename -- "${WORK_DIR}")"
if [[ "${WDIR_LABEL}" == "." ]]; then
  WDIR_LABEL="${PROJECT_LABEL}"
else
  WDIR_LABEL="${PROJECT_LABEL}/${WDIR_LABEL}"
fi
WDIR_LABEL="${RECORD_WORKDIR_LABEL:-${WDIR_LABEL}}"

if (( SKIP_ENV_FILE == 1 )); then
  LOADED_ENV_FILE=""
elif [[ "${RECORD_ENV_FILE+x}" == "x" ]]; then
  LOADED_ENV_FILE="${RECORD_ENV_FILE}"
else
  LOADED_ENV_FILE="${PROJECT_ROOT}/.env"
fi
if [[ -n "${LOADED_ENV_FILE}" && -f "${LOADED_ENV_FILE}" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "${LOADED_ENV_FILE}"
  set +a
fi

OUT_DIR="${RECORD_OUT_DIR:-${PROJECT_ROOT}/recordings}"
mkdir -p "${OUT_DIR}"

TS="$(date +%Y%m%d-%H%M%S)"
OUT_BASENAME="${RECORD_OUT_BASENAME:-${TS}}"
CAST="${OUT_DIR}/${OUT_BASENAME}.cast"
GIF="${OUT_DIR}/${OUT_BASENAME}.gif"

FONT_SIZE="${RECORD_FONT_SIZE:-22}"
COLS="${RECORD_COLS:-160}"
ROWS="${RECORD_ROWS:-30}"
RENDER_SELECT="${RECORD_SELECT:-0.2..}"
IDLE_LIMIT="${RECORD_IDLE_LIMIT:-1.5}"
LAST_FRAME_DURATION="${RECORD_LAST_FRAME_DURATION:-3}"
LINE_DELAY="${RECORD_LINE_DELAY:-0}"
LINE_CHUNK="${RECORD_LINE_CHUNK:-1}"
SOURCE_ZSHRC="${RECORD_SOURCE_ZSHRC:-0}"
PROMPT_LABEL="${RECORD_PROMPT_LABEL:-${PROJECT_NAME}}"
PROMPT_COLOR="${RECORD_PROMPT_COLOR:-#af5fff}"
DEMO_NAME="${RECORD_DEMO_NAME:-demo}"
RECORD_TITLE="${RECORD_TITLE:-${PROJECT_NAME} demo}"
TARGET_CMD="${TARGET_CMD_ARGS[*]}"
PRELOAD_CMD="${TARGET_CMD}"

if (( PRINT_CONFIG == 1 )); then
  cat <<EOF
WORK_DIR=${WORK_DIR}
PROJECT_ROOT=${PROJECT_ROOT}
OUT_DIR=${OUT_DIR}
CAST=${CAST}
GIF=${GIF}
TITLE=${RECORD_TITLE}
DEMO_NAME=${DEMO_NAME}
WORKDIR_LABEL=${WDIR_LABEL}
PROMPT_LABEL=${PROMPT_LABEL}
PROMPT_COLOR=${PROMPT_COLOR}
ENV_FILE=${LOADED_ENV_FILE}
COLS=${COLS}
ROWS=${ROWS}
FONT_SIZE=${FONT_SIZE}
SELECT=${RENDER_SELECT}
IDLE_LIMIT=${IDLE_LIMIT}
LAST_FRAME_DURATION=${LAST_FRAME_DURATION}
LINE_DELAY=${LINE_DELAY}
LINE_CHUNK=${LINE_CHUNK}
SOURCE_ZSHRC=${SOURCE_ZSHRC}
COMMAND=${TARGET_CMD}
EOF
  exit 0
fi

cat <<EOF

Recording ${DEMO_NAME}: ${WDIR_LABEL}
Output:         ${GIF} (also: ${CAST})
Geometry:       ${COLS}x${ROWS}  font=${FONT_SIZE}pt
Render select:  ${RENDER_SELECT}
Loop pause:     ${LAST_FRAME_DURATION}s
Line pacing:    ${LINE_DELAY}s after every ${LINE_CHUNK} line(s)
Prompt:         ${PROMPT_LABEL} $
EOF

if [[ -n "${TARGET_CMD}" ]]; then
cat <<EOF

When the recorded shell opens:
  1. Press Enter to run: ${PRELOAD_CMD}
  2. Press Ctrl-D when finished.

Starting in 2s...
EOF
else
cat <<EOF

When the recorded shell opens:
  1. Type your commands manually.
  2. Press Ctrl-D when finished.

Starting in 2s...
EOF
fi
sleep 2

ASCIINEMA_PROMPT="%F{${PROMPT_COLOR}}${PROMPT_LABEL} $%f "

TMPRC_DIR="$(mktemp -d -t record-zdotdir.XXXXXX)"
trap 'rm -rf "${TMPRC_DIR}"' EXIT
REAL_ZDOTDIR="${ZDOTDIR:-$HOME}"
cat > "${TMPRC_DIR}/.zshrc" <<RC
if [[ "${SOURCE_ZSHRC}" == "1" && -f "${REAL_ZDOTDIR}/.zshrc" ]]; then
  source "${REAL_ZDOTDIR}/.zshrc"
fi
cd "${WORK_DIR}"
unsetopt prompt_cr prompt_sp 2>/dev/null
PROMPT='${ASCIINEMA_PROMPT}'
RPROMPT=''
unset RPS1 RPS2 2>/dev/null
clear
RC

if (( ${#TARGET_ENV[@]} > 0 )); then
  echo '# --env injected variables' >> "${TMPRC_DIR}/.zshrc"
  for kv in "${TARGET_ENV[@]}"; do
    KEY="${kv%%=*}"
    VAL="${kv#*=}"
    printf 'export %s=%q\n' "${KEY}" "${VAL}" >> "${TMPRC_DIR}/.zshrc"
  done
  echo >> "${TMPRC_DIR}/.zshrc"
fi

if [[ -n "${TARGET_CMD}" ]]; then
  {
    echo '__record_preload() {'
    printf '  BUFFER=%q\n' "${PRELOAD_CMD}"
    echo '  CURSOR=${#BUFFER}'
    echo '  zle -D zle-line-init'
    echo '}'
    echo 'zle -N zle-line-init __record_preload'
  } >> "${TMPRC_DIR}/.zshrc"
fi

ZDOTDIR="${TMPRC_DIR}" \
  TERM="${TERM:-xterm-256color}" \
  asciinema rec \
    --overwrite \
    --output-format asciicast-v2 \
    --idle-time-limit "${IDLE_LIMIT}" \
    --window-size "${COLS}x${ROWS}" \
    --title "${RECORD_TITLE}" \
    --command "zsh -i" \
    "${CAST}"

echo
echo "Scrubbing paths in: ${CAST}"
sed -i "s|${WORK_DIR}|${WDIR_LABEL}|g" "${CAST}"
sed -i "s|${PROJECT_ROOT}|${PROJECT_LABEL}|g" "${CAST}"

if [[ -n "${LINE_DELAY}" && "${LINE_DELAY}" != "0" && "${LINE_DELAY}" != "0.0" ]]; then
  echo "Pacing cast output: +${LINE_DELAY}s after every ${LINE_CHUNK} rendered line(s)"
  tmp_cast="${CAST}.paced"
  awk -v delay="${LINE_DELAY}" -v chunk="${LINE_CHUNK}" '
    function emit_output(t, payload) {
      printf("[%.6f, \"o\", \"%s\"]\n", t, payload)
    }

    function pace_output_event(ts, payload,    remaining, current, pos_r, pos_n, pos, len, rendered, t) {
      remaining = payload
      current = ""
      rendered = 0
      t = ts + extra
      while (remaining != "") {
        pos_r = index(remaining, "\\r\\n")
        pos_n = index(remaining, "\\n")
        if (pos_r > 0 && (pos_n == 0 || pos_r < pos_n)) {
          pos = pos_r
          len = 4
        } else if (pos_n > 0) {
          pos = pos_n
          len = 2
        } else {
          current = current remaining
          remaining = ""
          break
        }
        current = current substr(remaining, 1, pos + len - 1)
        remaining = substr(remaining, pos + len)
        rendered++
        if (rendered % chunk == 0) {
          emit_output(t, current)
          current = ""
          extra += delay
          t = ts + extra
        }
      }
      if (current != "") {
        emit_output(t, current)
      }
    }

    BEGIN {
      delay += 0
      chunk = int(chunk)
      if (chunk < 1) {
        chunk = 1
      }
      extra = 0
    }
    NR == 1 {
      print
      next
    }
    /^\[[0-9.]+, "o", "/ && /"\]$/ {
      ts = $0
      sub(/^\[/, "", ts)
      sub(/,.*/, "", ts)
      payload = $0
      sub(/^\[[0-9.]+, "o", "/, "", payload)
      sub(/"\]$/, "", payload)
      pace_output_event(ts + 0, payload)
      next
    }
    /^\[[0-9]/ {
      ts = $0
      sub(/^\[/, "", ts)
      sub(/,.*/, "", ts)
      rest = $0
      sub(/^\[[0-9.]+/, "", rest)
      printf("[%.6f%s\n", ts + extra, rest)
      next
    }
    {
      print
    }
  ' "${CAST}" > "${tmp_cast}"
  mv "${tmp_cast}" "${CAST}"
fi

tmp_cast="${CAST}.trimmed"
awk '
  function payload_of(line, payload) {
    payload = line
    sub(/^\[[0-9.]+, "o", "/, "", payload)
    sub(/"\]$/, "", payload)
    return payload
  }

  function tail_noise(line, payload, stripped) {
    if (line !~ /^\[[0-9.]+, "o", "/ || line !~ /"\]$/) {
      return 0
    }
    payload = payload_of(line)
    if (payload ~ /\$[^[:alnum:]_]?/) {
      stripped = payload
      gsub(/\\u001b\[[0-9;?]*[A-Za-z]|\\u001b./, "", stripped)
      if (stripped ~ / \$ ?$/ || stripped ~ /^[[:space:]]*[$][[:space:]]*$/) {
        return 1
      }
    }
    stripped = payload
    gsub(/\\r|\\n|\\t| |\\u001b\[[0-9;?]*[A-Za-z]|\\u001b./, "", stripped)
    return stripped == ""
  }

  function tail_ignorable(line) {
    if (line ~ /^\[[0-9.]+, "x", "/) {
      return 1
    }
    return tail_noise(line)
  }

  {
    lines[NR] = $0
  }

  END {
    n = NR
    while (n > 1 && tail_ignorable(lines[n])) {
      n--
    }
    for (i = 1; i <= n; i++) {
      print lines[i]
    }
  }
' "${CAST}" > "${tmp_cast}"
mv "${tmp_cast}" "${CAST}"

echo "Rendering GIF: ${GIF}"
AGG_FONT_SIZE="${AGG_FONT_SIZE:-${FONT_SIZE}}"
AGG_THEME="${RECORD_AGG_THEME:-232323,e8e6e3,26242c,ff6b7a,10a889,d9b86c,35b8f0,8b5cf6,38d0c8,e8e6e3,6e6a76,ff8490,22c7a5,f0d58a,54c7ff,a78bfa,6be8df,ffffff}"
AGG_TEXT_FONTS="${RECORD_TEXT_FONTS:-Monaco,Consolas,Menlo,Bitstream Vera Sans Mono,DejaVu Sans Mono,Liberation Mono}"
agg \
  --text-font-family "${AGG_TEXT_FONTS}" \
  --font-size "${AGG_FONT_SIZE}" \
  --theme "${AGG_THEME}" \
  --speed 1 \
  --idle-time-limit "${IDLE_LIMIT}" \
  --last-frame-duration "${LAST_FRAME_DURATION}" \
  --select "${RENDER_SELECT}" \
  "${CAST}" "${GIF}"

echo
echo "Done."
ls -lh "${CAST}" "${GIF}"
