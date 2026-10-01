#!/usr/bin/env bash
# audit.sh — read-only repository audit for the polish-repo skill.
# Emits a deterministic snapshot the skill interprets. Makes NO changes.
#
# Usage: bash audit.sh [path]   (default: current directory)
set -uo pipefail

REPO="${1:-.}"
cd "$REPO" 2>/dev/null || { echo "ERROR: cannot cd into '$REPO'"; exit 1; }
REPO_ABS="$(pwd)"

# Thresholds
LARGE_KB=5120          # flag tracked files >= 5 MB
MANY_FILES=2000        # flag repos with a suspiciously high tracked-file count

section() { printf '\n## %s\n' "$1"; }
have()    { command -v "$1" >/dev/null 2>&1; }

printf '# Polish audit: %s\n' "$REPO_ABS"
printf '_generated %s (read-only)_\n' "$(date +%Y-%m-%d)"

# ---------------------------------------------------------------------------
# Git context
# ---------------------------------------------------------------------------
section "Git context"
IS_GIT=no
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  IS_GIT=yes
  BRANCH="$(git branch --show-current 2>/dev/null || echo '(detached)')"
  REMOTE="$(git remote get-url origin 2>/dev/null || echo '(none)')"
  DIRTY="$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
  USER_NAME="$(git config user.name 2>/dev/null || echo '?')"
  # Parse owner/org from a github remote (handles ssh + https)
  OWNER="$(printf '%s' "$REMOTE" | sed -E 's#(git@[^:]+:|https?://[^/]+/)##; s#/[^/]+$##; s#\.git$##')"
  echo "- git repo: yes"
  echo "- branch: ${BRANCH}"
  echo "- remote: ${REMOTE}"
  echo "- remote owner/org: ${OWNER:-?}"
  echo "- git user.name: ${USER_NAME}"
  echo "- uncommitted changes: ${DIRTY}"
  echo "- NOTE: confirm whether remote owner is the user; if not, treat as SHARED (additive-only, never push)."
else
  echo "- git repo: NO (offer 'git init'; README/LICENSE/structure still apply)"
fi

# ---------------------------------------------------------------------------
# Size & file counts
# ---------------------------------------------------------------------------
section "Size & counts"
if [ "$IS_GIT" = yes ]; then
  TRACKED="$(git ls-files | wc -l | tr -d ' ')"
  echo "- tracked files: ${TRACKED}"
  [ "${TRACKED:-0}" -ge "$MANY_FILES" ] && echo "  ⚠️  very high file count — likely committed cruft/artifacts"
  GITDIR_KB="$(du -sk .git 2>/dev/null | cut -f1)"
  echo "- .git directory: $(( ${GITDIR_KB:-0} / 1024 )) MB (history size)"
fi
WORKTREE_KB="$(du -sk --exclude=.git . 2>/dev/null | cut -f1)"
echo "- working tree (excl .git): $(( ${WORKTREE_KB:-0} / 1024 )) MB"

# ---------------------------------------------------------------------------
# Largest tracked files (working tree)
# ---------------------------------------------------------------------------
section "Largest tracked files (working tree)"
if [ "$IS_GIT" = yes ]; then
  git ls-files -z | xargs -0 du -k 2>/dev/null | sort -rn | head -15 \
    | awk -v t="$LARGE_KB" '{f=$1; $1=""; sub(/^ /,""); flag=(f>=t)?"  ⚠️":""; printf "- %6.1f MB  %s%s\n", f/1024, $0, flag}'
else
  echo "(not a git repo — skipping)"
fi

# ---------------------------------------------------------------------------
# Largest blobs in HISTORY (may differ from working tree; bloats clones)
# ---------------------------------------------------------------------------
section "Largest blobs in git history"
if [ "$IS_GIT" = yes ]; then
  git rev-list --objects --all 2>/dev/null \
    | git cat-file --batch-check='%(objecttype) %(objectsize) %(rest)' 2>/dev/null \
    | awk '/^blob/ {print $2"\t"$3}' | sort -rn | head -15 \
    | awk -F'\t' -v t="$((LARGE_KB*1024))" '{flag=($1>=t)?"  ⚠️":""; printf "- %6.1f MB  %s%s\n", $1/1048576, $2, flag}'
  echo "  (⚠️ entries persist in clones until history is rewritten — see history-bloat.md)"
fi

# ---------------------------------------------------------------------------
# Tracked cruft (should usually be gitignored)
# ---------------------------------------------------------------------------
section "Tracked cruft / artifacts"
if [ "$IS_GIT" = yes ]; then
  CRUFT='(^|/)(\.history|\.idea|\.vscode|__pycache__|node_modules|\.pytest_cache|\.mypy_cache|\.ruff_cache|\.ipynb_checkpoints|\.DS_Store|dist|build|runs|outputs?|wandb|mlruns)(/|$)'
  # Group by which cruft directory matched, with a file count each.
  git ls-files | grep -oE "$CRUFT" | tr -d '/' | sort | uniq -c | sort -rn | head -20 \
    | awk '{printf "- %5s files under: %s\n", $1, $2}'
  CNT="$(git ls-files | grep -cE "$CRUFT")"
  echo "- total tracked cruft files: ${CNT:-0}"
  [ "${CNT:-0}" = 0 ] && echo "  (none — good)"
fi

# ---------------------------------------------------------------------------
# Large-binary file TYPES present (datasets / weights / media)
# ---------------------------------------------------------------------------
section "Heavy file types present"
if [ "$IS_GIT" = yes ]; then
  git ls-files | grep -oiE '\.(pt|pth|ckpt|safetensors|h5|hdf5|onnx|pb|tflite|gguf|bin|zip|tar|gz|csv|parquet|npy|npz|mp4|mov|avi|psd|iso)$' \
    | tr 'A-Z' 'a-z' | sort | uniq -c | sort -rn | head -20 | awk '{printf "- %4s × %s\n", $1, $2}'
  echo "  (model weights & datasets usually belong out of git — see hygiene.md)"
fi

# ---------------------------------------------------------------------------
# Stack / archetype signals
# ---------------------------------------------------------------------------
section "Stack signals"
for f in pyproject.toml requirements.txt setup.py package.json Cargo.toml go.mod \
         Makefile CMakeLists.txt pom.xml build.gradle Gemfile composer.json Dockerfile; do
  [ -e "$f" ] && echo "- found: $f"
done
ML_HITS="$(git ls-files 2>/dev/null | grep -ciE '\.(ipynb|pt|ckpt|safetensors)$|(^|/)(datasets?|weights|checkpoints|runs)/' || true)"
[ "${ML_HITS:-0}" -gt 0 ] && echo "- ML/data-science signals: ${ML_HITS} (notebooks/weights/datasets)"

section "Existing project files"
for f in README.md README.rst README LICENSE LICENSE.md COPYING .gitignore \
         .gitattributes .editorconfig CONTRIBUTING.md SECURITY.md CHANGELOG.md \
         .github/workflows .gitlab-ci.yml .pre-commit-config.yaml .env.example; do
  if [ -e "$f" ]; then echo "- present: $f"; else echo "- MISSING: $f"; fi
done

# ---------------------------------------------------------------------------
# Secret scan (working tree only; history scan is a separate, heavier step)
# ---------------------------------------------------------------------------
section "Secret scan (working tree)"
SECRET_RE='sk-[A-Za-z0-9]{20,}|sk-ant-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{30,}|AIza[0-9A-Za-z_-]{30,}|xox[baprs]-[0-9A-Za-z-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----'
PLACEHOLDER='your_.*_here|xxxx+|<[^>]+>|changeme|placeholder|example|EXAMPLE'
HITS="$(grep -rInE "$SECRET_RE" . \
        --exclude-dir={.git,node_modules,.venv,venv,__pycache__} \
        2>/dev/null | grep -vEi "$PLACEHOLDER" | grep -vE '\.(env\.(example|sample|template))' | head -20)"
if [ -n "$HITS" ]; then
  echo "⚠️  POSSIBLE SECRETS (verify — may be false positives):"
  echo "$HITS" | sed 's/^/    /'
  echo "    → if real and ever committed/pushed: ROTATE the credential (see secrets.md)"
else
  echo "- no high-signal secret patterns in working tree (still review .env / config by hand)"
fi
# Real .env files tracked?
if [ "$IS_GIT" = yes ]; then
  ENVS="$(git ls-files | grep -iE '(^|/)\.env($|\.)' | grep -viE '\.(example|sample|template)$' || true)"
  [ -n "$ENVS" ] && { echo "⚠️  tracked .env file(s):"; echo "$ENVS" | sed 's/^/    /'; }
fi

# ---------------------------------------------------------------------------
# Junk / awkward names
# ---------------------------------------------------------------------------
section "Junk / awkward names"
if [ "$IS_GIT" = yes ]; then
  git ls-files | grep -nE '(^|/)(asd|tmp|temp|scratch|untitled|test|copy of|[0-9]+)\.[a-z0-9]+$|~$|\.bak$| ' \
    | head -15 | sed 's/^/- /'
  SP="$(git ls-files | grep -c ' ' || true)"
  [ "${SP:-0}" -gt 0 ] && echo "- paths containing spaces: ${SP} (brittle in scripts/CI)"
fi

section "Available scanners"
for t in gitleaks trufflehog git-filter-repo ruff; do
  if have "$t"; then echo "- $t: available"; else echo "- $t: not installed (skill will note manual install)"; fi
done

printf '\n_End of audit. The skill interprets these signals; it changes nothing on its own._\n'
