# Discovery & archetype detection

Goal: in one pass, learn enough to pick the right templates and spot the
problems. `scripts/audit.sh` gathers most of this deterministically; this file
explains how to interpret and extend it.

## Language & manifest signals

| File(s) present | Stack | Package manager |
|---|---|---|
| `pyproject.toml` | Python (modern) | poetry / uv / pip / hatch (read `[build-system]`) |
| `requirements*.txt`, `setup.py`, `setup.cfg` | Python (classic) | pip |
| `package.json` | Node/JS/TS | npm / yarn / pnpm (lockfile decides) |
| `Cargo.toml` | Rust | cargo |
| `go.mod` | Go | go modules |
| `Makefile`, `CMakeLists.txt`, `configure` | C/C++ | make / cmake |
| `pom.xml`, `build.gradle` | Java/Kotlin | maven / gradle |
| `Gemfile` | Ruby | bundler |
| `composer.json` | PHP | composer |
| `*.csproj`, `*.sln` | .NET | dotnet |

If multiple manifests exist in different subdirectories → **monorepo**; treat
each as its own sub-project and also polish the root (root README that links to
each package; root `.gitignore`; root CI matrix).

## Domain / archetype refinement

Beyond language, classify the *kind* of project — this changes the README and
how aggressively to treat binaries:

- **Library** — has a public API, packaging metadata, version. README leads with
  install-from-registry + API usage. CI should test multiple language versions.
- **Application / service** — has an entrypoint, maybe a Dockerfile. README leads
  with run/deploy + configuration.
- **CLI tool** — argparse/click/cobra/clap. README leads with install + command
  reference.
- **ML / data-science** — `*.pt/*.ckpt/*.h5/*.onnx/*.pb/*.safetensors`, `*.ipynb`,
  `torch/tensorflow/sklearn/ultralytics/yolo` imports, `data/`, `datasets/`,
  `runs/`, `checkpoints/`. Expect huge committed binaries and notebook output.
  README needs: data source, how to get it, model card, training command,
  inference example, reproducibility (seed, env). Treat weights/datasets as
  artifacts (untrack + document + maybe LFS), never as source.
- **Infra / config** — `*.tf`, `k8s/`, `helm/`, `ansible/`. Scan hard for
  secrets; add `tflint`/validation CI.
- **Coursework / assignment** — remote in an org like `*-cse-*`, `*-edu`, a class
  GitHub org, or a fork of a template. Often **shared remote** → additive-only,
  never push. Expect process cruft (transcripts, feedback docs).

## Commands

```bash
# What's the repo and who owns the remote?
git -C "$repo" remote get-url origin 2>/dev/null     # parse host/org/name
git -C "$repo" config user.name; git config user.email

# Tracked size & worst offenders in the WORKING TREE
git -C "$repo" ls-files | xargs -d '\n' du -k 2>/dev/null | sort -rn | head -20

# Worst offenders in HISTORY (catches blobs that were deleted but still bloat)
git -C "$repo" rev-list --objects --all \
  | git -C "$repo" cat-file --batch-check='%(objecttype) %(objectsize) %(rest)' \
  | awk '/^blob/ {print $2, $3}' | sort -rn | head -20

# Cruft directories already tracked
git -C "$repo" ls-files | grep -E '(^|/)(\.history|\.idea|\.vscode|__pycache__|node_modules|\.pytest_cache|\.ipynb_checkpoints)/' | head

# Count by extension to sense the project shape
git -C "$repo" ls-files | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -20
```

## Remote ownership rule

Parse `origin`. If `org/owner` ≠ the user's GitHub login (infer from
`git config user.*`, other personal repos, or just ask once), mark **shared**.
Shared ⇒ additive-only, and never present "push" as an option — only "open a PR
yourself if appropriate." A graded course repo is the canonical example: polish
locally, hand back a clean diff, let the human decide.

## Output of this phase

A small fact sheet you carry into later phases:
`{ archetype, languages[], pkg_manager, build_cmd, test_cmd, has_ci,
remote_ownership: yours|shared|none, tracked_files, repo_size,
largest_tree_blobs[], largest_history_blobs[], cruft[], secrets_suspected[] }`.
