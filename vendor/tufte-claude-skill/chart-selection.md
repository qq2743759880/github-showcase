# Chart selection

Pick the chart from the data and goal. Don't pick by familiarity.

## Step 1 — name the data

| Type | Looks like |
|---|---|
| **Single number with context** | "Revenue is $4.2M, up from $3.8M last quarter" |
| **One variable, many items** | Sales by product, latency by endpoint, headcount by team |
| **One variable over time** | Daily active users, monthly revenue |
| **Two variables, many items** | Price vs. rating, size vs. churn |
| **Distribution** | Response times, salaries, ages |
| **Part-to-whole** | Revenue mix, traffic sources |
| **Flow / transition** | Funnel stages, cohort retention |
| **Geographic** | Sales by state, latency by region |

## Step 2 — name the goal

| Goal | Test |
|---|---|
| **Compare** | Reader will rank, pick a winner, spot the laggard |
| **Track** | Reader will look at one thing across time |
| **Relate** | Reader will see if X is connected to Y |
| **Distribute** | Reader will understand the spread, the typical, the outliers |
| **Locate** | Reader will find where something is |

## Step 3 — the table

| Data | Goal | Use | Don't use |
|---|---|---|---|
| Single number with context | Compare | Sparkline + number side by side | KPI card with giant number alone |
| One variable, many items | Compare / rank | Sorted dot plot or horizontal bar | Pie chart, donut, treemap |
| One variable over time | Track | Line chart with range frame | Bar chart for continuous time, dual-axis line |
| Two variables, many items | Relate | Scatterplot, range frame, no grid | Bubble chart with size encoding a third variable |
| Two snapshots, many items | Compare change | Slopegraph | Side-by-side bars, before/after pair charts |
| Distribution | Distribute | Strip plot, dot plot, or histogram with thin bars | Boxplot for non-statistical audience, violin plot for general use |
| Part-to-whole, small n (≤6) | Compare shares | Sorted bar with direct labels, or a small table | Pie chart |
| Part-to-whole, large n | Compare shares | Sorted bar; group long tail | Treemap, donut, sunburst |
| Flow through stages | Track drop-off | Sorted horizontal bar (funnel) or sparkline column in a table | Funnel chart with 3D, Sankey for simple flows |
| Geographic | Locate / compare | Choropleth in single-hue sequential, small annotations | Choropleth with rainbow, bubble map sized by raw count |
| Multivariate, many items | Compare across dimensions | Small multiples (one chart per dimension, shared scale) | Radar/spider chart, parallel coordinates for general audiences |
| Multivariate table | Compare values | Table with sparklines and conditional shading | Heatmap for any small table (just show numbers) |

## Step 4 — the gut checks

Before drawing, ask:

1. **Could a small table do this job?** If n ≤ ~15 and exact values matter, a table beats a chart.
2. **Could a single sentence do this job?** "Revenue grew 22% to $4.2M" needs no chart.
3. **Am I about to add a second axis?** Don't. Use small multiples.
4. **Am I about to encode three things in one chart?** Color and position and size are three things. Pick one quantity per channel.
5. **Am I sorting by alphabetical, or by category as input?** Almost always wrong. Sort by the value the reader cares about.

## Step 5 — sorting

Default sort orders:

- **Bar / dot plot**: by value, descending. Largest at top.
- **Time series**: time, ascending left to right.
- **Funnel**: by stage, in the order users flow through.
- **Geographic**: by region category, then value within.

Alphabetical is for indexes and directories. Almost never for data graphics.
