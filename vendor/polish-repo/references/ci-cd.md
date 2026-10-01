# CI/CD

## Principles
- **Detect before adding.** If `.github/workflows/`, `.gitlab-ci.yml`,
  `.circleci/`, or `azure-pipelines.yml` already exist, **augment** (add a
  missing test/lint job) rather than dropping a competing workflow.
- Match the stack. Pull the right file from `assets/ci/` and fill in the version
  matrix + install/test commands you detected in Phase 1.
- A good first CI does three things: **build**, **lint/format-check**, **test**.
  Don't over-engineer (no deploy/release unless the repo is a published library
  *and* the user asks).
- Only add badges for workflows that actually exist.

## Stack → workflow (from `assets/ci/`)

| Stack | File | Jobs |
|---|---|---|
| Python | `python.yml` | matrix py3.10–3.12 · `pip install` · `ruff check` · `ruff format --check` · `mypy` (if typed) · `pytest` |
| Node | `node.yml` | setup-node LTS · install (detect npm/pnpm/yarn) · `lint` · `test` · `build` |
| Rust | `rust.yml` | `cargo fmt --check` · `cargo clippy -D warnings` · `cargo test` |
| Go | `go.yml` | `go vet` · `golangci-lint` · `go test ./...` |
| C/C++ (make) | `c-make.yml` | gcc + clang matrix · `make` · `make test` or `make run` · optional `-fsanitize` |
| any | `secret-scan.yml` | gitleaks on push/PR |

If the project has **no test command**, don't fabricate green CI — add a build
+ lint workflow and note "add tests" in the report's roadmap. A workflow that
always passes because it tests nothing is worse than honest absence.

## Lint/format config (add if missing)
- Python: `ruff` config in `pyproject.toml` (or `ruff.toml`); `mypy` section if
  the code has type hints.
- Node: `.eslintrc`/`eslint.config.js`, `.prettierrc`.
- Rust: `rustfmt.toml` (usually defaults are fine).
- C/C++: `.clang-format` (pick a base style, e.g. LLVM/Google).

Keep configs lenient on a first pass — the goal is signal, not turning the
user's repo red with 400 style errors. Note stricter options in the report.

## Badges (wire into README)
After CI exists, add to the top of the README:
```markdown
![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/github/license/OWNER/REPO)
```
Use the real `OWNER/REPO` from the remote. Skip if the remote is shared/unknown.

## Optional, offer don't impose
- **pre-commit** (`.pre-commit-config.yaml`): format, trailing-whitespace,
  end-of-file-fixer, large-file guard, gitleaks. Great DX but adds a dependency.
- **Large-file guard** in CI: fail if any pushed blob > N MB (cheap insurance
  against re-bloating after you cleaned it up).
- **Release automation**: only for published libraries, only on request.
