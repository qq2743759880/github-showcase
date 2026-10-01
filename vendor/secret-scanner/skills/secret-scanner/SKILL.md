---
name: secret-scanner
description: >-
  Scan a codebase for hardcoded secrets — API keys, tokens, private keys and
  passwords — using a custom regex + Shannon-entropy engine. Use when the user
  asks to "find secrets", "check for leaked credentials", "scan for API keys",
  do a pre-commit secret check, or audit a repo before making it public.
license: MIT
---

# Secret Scanner

A dependency-free engine that finds committed credentials by combining
**high-signal vendor regex rules** (AWS, GitHub, GCP, Stripe, OpenAI,
Anthropic, Hugging Face, Replicate, Groq, Cohere, DigitalOcean, Slack, …)
with **Shannon-entropy gating** to catch generic secrets while keeping
false positives low.

## When to use this skill

- "Are there any secrets / API keys committed in this repo?"
- "Scan this folder before I open-source it."
- Pre-commit / pre-push credential checks.
- Investigating a suspected leak.

## How to run it

The engine has **no third-party dependencies** — just Python 3.9+.

```bash
# Human-readable report (default)
python skills/secret-scanner/engine.py .

# Machine-readable JSON (pipe into other tooling)
python skills/secret-scanner/engine.py . --json

# Tune entropy sensitivity (lower = more findings)
python skills/secret-scanner/engine.py src/ --min-entropy 3.0

# Include test directories (skipped by default)
python skills/secret-scanner/engine.py . --include-tests
```

**Exit codes:** `0` clean · `1` findings present · `2` usage error.
This makes it drop-in for CI: a non-zero exit fails the build.

## How to interpret results

Each finding reports `severity`, `rule_id`, `path:line:column`, a **redacted**
preview of the value (never the full secret), and the measured entropy.

Severity guide:
- **critical** — live credential material (private keys, cloud secret keys,
  provider tokens). Rotate immediately.
- **high** — access key IDs, third-party API keys.
- **medium** — generic `password=`/`secret=` assignments.
- **low** — JWTs and other context-dependent values; verify before acting.

## Recommended workflow for Claude

1. Run the scanner with `--json` and parse the findings.
2. For each finding, open the file at the reported line to confirm it is a
   real secret and not a placeholder/test fixture.
3. Report confirmed leaks grouped by severity, and advise the user to
   **rotate** the credential (committing a fix does not un-leak git history).
4. If the secret is in git history, recommend `git filter-repo` / BFG and
   credential rotation — deleting the line is not enough.

## False positives

The engine already filters obvious placeholders (`example`, `<your-key>`,
`xxxx`, `changeme`, `${ENV}`, etc.) and gates generic rules behind entropy.
If a finding is a known dummy value, treat it as noise. To re-check with
stricter entropy, raise `--min-entropy`.

## Notes

- Binary files, `node_modules`, `.git`, virtualenvs and oversized files are
  skipped automatically.
- The scanner never prints full secret values — only redacted previews.
