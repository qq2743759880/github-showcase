# Preset — React (Recharts + D3)

For React projects. Recharts where the chart type fits cleanly; raw D3-in-React (via `d3-scale`, `d3-shape`) for the cases Recharts handles badly.

## Theme tokens

```ts
// tufte-theme.ts
export const tufte = {
  ink: "#1a1a1a",
  paper: "#fafaf7",
  rule: "#d8d4cc",
  muted: "#8a857c",
  accent: "#b3261e",
  gray1: "#efece4",
  gray2: "#c8c2b5",
  gray3: "#6b665d",
  fontSerif: '"Charter", "Iowan Old Style", Georgia, serif',
  fontMono: '"SF Mono", "Berkeley Mono", monospace',
};
```

Type sizes default generous for readability: axis ticks ≥ 12px, labels ≥ 15px,
focal numbers ≥ 16px. Scale up for slides and dashboards, never down.

## Recharts — what fits, what doesn't

| Chart | Recharts? | Notes |
|---|---|---|
| Line chart | Yes | Strip gridlines, set range frame manually |
| Bar chart | Yes | But you almost always want a sorted dot plot instead — use D3 |
| Area chart | Sparingly | Only with a single series and meaningful baseline |
| Scatter | Yes | Disable grid, axis ticks at endpoints only |
| Pie | No | Replace with sorted bar |
| Radar | No | Replace with small multiples |
| Composed | No | Replace with two small multiples |
| Sparkline | Yes, trivially | Or write 10 lines of SVG; cheaper |
| Slopegraph | No | D3 |
| Dot plot | No | D3 |
| Small multiples | Via grid of `<LineChart>` | Or D3 inside grid |

## Recharts — Tufte-compliant LineChart

```tsx
import { LineChart, Line, XAxis, YAxis, ReferenceDot } from "recharts";
import { tufte } from "./tufte-theme";

const data = [
  { month: "Jan", mau: 410 }, { month: "Feb", mau: 432 },
  // ...
  { month: "Oct", mau: 780 },
];

const last = data[data.length - 1];

export function MAUChart() {
  return (
    <LineChart
      width={500}
      height={220}
      data={data}
      margin={{ top: 30, right: 60, bottom: 30, left: 30 }}
    >
      <XAxis
        dataKey="month"
        axisLine={{ stroke: tufte.gray3, strokeWidth: 0.5 }}
        tickLine={false}
        tick={{ fill: tufte.gray3, fontSize: 12, fontFamily: tufte.fontMono }}
        interval={9}  /* show first and last tick only */
      />
      <YAxis
        axisLine={{ stroke: tufte.gray3, strokeWidth: 0.5 }}
        tickLine={false}
        tick={{ fill: tufte.gray3, fontSize: 12, fontFamily: tufte.fontMono }}
        domain={["dataMin", "dataMax"]}  /* range frame */
        ticks={[Math.min(...data.map(d => d.mau)), Math.max(...data.map(d => d.mau))]}
      />
      <Line
        type="monotone"
        dataKey="mau"
        stroke={tufte.ink}
        strokeWidth={1.5}
        dot={false}
        isAnimationActive={false}
      />
      <ReferenceDot x={last.month} y={last.mau} r={3} fill={tufte.accent} stroke="none" />
    </LineChart>
  );
}
```

Key compliance moves:
- No `<CartesianGrid>` — kill it
- No `<Tooltip>` for static views — it's interaction chartjunk
- No `<Legend>` for a single series
- `domain={["dataMin", "dataMax"]}` for a range frame
- `dot={false}` — markers are redundant when the line is visible
- `isAnimationActive={false}` — animation on static data is decoration
- One `<ReferenceDot>` in accent color for the focal point

## D3-in-React — dot plot

For sorted categorical comparison, Recharts' `<BarChart>` produces vertical bars by default and the typography is opinionated. Use D3 to compose the SVG yourself.

```tsx
import { scaleLinear } from "d3-scale";
import { tufte } from "./tufte-theme";

type Datum = { name: string; value: number };

export function DotPlot({ data, focal }: { data: Datum[]; focal?: string }) {
  const sorted = [...data].sort((a, b) => b.value - a.value);
  const max = Math.max(...sorted.map(d => d.value));
  const x = scaleLinear().domain([0, max]).range([120, 380]);
  const rowH = 28;
  const height = sorted.length * rowH + 40;

  return (
    <svg viewBox={`0 0 420 ${height}`} width="100%">
      <line x1={120} y1={20} x2={120} y2={height - 20}
        stroke={tufte.gray3} strokeWidth={0.5} />
      <text x={115} y={24} textAnchor="end" style={tickStyle}>{max}</text>
      <text x={115} y={height - 14} textAnchor="end" style={tickStyle}>0</text>
      <line x1={120} y1={20} x2={380} y2={20} stroke={tufte.gray1} strokeWidth={0.5} />

      {sorted.map((d, i) => {
        const y = 40 + i * rowH;
        const isFocal = d.name === focal;
        return (
          <g key={d.name}>
            <line x1={120} y1={y} x2={x(d.value)} y2={y}
              stroke={tufte.gray2} strokeWidth={0.5} />
            <circle cx={x(d.value)} cy={y} r={4}
              fill={isFocal ? tufte.accent : tufte.ink} />
            <text x={115} y={y + 4} textAnchor="end" style={labelStyle}>{d.name}</text>
            <text x={x(d.value) + 8} y={y + 4} style={valueStyle}>{d.value}</text>
          </g>
        );
      })}
    </svg>
  );
}

const tickStyle  = { fontFamily: tufte.fontMono, fontSize: 12, fill: tufte.gray3 };
const labelStyle = { fontFamily: tufte.fontSerif, fontSize: 15, fill: tufte.ink };
const valueStyle = { fontFamily: tufte.fontMono, fontSize: 16, fill: tufte.ink, fontWeight: 600 };
```

## D3-in-React — slopegraph (before/after comparison)

```tsx
type SlopeDatum = { name: string; before: number; after: number };

export function Slopegraph({ data }: { data: SlopeDatum[] }) {
  const allValues = data.flatMap(d => [d.before, d.after]);
  const y = scaleLinear()
    .domain([Math.min(...allValues), Math.max(...allValues)])
    .range([220, 30]);

  return (
    <svg viewBox="0 0 420 280" width="100%">
      <text x={80} y={20} textAnchor="end" style={labelStyle}>Before</text>
      <text x={340} y={20} textAnchor="start" style={labelStyle}>After</text>

      {data.map(d => {
        const declined = d.after < d.before;
        return (
          <g key={d.name}>
            <line x1={84} y1={y(d.before)} x2={336} y2={y(d.after)}
              stroke={declined ? tufte.accent : tufte.ink}
              strokeWidth={1} />
            <circle cx={84} cy={y(d.before)} r={3} fill={tufte.ink} />
            <circle cx={336} cy={y(d.after)} r={3} fill={tufte.ink} />
            <text x={80} y={y(d.before) + 4} textAnchor="end" style={labelStyle}>
              {d.name} · {d.before}
            </text>
            <text x={340} y={y(d.after) + 4} textAnchor="start" style={labelStyle}>
              {d.after}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
```

## Recharts overrides — global Tufte theme

If you have many charts in one app, override defaults in a single wrapper:

```tsx
import { ResponsiveContainer, LineChart as RechartsLine } from "recharts";

export function Line({ children, ...rest }) {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <RechartsLine {...rest} margin={{ top: 24, right: 48, bottom: 24, left: 24 }}>
        {children}
      </RechartsLine>
    </ResponsiveContainer>
  );
}
```

Then forbid `<Tooltip>`, `<CartesianGrid>`, `<Legend>` at the lint level if the team needs the discipline.

Always wrap charts in `ResponsiveContainer` so nothing clips or bleeds at narrow
widths, and leave enough `margin` (right ≥ 48, left ≥ 24) for end-of-line value
labels. Open the rendered view at its real width and confirm no label or axis is
cut off.

## What to never import

- `recharts/Pie`, `recharts/PieChart`, `recharts/RadialBar`, `recharts/Radar`
- Any chart library that does 3D
- `framer-motion` for chart entry animations — it's decoration on top of data
- Color libraries that default to rainbow scales (`d3-scale-chromatic`'s `interpolateRainbow`, `interpolateSpectral`)

Acceptable color imports for ordered data:
- `d3-scale-chromatic`: `interpolateGreys`, `interpolateBlues`, `interpolateOranges` (single-hue sequential)
- For diverging: `interpolateRdBu`
