---
name: wtfismyrepo
description: Onboarding companion that explains an unfamiliar codebase using the ADHD diverge→score→deepen engine (github.com/UditAkhourii/adhd). Use whenever someone is new to a repo, lost in a codebase, or asks: "where do I start", "how does this work", "explain this repo", "I'm new to this codebase", "walk me through", "give me a tour", "what is going on here", "where is X handled", "what breaks if I touch this", "what should I work on first", "how do I run this", "trace this request", "onboard me", "ramp up", "understand this project", "wtf is this". Trigger aggressively on any codebase confusion.
---

# wtfismyrepo skill

**Engine**: ADHD diverge→score→cluster→deepen loop (MIT, [github.com/UditAkhourii/adhd](https://github.com/UditAkhourii/adhd))
**Data layer**: wtfismyrepo deterministic analysis — import-graph PageRank, git-churn fragility, GitHub PR/issue signals

---

## How this skill works

Most "explain my code" approaches are linear: read the code, summarize it, done. That anchors on whatever angle the first pass happens to take.

**This skill treats codebase onboarding as an ideation problem** using the ADHD two-phase architecture:

1. **DIVERGE** — Generate N independent onboarding angles under deliberately different cognitive frames (new-grad, archeologist, security researcher, on-call engineer…). Zero cross-talk between frames during generation so no anchoring.
2. **SCORE → CLUSTER → DEEPEN** — A critic pass scores each angle for this developer's situation (novelty to them, viability for their goal, fit to the codebase's actual complexity). Cluster angles by underlying approach. Deepen the best one into a full walkthrough.

The hard data (entry points, spine, fragility, hot zones) comes from `wtfismyrepo --json`. The ADHD loop decides *how to explain it* given who's asking and why.

---

## Step 0 — Get the hard data first

Before any explanation, run the deterministic engine to get ground-truth:

```bash
wtfismyrepo . --json --no-color    # full analysis: PageRank, churn, history
# or from GitHub without a local clone:
npx github:nandnijaiswal/wtfismyrepo . --json --no-color
```

If the CLI is unavailable, use these tools directly:
- `gh repo view --json name,description,languages`
- `gh pr list --state open --json number,title,files`
- `gh issue list --state open --label "good first issue"`
- `git log --pretty=format: --name-only | sort | uniq -c | sort -rg | head -20`
- File read + import parsing for the dependency graph (manual)

Store the JSON. Every explanation you give should be anchored to it — not guessed.

---

## Step 1 — DIVERGE: generate onboarding angles across frames

**This is the ADHD diverge phase.** Run each frame as a **separate, isolated** reasoning thread. Do NOT let one frame's output influence another while generating. No evaluation during generation — pure ideation only.

For each frame below, generate 3–5 distinct onboarding angles: different ways of *entering* and *explaining* this codebase. Each angle is one sentence describing the approach.

### The onboarding frames (select 4–6 per run, always include one wild)

| Frame | Vantage point |
|---|---|
| **New grad, day one** | 5-word mental model + the single file to open first |
| **Archeologist** | The git history / closed PRs / old issues: what decisions were made and reversed? |
| **Security researcher** | Trust boundaries, data flows, attack surfaces |
| **CTO doing due diligence** | Blast radius, technical debt, single points of failure |
| **On-call at 3am** | Failure modes, runbooks, diagnostic entry points |
| **Product manager** | Trace user value, not code paths |
| **Refactorer** | The coupling graph — what depends on what before touching anything |
| **Data engineer** | Sources → transforms → sinks → state stores |
| **Performance engineer** | Hot paths, latency budget, N+1 queries, blocking I/O |
| **Inversion** *(wild)* | Work backwards from failure modes — what failures tell you what the system actually is |
| **Domain expert** | The business entities and invariants that exist regardless of implementation |
| **Contrarian** *(wild)* | Where the code is wrong or weird — often faster to understand than where it's right |

**Diverge output format** (per frame, before any scoring):
```
Frame: [label]
Angles:
- [one sentence: a distinct way to enter/explain this codebase from this vantage]
- ...
```

---

## Step 2 — SCORE each angle

**Critic phase.** Now evaluate every generated angle on three axes:

| Axis | Definition | Weight |
|---|---|---|
| **Novelty** | Distance from "start at `main()` and read down" — does this surface something the dev wouldn't find on their own? | 35% |
| **Viability** | Can this angle be fully executed with the data we have? Is it concrete, not vague? | 40% |
| **Fit** | Does this match *this developer's* stated goal and experience level? | 25% |

For each angle, also flag **traps**: onboarding approaches that *look* helpful but waste the developer's time — e.g., "read all the tests first" when there are 800 tests and none document the domain model; "trace the codebase top-down" when the codebase has no clear entry point.

Score format:
```
Angle: [text]
  Novelty: N/10 — [one clause]
  Viability: N/10 — [one clause]
  Fit: N/10 — [one clause]
  Total: N.N
  Trap: [if applicable, one-line reason] | CLEAN
```

---

## Step 3 — CLUSTER

Group the top (non-trap) angles by their **underlying approach**, not surface keywords. Name the cluster by the strategy, e.g.:
- "Follow-the-data plays" (data engineer, performance engineer angles)
- "Read-the-history plays" (archeologist, contrarian angles)
- "Blast-radius-first plays" (CTO, on-call, refactorer angles)
- "User-value plays" (PM, domain expert angles)

Report: cluster label → angles in it.

---

## Step 4 — NON-OBVIOUS PICK + DEEPEN

Select the highest `novelty × viability` scorer (not just the highest total — the goal is to escape the obvious). This is the **non-obvious pick**.

Then deepen it:
1. **Sketch** — exactly how to execute this onboarding angle on *this* codebase (4–8 sentences, cite real files from the analysis data).
2. **Load-bearing risk** — what makes this approach fail (e.g., "only works if the git history is informative; shallow clones break it").
3. **First concrete step** — the exact file to open or command to run.
4. **Child angles** — 3–5 variations or combinations with other frames that this approach unlocks.

---

## Step 5 — DELIVER the walkthrough

Execute the deepened winning angle as an actual onboarding walkthrough. Ground every statement in the wtfismyrepo data:

- **Always link to real files** (`path/to/file.ext:line` where known).
- **Cite the history** — pull reasoning from PR/issue data, not invented.
- **One layer at a time** — explain one component, check understanding, then go deeper.
- **Surface the traps** — flag the winning angles the developer should skip, and why.

**End every session with "Your first move":**
1. The exact file to open.
2. The exact first safe change or issue to pick up.
3. The blast-radius warning: "Before touching `X`, know that `A` and `B` depend on it."

---

## The three questions that must be answerable after this skill runs

1. **"This system exists to ______, and it works by ______."**
2. **"If I need to change ______, I start in `______` and watch out for ______."**
3. **"The riskiest/most fragile part is ______, because ______."**

If the developer can't finish these sentences, the skill hasn't finished. Go deeper.

---

## Anti-patterns (do NOT do these)

- ❌ **Single-frame explanation** — pick one angle and explain. Run the diverge pass.
- ❌ **Explaining code without the data** — run the CLI first. No guessing at structure.
- ❌ **Dumping the whole directory tree** — one layer at a time.
- ❌ **Skipping "Your first move"** — a lost dev needs a first step, not a lecture.
- ❌ **Letting frames cross-contaminate during generation** — diverge is isolated, critic is separate.

---

*Engine: ADHD parallel divergent ideation framework, MIT license, by Udit Akhouri ([github.com/UditAkhourii/adhd](https://github.com/UditAkhourii/adhd)). Data layer: wtfismyrepo by Nandni Jaiswal ([github.com/nandnijaiswal/wtfismyrepo](https://github.com/nandnijaiswal/wtfismyrepo)).*
