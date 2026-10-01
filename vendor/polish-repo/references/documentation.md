# Documentation: README, LICENSE, and de-crufting docs

## Professional README (SAFE — augment, never destroy)

Start from `assets/readme/README.template.md`. **Before writing, read the
existing README** and preserve everything valuable: demo videos, screenshots,
references, example interactions, citation blocks. You are upgrading structure
and filling gaps, not erasing the author's voice.

Core sections (include the ones that fit the archetype; don't pad):

1. **Title + one-line description** — what it is, in a sentence a stranger gets.
2. **Badges** — CI status, license, language/version. Wire real URLs once CI
   exists (see `ci-cd.md`). Don't add badges that point at nothing.
3. **Why / what** — 2–4 sentences. The problem it solves; the key tech.
4. **Demo / screenshot** — keep existing; add a placeholder line if none.
5. **Features** — bulleted, concrete.
6. **Install** — exact commands for the detected package manager.
7. **Usage / Quickstart** — the smallest real example that works.
8. **Configuration** — a **table of env vars** generated from `.env.example`
   (name · required? · default · description).
9. **Project structure** — a trimmed `tree` of the top level with one-line
   notes. Helps readers orient.
10. **Testing** — the detected test command.
11. **License** — one line, links `LICENSE`.
12. Optional: Architecture/diagram, Roadmap, Contributing, Acknowledgements.

### Archetype flavors
- **Library:** lead with install-from-registry + minimal API example; document
  the public surface; note supported versions.
- **CLI:** install + a command/flag reference table + a couple of recipes.
- **Service/app:** run locally + configuration + deploy notes; Docker if present.
- **ML / data-science:** **Data** (source + how to obtain — never "it's in the
  repo" if you just untracked it), **Model** (architecture, a tiny model card:
  inputs/outputs/metrics), **Training** (command, hardware, time), **Inference**
  (a runnable example), **Reproducibility** (seed, env, versions). This is where
  most "ugly ML repos" are weakest — make these sections real.

Keep it skimmable: short paragraphs, real fenced code blocks with the right
language tag, working relative links.

## LICENSE (SAFE)

If none exists, add one (`assets/license/`). Pick by: an existing license
mention → match it; a personal repo → **MIT** default; ask once if genuinely
ambiguous (MIT vs Apache-2.0 vs "all rights reserved / none"). Fill in year +
author from `git config user.name`. Never relicense an existing licensed repo
without the user saying so.

## De-cruft the docs (CAUTION — relocate, don't shred)

Repos accumulate process artifacts that shouldn't ship as if they were product
docs:
- **AI/agent transcripts** (`transcripts/`, `conversation.md`, `fix1.md`),
  **feedback/response docs** (`FEEDBACK-RESPONSE.md`), scratch design drafts,
  graded-rubric notes.
- A scratch **`TODO.md`** → mine it for a real "Roadmap" section in the README,
  then untrack the scratch file.

Default action: **untrack** (`git rm --cached`) or **move to `docs/dev/`** rather
than delete — the user may want them. Exception: never relocate a file the build
or README links to without updating the link. List every relocation in the
report.

## Make it public-ready (de-identify)

When the user wants a repo *published* or *portfolio-grade* — especially one that
started as coursework, client work, or an internal project — polishing the code
isn't enough. You must strip the identifying wrapper. **The work stays; the
context that shouldn't be public goes.**

Before publishing, grep the whole tree (tracked files) for identity:

```bash
git ls-files | xargs grep -inE \
  'assignment|rubric|grading|grade|professor|cours|class|semester|sp2[0-9]|fa2[0-9]|\
<org-or-employer-name>|confidential|internal[- ]only' 2>/dev/null
# Third-party PII — the highest-risk category:
git ls-files | xargs grep -inE \
  '[A-Z][0-9]{8}|student[- ]?id|employee[- ]?id|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(edu|com)' 2>/dev/null
```

Then remove or rewrite:
- **Assignment / course scaffolding** — "Assignment N" titles, links to a class
  page, rubric references. Rewrite the README to lead with the *project*, not the
  assignment.
- **Grading & peer-review artifacts** — `FEEDBACK-RESPONSE.md`, review notes,
  TA comments. These almost always contain **other people's names and IDs** —
  remove them (untrack + recommend purging from history; see below).
- **AI/process transcripts** — conversation logs from building it.
- **Third-party PII** — classmates'/colleagues' names, student or employee IDs,
  personal emails. Treat like a secret: don't publish other people's data. If it
  was committed, the working-tree removal isn't enough — flag a history scrub.
- **Internal URLs / hostnames / ticket IDs** that leak an org's internals.

**Relocation, not push.** If `origin` is a shared/course/employer remote, do
*not* push the de-identified version back to it. Instead recommend:
```bash
gh repo create <user>/<clean-name> --private --source . --remote myrepo
# review, then: git push myrepo <branch>
```
**History caveat:** even after you clean the working tree, the shared remote's
history (old commits, the original README, the PII) is still there. For a truly
clean public repo, recommend starting its history fresh:
```bash
# In the relocated repo, collapse to a single clean commit:
git checkout --orphan clean && git add -A && git commit -m "Initial public release"
git branch -M clean main
```
Put both the relocation and the history decision in the report — they're the
user's call, not yours to push.

## Supporting docs (only when warranted)
- `CONTRIBUTING.md` — for shared/OSS/library repos (how to set up, test, the PR
  flow). Skip for throwaway scripts.
- `SECURITY.md` — for anything that handles credentials or is published; where to
  report vulns.
- `CHANGELOG.md` — for versioned libraries (Keep a Changelog format).
