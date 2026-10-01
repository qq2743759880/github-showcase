# Report, verify, commit

## `POLISH_REPORT.md`
Write this at the repo root (gitignored or untracked — it's a hand-off artifact,
not product). Structure:

```markdown
# Polish Report — <repo> (<date>)

## Detected
- Archetype: <…>   Languages: <…>   Package manager: <…>
- Remote: <yours | SHARED (org) | none>   Default branch: <…>
- Before: <N> tracked files, <size> on disk, largest history blob <…>

## Applied (on branch polish/<date>)
### SAFE
- [x] Added professional README (preserved demo link + references)
- [x] Added LICENSE (MIT)
- [x] Added .github/ (PR + issue templates, dependabot)
- [x] Added CI: <workflow>
- [x] Wrote/merged .gitignore (<n> rules)
### CAUTION (done, with your earlier OK)
- [x] Untracked <n> cruft files (.history/, __pycache__/, …) — kept on disk
- [x] Untracked large artifacts (<list>) — see README "Data/Weights" for how to fetch
- [x] Quarantined junk → .polish-quarantine/ (<list>)

## After
- <N'> tracked files, <size'> on disk

## ⚠️ Manual follow-ups (I did NOT do these — they're irreversible / need you)
- [ ] ROTATE leaked credential <name> at <provider> — it's in history, already exposed
- [ ] Shrink the clone (rewrite history) — back up first, then:
      <exact git filter-repo commands>
      git push --force --all   # only on YOUR repo, after coordinating
- [ ] Push the polish branch & open a PR:
      git push -u origin polish/<date>
- [ ] Set repo description/topics: gh repo edit … --add-topic …
- [ ] Enable branch protection + secret-scanning push protection
- [ ] Delete .polish-quarantine/ once you've confirmed its contents
```

Make the checklist **copy-pasteable** and specific to this repo — real paths,
real commands, real provider names. That's the difference between a report the
user acts on and one they ignore.

## Verify before declaring done
- **Build/test still works:** run the cheap test/build command if it exists
  (`make`, `pytest -q`, `npm test`, `cargo build`). If it now fails *because of
  your changes*, fix or revert that change. If it was already failing, note it —
  don't pretend you fixed it.
- **Ignore rules work:** `git check-ignore -v <path>` for a couple of the things
  you just untracked.
- **No secret left in the tree:** re-run the working-tree secret scan.
- **Idempotency sanity:** the things you added shouldn't be re-added on a second
  run.

## Commit strategy (on the `polish/<date>` branch, never push)
Small, conventional commits so the diff reviews cleanly:
- `docs: add professional README and LICENSE`
- `chore: add .gitignore and untrack build/editor artifacts`
- `ci: add <stack> test workflow`
- `chore(github): add PR/issue templates and dependabot`

Then **stop**. Tell the user exactly how to review and proceed:
> "Polished on branch `polish/<date>` — review with `git diff main...polish/<date>`.
> When happy: `git switch main && git merge polish/<date>`, then push yourself.
> The ⚠️ items in POLISH_REPORT.md are irreversible and left for you."

Never merge to the default branch or push on the user's behalf unless they say
so in this session.
