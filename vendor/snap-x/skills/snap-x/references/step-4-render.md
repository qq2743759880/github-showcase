# Step 4: Render, verify, deliver

## Render

```bash
npx -y @snap-x/cli render designs/*.mjs --out snap-output/     # or a single file
```

Output names come from each file's `FORMAT.name`. Use `--out` to keep results with the source (e.g. next to `designs/`).

## Verify — look at every PNG

`check` can't see visual problems, so open each rendered image (Read it) and go through this list:

- **Blank boxes** where a symbol/arrow/emoji should be → the font lacks the glyph (`check` warns about most); draw it as SVG (Step 3)
- **Wrapped or clipped text** — headlines broken mid-word, text running off an edge, content pushed off the canvas → reduce sizes
- **Text over decoration** — a sun, hill, blob or phone hiding letters or reducing contrast → move the shape, don't shrink the text
- **Elements clipped by the canvas edge** (an orbit node, an icon half off-screen)
- **Invisible logo** (dark on dark) or a stretched/blurry one
- **Contrast** — muted text readable against its background
- **Store graphics:** `FORMAT.alpha` is `false` (opaque PNG)
- **Copy** matches the source exactly (names, numbers, spelling); nothing invented
- **Brand** — colors, font and logo look like the brand's own

Fix the design file and re-render until clean. Fix what you see, then look again — don't assume a re-render fixed it.

### Render review

Score every image against `references/design-principles.md` § Render review (focal point, hierarchy, spacing/alignment, contrast, squint test, pack consistency) and record the scores in `snap-plan.md`. Fix anything scoring 1.

### Placement check: `snap-x guides`

For banners and covers (LinkedIn, X, YouTube channel art), YouTube thumbnails and stories, run:

```bash
npx -y @snap-x/cli guides designs/*.mjs --out guides/      # add --format <id> if the size isn't a known format
```

It writes `<name>.guides.png` (your design with the platform's danger zones in red — profile photo, duration badge, story UI, cropped edges — and the safe area dashed) and, where phones crop, `<name>.mobile.png` (what a phone shows). A format with no zones (an App Store screenshot, a Play feature graphic, a plain OG card) prints "nothing to check" — that is not a failure; there's simply no platform overlay to worry about. **View both.** No text may sit in a red zone, and the name/headline must survive the mobile crop. Decoration may go anywhere. Measure the text's pixel extent if it's close to a limit. (Don't hand-write QA designs or put them in `designs/` — `guides` replaces them.)

### `@2x` exports

`snap-x render designs/*.mjs --scale 2` renders the same design sharp at 2× (resvg re-rasterizes the same vector output at the larger size — no upscaling), writing `<name>@2x.png`. `snap-x check --scale 2` also verifies resvg can encode the design at that size. No second design file needed; only reach for a manual `width×2` / `height×2` root with `transform: "scale(2)"` if a size genuinely needs a *different* layout, not just a sharper export.

## share-copy.txt

Write `<out>/share-copy.txt`: where each image goes, plus a note on anything mock or illustrative and where the brand assets came from.

```
<Project> — image pack (generated with /snap-x)

og.png (1200×630)         → <meta property="og:image"> / twitter:image; link previews
readme-card.png (1280×640)→ top of README; GitHub Settings → Social preview
cover.png (1500×500)      → X / GitHub org banner
<linkedin-cover>.png      → LinkedIn: Profile → banner (1584×396)
poster.png (1080×1920)    → Instagram / WhatsApp story

Regenerate: npx -y @snap-x/cli render designs/*.mjs --out <dir>
Note: <illustrative content, asset sources>
```

List only the images you actually made.

## Deliver

Tell the user (short): where the images are, what each is for, anything mock or assumed, and one first action (e.g. "upload readme-card.png as the GitHub social preview").
