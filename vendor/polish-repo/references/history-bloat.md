# Rewriting history (DESTRUCTIVE — always opt-in, never auto-run)

Use this when the user explicitly wants to **shrink the clone** (purge large
blobs from history) or **scrub a leaked secret** from every past commit. Both
rewrite every affected commit's SHA, which means **everyone who cloned must
re-clone or hard-reset**, and you must **force-push**.

## Hard rules

- **Never run these for the user.** Produce the exact commands; they run them.
- **Refuse outright on a shared remote** (course/employer/upstream org). Rewriting
  shared history breaks everyone else and may violate the org's rules. Say so.
- **Require a fresh backup first** (a full mirror clone), every time.
- For a **leaked secret**, history scrub is *secondary* — rotation comes first
  (see `secrets.md`). Scrubbing reduces future exposure but the old value is
  already out.

## Preferred tool: `git-filter-repo`

(`pip install git-filter-repo`. BFG is an alternative; `git filter-branch` is
deprecated and slow — don't recommend it.)

Hand the user a checklist like this, filled in with their actual paths:

```bash
# 0. Back up — a mirror you can restore from if anything goes wrong.
git clone --mirror . ../REPONAME-backup.git

# 1. (Recommended) work from a fresh mirror clone.
cd /tmp && git clone --mirror git@github.com:OWNER/REPO.git && cd REPO.git

# 2a. Purge large paths/types from ALL history:
git filter-repo --invert-paths \
  --path runs/ --path model/ --path Datasets/ \
  --path-glob '*.pt' --path-glob '*.ckpt'

# 2b. OR scrub a leaked secret everywhere (replace value with ***REMOVED***):
printf 'THE_LEAKED_VALUE==>***REMOVED***\n' > ../replace.txt
git filter-repo --replace-text ../replace.txt
#   (then delete ../replace.txt)

# 3. Re-add the remote (filter-repo drops it for safety) and force-push.
git remote add origin git@github.com:OWNER/REPO.git
git push --force --all && git push --force --tags

# 4. Tell collaborators to re-clone (old clones still contain the data).
# 5. On GitHub, old blobs can linger in caches/PRs — for a true secret leak,
#    rotate the credential (done already) and optionally contact GH support.
```

## After a purge

- Run `git gc --prune=now --aggressive` on the rewritten repo to reclaim space.
- Re-run `scripts/audit.sh` to confirm the blobs/secret are gone from history.
- Going forward, the working-tree untrack + `.gitignore` from `hygiene.md` keeps
  them out.

## Git LFS migration (also history-rewriting)

If the binaries *should* stay versioned but not bloat normal clones:

```bash
git lfs install
git lfs migrate import --include='*.pt,*.ckpt,*.h5' --everything   # rewrites history
git push --force --all
```
Same shared-remote and backup caveats apply.
