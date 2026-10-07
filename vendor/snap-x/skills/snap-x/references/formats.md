# Formats: sizes, placement and layout

snap-x renders any size. This file is about choosing the right one and laying it out for where it will be seen.

## Look the numbers up — don't guess

```bash
npx -y @snap-x/cli formats                 # every platform format: id, size, [no-alpha] [zones] [unverified]
npx -y @snap-x/cli formats linkedin-cover  # notes, official source, and the placement zones (avoid / safe / mobile crop)
npx -y @snap-x/cli formats 1320x2868       # look up by size; aliases work (thumbnail, story, appstore-screenshot …)
```

Sizes marked verified were checked against the platform's official documentation (URL shown); the rest are widely used values — re-check them before a launch. Use the id's size as `FORMAT`. After rendering, `snap-x guides` draws each format's danger zones over your design (see Step 4).

## Alpha: store graphics must be opaque

App Store screenshots and Google Play graphics (feature graphic, screenshots) **cannot contain an alpha channel**. Set `FORMAT = { width, height, name, alpha: false }` and snap-x writes an opaque RGB PNG. `snap-x check` warns when a design has a store size but no `alpha: false`.

## Layout by platform

**Link previews (OG, 1200×630).** One idea, brand top-left, big headline. X's large card crops toward 2:1, so keep the important content centred and away from the top/bottom edges.

**YouTube thumbnail (1280×720).** Seen tiny (often ~200 px wide) and with a duration badge in the bottom-right. Use ≤ 4 huge words, one focal subject, strong contrast, no small text, nothing in the bottom-right corner. Expression and colour beat detail. If the source has no imagery, make the type the subject.

**YouTube channel art (2560×1440).** Only the centred 1546×423 area shows on every device. Put logo/text there; the rest is atmosphere. Check with `guides`.

**X header (1500×500) and LinkedIn cover (1584×396).** The profile photo covers the bottom-left, phones crop the sides, and the top/bottom edges get chrome. Put text in the safe box (right of the photo), decoration anywhere. Always run `guides` and open the `.mobile.png`.

**Instagram / Facebook / WhatsApp stories and Reels (1080×1920).** Leave ~250 px clear top and bottom for the app UI. Portrait feed posts (1080×1350, 4:5) take the most feed space.

**Facebook Page cover (851×315), Pinterest Pin (1000×1500), Twitch profile banner (1200×480).** Cover: the profile picture overlaps the bottom-left on mobile (no official zone published — keep text right-of-center). Pin: tall 2:3, safe content sits inside Pinterest's own inset (`guides` draws it); the exact WxH isn't stated in Pinterest's docs, so it's unverified — re-check before a launch. Banner: wide and short (5:2) — concentrate the logo/text on the left since browsers can stretch it wider; unverified (Twitch's help page couldn't be fetched to confirm).

**Google Play.** Feature graphic 1024×500 (no alpha): short headline + product, centred — it's often cropped in collections. Phone screenshots 1080×1920 (9:16; each side 320–3840 px; long side ≤ 2× the short side; at least 2, up to 8).

**App Store screenshots** (iPhone 6.9″ 1320×2868 is the required size; 6.5″ 1284×2778 is the alternative; iPad 13″ 2064×2752; 1–10 per device, no alpha). Pattern that works:
- a short headline (2–5 words) in the top ~15–20 %, then the app UI large below it, with a simple device frame
- the same layout, colors and type across the whole set; the first three matter most (they show in search)
- show the app in use (Apple's review guidelines ask for this — not just title art or a splash screen)
- **Fill the screen.** A 1320×2868 shot shows a phone ≈ 900–1000 px wide and ≈ 2000 px tall, so the screen needs 8–10 rows/cards at readable size (type ≥ 30 px, rows ≥ 120 px). A half-empty screen looks unfinished — add real-looking rows, enlarge the cards, or crop the phone off the bottom edge so less screen shows.
- **No real app UI yet?** Build a plainly generic, clearly-mock phone screen from shapes and label it mock in `share-copy.txt`. Never invent features or numbers. If the user has real screenshots, embed them (PNG) inside the frame — that's the best result.

```js
// device frame (Satori): rounded body + inner screen; drop a real screenshot <img> into `screen`
const phone = (w, screen) => ({ type: "div", props: { style: { display: "flex", width: w, height: w * 2.05, borderRadius: w * 0.14,
  border: `${w * 0.03}px solid #111`, background: "#000", overflow: "hidden" }, children: [screen] } });
```

## A set of sizes from one design

For several platforms (or a screenshot series), put a builder `(width, height) => tree` in a second helper (e.g. `_card.mjs`) that imports colors/fonts from `_brand.mjs` (see step-3-design.md), and write one small entry file per size, each with its own `FORMAT`, `FONTS` and — for stores — `alpha: false`. A screenshot series is usually better as one design with `VARIANTS` (step-3-design.md) instead of one file per size. Re-check placement per size; one layout rarely fits both a 1584×396 banner and a 1080×1920 story.
