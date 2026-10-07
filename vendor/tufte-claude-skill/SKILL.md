---
name: tufte
description: Apply Edward Tufte's principles to any data visualization, chart, dashboard, or infographic. Use when the user asks to produce, design, critique, or improve a chart, graph, dashboard, KPI tile, table-with-data, sparkline, small multiple, time series, distribution plot, choropleth, or any other visual that communicates quantitative or categorical information. Also triggers on words like "visualize", "viz", "data viz", "chart", "graph", "dashboard", "infographic", "Tufte". Outputs Tufte-compliant designs in either self-contained HTML/SVG or React (Recharts/D3). Defaults to Tufte rules; user can opt out per chart.
---

# Tufte — visual display, by the book

This skill turns "make me a chart" into a Tufte-compliant chart. Distilled from *The Visual Display of Quantitative Information* (1983/2001), *Envisioning Information* (1990), and *Visual Explanations* (1997).

## What this skill produces

Two output stacks, selected by the user's project context:

1. **Self-contained HTML/SVG** — single file, inline SVG, no external deps. For one-offs, embeds, screenshots, slide decks.
2. **React (Recharts + D3 fallback)** — for projects that already use React. Recharts where the chart type fits; raw D3-in-React where it doesn't (slopegraph, sparkline-in-table, small multiples).

## How to use this skill

When invoked, work through these in order:

1. **Read `principles.md`** — 10 rules, one paragraph each. The whole frame.
2. **Use `chart-selection.md`** to pick the chart type from the user's data and goal. Don't reach for a chart you know; reach for the one this table prescribes.
3. **Apply `kill-list.md`** before rendering — strip the things that don't belong in any Tufte-compliant chart.
4. **Check `before-after.html`** when the user wants to see the difference. Six side-by-side examples covering the cases AI tools default to badly.
5. **Read `report-voice.md`** when the output is a report, recap, or slide with prose around the chart. The writing can ruin a clean chart. Plain business English, no em-dashes, no AI slop.
6. **Run `checklist.md`** before declaring the chart done. Twenty items, takes 30 seconds.

For a quick lookup, `cheatsheet.html` (and `cheatsheet.pdf`) is the one-page reference.

## Default behavior

Tufte rules apply by default. If the user explicitly requests something on the kill list ("I need a pie chart for this board deck because the CFO wants one"), comply, but note the Tufte alternative in a one-line comment in the code or the response.

## Prose around the chart

When the output is a report, recap, or slide, the text matters as much as the
chart. Write plain business English: no em-dashes, no drama or theatrics, no hype
verbs, no AI-slop jargon. Name every label and caption for the specific case, not
a placeholder. First the number, then what it means. See `report-voice.md` for
the full kill/keep list. A clean chart wrapped in slop reads as slop.

## The kill list, summarized

These are not in any Tufte-compliant chart unless the user explicitly overrides:

- 3D effects on any 2D quantity
- Pie charts (use a sorted bar or a small table)
- Dual-axis charts (use two small multiples instead)
- Rainbow color scales for ordered data (use sequential single-hue)
- Heavy gridlines, frame boxes, tick marks at every minor unit
- Drop shadows, gradient fills, bevels, glow, "ducks"
- Legends placed away from data (label data directly)
- Moiré patterns, cross-hatching, dense stippling
- Redundant data-ink (bar plus number plus axis plus gridline all showing the same quantity)
- KPI cards with giant numbers and no context

## The keep list

These belong in most Tufte charts:

- Direct labels on data (no legends)
- Sparklines next to numbers
- Small multiples for any cross-cut
- Range frames (axes only span where data exists)
- Subtle gridlines (white-on-light, or omit)
- A single accent color (`--accent` red), **actually applied to the focal data point** — not declared and left unused. Minimal ink is not the same as no signal. If nothing carries the accent, the chart is flat; pick the point the reader should look at and color it.
- Data marks where they aid reading: dots on line endpoints, dot plots in place of bare bars
- Sorted categories (rarely alphabetical, almost never as-input)
- Tables when n ≤ ~20 and exact values matter

## File index

| File | Purpose |
|---|---|
| `principles.md` | Tufte's 10 rules with practical interpretation |
| `chart-selection.md` | Data + goal → chart type decision table |
| `kill-list.md` | What to remove from any chart |
| `before-after.html` | Six side-by-side comparisons (open in browser) |
| `report-voice.md` | Prose rules for reports/recaps/slides (no slop, no em-dashes) |
| `checklist.md` | 20-item pre-publish check |
| `cheatsheet.html` | One-page printable reference |
| `cheatsheet.pdf` | Same, as PDF |
| `presets/html-svg.md` | Style tokens + a working SVG bar chart, line chart, sparkline, small multiple |
| `presets/react.md` | Recharts theme + D3 patterns for slopegraph, sparkline-in-table, small multiples |
