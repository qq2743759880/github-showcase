# Step 2: Plan the image pack

Write `<out>/snap-plan.md`. Commit to a creative direction before touching any design files.

## Planning rubric

Answer these for the full pack:

1. **Hook** — What is the single most important thing to communicate? This goes on every card.
2. **Copy per format** — For each format, what exact text goes where?
3. **Visual direction** — Any layout or style changes from the defaults? (centered vs left-aligned, large title vs balanced, etc.)
4. **Colors** — The brand accent hex (and any other colors) to hardcode directly into each design file.
5. **Fonts** — Confirmed Google Font family name(s) and weights — this becomes each file's `FONTS` export.
6. **Brand assets** — Which logo/icon file (and which *variant* for the card's background) goes on which format, at what size, and where (header lockup, watermark, footer). Note the file's origin in `assets/SOURCES.md`. If none was found, say "text wordmark".
7. **Facts ledger** — every number, quote or claim that will appear, with where it came from. Mark anything illustrative (mock notifications, sample names) as mock.
8. **Every element has a purpose** — if a viewer would ask "what is that?", cut it. Prefer one strong idea per card over many small decorations.
9. **Which formats** — only what the project needs. A CLI tool doesn't need a poster; a person needs a profile banner, not an OG card.

**A real series** (episodes, products, locales, screenshots) is **one design file with `VARIANTS`**, not one `.mjs` per image — see `references/step-3-design.md`. A one-off image never gets a `VARIANTS` of one row.

## Per-format specs (fill these in snap-plan.md)

```
### OG (1200×630)
label:       [domain or short name]
title:       [main headline — keep under 60 chars]
description: [one line — keep under 100 chars]
tags:        [2–3 pills, only real ones]
domain:      [bottom-right brand]

### Thumbnail (1280×720)
eyebrow:  [domain or category]
title:    [punchy, 3–6 words max]
subtitle: [optional one-liner]
tag:      [filled pill bottom-left]

### Cover (1500×500)
name:    [project name, left side]
tagline: [right side — split at —, &, ·, or |]
domain:  [below name]

### Poster (1080×1920)
eyebrow:  [short label]
title:    [2–4 words, big]
subtitle: [optional]
footer:   [domain]

### YouTube thumbnail (1280×720)
hook:     [≤ 4 huge words — what the video is]
subject:  [one focal thing: face, object, emoji, or the type itself]
brand:    [small logo, top-left; nothing in the bottom-right (duration badge)]

### App Store / Play screenshot series (1320×2868 · 1080×1920; alpha: false)
per shot: headline (2–5 words) · which app screen it shows · what the screen contains (8–10 real-looking rows)
series:   same layout, colors and type across all shots; order = the story (the first three show in search)
mock:     if there are no real screenshots, say the UI is a labelled mock
file:     **one design with `VARIANTS`** (one row per shot), not one `.mjs` per shot — see `references/step-3-design.md`

### Play feature graphic (1024×500; alpha: false)
headline: [short, left]   visual: [product/phone, right]   keep the centre readable — it's cropped in collections

### LinkedIn cover (1584×396) · X header (1500×500)
text:     [name/role/hook in the safe box only]   decoration: [rings, shapes — may sit in the avatar zone]
check:    `snap-x guides` + the mobile crop

### README card (1280×640)
name:        [project name]
description: [one line, ≤140 chars]
stack:       [2–4 real pills — tech, platform, license; skip pills if there's nothing true to say]
owner:       [optional — GitHub org or author]
```

## Design system for the pack

Read `references/design-principles.md`. In `snap-plan.md`, name for the whole pack:
- **Spacing unit** — one base unit (e.g. 8px at ~1200px wide, scaled with the canvas) used for every padding, gap and offset.
- **Type scale** — the headline:support:detail size ratio (≈ 3:1.5:1) you'll use.

And for **each format**, one **archetype** from `design-principles.md` § Archetypes (Big type, Split, Centred badge, Device mock, Quote card, Stat card) — pick on purpose, don't improvise per file. Vary archetypes across a pack when formats differ in purpose; keep one archetype across a series (episodes, products, locales).

## Formats and placement

Read `references/formats.md`, then pick each format with `npx -y @snap-x/cli formats` (sizes, no-alpha rules, verified/unverified, and the danger zones for banners, covers, thumbnails and stories). Write the chosen ids and any placement rules into the plan, and plan the Step 4 placement check (`snap-x guides`) for every format that has zones.

## When you can't ask questions

Make the best decision the skill allows and write it down: an **Assumptions** list in `snap-plan.md` (palette choices, missing domain, derived tags, mock content). Never fill a gap with an invented fact.

## Gate

`snap-plan.md` must exist with copy decided for every format before Step 3. Include the exact **regenerate command** (`npx -y @snap-x/cli render designs/*.mjs --out <dir>`) so anyone can rebuild the images.
