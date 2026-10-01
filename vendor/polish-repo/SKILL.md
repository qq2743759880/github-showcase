---
name: polish-repo
description: >-
  Polish, clean up, and professionalize any code repository — of any language,
  framework, or domain. Use when the user wants to make a repo presentable,
  publish-ready, or portfolio-grade: "polish this repo", "clean up my
  repository", "professionalize this project", "prepare this for GitHub /
  open-source / a recruiter", "write a proper README", "add CI/CD", "add a PR
  template", "set up a .gitignore", "remove secrets", "get rid of junk / large
  files / committed datasets / model weights / .idea / __pycache__". Handles
  secrets removal, git-history bloat, README/docs, .github templates, CI/CD,
  licensing, and hygiene — safely, never pushing or rewriting history without
  explicit consent.
---

# polish-repo

Take a messy repository and make it **clean, documented, and professional** —
tailored to whatever kind of project it is — without ever destroying the user's
work or doing anything irreversible behind their back.

You are the orchestrator. This file is the control loop; the deep detail for
each concern lives in `references/` and is loaded **only when that phase runs**
(progressive disclosure — don't pre-read everything). Concrete templates live in
`assets/`. A deterministic scanner lives in `scripts/audit.sh`.

---

## 0. Prime directives (never violate these)

These override any other instinct, including the urge to be thorough.

1. **Never push. Never force-push. Never rewrite published history** unless the
   user explicitly says to, *for this repo, in this session*. Approval for one
   repo or one action is not approval for another.
2. **Classify every action by tier and respect the gates:**
   - **SAFE** — adds new files only (README, LICENSE, `.github/`, CI, `.gitignore`
     additions). Apply freely.
   - **CAUTION** — removes files from git tracking or moves/deletes working-tree
     files. Prefer `git rm --cached` (untrack, keep on disk) and *quarantine*
     over `rm`. Batch these, show the list, get a yes.
   - **DESTRUCTIVE** — rewrites git history (`filter-repo`, BFG), force-push,
     `reset --hard`, deleting data with no copy. **Never auto-run.** Produce the
     exact commands and hand them to the user.
3. **Deletion ≠ disappearance.** Removing a secret or a 100 MB blob from the
   working tree does **not** remove it from git history (it's still cloneable,
   and for a leaked secret, still compromised). Say so explicitly and route to
   the history/secrets playbooks.
4. **Preserve, don't destroy.** Default to untracking + `.gitignore` + a
   `.polish-quarantine/` move, not `rm`. The user can always delete later; they
   can't un-delete.
5. **Augment, don't clobber.** If a README/CI/LICENSE/`.gitignore` already
   exists, *merge and improve* it — never silently overwrite good content
   (demo links, references, custom config).
6. **Check who owns the remote before *pushing*.** If `origin` points at an org
   that isn't the user (a fork, a course/employer org, an upstream), treat it as
   **shared**: **never push there.** This does *not* mean "don't improve" — you
   may still fully polish the content locally on a branch. When the user wants it
   published, the path is to **relocate to a repo under their own account**
   (`gh repo create`), not to push to the shared origin. Note that git *history*
   on the shared remote may still hold identifying info, so a pristine public
   repo may warrant a fresh/squashed history (see `references/documentation.md`
   → "Make it public-ready").
7. **Be idempotent.** Re-running on an already-polished repo should be a near
   no-op. Detect what's already done and skip it.
8. **Report first, then act.** Always run the audit and present the plan before
   mutating anything beyond a safety branch.

---

## 1. Operating modes

Pick based on how the user invoked the skill (default = **safe**):

| Mode | Trigger | Behavior |
|---|---|---|
| `report` | "audit", "what's wrong with", "dry run", "don't change anything" | Run discovery + audit, emit `POLISH_REPORT.md`, change nothing. |
| `safe` (default) | "polish", "clean up", "professionalize" | Do all SAFE work + CAUTION work with confirmation. Defer DESTRUCTIVE to the follow-up checklist. |
| `full` | "do everything", "aggressive", user explicitly opts into history rewrite | Same as safe, **plus** walk the user through DESTRUCTIVE steps interactively (still no auto-push). |

If a `.polishrc` (JSON/YAML) or `[tool.polish]` block exists, honor its
`mode`, `keep`, `ignore_extra`, and `license` keys.

---

## 2. The pipeline

Run phases in order. After **Phase 0–1** you have the facts; from there, do SAFE
work first (high value, zero risk), then CAUTION (with one batched confirmation),
then write the report listing deferred DESTRUCTIVE items.

### Phase 0 — Establish a safe workspace
- Confirm it's a git repo. If not: offer `git init` (SAFE) — many polish steps
  still apply to a non-git folder (README, LICENSE, structure).
- `git status` — if the tree is dirty or mid-merge/rebase, **stop and tell the
  user**; don't mix polish changes with their in-flight work.
- Identify default branch and remote owner (see directive 6). Record whether the
  remote is **yours** or **shared**.
- Create a working branch: `git switch -c polish/YYYY-MM-DD`. All commits land
  here so the user reviews a clean diff before any merge.

### Phase 1 — Discover & classify
Run `bash scripts/audit.sh <repo>` for a deterministic snapshot, then interpret.
Detect, in this order:
- **Language(s)** from manifests/extensions; **package manager**; **build/test
  system**; **existing CI**; **license/author** (from `git config`, headers).
- **Archetype** (drives every downstream template) — see the table below.
- **Repo health stats**: tracked-file count, total size, largest blobs in the
  **working tree _and_ in history**, binary ratio, cruft directories present.

| Signal | Archetype | Tailoring |
|---|---|---|
| `pyproject/requirements/setup.py` | Python app/lib | ruff+mypy+pytest CI, Python `.gitignore`, lib-vs-app README |
| `package.json` | Node/JS/TS | eslint+test+build CI, Node `.gitignore` |
| `Cargo.toml` | Rust | fmt+clippy+test CI |
| `go.mod` | Go | vet+test CI |
| `Makefile`/`CMakeLists` + `*.c/*.cpp` | C/C++ | make/cmake build+run, gcc/clang matrix |
| `*.pt/*.ckpt/*.h5/*.onnx`, `*.ipynb`, `torch/tf/yolo`, big datasets | **ML / data-science** | model/dataset/repro README, big-blob + LFS handling, notebook output stripping |
| workspaces / multiple manifests | Monorepo | detect each sub-project; polish per-package + root |
| no manifest, few files | Script/empty | minimal README + LICENSE + `.gitignore` |

Load the matching detail as you go:
- `references/discovery.md` — full detection heuristics & commands.

### Phase 2 — Secrets & sensitive data  → `references/secrets.md`
- Scan tree **and history** for real credentials (keys, tokens, PEM, `.env`,
  `credentials.json`). Filter out placeholders/examples.
- **In working tree only:** untrack (`git rm --cached`), add to `.gitignore`,
  regenerate a safe `.env.example` from the env vars the code references.
- **In history:** STOP. Tell the user to **rotate the credential now** (it's
  already leaked), then provide the opt-in `git filter-repo` removal commands.
  Do not pretend a working-tree delete fixes a historical leak.
- Recommend a `gitleaks` CI job (asset provided).

### Phase 3 — Hygiene: ignore & de-clutter  → `references/hygiene.md`
- Write/merge a tailored `.gitignore` from `assets/gitignore/*` (stack-specific
  + common), de-duped, preserving the user's existing lines.
- Untrack already-committed cruft: `__pycache__/`, `*.pyc`, `.idea/`,
  **`.history/`** (editor local-history — never belongs in git), `.DS_Store`,
  `node_modules/`, `dist/`/`build/`, `.pytest_cache/`, `*.o`, virtualenvs,
  generated outputs (`runs/`, `output.json`, result images).
- **Large binaries** (datasets, model weights, media): untrack + ignore +
  document how to obtain/regenerate them (a `scripts/` fetch note or README
  section). Offer Git LFS migration. History purge is DESTRUCTIVE → checklist
  (`references/history-bloat.md`).
- Junk/scratch files (`asd.png`, numeric-named, `tmp`, `Untitled`), paths with
  spaces, duplicates → flag, quarantine, or rename with confirmation.
- **File-structure refactor** (for portfolio/public-readiness) → see
  `references/structure.md`. Propose a clean, conventional layout (e.g. group
  source under `src/`, fix directory names with spaces, fix obvious typos). This
  is **CAUTION**: moving files breaks imports/build paths, so only do it by also
  updating every reference and then re-running the build/tests. Offer light /
  moderate / deep aggressiveness; default light for archived projects.

### Phase 4 — Documentation  → `references/documentation.md`
- Generate or upgrade a **professional README** from
  `assets/readme/README.template.md`, tailored to the archetype. **Preserve**
  existing demo links, references, screenshots. Include an env-var table built
  from `.env.example`.
- Add a `LICENSE` (`assets/license/`); pick via the user's `git` author / a
  quick question; default MIT for personal projects.
- Relocate process cruft (AI transcripts, `FEEDBACK-RESPONSE.md`, scratch
  `TODO.md`, `DESIGN.md` drafts) → untrack or move to `docs/dev/`; convert a real
  TODO into a README "Roadmap" section.
- **Make it public-ready / de-identify** (when the user wants this published or
  portfolio-grade) → `references/documentation.md` → "Make it public-ready".
  Strip identity that shouldn't go public: course/employer/client names,
  assignment scaffolding, grading & peer-review artifacts, internal URLs, and —
  critically — **third-party PII** (classmates'/colleagues' names, student/employee
  IDs, emails). Grep the whole tree for these before publishing. The work code
  stays; the identifying wrapper goes.
- Add `CONTRIBUTING.md` / `SECURITY.md` when the repo is a shared/library/OSS
  project (skip for throwaway scripts).

### Phase 5 — `.github` & repo metadata  → `references/dotgithub.md`
- `PULL_REQUEST_TEMPLATE.md`, `ISSUE_TEMPLATE/` (bug + feature + config),
  `dependabot.yml` (ecosystem matched to the detected stack), optional
  `CODEOWNERS`. All from `assets/github/`.
- `.gitattributes`: EOL normalization + `linguist-generated`/`linguist-vendored`
  so committed datasets/vendored code don't skew language stats.

### Phase 6 — CI/CD  → `references/ci-cd.md`
- If CI already exists, **augment** it; don't add a competing workflow.
- Else add the stack-matched workflow from `assets/ci/` (build + lint + test).
- Add missing lint/format config (ruff, eslint, rustfmt, clang-format).
- Wire status + license badges into the README.
- Offer (don't force) pre-commit, secret-scan, and large-file-guard jobs.

### Phase 7 — Build/dep hygiene
- `.editorconfig` (`assets/editorconfig/`); ensure lockfiles are committed;
  surface a task runner (`make`/`just`/npm scripts) for build/test/lint/run.

### Phase 8 — Report, verify, commit  → `references/reporting.md`
- Write `POLISH_REPORT.md`: detected archetype, before/after stats
  (file count, repo size), every change made, and a **manual follow-up
  checklist with copy-paste commands** for the deferred DESTRUCTIVE/manual items
  (rotate secret X, run filter-repo, `git push`, set repo topics, enable branch
  protection).
- Verify: project still builds/tests (run the quick test command if cheap);
  `git check-ignore` confirms intended files are ignored; re-scan confirms no
  secret remains in the tree.
- Commit in small, conventional-commit chunks on the `polish/*` branch
  (e.g. `docs: add professional README`, `chore: untrack build artifacts`,
  `ci: add Python test workflow`). **Stop there.** Tell the user how to review,
  merge, and push themselves.

---

## 3. Decision quick-reference

- *"There's a 100 MB model / a committed dataset."* → untrack + ignore +
  document fetch (SAFE). Shrinking the clone needs history rewrite → checklist.
- *"There's an API key in the code."* → untrack + ignore now, **and tell them to
  rotate it** (CAUTION + manual), history scrub → checklist.
- *"The remote is someone else's org."* → polish the content locally, but never
  push *there*; to publish, relocate to the user's own repo (`gh repo create`).
- *"Make this public / portfolio-ready."* → also de-identify: strip course/
  employer references, grading artifacts, and third-party PII (see Phase 4).
- *"README already looks decent."* → augment sections, don't rewrite.
- *"It's not even a git repo."* → offer init; still do README/LICENSE/structure.
- *"User said do everything / aggressive."* → `full` mode: walk them through
  DESTRUCTIVE steps interactively, but still never push for them.

When unsure whether something is cruft or intentional, **quarantine, don't
delete**, and list it in the report for the user to confirm.

## 4. Extending

To support a new stack: add `assets/gitignore/<stack>.gitignore`, an
`assets/ci/<stack>.yml`, a detection row in the Phase 1 table, and (if needed) a
README flavor note in `references/documentation.md`. No code changes required —
this skill is data-driven by its assets.
