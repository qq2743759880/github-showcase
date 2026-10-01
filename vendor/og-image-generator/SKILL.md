---
name: OG-image-generator
description: Build a custom Open Graph image editor for the current website. Detects the site's design tokens, fonts, and logo from source, then emits a standalone HTML + JS Canvas editor with the universal OG controls (headline, sub, brand, logo, theme, export PNG) plus any site-specific extras the source actually warrants. Use when the user asks to build an OG image generator, social card editor, or "the social cards thing" for their site.
---

# /OG-image-generator

Build an Open Graph image editor tailored to the current website. The editor reuses the site's real colors, fonts, and logo so the exported PNG looks like the site — not like a generic OG template.

Deliverable: a two-pane browser tool — canvas preview on the left, control panel on the right. Runs under the project's existing dev server. No new dependencies.

## What makes a good OG image

The editor must make these easy to honor and hard to violate.

- **1200 × 630 px (1.91:1).** The Facebook / LinkedIn / Open Graph standard. Twitter `summary_large_image` cards use the same. This is the one size every editor must ship.
- **Safe zone: center 1080 × 540.** Some surfaces crop edges. Keep critical content centered.
- **Legibility at thumbnail size.** Feeds display OG cards at ~500 px wide. Default headline 60–90 pt; sub 24–32 pt. Anything smaller blurs out.
- **Brevity.** Headline ≤ 10 words / ≤ 60 chars. Sub ≤ 20 words. Total text ≤ 40 words. Walls of text are unreadable as thumbnails.
- **One focal point.** Headline + brand mark is enough. Don't cram a hero illustration *and* a sub *and* a feature list.
- **Contrast ≥ 4.5:1.** A semi-transparent dark wash over busy backgrounds is the cheap fix.
- **Brand presence.** Logo + wordmark in a corner (typically bottom-left), recognizable at thumbnail scale.
- **Match the site's identity.** Same fonts, same palette, same wordmark. Don't reach for "more designy" choices.

## What makes a good OG editor

- **Live preview at native resolution.** Canvas is 1200 × 630 in pixels; CSS scales it to fit. WYSIWYG.
- **A handful of controls, not a dashboard.** Anything beyond the universal set below is feature creep for an OG card.
- **Sensible defaults pulled from the site.** Don't make the user re-type their headline.
- **One-click PNG export at native resolution.**
- **Reset to defaults** — recovery from experimentation.

## Controls every generated editor includes

Universal — every site needs these, no exceptions:

- **Headline** (textarea)
- **Subhead** (textarea, can be empty)
- **Brand name** (text input)
- **Show logo** (checkbox)
- **Theme** (select — derived from the site's palette; typically one or two options like "Dark on brand" / "Light on brand". Single-theme sites get a single option and the select can be hidden.)
- **Export PNG** button
- **Reset to defaults** button

That's the entire default control panel. Five fields and two buttons.

## Conditional controls — principles, not a checklist

The universal panel above is enough for most sites. A typical clean SaaS landing page with a single-tone background and no animation needs nothing more — its editor is the universal panel and that's a perfectly good editor.

For sites with distinctive visual treatments, add **one extra control per treatment**. Never more. The job is to pick the right kind of control for what the site actually does — not to work through a checklist.

### Principles

- **One control per treatment, not one per parameter.** A noise-grain overlay gets one intensity slider, not separate sliders for amplitude, frequency, and color. The user wants vibe control, not engineering control.
- **Pick the most expressive dial.** Animated background? A frame/time slider beats a play/pause button. CRT overlay? A single intensity slider beats stripe-spacing + opacity + color.
- **Default each control to the value that produces the homepage hero look.** The editor should open with the composition that already exists on the site, not a blank state.
- **Match the control type to the treatment category:**

  | Treatment category                              | Control type             |
  |-------------------------------------------------|--------------------------|
  | Time-based (animation, drift, particle motion)  | Frame / time slider      |
  | Level-based (grain, blur, scanlines, vignette)  | Intensity slider (0–100) |
  | Discrete modes (day/night, hero/footer, themes) | Variant select           |
  | Per-glyph styling (hero h1 word emphasis)       | `[[word]]` markup        |
  | Optional decorations (status pill, badge, tag)  | Checkbox                 |
  | Resolution / scale (pixel-art, halftone)        | Single integer slider    |

- **Skip controls for treatments that exist but aren't expressive.** A site with a static gradient doesn't need hex inputs — the gradient is already correct. A site with a glass-blur overlay nobody would tune doesn't need a blur slider — bake it in.
- **When in doubt: leave it out.** The user can ask. You can't undo dashboard creep.

### Worked example — a typical site

Clean SaaS landing page. Sans-serif h1 over a single-tone background. No animation, no overlays. No hero-h1 word emphasis.

Editor controls: **the universal panel. Nothing else.**

### Worked example — a maximalist site (loisa.ai)

The loisa site is unusually rich: pixel-art rendering, animated agents wandering a sunset scene, CRT scanlines + vignette + flicker overlays, a hero h1 with chromatic-aberration ghosts on specific words, a footer "All systems normal" status pill.

Applying the principles above, its editor adds, on top of the universal panel:

- **Variant select** — hero day band vs. footer night scene (two distinctive discrete modes)
- **Frame slider** — drives agents, clouds, sun shimmer (time-based animation)
- **Pixel-size slider** — the page's signature is pixel-art chunkiness (resolution/scale)
- **Scanlines intensity slider** — the signature CRT effect (level-based overlay)
- **Darken-wash slider** — busy background needs legibility help (level-based overlay)
- **`[[word]]` markup** — the h1 emphasizes specific words (per-glyph styling)
- **Status pill toggle** — "All systems normal" is part of the voice (optional decoration)

Seven extras. **That's about the most any site should need.** If you find yourself adding more than this for a single site, you're exposing engineering knobs instead of vibe controls — back up.

The loisa list is one site's manifestation of the principles, not the canonical conditional set. Different sites will warrant different controls drawn from the same principles.

## Workflow

### 1. Survey the repo

Detect the framework so the editor file lands somewhere the dev server will serve it:

- Look for `vite.config.*`, `next.config.*`, `astro.config.*`, `nuxt.config.*`, `svelte.config.*`, `eleventy.config.*`, `gatsby-config.*`, or plain `index.html` at root.
- Read `package.json` `scripts` for the dev command.
- Identify the homepage shell and its CSS entry.

State one line about what you found before writing files.

### 2. Extract design tokens

From the main CSS:
- `:root` CSS custom properties — palette, ink, surface, border, hairline. Capture names AND values.
- Body/heading font-family declarations.

From `<head>`:
- Google Fonts `<link>` URLs — **copy verbatim into the editor's `<head>`**.
- `@font-face` declarations — if self-hosted, reference the same source files.

From config files:
- `tailwind.config.*` — read `theme.colors`, `theme.fontFamily`.
- CSS-in-JS theme objects (styled-components / Emotion / Chakra) — find and extract.

Build a tokens dict the renderer will reference:
```js
const TOKENS = {
  ink:    "#…",  // text/foreground
  bg:     "#…",  // canvas base
  surface:"#…",  // optional secondary
  accent: "#…",  // optional brand pop color
};
```

### 3. Find the logo

Search in this order. Take the first solid match:

1. **Inline SVG** in the page header / nav / footer — often the wordmark or icon mark.
2. **`<link rel="icon">`** and **`<link rel="apple-touch-icon">`** — read `href`, prefer SVG.
3. **Common file locations** — search `public/`, `static/`, `assets/`, `src/assets/` for files matching `logo.*`, `mark.*`, `brand.*`, `wordmark.*`, `icon.*`.
4. **Components named** `Logo`, `Brand`, `Wordmark`, `Mark` in `src/components/` or equivalent.
5. **`<meta property="og:image">`** — note for reference but don't use it as the logo (it IS an OG image).

Preference: **inline SVG > SVG file > PNG file > favicon.ico**.

Embed in the editor by format:
- **Inline SVG**: capture source as a string, render via `Image()` with a `data:image/svg+xml;base64,…` src.
- **SVG file**: load via `Image()` with the file path.
- **PNG file**: load via `Image()`, `drawImage` once `complete`.
- **ICO**: extract a frame and treat as PNG.
- **None found**: text wordmark fallback in the brand font, and tell the user.

Default placement: **bottom-left, 56 px inset, logo mark height 36–48 px, brand name 28 px to its right, vertically centered with the mark.**

### 4. Find conditional treatments

Walk the conditional-controls table above. For each row, decide based on actual source evidence whether to include the control. If you're not sure, leave it out.

### 5. Extract sample copy

From the homepage hero:
- h1 → default Headline (strip emphasis markup unless you decided to add the emphasis control)
- Sub/lede paragraph → default Subhead
- Wordmark text → default Brand

Don't seed copy fields with placeholder text like "Your headline here". Use the site's real copy as defaults.

### 6. Pick the editor location

| Framework         | Editor HTML path              | URL after `npm run dev`              |
|-------------------|-------------------------------|--------------------------------------|
| Vite              | `og.html` at root             | `/og.html`                           |
| Next.js (app)     | `app/OG-image-generator/page.tsx`      | `/OG-image-generator` (with `'use client'`)   |
| Next.js (pages)   | `pages/OG-image-generator.tsx`         | `/OG-image-generator`                         |
| Astro             | `src/pages/og.astro`          | `/og`                                |
| Eleventy          | `og.html` in input dir        | `/og/`                               |
| Plain static      | `og.html` at root             | `/og.html`                           |

JS renderer goes alongside the site's other modules (`src/og.js` for Vite, etc.).

### 7. Generate the editor

**HTML shell**
- Two-pane grid (canvas-wrap left, sticky controls right).
- Webfont `<link>` tags in `<head>` — Canvas `fillText` only respects loaded fonts.
- Use the site's own fonts in the controls panel UI too.

**JS renderer**
- `state` object holding defaults.
- `render()` pipeline: clear → background → (optional overlays) → (optional darken wash) → headline → sub → brand+logo → (optional status).
- Helpers: `drawHeadline`, `drawSub`, `drawBrand` (handles logo + name); conditional helpers only if their treatment is present.
- `exportPNG()` — pause animation, render still, `canvas.toBlob` → download.
- After `document.fonts.ready`, re-render so first paint uses real webfonts.

### 8. Verify

Start the dev server, open the editor URL, confirm: canvas renders at 1200 × 630, webfonts are loaded (not fallback), all controls update the preview, logo appears, export downloads a valid PNG at 1200 × 630.

If the logo is wrong size or wrong file, iterate once before declaring done.

## Architecture reference

### Canvas at native resolution

```html
<canvas id="ogCanvas" width="1200" height="630"></canvas>
```

```css
.canvas-wrap { aspect-ratio: 1200 / 630; max-width: 1200px; }
#ogCanvas    { display: block; width: 100%; height: 100%; }
```

Canvas keeps native pixel size; CSS scales the wrapper. `toBlob` exports at full resolution.

### State + render pipeline

```js
const W = 1200, H = 630;

const DEFAULTS = {
  headline: "…",          // from the site's homepage h1
  sub:      "…",          // from the site's lede
  brand:    "Brandname",  // from the site's wordmark
  showLogo: true,
  theme:    "default",
};
const state = { ...DEFAULTS };

function render() {
  ctx.clearRect(0, 0, W, H);
  drawBackground();
  drawHeadline(padX, headlineY, headlineSize, W - padX * 2);
  drawSub(padX, subY, W - padX * 2);
  drawBrand(padX, H - 96);
}
```

### Logo render — image file

```js
const logo = new Image();
logo.crossOrigin = "anonymous";
logo.src = "/logo.svg";          // or whatever was detected
logo.onload = () => render();

function drawBrand(x, y) {
  if (state.showLogo && logo.complete && logo.naturalWidth > 0) {
    const h = 40;
    const w = logo.width * (h / logo.height);
    ctx.drawImage(logo, x, y, w, h);
    ctx.font = '500 28px "Brand Font", sans-serif';
    ctx.fillStyle = TOKENS.ink;
    ctx.textBaseline = "middle";
    ctx.fillText(state.brand, x + w + 14, y + h / 2);
  } else {
    ctx.font = '500 32px "Brand Font", sans-serif';
    ctx.fillStyle = TOKENS.ink;
    ctx.textBaseline = "top";
    ctx.fillText(state.brand, x, y + 4);
  }
}
```

### Logo render — inline SVG via data URI

```js
const svgSrc = `<svg xmlns="http://www.w3.org/2000/svg" …>…</svg>`;
const logo = new Image();
logo.src = "data:image/svg+xml;base64," + btoa(svgSrc);
logo.onload = () => render();
```

### Headline wrap

Default: left-aligned, top-left of the canvas with a generous left/right pad.

```js
function drawHeadline(x, y, size, maxWidth) {
  ctx.save();
  ctx.font = `600 ${size}px "Headline Font", sans-serif`;
  ctx.fillStyle = TOKENS.ink;
  ctx.textBaseline = "top";
  const lineHeight = size * 1.08;
  const lines = wrapText(state.headline, maxWidth);
  let cy = y;
  for (const line of lines) { ctx.fillText(line, x, cy); cy += lineHeight; }
  ctx.restore();
  return cy;
}
```

### PNG export

```js
function exportPNG() {
  canvas.toBlob((blob) => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${state.brand.toLowerCase().replace(/\s+/g, "-")}-og.png`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }, "image/png");
}
```

### Fonts ready

```js
render();
if (document.fonts?.ready) document.fonts.ready.then(() => render());
```

### Word-emphasis markup (only if added)

If you decided the site emphasizes hero h1 words, expose `[[word]]` markup. The tokenizer emits `{text, em}` runs per line; render emphasized runs in the site's accent color. Match the site's actual hero treatment — don't impose a specific recipe (no chromatic ghosts unless the source has them).

## Constraints

- **Don't invent treatments.** Flat sites get flat editors. No CRT scanlines because they look cool. No frame slider when the background isn't animated.
- **One canvas size: 1200 × 630.** Don't ship multi-format unless the user explicitly asks.
- **Reuse real code.** If the site has a hero renderer in JS, import it directly. Don't reimplement.
- **Webfonts in `<head>`.** Canvas `fillText` only respects loaded fonts.
- **Re-render after `document.fonts.ready`.** First paint shouldn't be in fallback fonts.
- **Default layout works everywhere.** Headline top-left, sub below, brand+logo bottom-left. Don't redesign per site.
- **Keep the controls panel short.** Headline, Sub, Brand, Show logo, Theme, Export, Reset. Add nothing else unless the source warrants it.
- **Logo placement is bottom-left by default.** Move it only if the site's hero composition strongly suggests otherwise.

## Output report

After generating, tell the user:

- Files written and their paths
- Editor URL
- Tokens / fonts pulled from source — name them, don't say "extracted tokens"
- **Logo source**: file path and format, or "no logo found, used text wordmark fallback"
- Which conditional controls were added and **why** ("added emphasis markup because hero h1 uses `<em>` styling for the word 'coworker'")
- Anything to verify ("I assumed `--accent-pink` is the emphasis color — correct me if wrong")
