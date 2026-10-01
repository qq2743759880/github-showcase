---
name: record
description: "Record terminal demos of CLIs and TUIs and publish them as README-ready GIFs — interactively via asciinema/agg, or fully unattended by driving the recorder inside a pty with a timed key script. Covers storyboarding from the app's real keybindings, frame-by-frame verification, and the docs/media embed convention. Use when asked to record a demo, capture a TUI, make a GIF/screencast, or add a video example to a README."
metadata:
  author: TGPSKI
  version: "1.0"
compatibility: "POSIX, zsh, asciinema, agg. Unattended driving and frame checks additionally use Python 3 (stdlib) and ImageMagick."
---

# Record

Produce a terminal-demo GIF that is worth committing: storyboarded from the
app's actual keybindings, recorded at a deliberate geometry, verified frame
by frame, and embedded where a reader will meet it.

The claim this workflow is built on:

> **A demo GIF is a claim about the software. Verify it like one.**

A recording that opens on the wrong view, types into a picker nobody knew
was there, or scrolls past the table it was supposed to show does not just
look sloppy — it documents behavior the software doesn't have. Every failure
this skill guards against was hit in production use the day it was written.

## The two modes

| Mode | When | How |
|---|---|---|
| **Interactive** | A human at the keyboard wants to narrate their own pacing | `./record.sh DIR CMD...` — the command is preloaded into the prompt buffer; press Enter, drive, Ctrl-D |
| **Unattended** | An agent is producing the demo, or the demo must be reproducible | `assets/drive.py` runs `record.sh` inside a pty and feeds it a timed key script |

`record.sh` is the single recorder either way: asciinema capture → path
scrubbing → optional line pacing → tail trim → agg GIF render. The wrappers
(`record-demo.sh`, `record-example.sh`) are thin project-flavored defaults.

## Phase 1 — Storyboard from source, not memory

Before recording anything:

1. **Read the app's key handling** (`handle_key`, `case "$key"`, keymap
   table). Do not guess bindings. The storyboard is a sequence of
   `(dwell, key)` pairs, and a wrong key silently ruins the take.
2. **Establish the startup view.** Apps open in pickers, splash states, or
   data-dependent views ("live" when work is in flight, "cells" otherwise).
   A tab-cycle script written against the wrong start view lands every
   subsequent frame one view off. If the start view depends on state, pin
   the state or storyboard from what will actually be on screen.
3. **Choose geometry for the content.** Dense matrices want more columns and
   a smaller font (160×42 @ 14pt); a simple two-view demo reads better at
   120×30 @ 16pt. The GIF is read at README width — favor legibility over
   fitting everything.
4. **Plan the ending.** The final frame lingers (`--last-frame-duration`);
   end on the view that sells the tool, not on a quit message.

## Phase 2 — Smoke before you record

Run the exact command through a pty smoke first (if the target repo vendors
`pane`, `pane.pty_smoke` is already there; otherwise `assets/drive.py
--smoke` does the same job): correct exit, no traceback, and — for a key
script — no key swallowed by an unexpected mode. Recording is the expensive
way to discover the app opened in a search prompt.

## Phase 3 — Record

Interactive: `./record.sh . make demo` and drive it yourself.

Unattended:

```bash
assets/drive.py \
  --record ./record.sh --dir /path/to/repo \
  --basename demo --cols 120 --rows 30 --font-size 16 \
  --script "6:ENTER 3.5:v 2.5:j 1.2:k 1.5:/ 0.6:scan 0.8:ENTER 2.8:r 1.5:v 3:q 1.5:CTRL_D"
```

The script grammar is `delay:keys` pairs — literal characters sent as-is,
named keys in caps (`ENTER`, `TAB`, `SPACE`, `ESC`, `CTRL_D`, `UP`, `DOWN`).
The first `ENTER` fires the preloaded command; the final `CTRL_D` closes the
recorded shell so agg can render. Leave real dwells between keys: the GIF
inherits your pacing, and idle compression (`--idle-time-limit`) trims dead
air anyway.

## Phase 4 — Verify every frame

Never ship a GIF you have only seen described. Extract and read the frames:

```bash
magick out.gif -coalesce frame_%02d.png
```

**`-coalesce` is mandatory.** Plain extraction yields inter-frame diffs that
look like corrupted renders and will send you chasing a bug that isn't
there.

Check, at minimum:

- the storyboard actually happened — every view you meant to show is there,
  none you didn't (a tab overshoot lands on a view whose empty state reads
  as breakage);
- no half-drawn or input-mode frames as load-bearing content;
- text is legible at the size a README renders it;
- the last frame is the one you chose in Phase 1.

A failed check means adjusting the key script or dwells and re-recording —
takes are cheap, published mistakes are not.

## Phase 5 — Publish

- Commit the curated GIF to `docs/media/<name>.gif`; keep raw takes out of
  history (`recordings/` is gitignored — the committed artifact is the
  publication, the cast is regenerable).
- Embed near the top of the README with **alt text that narrates the
  storyboard** (what views appear, what the interaction shows) and a one-line
  caption pointing at the demo's entry point (`make demo`, the example dir).
- Keep GIFs small: idle-time-limit ~1.5s, deliberate dwells, minimal font.
  Tens-of-KB to low-hundreds is the healthy range for a README.

## What NOT to do

- **Never publish unverified frames.** The one time you skip Phase 4 is the
  time the demo opened in a facet picker and space-ticked a checkbox instead
  of opening the detail card.
- **Never guess keybindings or the start view** — read them from source, and
  re-read them when the app's state can change what launches.
- **Never leave real paths in a cast.** `record.sh` scrubs the working
  directory and project root into labels; keep it that way when adding
  flags. Check visibility before a recording shows repo names, hostnames, or
  data that isn't public.
- **Never pipe the command's output into the recorder.** The preloaded
  prompt buffer exists so TTY-aware programs behave; piping breaks curses
  apps and progress bars.
- **Never re-record over a published basename without re-verifying** — the
  README now claims whatever the new take shows.
