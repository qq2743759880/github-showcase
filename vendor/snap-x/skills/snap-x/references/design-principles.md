# Design principles

`step-3-design.md` keeps images correct (fit, contrast, glyphs, logos). This file makes them good. Apply every rule; the render review in Step 4 scores against them.

## 1. One focal point
Each image has one thing the eye lands on first: usually the headline, sometimes the product or a face. Everything else is visibly secondary. If two things compete, shrink or remove one.

## 2. Hierarchy by size
- At most **3 text levels** per image (headline, support line, detail) and at most **2 font families**.
- Use a ratio, roughly **headline : support : detail ≈ 3 : 1.5 : 1**. Adjacent levels must differ clearly in size or weight, not just colour.
- Thumbnails and small-view formats: 1–2 levels only.

## 3. Spacing system
- Pick one base unit per pack: **8 px at ~1200 px wide**, scaled with the canvas (e.g. 16 px at 2400 px). Use only multiples of it for padding, gaps and offsets.
- Outer margin ≥ **6–8% of the canvas's short side**, and never less than the format's safe area.
- Related items sit closer together than unrelated ones (grouping by proximity).

## 4. Alignment
- Align everything to a few shared edges or axes. Left-align multi-line text; centre only short, single-line compositions.
- Logo, headline and support text share an alignment edge unless the archetype says otherwise.

## 5. Whitespace
Empty space is a feature. When a design feels busy, **remove** elements before shrinking them. A card with a headline, one support line and a logo is complete.

## 6. Colour proportion
Dominant background, secondary surface, one accent: roughly **60 / 30 / 10**. The accent marks the focal point or a single key word, not everything. Contrast rules from `step-3-design.md` still apply.

## 7. Readable at real viewing size
Know how big the image is actually seen (`snap-x formats <id>` notes): YouTube thumbnails ~200 px wide, covers on phones, stories full-screen. **Squint test:** view the render downscaled to that size; if the headline doesn't read, the design fails.

## 8. Consistency across a pack
Every image in a pack shares fonts, palette, spacing unit, logo treatment and corner radius, so the set reads as one brand. Series (episodes, products, locales) share one layout; only the data changes.

## 9. Archetypes: choose one on purpose
Pick an archetype per format in the plan instead of improvising. Vary archetypes across a pack when formats differ; keep one archetype across a series.

| Archetype | Use for | Shape |
|---|---|---|
| **Big type** | OG, covers, thumbnails without imagery | Headline dominates (≥ 40% of height), logo small in a corner |
| **Split** | OG, feature graphics, banners with a visual | Text on one side (~55%), visual/product/mock on the other |
| **Centred badge** | Announcements, releases, events | Short centred headline, a pill/badge above, logo below |
| **Device mock** | App Store / Play screenshots, product launches | Caption on top (≤ 2 lines), device or UI frame below |
| **Quote card** | Testimonials the user supplied, talks, posts | Large quote, attribution line, generous margins |
| **Stat card** | A real number from the source | One huge number, one-line label, context below |

Stat and quote cards need real data from the source or the user (facts-only rule).

## Render review (Step 4)
For each rendered image, score 1–3 on: focal point, hierarchy, spacing/alignment, contrast, squint test, pack consistency. Fix anything scoring 1 before delivering, and record the scores in `snap-plan.md`.
