# Checklist

Twenty items. Walk through before declaring any chart done.

## Data

- [ ] Is the data sorted by the value the reader cares about (not alphabetical, not as-input)?
- [ ] Are all data points visible, or is the chart hiding outliers behind summary lines?
- [ ] If categories were grouped into "Other", is that group small enough not to mislead?

## Honesty

- [ ] Lie factor between 0.95 and 1.05? (Visual change matches numerical change.)
- [ ] Bar charts start at zero?
- [ ] Truncated line-chart axes have the baseline labeled?
- [ ] No area or volume encoding a single number?

## Ink

- [ ] Gridlines either light gray or absent?
- [ ] No chart border / frame box (range frame only where needed)?
- [ ] No redundant encoding (bar + number + label + axis tick all saying the same thing)?
- [ ] One accent color, used for focal data only?

## Labels

- [ ] Direct labels on data, not a separate legend (unless ≥ 5 categories)?
- [ ] Numbers formatted readably (4.2M not 4,200,000)?

## Not flat

- [ ] The one accent color is actually applied to the focal data point, not left unused?
- [ ] Data marks present where they help reading (dots on line endpoints, dot plots over bare bars)?

## Readability

- [ ] Type large enough to read at a glance: body ≥ 14px, axis ticks ≥ 12px, focal numbers ≥ 16px?

## Layout

- [ ] Nothing clipped, cut off, or bleeding outside its container or the page?
- [ ] Container is responsive (width 100%, viewBox set) so it fits without horizontal scroll?

## Prose (reports, recaps, slides)

- [ ] No em-dashes, no drama, no hype verbs, no AI-slop jargon (see `report-voice.md`)?
- [ ] Every label and caption named for the specific case, not a placeholder?
