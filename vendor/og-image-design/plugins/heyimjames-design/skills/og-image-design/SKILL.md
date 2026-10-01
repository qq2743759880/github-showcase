---
name: og-image-design
description: Design and produce on-brand OG (Open Graph) images for websites, product pages, blog posts, campaigns, and personal portfolios. Use this skill whenever the user asks to "make an OG image", "design a social preview", "create a link preview", "build the og:image", "make a Twitter card", "design a share image", or any equivalent — including when pairing with brand guidelines, style guides, color palettes, type systems, or a Figma/Paper.design file. Covers technical specs (1200×630, 1.91:1, format/size limits), thumbnail survival rules (minimum type sizes, word-count limits, the Slack-sidebar test at 200 px), composition archetypes drawn from direct visual analysis of ~50 OG images on ogimage.gallery (Stripe, Cash App, Liveblocks, ReadMe, Rauno, Until, Beside, DeepJudge, Span, Dock, Grammarly, Ditto, L'Étude, Popcorn, Studio Tyrsa, etc.), brand-fit decisioning, design principles (typography, color, hierarchy, gestalt, negative space, contrast), an image-generation playbook (prompt anatomy, model selection across gpt-image / Flux / Midjourney / Recraft, hybrid AI+typography workflow), and routing between Figma MCP / Paper MCP / Pencil MCP / AI image generation / code-based (next/og, satori) production paths.
---

# OG Image Design

> Synthesised from the [ogimage.gallery](https://www.ogimage.gallery/) library after direct visual inspection of ~50 featured OG images.

An OG image is the **visual handshake** before the headline — the first frame of your brand someone sees in iMessage, Slack, Discord, Twitter/X, LinkedIn, or any link unfurl. It does three jobs in one glance:

1. **Intrigue** the viewer.
2. **Reassure** them they're in the right place (clear brand attribution).
3. **Express the brand** — tone, type, palette — without explaining.

You don't need to scream. You need to **feel real**.

---

## Always do this first

Gather inputs. Ask the user (or read from the project) for whatever's missing:

- **Brand guidelines** — palette (hex), typefaces (font files or names), logo files (SVG/PNG with transparency), wordmark vs. mark usage rules.
- **What is being shared?** A whole site, a single product page, a blog post, an event, a campaign, a portfolio, a person? The archetype follows from this.
- **Where will it be shared most?** Twitter/X, LinkedIn, iMessage, Slack/Discord, Pinterest? Affects safe-zone and aspect choices.
- **Static or animated?** Animated = high-craft signal but only renders on Twitter/X, Discord, some chats. Default static; offer animated as an upgrade.
- **One-off, or templated system?** (e.g. one per blog post) — decides the tool path.

If brand guidelines are absent, **say so explicitly** and offer to either (a) infer style from existing assets, or (b) propose a system first. Don't fake-brand by guessing colors.

---

## Technical specs (non-negotiable)

| Spec | Value |
|---|---|
| **Master size** | **1200 × 630 px** (1.91:1) — Facebook, LinkedIn, general `og:image` |
| **Twitter `summary_large_image`** | 1200 × 675 px (16:9) — 1200×630 still renders fine |
| **Minimum acceptable** | 600 × 315 px |
| **File size** | Under 5 MB; aim under 1 MB |
| **Format** | JPEG for photographic / gradient-heavy; PNG for transparency or crisp text; WebP fine for modern crawlers (keep a PNG/JPG fallback) |
| **No GIFs** | Most platforms strip them. Use a still + MP4/WebM for `og:video` if you need motion |
| **Color profile** | sRGB. Never embed wide-gamut — it'll desaturate on render |
| **Safe zone** | Focal content in the **center 1000 × 500** — platforms crop edges |

Include `twitter:image` + `twitter:card` ("summary_large_image") alongside `og:image`. LinkedIn caches aggressively — re-clear with Post Inspector after every change.

---

## Thumbnail survival — the rule that overrides every other rule

OG images render small. **A lot smaller than you think.** The places they actually appear:

| Surface | Width it renders at | Reduction from 1200px |
|---|---|---|
| Slack channel sidebar / iMessage preview | ~200 px | **6×** |
| Discord small embed | ~250 px | 4.8× |
| LinkedIn feed thumbnail | ~300 px | 4× |
| Twitter/X timeline card | ~600 px | 2× |
| LinkedIn / FB full unfurl | ~700 px | 1.7× |

If the OG only works at 1200×630 in Figma, **it doesn't work.** Most of the audience sees it at 200–300 px.

### Minimum type sizes (at 1200×630 master canvas)

Every text element must clear the bar for the smallest surface you actually expect it to render on. Convert this way: target legible-thumbnail size × the surface's reduction factor.

| Role | Min size at master | Reads down to | When to break the rule |
|---|---|---|---|
| **Headline / primary message** | **80 px** | 200 px (Slack-safe) | Never |
| **Subhead / secondary line** | **40 px** | 300 px (LinkedIn-safe) | Only if not load-bearing |
| **Card titles / labels in product UI fragments** | **28 px** | 600 px (Twitter-card-safe) | When the card is decorative, not informational |
| **Body copy / supporting text** | **22 px** | 600 px | When optional |
| **Tiny captions, mono colophons, registration marks** | **16 px floor** | only 700+ px (full unfurl) | If they're load-bearing (a URL someone must read, a date that matters), they MUST be 22 px+ instead |

The 16 px floor for "tiny" text exists because below that, it stops being *small text* and becomes *visual texture* — invisible at thumb, suggestive at full size. That's a valid design move, but you must be honest that no one will *read* it.

**Anything below 16 px at master is decoration only.** No tagline, no important info, no URL, no agent name. If a future reader needs to read it to understand the image, it's the wrong size.

### Word-count limits at thumbnail size

| Surface render width | Words a reader can actually parse | Practical limit |
|---|---|---|
| 200 px | 4–6 | One short headline |
| 300 px | 6–10 | Headline + 1 supporting word |
| 600 px | 12–18 | Headline + tagline |
| 1200 px (full) | 25–40 | Headline + tagline + small caption |

Design for the **smallest** surface in your distribution. If you're posting to Slack and iMessage, that's 200 px — so 4–6 readable words total.

### The "across-the-room" sanity check

A faster gut-check than measuring pixels: take your 1200×630 design and **stand back 2 metres from your monitor.** Squint. What can you still read? That's roughly what the Slack sidebar shows. Anything that disappears at 2 m disappears in the sidebar.

### Type-specimen archetype warning

The "design-spec watermark" / "type-specimen" archetypes (#3, #12 in the archetype catalogue below — Otherkind, Studio Tyrsa, Stripe BFCM) are tempting because they look *designer*. They use lots of small annotations, registration marks, monospace metadata, colophons. They look great at 1200×630 in your design tool.

**Most of those examples were screenshots from designers' portfolios, not real share-traffic OG images.** When you ship one as an actual OG, the corner annotations vanish in the iMessage thumbnail and you're left with the hero glyph only. That can still work — but ONLY if the hero glyph alone carries the brand. Don't kid yourself that the tiny annotations are doing any work for shareability; they're decoration for full-size viewers. Cut them if the hero can't stand alone.

---

## Design principles (synthesised across ~50 images)

These are the cross-image patterns the best OG images share. Apply them *before* picking an archetype.

### Typography

| Voice you want | Typeface family | Examples in sample |
|---|---|---|
| Tech / SaaS / product | Geometric grotesk (Inter, GT America, Söhne, Aeonik) | Smoo.link, Span, Owner, Dock, Beside-brand |
| Trust / law / luxury / editorial | Editorial serif (PP Editorial New, GT Sectra, Söhne-Serif) | DeepJudge, Beside-vinyl, Ditto, Popcorn, New Genre |
| Brand-is-type / craft | Custom display, blackletter, hand-script | Studio Tyrsa, Craft, Stripe BFCM, Dirt |
| Engineering / IDE / spec | Mono (JetBrains, Berkeley, IBM Plex Mono) | DeepJudge prompt chip, Otherkind, ReadMe captions |

- **Headline length: 3–8 words is the sweet spot.** Cross 12 words and it reads as a press release at thumbnail size.
- **Type sizes: see the Thumbnail survival table above.** Headline floor is 80 px at master, not 56 — 56 px barely survives a 600 px Twitter card and dies in a 200 px Slack sidebar.
- **One weight contrast.** Display heavy + caption light is enough. Three weights is a layout problem.
- **Treat one or two words specially** — italic, brand-color highlight, dashed-selection-box, or larger size. Span's "big/small" pun. v0's selection-boxed "it." ReadMe's italic "adoption."
- **Numerical anchors get monospace.** Funding amounts, version tags, dates — Beside `$32m`, ReadMe API labels.

### Text load

| Load | Words on canvas | When to use |
|---|---|---|
| **Zero** | 0 | Mood-first OG, brand promise is the *feeling* (Board, Treeo). Risky if brand isn't recognisable. |
| **Wordmark only** | 1–2 (the name) | Brand identity card. Default when no campaign exists (Beside-brand, Dirt, Cosmos). |
| **Wordmark + tagline** | 4–10 | Most common, safest choice. Most product launches (Until, Span, Owner, Smoo.link, Dock, DeepJudge, Ditto, Popcorn). |
| **Long-form poem / portfolio** | 15–30 | Personal portfolio only. Never product (Rauno). |

If you go over ~12 words, **reduce or split into hierarchy** (small caption + big headline + tiny tag), don't shrink type.

### Color logic

The single highest-leverage decision. Pick **one** of these strategies, don't mix:

1. **Saturated single-hue field** — full canvas of one brand color. Cash App red, L'Étude red, Rauno white-with-yellow-disc, Craft sky-blue. Bold and instantly recognisable but the whole image lives or dies on that one decision.
2. **Cream / parchment surface** (`#F8F8F3`-`#FFFBF0` family) — warmer than pure white; reads as crafted, not corporate. Ditto, DeepJudge, Owner (off-white), Matt Sellers, Shiori. Strong for editorial / luxury / trust positions.
3. **Dark brand field** — navy / near-black / deep brand color. Beside-brand, Grammarly green, Liveblocks tinted. Strong but loses recognition if a competitor uses similar darks.
4. **Photo-as-color** — full-bleed photograph supplies the palette. Until (grass green), New Genre (gold + blue gradient), Board (rust + mid-century chromatic). The most evocative; the most expensive to do well.
5. **Brand color + neutral** — one accent on white/cream. Span (peach + white), Dock (blue + white), DeepJudge (purple accent in cream). Safe and templatable.

**Complementary tension** (warm focal + cool field, or vice versa) reliably outperforms a flat single-temperature palette. New Genre's gold flower on cool blue is the cleanest example.

### Hierarchy

Three layouts cover most cases:

- **F-pattern** — brand top-left, headline center-left, supporting visual right (Smoo.link, Span, Owner, Dock, Grammarly). The default for product launches.
- **Symmetry** — centered mark, centered headline, centered visual. (Beside-brand, Ditto, DeepJudge, Liveblocks.) Reads as confident, considered.
- **Z-pattern** — brand top-left, headline center, supporting mark or tag bottom-right or bottom-left (Until, Popcorn, Matt Sellers). Works when one corner is the "exit."

**Three-tier vertical** (brand → headline → metaphor visual) is a special case of symmetry that handles 80% of single-headline OG needs (Ditto, DeepJudge).

### Negative space

- **High whitespace (≥60% empty) = luxury / considered.** Beside-vinyl, Ditto, DeepJudge, Shiori. Pairs with editorial serifs.
- **Edge-to-edge fill = energy / abundance.** Treeo, Board, L'Étude, Studio Tyrsa, Mitchivin. Pairs with photography or saturated fields.
- **Half-and-half = product-led but breathing.** Span, Dock, Smoo.link. Pairs with grotesks.

Pick one and commit. Awkward middle (40–50% empty) looks unfinished.

### Gestalt / focal-point patterns

- **One dominant focal point.** Always. A wordmark *or* a face *or* a hero object *or* a headline. The other elements support, never compete.
- **Figure-ground via density inversion** — Treeo proves it: chaos field + calm island is as strong as calm field + bold subject.
- **Image-within-image / broken frames** add depth — L'Étude's wordmark crosses the photograph; Grammarly's UI floats over a flower. Use sparingly.
- **Recognisable silhouette at 200px.** Rauno's yellow circle, Ditto's pill chain, L'Étude's red field. If you can describe the shape in 4 words, it'll survive thumbnailing.

### What reads at 200 px (the Slack-sidebar test)

See the full Thumbnail survival section above for type-size and word-count tables. Quick check:

✅ Single dominant focal point with high value-contrast against ground.
✅ Headline ≥ 80 px at master canvas.
✅ Recognisable silhouette / shape.
✅ One memorable element minimum: a mark, a face, an object, a metaphor.
✅ Total word count ≤ 6 if Slack/iMessage are primary distribution.

❌ Full UI screenshots (every detail dies).
❌ Light-grey-on-white type.
❌ More than ~12 words anywhere on the canvas.
❌ Generic stock photography.
❌ Two equally-weighted focal points competing.
❌ "Design-spec" mono captions or registration marks under 16 px — they vanish at thumbnail and you can't pretend they're load-bearing.

---

## Composition archetypes

> All confirmed by direct image inspection. Pick one that fits the subject, bend the brand into it. Don't invent a new pattern without a strong reason.

### Wordmark family (low text load)

**1. Centred wordmark on solid field** — Beside-brand, Cosmos-style.
Mark+wordmark centred on dark or saturated surface. ~80% empty. The "we're shipping but don't have a campaign" template. Lowest-risk default.

**2. 3D / glassy wordmark on cream** — Dirt.
Wordmark rendered as a 3D refractive object on a near-white field. Editorial / cultural / publication brands. Requires render craft; flat fallback if not.

**3. Custom-display wordmark in atmospheric field** — Craft, New Genre, Stripe BFCM.
Bespoke wordmark (rounded blackletter / scenic-fill / risograph) on a thematic field (clouds, flowers, vintage postcard). Brand IS the type.

### Headline + visual family (medium text load)

**4. Cream + serif headline + bottom metaphor band** — Ditto, DeepJudge.
Mark top, editorial serif headline mid, abstract visual metaphor along the bottom edge. Three-tier vertical hierarchy. Highest-utility template for funded / mature B2B.

**5. F-pattern: headline left, product UI right** — Span, Grammarly × Superhuman.
Mark top-left, bold sans headline left third, real product UI fragment right two-thirds. Soft brand gradient unifies the seam. The "product proof" template.

**6. Headline top, product UI bottom** — Smoo.link, Dock.
Same idea stacked vertically. UI as proof, not centrepiece. The tab labels / column headers in the UI carry implicit feature lists.

**7. Hub: centred headline + floating UI fragments** — Liveblocks.
Big centred headline on dark/tinted field, small UI fragments (chat bubbles, cursors, presence) floating in the corners. Brand mark bottom-centre. Strong for collaborative / multiplayer / network products.

**8. Big disc + indented poetic typography** — Rauno.
Personal portfolio. Long indented copy fills 2/3, single bold shape fills 1/3, rule-of-thirds split. Not for product.

### Photo / object family (image-led)

**9. Full-bleed editorial photograph + small caption** — Until, New Genre, Board.
The photo IS the OG image. Tiny mark + 1-line caption in a corner pill. Photo carries 90% of meaning. Needs intentional photography — stock will kill it.

**10. Documentary flat-lay + wordmark overlay** — Opal Electronics, Studio Tyrsa.
Top-down photo of curated objects (or hands at work). Wordmark in white sans overlaid. Brand is the *world*. Hardware, makers, design studios.

**11. Saturated field + corner mark + photo vignette** — Cash App, L'Étude.
Brand color fills 50–70%. Tiny mark in one corner. Cropped photograph as image-within-image. The wordmark may cross the photo edge for depth.

### Spec / system family (design-forward)

**12. Engineering / design-spec watermark** — Otherkind.
Wordmark rendered as a design-system spec page — registration marks, dimension guides, monospace captions. Self-referential; only for actual design studios.

**13. Blueprint grid + product icon chips** — ReadMe.
Technical-blueprint background, centred lockup + italic-emphasised headline, four small framed icon chips at the corners showing integrations. Dev tools / platforms with multiple connectors.

**14. Product-UI close-up with interactive affordance** — v0.
Wordmark top-left, bold headline left-anchored with one word in a dashed selection box or cursor metaphor. Slice of real product UI right. For design/build tools where editing is the verb.

### Stylistic / playful family

**15. Stylized hero object + app UI proof** — MUNI Bus Ad Maker.
Stylized illustration of the output (glitchy bus, etc.), real editor UI cropped along the bottom third. Creator-tool template.

**16. Illustrated whimsy + serif headline** — Popcorn.
Hand-illustrated central object (suitcase in clouds, etc.) with a small serif headline + corner mark. Softens utilitarian categories (telecom, banking, insurance).

**17. Memetic culture-hijack** — Mitchivin (Windows XP), Stripe BFCM (vintage postcard).
Borrow a universally-recognised cultural artefact and graft the brand onto it. Borrowed recognition replaces brand recognition. Works for seasonal campaigns and personal brands; risky for serious B2B.

**18. Field of chaos + calm island** — Treeo.
High-saturation tiled background (emoji grid, sticker sheet), single calm card centred with the mark. Figure-ground via density inversion.

**19. Documentary craft photo** — Studio Tyrsa.
Photograph of the brand's own work being made (hands arranging type proofs, designer at desk). For craft studios where the work IS the demo.

### Animated archetype

**20. Subtle motion loop** — Cash App, Cosmos, basement.studio.
Any static archetype + 2–4s subtle loop (parallax, light sweep, particle drift, slow zoom). Export MP4/WebM + PNG poster fallback. Anything bigger than "you'd miss it on first watch" reads as a banner ad.

---

## Universal rules

These apply regardless of archetype:

- **One focal point.** Never compete a wordmark, product shot, and headline at equal weight.
- **The brand color is the background, not the accent.** Commit to a single field; let one or two elements live on it.
- **Headline = label, not slogan.** 3–8 words describing what the page IS.
- **Centre the focal point.** Never put critical content within 100 px of any edge.
- **Match the brand voice of the site.** Calm site + loud OG breaks the handshake.
- **Contrast aggressively.** Pastel-on-pastel disappears in a feed.
- **No stock photography.** Even custom illustration of stock is better.
- **Don't print the URL.** Platforms show it underneath.
- **Don't put "Click here" or arrow CTAs.** The unfurl IS the CTA.
- **Pure white (#FFFFFF) looks colder than cream (#F8F8F3).** Match the choice to the brand temperature.

---

## Tool routing

| Tool | Best for | Worst for |
|---|---|---|
| **Code: `@vercel/og` + Satori (or `next/og`)** | Templated images that vary per page — blog posts, product pages, dynamic titles. Deterministic typography, fast at runtime. | One-off hero images; complex visuals, gradients, photography. |
| **Figma MCP** (`mcp__plugin_figma_figma__*`) | Brand-system-aware static images. Reuses existing components and tokens. | Quick one-offs; photographic compositions. |
| **Paper MCP** (`mcp__paper__*`) | Fast HTML-based composition. High iteration speed, exports clean. Good for animated explorations. | Heavy design-system enforcement; Figma component reuse. |
| **Pencil MCP** (`mcp__pencil__*`) | When the user has a `.pen` file open and wants the OG built in their existing design surface. | Without an existing pen file. |
| **AI image generation** (gpt-image, Flux, Midjourney) | Photographic / 3D / illustrated backgrounds and objects. The image-led archetypes (#9, #10, #11) when no physical product exists. | Crisp typography; brand-exact logos; final headline rendering. |
| **Hybrid (recommended)** | AI-generate the visual, composite logo + text in Figma/Paper/code crisp. How the gallery's most polished images are actually made. | Tightly templated per-page systems. |

### Decision sequence

1. **Per-page dynamic image (blog, product catalog, profile)?** → `@vercel/og` / Satori.
2. **One-off hero, brand has Figma library?** → Figma MCP.
3. **One-off, no Figma library, want speed?** → Paper MCP.
4. **Need photographic / 3D / illustrated visual?** → AI gen for background; composite type+logo in Figma/Paper/code (never let AI render the final wordmark — it will mangle it).
5. **Animated?** → Design still in Figma/Paper, animate in After Effects / Rive / CSS+JS, export MP4 (H.264, ≤2 MB) + PNG poster.

---

## Image generation playbook

AI image generation is the biggest unlock for image-led OG archetypes — but the wrong tool for ~70% of OGs. Use it for the *background*, never the *type*. The hybrid workflow (AI visual + crisp typography composited on top) is how the gallery's most polished image-led OGs (Until, New Genre, Popcorn, the photo-led half of Grammarly) are actually made.

### When to use AI image generation

✅ **Photographic mood backgrounds** — atmospheric scenes, golden-hour light, botanical close-ups, interior textures. Powers archetypes #9 (full-bleed photo), #10 (documentary flat-lay), #11 (saturated field + photo vignette).
✅ **Illustrated hero objects** — single subject in a stylised treatment (Popcorn's pencil-shaded suitcase, Cofounder's pixel-art figures). Powers archetype #16.
✅ **Surreal / impossible imagery** — when the brief calls for something that doesn't exist (e.g., Mitchivin's "MITCHIVIN" extruded into the Windows XP hill).
✅ **Atmospheric textures and gradients** — risograph grain, halftone clouds, paper deckle edges, wood-grain surfaces.

### When NOT to use AI image generation

❌ **Final headline or tagline rendering.** Even SOTA models produce subtly broken letterforms, wrong kerning, and one extra letter you won't notice until it's in iMessage. Always composite type on top with real fonts.
❌ **Brand logos or wordmarks.** Same reason. AI cannot replicate your wordmark cleanly; do not even try.
❌ **Product UI screenshots.** Fabricated UI looks fabricated. Use Figma/Paper for realistic product fragments.
❌ **Anything requiring pixel-precise alignment** to a layout grid.
❌ **When the brand is built on calm restraint** (Linear, Stripe corporate, Mercury). AI-generated visuals add information; restrained brands subtract it.

### Prompt anatomy for OG backgrounds

A prompt that works for OG images has six elements, in this order:

1. **Subject** — what's in the frame (one main thing, no clutter).
2. **Composition cue** — where the subject sits, where the negative space is. *Always* tell the model where to leave room for type. "Centred subject with empty 40% on the left for text overlay" or "subject occupying the right two-thirds, top-left two-thirds empty for headline."
3. **Lighting cue** — golden hour, candlelit, overcast, studio softbox, harsh midday. Lighting carries 60% of the mood.
4. **Colour cue** — derive from the brand palette: name the primary colour family and the secondary if any. "Warm amber and cream palette with one deep ember accent."
5. **Style cue** — photographic / pencil illustration / 3D render / risograph / oil painting / vector flat. Be specific or the model defaults to its generic look.
6. **Negative cues** — what to exclude. Always include: "no text, no letters, no watermarks, no logos."

#### Prompt template

```
[Subject] in [composition], lit by [lighting], in a palette of [colours],
rendered as [style]. Wide-angle 16:9 composition with deliberate negative
space [where for type]. No text, no letters, no watermarks, no people unless
described, no UI elements.
```

#### Worked example — for a J&J-style warm editorial OG

> "A worn oak desk in a sunlit study, late-afternoon light slanting through a window from the right, with a single open hardcover book and a small brass desk lamp casting amber light. Warm cream paper and ember-orange accents. Photographic, shallow depth of field, editorial magazine style. Wide-angle 16:9 with the right two-thirds empty above the desk for headline text. No text, no letters, no watermarks, no people."

### Model selection

| Model | Strengths | Use for |
|---|---|---|
| **gpt-image-1** (OpenAI) | Best prompt-adherence among current models, handles composition cues well, follows "leave space for type" instructions reliably | Default first choice for OG backgrounds, especially when you need a specific composition |
| **Flux 1.1 Pro / Ultra** (Black Forest Labs) | Best photographic realism, skin/texture detail | Photographic mood backgrounds, full-bleed editorial photos |
| **Midjourney v6+** | Strongest aesthetic / "moodboard" look, painterly textures | Surreal, painterly, illustrative; less good when you need precise composition |
| **Recraft v3** | Vector-clean illustration, brand-grade flat illustration | Illustrated hero objects (Popcorn / Cofounder territory) |
| **Ideogram** | Best at typography *within* the image (rare exception) | If you genuinely need rendered text inside the image — but still composite the final headline on top crisp |

### Output sizing for AI gen

Generate at **slightly oversize** so you can crop without quality loss:

- Target ratio: 16:9 (so 1456 × 819, or 1792 × 1024, or model's nearest native size)
- Then crop / pad to 1200 × 630 in your composition tool
- Never accept the model's first output. Run 4–8 candidates and pick the one with the best negative space exactly where your headline needs to go

### Hybrid workflow (the one that actually ships)

1. **Sketch the layout first** in Figma/Paper at 1200×630 — block in where the headline, mark, and any other crisp elements will sit. The AI background fills the rest.
2. **Write the prompt with that layout in mind** — tell the model exactly where negative space must be.
3. **Generate 4–8 candidates.** Pick the one with the right composition AND the right negative space AND the right colour. Don't compromise on negative space — bad layout never recovers.
4. **Composite in Figma/Paper/code** — drop the AI image as background, layer the crisp wordmark + headline + mark in real fonts on top. The headline still has to clear the thumbnail-survival type-size minimums above.
5. **Run thumbnail tests** — the photo background may have low contrast against your headline. Add a subtle scrim (linear-gradient overlay at 20–40% black or brand-tinted opacity) just behind the headline area if needed. Apple, Vercel, and Liveblocks all do this.

### Failure modes to watch for

- **Fabricated text in the image** — the model hallucinated letters somewhere in the scene (a book spine, a sign, a wall poster). Reject the candidate; don't try to fix.
- **Six-fingered hands / extra limbs** — only relevant if your prompt involved people. Generally avoid people in OG backgrounds entirely; they invite identity questions ("who is this?") and date faster than abstract imagery.
- **Cluttered subject** — when the model adds extra props you didn't ask for. Re-prompt with "single subject only, no extra objects."
- **Wrong negative space** — model put the subject where you wanted text. Re-prompt with sharper composition language, or use a different seed.
- **Generic-AI look** — pastel gradients, smooth volumetric lighting, "concept art" feel. Counter by getting more specific on style cue (named photographer / illustrator / film stock / paint medium) and by tightening the lighting cue.

---

## Workflow

1. **Confirm inputs** — palette, type, logo paths, what's being shared. Ask in one message, not five.
2. **Identify primary distribution surface** — Slack/iMessage (200 px) is the harshest, Twitter (600 px) is mid, LinkedIn full unfurl (700 px) is the most forgiving. Design for the *smallest* surface in your distribution. This sets the word-count + type-size budget from the Thumbnail survival table.
3. **Pick the archetype** — name it explicitly ("going to use #4: cream + serif headline + metaphor band, like Ditto") so the user can redirect before you build.
4. **Pick the tool path** — name it ("doing this in Paper, composite the logo crisp" or "AI background + Figma composite").
5. **Build at 1200 × 630** — never design at 2x and downscale type.
6. **Test at 200 × 105 BEFORE adding flourish.** Block in just the hero element + headline at master sizes, screenshot at 200 px, confirm it reads. Add the rest of the design ON TOP of that confirmed-readable foundation. Don't design at 1200 then hope it survives — start from the floor.
7. **Final screenshot at 600 × 315 AND 200 × 105.** Both must still read. If either fails, the design fails. Anything decorative that vanishes at 200 px is fine — anything *load-bearing* that vanishes is a redesign.
8. **Test the unfurl** before declaring done.

---

## QA / debug

- **Visual check at 3 scales:** 1200×630, 600×315, **200×105**. The 200px check kills most images.
- **Centre-crop check:** mask outer 100 px each side — is focal content still intact?
- **Greyscale check:** convert to greyscale — if focal point disappears, it'll die in dark-mode feeds.
- **Unfurl previewers:**
  - [Preview.ogimage.gallery](https://preview.ogimage.gallery/)
  - [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)
  - Facebook Sharing Debugger
  - Twitter/X Card Validator
- **Meta tags:**
  ```html
  <meta property="og:image" content="https://.../og.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Plain-language description">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="https://.../og.png">
  ```
- **Cache busting:** append `?v=2` or rename the file. Slack and iMessage cache for *days*.

---

## Common mistakes — don't ship if any apply

1. Wrong dimensions (not 1200×630). Causes letterboxing or crop.
2. Tiny illegible logo / type at 200 px. The Slack-sidebar test.
3. Text bleeds to the edge. Cropped on at least one platform.
4. Repeats the page URL / domain. Redundant; platform shows it already.
5. CTA arrows / "Click here" / "Read more". The unfurl is the CTA.
6. AI-rendered final logo or headline text. Crisp text via code or Figma.
7. Stock photography of laptops, handshakes, abstract networks.
8. Inconsistent with the site (bright OG + muted site, or corporate OG + playful site).
9. Still-frame from a GIF. Platforms strip GIFs.
10. Forgot to bust the cache after replacing.

---

## When pairing with brand assets

If the user provides a brand guideline doc, asset folder, or Figma file:

1. **Extract:** primary palette (≤5 hex), secondary palette, type system (display + body), logo files (mark + wordmark + lockup), illustration style, voice notes.
2. **Map to the most appropriate archetype** — don't force a mismatch (a serif editorial brand should not get an isometric tech-event treatment).
3. **Default to the brand's *quietest* expression of itself.** OG images that try too hard age fastest.
4. **If a brand-voice skill is loaded** (e.g. `jackandjill-brand-voice`), pull headline from that voice — don't write generic marketing copy.

---

## References

- Gallery: https://www.ogimage.gallery/
- Library: https://www.ogimage.gallery/library (article paths use the typo `/libary/`)
- Synthesised from: "What Makes a Great OG:image?", "Why Your OG Image Matters More Than Ever in 2026", "Ultimate Guide to OG Image Dimensions", "5 Common Mistakes", "OG Images and SEO", "How to Check and Debug" — plus direct inspection of ~50 featured images.

---

## My defaults

> Edit this section to make the skill route correctly the first time. Examples:
>
> - **Preferred tool path** — e.g. "Paper MCP first, Figma when there's an existing JJ component library, Satori for per-page templates."
> - **Brand defaults** — e.g. "For Jack & Jill: cream parchment (`#F8F8F3` main / `#F2F2EB` sidebar), JJ Sans wordmark centred, warm wood + amber lamp light if a background image is needed (per visual-taste memory)."
> - **Archetype defaults by content type** — e.g. "Blog post → archetype #4 (cream + serif headline). Product launch → archetype #5 (F-pattern with UI proof). Personal portfolio → archetype #8 (Rauno-style)."
