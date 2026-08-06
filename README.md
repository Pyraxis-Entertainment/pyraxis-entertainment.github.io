# pyraxisentertainment.com

The Pyraxis Entertainment website. Plain static HTML and CSS, served by
GitHub Pages from this repository.

**No framework, no CMS, no build step, no dependencies.** That is deliberate:
the site should still work, unchanged, in ten years.

There is exactly one script on the site — `assets/compare.js`, about thirty
lines of first-party vanilla JavaScript that turns the before/after block
into a draggable comparison. No library, no CDN, nothing to install, and the
page is complete without it. That is the bar anything else has to clear.

## Layout

```
index.html                     Studio landing page
geomancer/index.html           Geomancer — pitch, features, gallery
devlog/index.html              Devlog venue — entry list, newest first
devlog/geomancer-devlog-1.html Devlog entry
assets/site.css                All site styles
assets/compare.js              Before/after slider (the only script)
assets/shots/                  Web images (WebP + JPEG), generated
assets/og-image.jpg            Social preview card, generated
tools/derive-shots.py          Image derivation (see below)
CNAME .nojekyll                Domain and Pages configuration — leave alone
```

The header and footer are duplicated in each page rather than shared by a
template. That is the accepted trade for having no build step. If you change
one, change all four.

**Each product gets a directory**, so `/geomancer/` can grow a changelog,
docs or a press kit later without moving anything. Internal links point at
the directory (`geomancer/`, not `geomancer/index.html`) so the canonical URL
and the linked URL are the same string. A URL is cheap to change now and
expensive after publication — get it right before the site is live.

## Local preview

```bash
python -m http.server 8000
```

Then open <http://localhost:8000/>. Use the server rather than opening the
files directly: links point at directories, which a `file://` page cannot
resolve.

## Design rules

Colours are defined once as custom properties at the top of `assets/site.css`.

| Token | Value | Use |
|---|---|---|
| Void | `#12121A` | Page background |
| Charcoal | `#1A1A22` | Cards, secondary surfaces |
| Warm Gold | `#C9963C` | Headings, rules, accents |
| Crimson | `#8B1E2F` | Alerts, and one reserved call-to-action |
| Warm White | `#F0EDE6` | Body text |

- **Never** pure black or pure white on a designed surface.
- **Michroma** is for the wordmark only, uppercase, `0.14em` tracking.
  Everything else is **DM Sans**.
- Body text is Warm White on Void. Gold is for headings and rules.
- Every text colour in the stylesheet clears WCAG AA (4.5:1) on Void.
  If you add one, check it.
- Every image needs real alt text describing the visual.
- Keep the `prefers-reduced-motion` block working for any animation added.

`.cta-crimson` is defined but unused. It is reserved for a "View on Fab"
button once the Geomancer listing exists. Do not remove it as dead code.

### Two kinds of placeholder, doing two different jobs

- **`.pending`** — the loud crimson banner at the top of a page. This is the
  safety net that stops an unfinished page going live. It is ugly on purpose.
  Do not soften it.
- **`.frame-pending`** — a media slot whose image has not been shot yet. This
  one is quiet and in-brand: a thin gold frame on Charcoal holding the final
  aspect ratio, with the real caption already beneath it. It should read as
  "not photographed yet", never as "broken".

The frames reserve **16:9**, the native capture aspect. Real captures land
slightly off that once editor chrome is cropped, so expect a percent or two
of shift when an image drops in — not the zero it would be if the exact
dimensions were known in advance.

## Adding a devlog entry

1. Copy `devlog/geomancer-devlog-1.html` to
   `devlog/<product>-devlog-<n>.html`.
2. Replace the `<article>` contents. Update `<title>`, the meta description,
   `og:title`, `og:description` and the canonical URL.
3. Set the entry date in `.entry-date`, and the verified date in the
   `.verified-note` paragraph.
4. Add a `<li>` to the top of `.entry-list` in `devlog/index.html`. Newest
   first.

**Entries are dated logs.** Each one says when its figures were checked and
reports what was true that day. An entry does not get edited later because
the numbers moved — that is the point of the date. Write the entry, date it,
leave it alone.

## Refreshing the shots

Web images are generated from the full-size captures; the captures
themselves are never committed.

```bash
python tools/derive-shots.py --check     # report only
python tools/derive-shots.py             # write the web set
```

Requires Pillow (`pip install Pillow`). This is asset preparation you run by
hand — it is not part of serving the site, and the site has no build step.

Tell it where the captures live, once:

```bash
echo "/path/to/your/Shots" > tools/source-path.txt
```

That file is untracked on purpose — this repository is public.

### How the healing works

Each capture has one canonical filename. Re-capturing a shot means
**overwriting that file**, then re-running the script. The pages never
change, because they already point at stable generated names.

| Capture file | Becomes | Status |
|---|---|---|
| `Devlog1_B_Island_Hero.png` | `geomancer-island-hero` | present |
| `Devlog1_C_Before_Plates.png` | `geomancer-range-plates-before` | present |
| `Devlog1_D_Before_FarHalf.png` | `geomancer-range-farhalf-before` | present |
| `Devlog1_E_After_Complete.png` | `geomancer-range-complete-after` | present, re-capture recommended |
| `Devlog1_A_Before_Template.png` | `geomancer-template-before` | **not captured yet** |
| `Devlog1_A_After_Template.png` | `geomancer-template-after` | **not captured yet** |
| `Devlog1_F_Basin_Wetland.png` | `geomancer-basin-wetland` | **not captured yet** |

Capture the three outstanding shots to exactly those filenames and the
script picks them up with no further changes.

**One thing the script cannot do for you.** Some captures have a strip of
editor UI along the top or bottom edge; the script detects and crops it,
which changes the image's height. So after a re-capture, update the `width`
and `height` attributes on the matching `<img>` tags — the script prints the
exact values to use. Stale numbers make the page jump as images load.

Anything not in that table is not site material. The script also refuses
files whose names contain `Evidence_Comparison`, `_alt_` or `_Raw`.

## Publishing

The site currently carries **`.pending` banners that must not go live**.
They are loud and crimson so they cannot be missed. (The quiet media frames
are fine to show anyone — they are the point of `.frame-pending`.)

Before this goes to `main`:

- [ ] Capture the three outstanding shots and re-run the derive script.
- [ ] Update every `<img>` `width`/`height` to the values the script prints.
- [ ] Replace each `.frame-pending` on `geomancer/index.html` and the devlog
      entry with a real `<picture>`. Each reserved slot carries the exact
      markup and alt text to use in an HTML comment beside it.
- [ ] Set the entry date in `devlog/geomancer-devlog-1.html`.
- [ ] Set the figures-verified date in the same file.
- [ ] Set the date on the entry card in `devlog/index.html`.
- [ ] Remove the `.pending` banner from `geomancer/index.html`.
- [ ] Remove the `.pending` banner from `devlog/index.html`.
- [ ] Remove the `.pending` banner from `devlog/geomancer-devlog-1.html`.
- [ ] Search the repository for `PENDING` — it should return nothing.
- [ ] Check every link resolves.

Nothing on the site carries a release date, and nothing should. "When it's
ready" is the promise.

## What never goes on this site

Unreleased game titles and working names, revenue or pricing, release dates,
internal technical detail, internal file or folder paths, contributor names
without their consent, and AI-generated images presented as final art.

---

© 2026 Pyraxis Entertainment. All rights reserved.
