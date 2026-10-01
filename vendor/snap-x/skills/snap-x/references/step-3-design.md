# Step 3: Write the design files

One `.mjs` per format in `designs/`. Each file is a self-contained Satori tree — hardcode the copy you settled in Step 2. Nothing is passed in and there is no config.

**Always write `designs/_brand.mjs`** and import it from every design in the pack — see "The brand file" below. It's a normal `_`-prefixed helper the user owns (PRINCIPLES.md §2), not a config file: it's just the pack's own colors/fonts/logo/spacing written once instead of copy-pasted into every file.

## Rules (Satori)

- Every container needs `display: "flex"` (no block/grid/inline). `children` is always an array; text is a string in it: `children: ["Hello"]`.
- `position: "absolute"` works; `position: "fixed"`, `z-index`, CSS grid and animations don't (layer with DOM order).
- The root node needs an explicit `width`/`height` matching `FORMAT`. Every `undefined` style value crashes the render — omit the key instead.
- For a sharp `@2x`/`@3x` export, use `snap-x render --scale <n>` (see Step 4) — no design-file change needed. `transform: scale(n)` (with `transformOrigin`) still works if a size genuinely needs a *different* layout, not just a sharper export of the same one.

## The brand file

`designs/_brand.mjs` — written once in Step 3, imported by every design file in the pack. Files starting with `_` are never rendered (skipped even when the shell expands `designs/*.mjs`).

```js
// designs/_brand.mjs — helper, not rendered
export const FONTS = [{ family: "Saira", weights: [400, 700, 900] }]; // omit per-file → Inter 400/700/900
export const COLORS = { bg: "#000000", text: "#f5f5f5", accent: "#eb1d25" };
export const LOGO = "../assets/logo.png"; // relative to the design file that imports it — see step-1-inspect.md
export const SPACING = 8;    // base unit at ~1200px wide — design-principles.md § Spacing system
export const TYPE_SCALE = { headline: 72, support: 32, detail: 20 }; // ≈ 3:1.5:1 — design-principles.md § Hierarchy
export const RADIUS = 12;
```

## File shape

```js
import { COLORS, FONTS as F } from "./_brand.mjs";

export const FORMAT = { width: 1200, height: 630, name: "og.png" };
export const FONTS = F;

export default function () {                    // zero arguments; may be async
  return {
    type: "div",
    props: {
      style: { width: 1200, height: 630, background: COLORS.bg, display: "flex", fontFamily: "Saira", position: "relative", overflow: "hidden" },
      children: [ /* … */ ],
    },
  };
}
```

A static tree (`export default { type: "div", … }`) also works.

**Beyond the brand file:** a `_helper.mjs` can also hold an icon set, or a composition rendered several ways (1×, @2×, QA) — same rule, same import pattern. Each entry file still exports its own `FORMAT` and `FONTS`.

## A series → one design with VARIANTS, not one file per image

When a pack needs the same layout repeated with only the data changing (an episode series, a batch of product banners, localized screenshots), export `VARIANTS` instead of writing `episode-1.mjs`, `episode-2.mjs`, … :

```js
export const FORMAT = { width: 1280, height: 720, name: "episode.png" };
export const VARIANTS = [
  { id: "ep-01", title: "Setting up", number: 1 },
  { id: "ep-02", title: "First render", number: 2 },
];

export default function (variant) {           // called once per row when VARIANTS exists
  return { /* tree using variant.title, variant.number */ };
}
```

- Every row needs a unique string `id`. Output is named `<name-stem>-<id>.<ext>` (e.g. `episode-ep-01.png`) — unless a row sets its own `format: { name: "…" }` (useful for a localized screenshot that needs a different name or size than the rest of the series).
- `snap-x check` and `snap-x guides` run every row and label failures with the row's id.
- `snap-x render designs/episode.mjs --only ep-01` renders a subset while iterating.
- A design without `VARIANTS` behaves exactly as before — only reach for this when a real series exists; don't add `VARIANTS = [{ id: "x" }]` for a single one-off image.

## Fonts

- `FONTS` per file: any Google Font and weights. `fontWeight` must be one you declared. A font that can't be fetched falls back to Inter with a warning — check the render if you see it.
- Non-Latin copy (Japanese, Korean, Arabic, Hebrew, Thai, Devanagari, Bengali, …) gets a Noto fallback automatically; no extra entry needed.
- **Code-like copy** (`LucideIcons.heart`, commands, file names) needs a monospace font in `FONTS` (e.g. JetBrains Mono): sans fonts confuse `I` / `l` / `1`, so "LucideIcons" can read as "Lucidelcons".

## Glyphs: draw, don't type, anything the font might lack

**Emoji work** — snap-x draws them as Twemoji images (fetched once, cached, works offline afterwards). Other characters the loaded fonts don't contain still render as a **blank box** and Satori doesn't error — `snap-x check` *warns* about them (`no loaded font has: "◷" …`); don't ignore the warning. `✓ ◷ ∎` and even `→` / `↓` fail in some fonts (e.g. Poppins has none of those). Use instead:
- an inline SVG for arrows, stars, chevrons, icons; a CSS circle for bullets; numerals or letters in icon squares
- only glyphs you have seen render — then verify in Step 4

```js
{ type: "svg", props: { width: 24, height: 24, viewBox: "0 0 24 24", fill: "none", stroke: accent, strokeWidth: 2,
  strokeLinecap: "round", strokeLinejoin: "round", children: [{ type: "path", props: { d: "M6 9l6 6 6-6" } }] } }
```

**A real icon set (Lucide, Heroicons, …):** don't hand-convert SVG markup into nodes. Download the `.svg` files and embed each as an `<img>` data URI (`asset("../assets/heart.svg", "image/svg+xml")`, see below). SVGs using `stroke="currentColor"` render black inside an `<img>` — replace `currentColor` with your hex in the file text first (`svgText.replaceAll("currentColor", "#f5f5f4")`) and embed the result as `data:image/svg+xml;base64,…`. Icon SVGs with no `<text>` work fine this way.

## Fit the text

Oversized headlines wrap mid-word and shove everything off the canvas. For each headline line:
- set `whiteSpace: "nowrap"` and size it so it fits: bold display type is roughly **0.5 em per character** (heavy condensed like Saira 900 ≈ 0.48, wide like Poppins 800 ≈ 0.52, with tight tracking). Longest line ≤ available width ÷ (0.5 × chars).
- if it wraps or the layout collides after rendering, reduce the size — don't add more wrapping
- `nowrap` collapses the space before an adjacent coloured `<span>`/text node ("your" + "HTML." → "yourHTML."): use `whiteSpace: "pre"` on that line, or put the pieces in a flex row with `gap`
- long paragraphs: `flexWrap: "wrap"` plus a `maxWidth`
- **Keep text off decoration.** Suns, hills, blobs, rings and phone mocks are the usual culprits: a big shape behind a headline hides letters or kills contrast ("together" half-covered, cream text on an orange sun). Put decoration in its own region (a corner, the bottom edge), or keep it well behind and low-contrast, and check every text/shape overlap when you look at the render

## Sizes, platforms and alpha

Pick sizes with `snap-x formats` and read `references/formats.md` for layout by platform (YouTube thumbnails, banners, Play Store and App Store screenshots …). **App Store and Google Play graphics need `alpha: false` in `FORMAT`** — `check` warns if it's missing.

## Logos and local assets

Embed the files you saved in Step 1 as base64 `<img>` nodes, resolving paths from the **design file** so it renders from any directory:

```js
import fs from "fs/promises";
import { fileURLToPath } from "url";

const asset = async (rel, mime) =>
  `data:${mime};base64,${(await fs.readFile(fileURLToPath(new URL(rel, import.meta.url)))).toString("base64")}`;

export default async function () {
  const logo = await asset("../assets/logo.png", "image/png");   // assets/ sits beside designs/
  // { type: "img", props: { src: logo, width: 231, height: 44, style: { display: "flex" } } }
}
```

- `width` AND `height` from the file's real aspect ratio — never stretch a logo.
- A dark logo on a dark card vanishes: use the light variant, or set the mark on a ring/pill. Round icons: wrap the `<img>` in a `borderRadius: 999`, `overflow: "hidden"` box (add a thin accent ring if it's near the background).
- PNG/JPEG/SVG only (no AVIF/WebP); rasterise SVGs that contain `<text>` — see Step 1.

## Color and contrast

Hardcode the brand's palette. Measure contrast instead of eyeballing it:

```bash
node -e "const L=h=>{const c=[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)/255).map(v=>v<=.03928?v/12.92:((v+.055)/1.055)**2.4);return .2126*c[0]+.7152*c[1]+.0722*c[2]};const r=(a,b)=>{const[x,y]=[L(a),L(b)].sort((p,q)=>q-p);return ((x+.05)/(y+.05)).toFixed(1)};console.log(r('#fff3e0','#0f2e1f')+':1')"   # text hex, background hex
```

Body text needs ≥ 4.5:1 against its background (large text ≥ 3:1); compute it if unsure — muted greys on black are the usual failure. Keep one accent dominant.

## Check, then fix

Run `npx -y @snap-x/cli check designs/*.mjs`. Common failures:
- `display:"block"|"grid"` → `"flex"`; `position:"fixed"` → `"absolute"`
- "Satori render failed" → a `fontWeight` not in `FONTS`, an `undefined` style value, or a bad image data URI
- `check` passing does **not** mean it looks right — that's Step 4
