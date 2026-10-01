# Principles

Ten rules. Tufte's own words where they're canonical (in quotes). The rest is the practical interpretation for someone building a chart right now.

---

## 1. Show the data

> "Above all else show the data." — VDQI, p. 92

The most important thing in any data graphic is the data. Everything else — gridlines, titles, axes, labels, legends, frames, color, shapes — is overhead that competes for attention. Decisions about overhead should be made by asking "does this help the reader see the data, or does it get in the way?"

Practical application: when in doubt, take it out. The chart that survives aggressive subtraction is almost always better than the one that survives addition.

---

## 2. Maximize the data-ink ratio

> "Maximize the data-ink ratio, within reason." — VDQI, p. 96

Data-ink is ink (or pixels) that would change if the data changed. Non-data-ink is everything else: the box around the chart, the gridlines, the tick marks, the axis-line that exists just because charts have them. The ratio of data-ink to total ink should be high.

Practical application: ask of every visual element "if I changed the underlying data, would this change?" If not, it's a candidate for deletion.

---

## 3. Erase non-data-ink

> "Erase non-data-ink, within reason." — VDQI, p. 96

The corollary to maximizing the ratio. Tufte's redrawn examples typically remove 50-65% of the ink in a published scientific chart without losing any information.

Practical application: drop the chart border, drop the gridlines (or fade them to near-white), drop ticks at minor units, drop the axis line where the data doesn't reach (use a range frame). Replace cross-hatching with light gray fills.

---

## 4. Erase redundant data-ink

> "Erase redundant data-ink, within reason." — VDQI, p. 100

A bar chart's bar communicates its value six ways: left edge height, right edge height, top edge position, shading height, label position, label content. Five of those are redundant. Same value, said five times louder, is not louder; it's noise.

Practical application: pick one encoding per quantity. A number with a sparkline is two encodings of one thing — both useful, both used differently. A bar with its value printed on top *and* gridlines *and* an axis label *and* a colored fill is one thing repeated.

---

## 5. Graphical integrity — never lie

A graphic has integrity when the visual representation matches the numerical reality. The "lie factor" is the ratio of effect-size-in-graphic to effect-size-in-data. Anything outside 0.95-1.05 is a lie.

Concrete violations:
- Truncated y-axes that exaggerate change (small movement looks dramatic)
- Area encoding a one-dimensional value (a circle "twice as big" by radius is four times as big by area)
- 3D perspective that compresses distant bars
- Inconsistent scales across small multiples that look comparable but aren't
- Dual-axis charts that invite false correlation

Practical application: y-axis starts at zero for bar charts. For line charts where zero isn't meaningful, label the baseline explicitly so the reader sees the truncation. Never use area or volume to encode a single number.

---

## 6. Use small multiples for any cross-cut

> "At the heart of quantitative reasoning is a single question: Compared to what?" — VDQI, p. 67

If you have one variable changing over time and a second dimension (region, segment, cohort), don't overlay six lines on one chart. Make six small charts, identical scales, lined up. The eye reads parallelism faster than it untangles overlap.

Practical application: any time you're about to add a second line, a stacked bar, or a dual axis — ask whether two small charts side by side would be clearer. Almost always: yes.

---

## 7. Layering and separation

The visual layers of a chart should be ordered by importance. Data on top, labels next, scaffolding (axes, gridlines) faintest. When two elements interact and create unintended visual noise (Tufte calls it "1+1=3"), one of them is too heavy.

Practical application: gridlines white on light gray, or omit. Axes thin and gray, not black. Data in solid black or a single accent color. Type set in a clean sans-serif at 11-13px for labels, never bold unless it's the focal value.

---

## 8. Micro/macro readings

> "To clarify, add detail." — *Envisioning Information*

A good chart works at two scales. From across the room: one shape, one story. Up close: every individual data point legible. Bad charts force you to choose between density and clarity. Good ones reward proximity.

Practical application: use range frames so the chart fills the data's actual extent, not arbitrary round numbers. Show all data points where possible (no hiding behind summary lines unless the points are also drawn). Label the salient ones directly.

---

## 9. The smallest effective difference

> "Make all visual distinctions as subtle as possible, but still clear and effective." — *Visual Explanations*, p. 73

The contrast between two visual elements should be the minimum needed to distinguish them. Loud contrast fatigues the eye and competes with data. Quiet contrast lets the reader's attention rest on what matters.

Practical application: don't separate two categories with red vs blue when light gray vs dark gray does the job. Reserve high-contrast color for the one or two values you actually want the reader to focus on.

---

## 10. Word-data integration

Charts should sit inside sentences, not float in boxes labeled "Figure 1." Numbers should appear next to their visual representation. Sparklines belong in tables, in paragraphs, on dashboards next to the value they summarize.

Practical application: a row in a table can carry the number, a one-word label, and a tiny sparkline. That's a complete data graphic. No frame needed. Many small graphics beat one big one.

---

## The conclusion (Tufte's own five-line summary, VDQI p. 105)

> Above all else show the data.
> Maximize the data-ink ratio.
> Erase non-data-ink.
> Erase redundant data-ink.
> Revise and edit.
