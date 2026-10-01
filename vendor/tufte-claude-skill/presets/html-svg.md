# Preset — HTML/SVG (self-contained)

For one-offs, embeds, screenshots, slide decks. No external dependencies. Inline SVG. Open the file in any browser.

## Style tokens

Drop this `:root` block into any chart. These are the Tufte palette and type defaults.

```css
:root {
  --ink:    #1a1a1a;   /* data, text */
  --paper:  #fafaf7;   /* background */
  --rule:   #d8d4cc;   /* dividers */
  --muted:  #8a857c;   /* captions */
  --accent: #b3261e;   /* the one focal color */
  --gray-1: #efece4;   /* faintest gridline */
  --gray-2: #c8c2b5;   /* light element */
  --gray-3: #6b665d;   /* secondary text */
}

.tick   { font: 12px/1 "SF Mono", "Berkeley Mono", monospace; fill: var(--gray-3); }
.label  { font: 15px/1.3 "Charter", Georgia, serif; fill: var(--ink); }
.value  { font: 16px/1 "SF Mono", monospace; fill: var(--ink); font-weight: 600; }
.value-focal { font: 16px/1 "SF Mono", monospace; fill: var(--accent); font-weight: 700; }
.axis   { stroke: var(--gray-3); stroke-width: 0.5; fill: none; }
.grid   { stroke: var(--gray-1); stroke-width: 0.5; }
```

Type sizes are deliberately generous: charts get read at a glance and on shared
screens, so default to readable, not cramped. Body text ≥ 14px, axis ticks ≥ 12px,
focal numbers ≥ 16px. Scale up for slides and dashboards, never down. Put the
accent on the one focal value with `.value-focal`.

## Sparkline (the smallest chart that works)

```html
<svg viewBox="0 0 120 30" width="120" height="30">
  <polyline fill="none" stroke="#1a1a1a" stroke-width="1.2"
    points="0,22 12,20 24,17 36,14 48,15 60,11 72,9 84,6 96,4 108,3 120,2"/>
  <circle cx="120" cy="2" r="2" fill="#b3261e"/>
</svg>
```

Inline sparkline next to a value:

```html
<span class="metric">
  <span class="num">780K</span>
  <svg class="spark" viewBox="0 0 80 16" width="80" height="16">
    <polyline fill="none" stroke="currentColor" stroke-width="1"
      points="0,14 10,13 20,11 30,9 40,8 50,6 60,4 70,3 80,1"/>
  </svg>
  <span class="delta">+12%</span>
</span>
```

## Dot plot (the default category chart)

```html
<svg viewBox="0 0 420 280" width="100%" height="260">
  <line x1="120" y1="40" x2="120" y2="240" class="axis"/>
  <text x="115" y="44" text-anchor="end" class="tick">500</text>
  <text x="115" y="244" text-anchor="end" class="tick">0</text>
  <line x1="120" y1="40" x2="400" y2="40" class="grid"/>

  <!-- one row per item, sorted desc -->
  <line x1="120" y1="60" x2="288" y2="60" stroke="#c8c2b5" stroke-width="0.5"/>
  <circle cx="288" cy="60" r="4" fill="#1a1a1a"/>
  <text x="115" y="64" text-anchor="end" class="label">Atlas</text>
  <text x="296" y="64" class="value">420</text>
</svg>
```

## Line chart with range frame

```html
<svg viewBox="0 0 420 280" width="100%" height="260">
  <!-- range frame: y-axis only spans actual data range -->
  <line x1="60" y1="60" x2="60" y2="220" class="axis"/>
  <text x="55" y="64" text-anchor="end" class="tick">800</text>
  <text x="55" y="224" text-anchor="end" class="tick">400</text>

  <!-- no gridlines (or one faint one) -->
  <line x1="60" y1="60" x2="380" y2="60" class="grid"/>

  <!-- the line -->
  <polyline fill="none" stroke="#1a1a1a" stroke-width="1.5"
    points="70,200 110,196 140,180 170,170 200,150 230,140 260,120 290,110 320,95 350,75"/>

  <!-- endpoints labeled, no markers in between -->
  <circle cx="70" cy="200" r="2" fill="#6b665d"/>
  <text x="70" y="216" class="tick" text-anchor="middle">Jan · 400</text>
  <circle cx="350" cy="75" r="3" fill="#b3261e"/>
  <text x="350" y="68" class="tick" text-anchor="middle" fill="#b3261e">Oct · 780</text>
</svg>
```

## Small multiples (the engine of comparison)

```html
<div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 14px;">
  <figure>
    <figcaption class="label">North · 420</figcaption>
    <svg viewBox="0 0 100 50">
      <polyline fill="none" stroke="#1a1a1a" stroke-width="1.2" points="..."/>
    </svg>
  </figure>
  <!-- repeat for South, East, West with IDENTICAL scales -->
</div>
```

Rules for small multiples:
- All panels share the same x and y scale
- Panels arranged in a meaningful order (by value, not alphabetical)
- One label per panel (the cross-cut variable)
- One shared title above the grid

## Sparkline-in-table (the dashboard replacement)

```html
<table style="border-collapse: collapse; font-family: Charter, serif;">
  <thead>
    <tr style="border-bottom: 0.5px solid #1a1a1a;">
      <th style="text-align:left; font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase; color: #6b665d;">Metric</th>
      <th style="text-align:right; font-size: 11px; text-transform: uppercase; color: #6b665d;">Now</th>
      <th style="text-align:center; font-size: 11px; text-transform: uppercase; color: #6b665d;">10mo</th>
      <th style="text-align:right; font-size: 11px; text-transform: uppercase; color: #6b665d;">vs Target</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Revenue</td>
      <td class="value" style="text-align:right;">$4.2M</td>
      <td><svg viewBox="0 0 80 16" width="80" height="16"><polyline fill="none" stroke="#1a1a1a" stroke-width="1" points="0,14 ..."/></svg></td>
      <td class="value" style="text-align:right;">+5% ↑</td>
    </tr>
  </tbody>
</table>
```

## Layout safety (never clip, never bleed)

The chart must fit its container with nothing cut off. Common failures and fixes:

- Set `width="100%"` and a `viewBox` on every `<svg>`; let it scale, don't hard-pin a pixel width that overflows narrow columns.
- Leave padding inside the `viewBox` for labels that extend past the plot (long category names, end-of-line value labels). Reserve ~120px left, ~40px right.
- Wrap multi-chart pages in a container with `max-width` and `margin: 0 auto`; keep `overflow: visible` on the SVG so labels are not chopped, and confirm the page itself has no horizontal scroll.
- For grids of cards or small multiples, use `grid-template-columns: repeat(auto-fit, minmax(...))` so cards reflow instead of bleeding off the right edge.
- Before declaring done, open the file in a browser at the intended width and confirm no label, axis, or value is clipped.

## What to never include

- `<svg>` with a `style="filter: drop-shadow(...)"` — chartjunk
- `<defs><linearGradient>` for bar fills — chartjunk
- `<rect>` chart border around the whole SVG — non-data-ink
- `<g class="gridlines">` with `stroke="#000"` or any saturated color
- Legend boxes when ≤ 4 series — label directly
