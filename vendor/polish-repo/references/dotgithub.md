# `.github/` and repo metadata (all SAFE — new files)

Copy from `assets/github/`, lightly customized to the repo.

## Pull request template
`.github/PULL_REQUEST_TEMPLATE.md` — sections: Summary, Motivation/Context, Type
of change, How tested, Screenshots (if UI), Checklist (tests pass, docs updated,
no secrets, self-reviewed). Keep it short enough that people actually fill it in.

## Issue templates
`.github/ISSUE_TEMPLATE/` (modern YAML *forms*):
- `bug_report.yml` — description, repro steps, expected vs actual, environment,
  logs.
- `feature_request.yml` — problem, proposed solution, alternatives.
- `config.yml` — `blank_issues_enabled: false` + optional contact links
  (discussions, docs).

## Dependabot
`.github/dependabot.yml` — set `package-ecosystem` to match the detected stack
(`pip`, `npm`, `cargo`, `gomod`, `bundler`, `gradle`, `composer`, `docker`) and
**always** add a `github-actions` entry so the CI actions stay current. Weekly
schedule is a sane default.

| Stack | `package-ecosystem` | directory |
|---|---|---|
| Python | `pip` | `/` (or where the manifest is) |
| Node | `npm` | `/` |
| Rust | `cargo` | `/` |
| Go | `gomod` | `/` |
| Any with workflows | `github-actions` | `/` |

For a monorepo, add one entry per sub-project directory.

## CODEOWNERS (optional)
`.github/CODEOWNERS` mapping paths → the repo owner's GitHub handle, if known.
Skip if you'd just be guessing the handle.

## `.gitattributes` (SAFE)
At repo root:
```gitattributes
* text=auto eol=lf
*.{png,jpg,jpeg,gif,pdf,zip,pt,ckpt,h5,onnx,bin} binary

# Keep committed datasets / vendored code / notebooks out of language stats:
Datasets/**      linguist-generated
**/vendor/**     linguist-vendored
*.ipynb          linguist-documentation
```
Tune the `linguist-*` lines to what the repo actually has — the point is that
GitHub's language bar reflects the *source*, not committed data dumps.

## Things only the user can do (→ put in the report checklist)
- Set the repo **description** + **topics**:
  `gh repo edit OWNER/REPO --description "..." --add-topic foo --add-topic bar`
- Enable **branch protection** on the default branch.
- Enable **Secret scanning + push protection** (Settings → Code security).
- Turn on **Discussions / Issues** as desired.
