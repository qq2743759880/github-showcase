# File-structure refactoring (CAUTION — moves break references)

Reorganizing a messy layout into a clean, conventional one is one of the
highest-impact things for *public-readiness* — a recruiter or new contributor
forms an opinion from the file tree before reading a line of code. But moving
files is **not** a cosmetic operation: it breaks imports, includes, build paths,
and relative file loads. Treat it as CAUTION and follow the procedure.

## When to do it
- The user explicitly wants the repo presentable / portfolio-grade, **and**
- the current layout actively hurts readability: source scattered at the root,
  directory names with spaces, obvious typos in package names, code mixed with
  data/notebooks/outputs.

Don't refactor structure just because you can. For an **archived** project,
prefer the *light* tier — the payoff of a deep rename rarely justifies the risk.

## Aggressiveness tiers (let the user pick)
- **Light** (default for archived repos): delete junk files; fix directory names
  with spaces (`Data Augmentation/` → `data_augmentation/`); remove generated
  outputs. No code-identifier renames.
- **Moderate**: the above + group runnable source under a clear top-level
  (`src/`, or a package dir) and separate `data/`, `notebooks/`, `scripts/`.
  Update imports/paths.
- **Deep**: the above + rename packages/modules to convention (fix typos like
  `VideoProcesser` → `video_processor`, snake_case), introduce packaging
  (`pyproject.toml` / `__init__.py`), wire entrypoints. Highest risk; only for
  repos the user actively maintains.

## The safe procedure (every move)
1. **Find every reference first.** Before moving `X`, grep for who depends on it:
   - Python: `grep -rn "import X\|from X\|['\"].*X/.*['\"]"` (imports + string paths).
   - C/C++: `grep -rn '#include ".*X"'` and any hard-coded paths.
   - Build/config: `Makefile`, `CMakeLists.txt`, `package.json`, CI YAML, Dockerfiles.
   - Hard-coded data paths in code (e.g. `"Datasets/MNIST/..."`).
2. **Move with `git mv`** (preserves history) — not `mv` + add.
3. **Update every reference** you found in step 1, including string literals and
   build files.
4. **Re-run the build and tests.** This is the gate: if `make` / `pytest` /
   `cargo build` no longer passes *because of the move*, you broke something —
   fix the missed reference or revert the move. Never leave a refactor that
   doesn't build.
5. **Commit the move on its own** (`refactor: reorganize source into src/`) so the
   diff is reviewable and revertible in isolation.

## Common, safe wins
- Directory/file names with **spaces** → hyphen/underscore (brittle in shells, CI,
  imports). Update references.
- **Junk**: `asd.png`, numeric-named files (`20`), `Untitled*`, `*.bak`, scratch
  notebooks → quarantine then delete.
- **Generated output** living in source dirs (`output.json`, `result_*.jpg`,
  `runs/`) → remove + gitignore (see `hygiene.md`), don't relocate.
- **Mixed concerns**: weights/data/notebooks interleaved with source → split into
  `data/`, `notebooks/`, `models/` (with the big files untracked per `hygiene.md`).

## Watch out for
- **Relative file loads in code** (open("data/x")) — moving the data or the code
  changes the relative path. Grep string literals, not just imports.
- **Notebooks** with hard-coded paths and **`sys.path` hacks**.
- Renames that look trivial but ripple: a package rename touches every importer.
- If you can't confidently update all references (no tests, opaque dynamic
  imports), **propose the refactor in the report instead of doing it** — a broken
  move is worse than a messy-but-working layout.
