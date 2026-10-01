# Kill list

Things to remove from any Tufte-compliant chart unless the user explicitly overrides.

## Visual decoration

| Kill | Why | Replace with |
|---|---|---|
| Drop shadows | Add ink, encode nothing | Nothing |
| Gradient fills on bars | Imply variation that isn't in the data | Flat fill |
| Bevels, glow, embossing | Pure chartjunk | Flat shapes |
| 3D bars / pies / surfaces | Distort comparison, hide bars behind bars | 2D version |
| Background images behind data | Compete with data | White or near-white background |
| Patterned fills (stripes, dots, crosshatch) | Moiré vibration | Gray tints |
| Icons inside data marks | Decoration as encoding | Direct labels |

## Chart types to avoid

| Kill | Why | Replace with |
|---|---|---|
| Pie chart | Humans read angles badly | Sorted bar or small table |
| Donut chart | Same as pie, plus the hole | Sorted bar |
| 3D pie | All sins of pie, amplified | Sorted bar |
| Radar / spider chart | Area encodes nothing meaningful | Small multiples or sorted bar |
| Funnel chart with 3D taper | Visual taper exaggerates drop-off | Horizontal bars by stage |
| Bubble chart for one variable | Area is hard to compare | Bar or dot plot |
| Word cloud | Frequency by font size is unreadable | Sorted bar |
| Stacked area for many categories | Top categories distort by middle ones moving | Small multiples |

## Axis and grid

| Kill | Why | Replace with |
|---|---|---|
| Dual y-axis | Implies correlation that may not exist | Two small charts side by side |
| Heavy black gridlines | Compete with data | Light gray, or omit |
| Tick marks at every minor unit | Visual noise | Ticks at labeled values only |
| Chart border / frame box | Non-data-ink | Range frame (axes only span data) |
| Y-axis truncated without note (on bars) | Lie factor | Start at zero, or use a line chart |
| Logarithmic scale without label | Confuses the reader | Label clearly; consider linear with annotations |

## Labels and legends

| Kill | Why | Replace with |
|---|---|---|
| Legend placed away from data | Forces eye to look up colors | Direct labels next to data |
| Color-coded legend with 7+ items | Beyond working memory | Small multiples or direct labels |
| Title bar with chart background color | Pure decoration | Plain text title, left-aligned |
| All-caps headers | Harder to read | Sentence case or title case |
| Bold + italic + underline on same label | One emphasis level at a time | One emphasis, applied sparingly |

## Color

| Kill | Why | Replace with |
|---|---|---|
| Rainbow / jet scale for ordered data | Hue is not ordinal; viewers misread | Sequential single-hue (light to dark) |
| Red + green only (deuteranopia) | 8% of men can't read it | Add value/luminance difference |
| Saturated color on every bar | Fatigues eye, kills hierarchy | Gray for context, accent for focal |
| More than 4 colors in one chart | Overload | Group small categories or use small multiples |
| Color as decoration only | Meaningless visual difference | One color, used to signal |
| Accent declared but never applied (all-gray, all-ink output) | Reads as flat; no point of focus | Apply the accent to the one focal data point |
| Bare bars where the value, not the magnitude bar, is the message | Flat, heavy | Dot plot with a labeled point |

## Dashboard sins (specific)

| Kill | Why | Replace with |
|---|---|---|
| Giant KPI tile with no context | Number alone tells nothing | Number + sparkline + delta |
| Gauges / speedometers | Half the chart is empty space | Number + threshold marker |
| Traffic-light status circles only | Coarse encoding | Number + colored dot + threshold |
| Identical-looking charts in a grid (different scales) | Reader assumes comparable | Shared scale or annotation |
| Animated transitions for static data | Disorienting | Static layout |

## Numbers in text

| Kill | Why | Replace with |
|---|---|---|
| "approximately ~around 4.2M" | Hedge soup | "4.2M" |
| "4,200,000" in body text | Hard to scan | "4.2M" |
| Two decimal places on counts | False precision | Integer |
| Mixing % and pp without distinction | Confuses reader | "up 3 percentage points" vs "up 3%" |
