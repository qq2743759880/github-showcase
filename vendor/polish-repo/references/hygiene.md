# Hygiene: ignore rules, cruft, and large files

## 1. `.gitignore` (SAFE — merge, never clobber)

Build the file from `assets/gitignore/common.gitignore` + the stack-specific set
(`python`, `node`, `c-cpp`, `rust`, `go`, `ml-datascience`). For a multi-stack
repo, concatenate the relevant sets.

**Merge, don't overwrite.** Read the existing `.gitignore`, union the lines,
preserve the user's custom entries and ordering, drop exact duplicates, and group
additions under a `# --- added by polish-repo ---` header so the diff is legible.

After writing, verify it actually catches the intended paths:
```bash
git check-ignore -v <some/cruft/path>     # should print the matching rule
```

## 2. Untrack already-committed cruft (CAUTION)

These should (almost) never be in version control. If they're tracked, untrack
with `git rm --cached -r` (keeps the local copy) and ensure they're ignored:

- **Editor/IDE:** `.idea/`, `.vscode/` (unless the repo intentionally shares
  settings), `*.swp`, **`.history/`** (VS Code *Local History* — pure noise,
  often thousands of files), `*.iml`.
- **Python:** `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.mypy_cache/`,
  `.ruff_cache/`, `.ipynb_checkpoints/`, `*.egg-info/`, `.venv/`/`venv/`.
- **Node:** `node_modules/`, `.next/`, `dist/`, `build/`, `coverage/`.
- **OS:** `.DS_Store`, `Thumbs.db`.
- **Build output:** `*.o`, `*.obj`, `*.class`, `target/`, compiled binaries.
- **Generated/run artifacts:** `runs/`, `outputs/`, `logs/`, `*.log`,
  result images/JSON the code produces (`result_*.jpg`, `output.json`).

```bash
git rm -r --cached --quiet .history .idea __pycache__   # example; keep on disk
# then make sure each is in .gitignore before committing
```

Batch all CAUTION removals, show the user the full list + how many files each
represents, get one confirmation, then do them in a single `chore: untrack ...`
commit.

## 3. Large binaries (CAUTION now; DESTRUCTIVE to fully fix)

Datasets, model weights (`*.pt/*.ckpt/*.h5/*.onnx/*.safetensors`), media, archives
(`*.zip` of data). Find them via the history-blob command in `discovery.md`.

For each large artifact, choose with the user:

1. **Untrack + ignore + document** (default, SAFE-ish): `git rm --cached`, add to
   `.gitignore`, and write *how to get it back* — a download command, a script in
   `scripts/`, or a README "Data / Weights" section (e.g. "MNIST: run
   `scripts/get_data.sh`" or "download `best.pt` from <release>"). The repo
   becomes lean *going forward*; the clone stays big until history is purged.
2. **Git LFS** (if the binary genuinely belongs in the repo): `git lfs track`,
   add `.gitattributes`. Note: migrating *existing* history to LFS rewrites it →
   DESTRUCTIVE → checklist.
3. **History purge** to actually shrink the clone → `history-bloat.md`,
   DESTRUCTIVE, opt-in, with rotation-style warnings about coordinating with
   anyone who has cloned.

Always state the trade-off plainly: "Untracking stops it growing; the existing
clone is still N MB until you rewrite history (commands in the checklist)."

## 4. Junk, scratch, and awkward names (CAUTION — quarantine)

- Scratch files: `asd.*`, `test.*` at root, numeric-only names (`20`, `123`),
  `Untitled*`, `tmp*`, `scratch*`, `Copy of *`, `*.bak`, `*~`.
- Paths **with spaces** (`Data Augmentation/`) — fine for git but brittle in
  scripts/CI; offer to rename to `data-augmentation/` (updates references).
- Duplicates (same content, two paths; or a dir and a flattened file of the same
  data, e.g. `x/x` and `x.idx`). Surface, let the user pick which to keep.

Don't hard-delete. Move suspected junk into `.polish-quarantine/` (gitignored)
and list it in the report: "moved these N files aside; delete them yourself if
you agree." Reversible by construction.

## 5. Empty dirs, symlinks, encoding

- Remove empty tracked dirs (git doesn't track them anyway — usually a stray
  `.gitkeep` that's no longer needed).
- Flag broken symlinks.
- `.gitattributes` with `* text=auto eol=lf` normalizes line endings (see
  `dotgithub.md`).
