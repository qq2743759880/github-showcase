---
name: snap-x
description: Make branded graphics for any platform from a project, a website URL or a written brief — YouTube thumbnails and channel art, LinkedIn/X covers and banners, Instagram posts and stories, e-commerce and promo banners, App Store and Google Play graphics and screenshots, OG/social cards, README cards, posters — by writing self-contained Satori design files and rendering them to exact-size PNGs with snap-x (no browser). Use when the user says "/snap-x", "make OG images", "YouTube thumbnail", "LinkedIn banner/cover", "store screenshots", "sale banner", "social images for this project/site", or "snap this". Finds the brand's real logo, colors and fonts.
---

# /snap-x

Write self-contained Satori `.mjs` design files, render them with `snap-x`, and deliver a branded image pack. snap-x only renders — **you** decide what the images say and look like.

**Input:** a repo, a website URL, or a written brief. **Output:** PNGs (any size, any names) plus a plan and share notes.

```bash
npx -y @snap-x/cli check  designs/*.mjs
npx -y @snap-x/cli render designs/*.mjs --out <dir>
```

`/snap-x --font "Saira"` suggests a default font; every other choice (formats, colors, copy) is yours.

## Workflow — do the steps in order, read each reference first

| Step | Read | Gate |
|---|---|---|
| **1. Inspect** the source — copy, colors, fonts, **real logo/brand assets** | `references/step-1-inspect.md` | all 9 rubric answers; any logo you'll use is downloaded and looked at |
| **2. Plan** — hook, copy per format, palette, fonts, assets, safe zones; pick sizes with `snap-x formats` | `references/step-2-plan.md`, `references/formats.md` | `snap-plan.md` written with per-format specs |
| **3. Write** `designs/*.mjs` — one self-contained file per format | `references/step-3-design.md`, `references/design-principles.md` | `snap-x check` passes with zero errors |
| **4. Render, verify, deliver** — look at every PNG; `snap-x guides` for banners/thumbnails/stories | `references/step-4-render.md` | every image viewed and clean; `share-copy.txt` written |

## Non-negotiables

- **Facts only.** Use numbers, quotes and claims found in the source or given by the user. Never invent stats, customers or testimonials; label anything illustrative as mock.
- **Self-contained files.** Each design exports `FORMAT`, optionally `FONTS`, and a zero-argument default export (may be async). No config, nothing passed in — hardcode the brand's colors, fonts and copy.
- **Satori rules.** Every container `display: "flex"`; `children` is an array; no `z-index`, CSS grid, animations or `position: "fixed"`; never an `undefined` style value.
- **Real logos, never redrawn.** Find the official file (favicon, header logo, brand page), pick the variant for the card's background, save it in `assets/` with `SOURCES.md`. None found → a text wordmark. No third-party customer logos unless asked.
- **Emoji work; other symbols may not.** Emoji render as Twemoji images. A character the font lacks (`✓ ◷`, sometimes `→`) renders as a blank box — `check` warns; draw those as inline SVG or shapes.
- **Sources disagree?** Prefer the README/manifest over API blurbs and say which you chose in the plan.
- **Text never fights decoration.** Keep suns, shapes and phone mocks out from behind headlines (a shape covering letters is the most common defect) — check every overlap in the render.
- **Fit the text.** Headlines `whiteSpace: "nowrap"`, sized to the canvas (≈ 0.5 em per character for bold display type). Wrapped or clipped text means the size is wrong.
- **Look before you deliver.** `check` passing ≠ looks right. Open every rendered PNG and fix what you see. Never hand-write QA designs — `snap-x guides` draws the danger zones and the mobile crop.
- **Right size, right place.** Only the formats the project needs; get sizes and rules from `snap-x formats` (YouTube, X, LinkedIn, Instagram, Play Store, App Store …). **Store graphics need `alpha: false`.** Formats that list placement zones (`snap-x formats <id>`: covers, channel art, thumbnails, stories) get a `snap-x guides` check; the rest are checked by eye.

## Output layout

```
<out>/
  designs/*.mjs        the design files (helpers start with "_")
  assets/              logos + SOURCES.md
  *.png                the images (FORMAT.name)
  guides/              placement overlays + mobile crops (`snap-x guides`)
  snap-plan.md         Step 2
  share-copy.txt       Step 4 — where each image goes, what's mock, asset sources
```

Default `<out>` is `snap-output/` (use a timestamped folder if it exists). Keep QA renders out of `designs/`. Real examples: [`examples/`](../../examples) in the repo.

## Agents without this skill (MCP)

`@snap-x/mcp` exposes `render_designs`, `check_designs`, `preview_guides`, `list_formats` (`npx @snap-x/mcp`). The agent still writes the `.mjs` files following the same rules; the server only renders and validates.
