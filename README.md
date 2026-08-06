# pyraxisentertainment.com

The Pyraxis Entertainment website. Plain static HTML and CSS, served by
GitHub Pages from this repository.

**No framework, no CMS, no build step, no JavaScript.** That is deliberate:
the site should still work, unchanged, in ten years. Anything that would add
a dependency needs a good reason.

## Layout

```
index.html                     Studio landing page
geomancer.html                 Geomancer — pitch, features, gallery
devlog/index.html              Devlog venue — entry list, newest first
devlog/geomancer-devlog-1.html Devlog entry
assets/site.css                All site styles
assets/shots/                  Web images (WebP + JPEG), generated
assets/og-image.jpg            Social preview card, generated
tools/derive-shots.py          Image derivation (see below)
CNAME .nojekyll                Domain and Pages configuration — leave alone
```

The header and footer are duplicated in each page rather than shared by a
template. That is the accepted trade for having no build step. If you change
one, change all four.

## Local preview

```bash
python -m http.server 8000
```

Then open <http://localhost:8000/>. Opening the files directly also works,
since all internal links are relative.

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

Anything not in that table is not site material. The script also refuses
files whose names contain `Evidence_Comparison`, `_alt_` or `_Raw`.

## Publishing

The site currently carries **placeholder blocks that must not go live**.
They are bordered and loud so they cannot be missed.

Before this goes to `main`:

- [ ] Capture the three outstanding shots and re-run the derive script.
- [ ] Replace the reserved-slot blocks on `geomancer.html` and the devlog
      entry with real `<figure>` elements.
- [ ] Set the entry date in `devlog/geomancer-devlog-1.html`.
- [ ] Set the figures-verified date in the same file.
- [ ] Set the date on the entry card in `devlog/index.html`.
- [ ] Remove the `.pending` block from `devlog/index.html`.
- [ ] Remove the `.pending` block from `devlog/geomancer-devlog-1.html`.
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
