# Secrets & sensitive data

The single most important thing to get right: **a secret committed to git
history is compromised the moment it's pushed, and deleting the file later does
not un-compromise it.** Your job is to (1) stop further exposure, (2) tell the
user to rotate, (3) optionally help scrub history — in that order.

## Detect

Scan the working tree first, then history. Distinguish *real* secrets from
*placeholders*.

High-signal patterns:

| Kind | Regex (approx) |
|---|---|
| OpenAI/Anthropic-style key | `sk-[A-Za-z0-9]{20,}`, `sk-ant-[A-Za-z0-9-]{20,}` |
| AWS access key | `AKIA[0-9A-Z]{16}` |
| GitHub token | `gh[pousr]_[A-Za-z0-9]{36,}` |
| Google API key | `AIza[0-9A-Za-z_\-]{35}` |
| Slack token | `xox[baprs]-[0-9A-Za-z-]{10,}` |
| Stripe | `sk_live_[0-9A-Za-z]{24,}` |
| Private key | `-----BEGIN (RSA |OPENSSH |EC |DSA |)PRIVATE KEY-----` |
| Generic assignment | `(?i)(api[_-]?key|secret|token|password|passwd)\s*[:=]\s*['"][^'"]{8,}` |

Sensitive files (whether or not they match a regex): `.env`, `.env.*` (except
`.env.example`/`.env.sample`/`.env.template`), `credentials.json`,
`service-account*.json`, `*.pem`, `*.key`, `*.pfx`, `*.keystore`, `id_rsa`,
`.npmrc`/`.pypirc` with tokens, `terraform.tfstate`.

```bash
# Working tree
grep -rInE '<patterns above>' "$repo" --exclude-dir={.git,node_modules,.venv} \
  --include='*.*' | grep -vE '\.env\.(example|sample|template)|your_.*_here|xxxx|<.*>|placeholder'

# History (every revision of every file)
git -C "$repo" log -p --all -S 'sk-' -- . | head   # repeat per token prefix
# Or, if available, the right tool for the job:
gitleaks detect --source "$repo" --no-banner        # tree + history
trufflehog git file://"$repo"
```

**Placeholder filter:** ignore values that are obviously fake — `your_*_here`,
`changeme`, `xxxx`, `<...>`, `example`, all-zeros, or living in a file named
`*.example`/`*.sample`/`*.template`/`README`. When in doubt, ask the user "is
this real?" rather than touching it.

## Remediate

### Case A — secret in the working tree only (never committed, or only staged)
SAFE/CAUTION:
```bash
git rm --cached path/to/secretfile        # untrack, keep the local copy
echo 'path/to/secretfile' >> .gitignore
```
If it's an inline literal in source, replace it with an env-var read and move the
value into a local (gitignored) `.env`.

### Case B — secret already committed to history
1. **Tell the user, prominently:** "`<file/key>` is in your git history. If this
   repo was ever pushed or shared, treat the credential as **leaked** — rotate
   it now (revoke + reissue at the provider). Removing it from history does not
   make the old value safe."
2. Untrack + ignore the current copy (Case A steps) so it stops re-leaking.
3. Put the history-scrub commands in the **follow-up checklist** (DESTRUCTIVE —
   never auto-run): see `history-bloat.md` — the same `git filter-repo` flow,
   targeting the secret path/blob.

## Generate a safe `.env.example`

Derive the *names* of required env vars from the code, never the values:

```bash
grep -rhoE 'os\.(getenv|environ(\.get)?)\(["'"'"']([A-Z0-9_]+)' "$repo" \
  | grep -oE '[A-Z0-9_]+$' | sort -u          # Python
grep -rhoE 'process\.env\.([A-Z0-9_]+)' "$repo" | sed 's/process.env.//' | sort -u  # Node
```
Emit each as `VAR_NAME=` with a `# what it is` comment. Mark which are required.
Add `.env` to `.gitignore` and commit `.env.example` (SAFE).

## Prevent recurrence

Offer the `gitleaks` workflow from `assets/ci/secret-scan.yml`, and optionally a
pre-commit hook. Mention enabling GitHub **Secret Scanning + Push Protection** in
repo settings (a one-click manual step → put it in the checklist).
