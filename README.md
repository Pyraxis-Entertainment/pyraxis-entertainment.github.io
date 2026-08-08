# pyraxisentertainment.com

The Pyraxis Entertainment website. Plain static HTML and CSS, served by
GitHub Pages from this repository.

## The three rules

An earlier version of this file banned frameworks, build steps and
JavaScript outright. That rule was aimed at the right target but described
it badly, and it got bent the first time a good idea came along. Here is
what it was actually protecting.

### 1. Zero money

Nothing on or around this site may cost anything, now or on a delay.

Free tiers count as free only while they are: form services, comment
widgets and analytics typically cap at a low monthly volume and then bill.
Before adopting one, write down its ceiling and what happens at the
ceiling. The risk is accumulation rather than any single charge — one small
monthly tool is nothing, five of them arriving separately over a year is a
bill nobody decided to pay.

Current incremental run rate is **zero**. Pages is free for public repos
and the domain is already committed. Keep it there.

### 2. One person must be able to edit and deploy this site in five years, with no toolchain archaeology

- **First-party JavaScript: unrestricted.** It is just files in the repo.
- **Third-party libraries: allowed, but never from a CDN.** A CDN link is a
  permanent dependency on someone else's uptime and versioning, and it
  fails *silently* years later. If a library earns its place, **vendor it**
  — copy the file into `assets/`, record its version and licence here, done.
- **Build steps and static site generators: not banned, triggered.** At
  this size, duplicating the header and footer is cheaper than a
  toolchain. If it is ever revisited, prefer a single-binary generator
  (Hugo) over an npm-dependency one: the failure being avoided is
  `npm install` not working in 2031.
- **The trigger is edit frequency, not page count.** An earlier version of
  this rule fired at "roughly ten pages or five devlog entries". That
  counted the wrong thing: page count is only a proxy for the real cost,
  which is **how often the shared header and footer actually change**. Ten
  copies nobody touches cost nothing to keep; three you edit weekly hurt.

  **The trigger: the next two times you change the header or footer and
  resent doing it N times over, adopt a generator.** Log the first
  occurrence here when it happens, with the date and what changed — one
  occurrence is an anecdote, two in a row is the signal.

  *Occurrences logged so far: none.*
- No paid fonts, no tracking scripts, no third-party embeds that phone
  home without a stated reason.

### 3. Confidentiality — unchanged

No game codenames, no revenue figures, no release dates, no AI-generated
images presented as final art. The confidentiality grep stays in the check
suite. See "What never goes on this site" at the end of this file.

### What that means in practice today

One script, `assets/compare.js` — about sixty lines of first-party vanilla
JavaScript that turns the before/after block into a draggable comparison.
No library, no CDN, nothing to install, and the page is complete without
it.

### Vendored assets

Anything copied into this repository from elsewhere gets a row here with its
licence, as Rule 2 requires. **The site makes no request to any host it does
not own.**

| Asset | Files | Licence | Source |
|---|---|---|---|
| DM Sans | `assets/fonts/dmsans-{normal,italic}-{latin,latin-ext}.woff2` | SIL Open Font Licence 1.1 | Google Fonts |
| Michroma | `assets/fonts/michroma-normal-{latin,latin-ext}.woff2` | SIL Open Font Licence 1.1 | Google Fonts |

Six files, 145 KB. DM Sans is a **variable** font, so one file per style
covers the whole 300–500 weight range. The `latin` / `latin-ext` split and
its `unicode-range` values are Google's own, kept so a browser downloads only
the subset a page needs. Declared with `@font-face` at the top of
`assets/site.css`, `font-display: swap`.

**Why self-hosted rather than linked.** Rule 2 bans CDN dependencies, and two
render-blocking requests per page is a real cost. But the deciding argument
was neither: this site has no privacy notice because it collects nothing, and
that claim was slightly untrue while a Google Fonts stylesheet sent every
visitor's IP to Google on page load. Self-hosting does not reduce a risk so
much as make a statement we already make completely true.

**If you add or update a font,** add its row above, keep the licence, and
re-check that no page requests an external host.

## Layout

```
index.html                        Studio landing page
geomancer/index.html              Geomancer — pitch, features, gallery, FAQ
geomancer/why/index.html          Why imported terrain has no rivers
geomancer/docs/index.html         Documentation — requirements, help, bug template
geomancer/docs/water/index.html   The Water module guide
geomancer/changelog/index.html    Releases and engine-version support
devlog/index.html                 Devlog venue — entry list, newest first
devlog/geomancer-devlog-1.html    Devlog entry
contact/index.html                Contact — routed by intent
404.html                          Not found — root-absolute paths only, see below
sitemap.xml                       Hand-written, one line per page
robots.txt                        Allows everything, points at the sitemap
assets/site.css                   All site styles
assets/compare.js                 Before/after slider (the only script)
assets/fonts/                     DM Sans and Michroma, vendored (see above)
assets/shots/                     Web images (WebP + JPEG), generated
assets/og-image.jpg               Social preview card, generated
tools/derive-shots.py             Image derivation (see below)
CNAME .nojekyll                   Domain and Pages configuration — leave alone
```

The header and footer are duplicated in each page rather than shared by a
template. That is the accepted trade for having no build step. **If you
change one, change them all** — and note that this duplication is exactly
what the trigger in Rule 2 is watching.

On documentation pages the primary nav marks Geomancer with
`aria-current="true"`, not `"page"`. A docs page is *inside* the Geomancer
section but is not the Geomancer page, and `"page"` would be a false claim
to a screen reader.

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
- **Check contrast by enumerating rendered pairs, not by checking the
  palette.** Walk every element that owns visible text, composite the
  background actually painted behind it through all its ancestors, and
  compare that to the computed colour. Nothing below 4.5:1. The floor today
  is `--text-dim` on Charcoal at **5.30:1**, over 89 pairs across nine pages.

  Checking the named tokens instead is not a shortcut, it is a different and
  weaker test, and it has already missed a real failure: the breadcrumb
  separators were set in `--rule-strong` and sat at **1.89:1**, failing both
  the 4.5:1 text floor and the 3:1 non-text floor, while a token-based pass
  reported the site clean. `--rule-strong` is a border tint — it is not on
  the text ladder, and a token used outside its purpose is exactly what pair
  enumeration catches and token-checking cannot.
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

## Maintaining the sitemap

`sitemap.xml` is hand-written, one `<url>` line per page. At eight pages that
is cheaper and more reliable than anything that would generate it, and it is
the same trade as the duplicated header and footer.

**A new page is added to `sitemap.xml` in the same sitting it is created.**
There is no build step to catch the omission and nothing will fail loudly —
the page simply never gets found, which is a bug you discover months later
via an empty analytics row you are not collecting either.

Three things deliberately not in that file:

- **`lastmod`, `changefreq`, `priority`.** The last two are ignored by search
  engines. A hand-kept `lastmod` goes stale the first time somebody edits a
  page and forgets, and a date that is wrong is worse than one that is absent
  because it is believed. If a generator ever arrives and can stamp these
  accurately, that is when they go in.
- **`404.html`.** An error page must never be offered as a destination.
- **Archived documentation** under `geomancer/docs/<version>/`. Those pages
  carry `noindex` and are meant to stay out of results entirely — listing
  them in a sitemap would say the opposite.

### Why there is no `Disallow` for archived docs

The obvious-looking belt-and-braces — `noindex` on the page *and* a `Disallow`
line in `robots.txt` — does not work, and is worth understanding before
someone adds it. `Disallow` stops the page being fetched, so the `noindex`
inside it is never read; a disallowed page that is linked from anywhere can
still appear in results as a bare URL. The two are alternatives. `noindex` is
the right one here because it removes the page outright rather than merely
declining to look at it. The version scheme's step 2 is the whole mechanism.

## The why page

`geomancer/why/` is the acquisition piece — everything else on the site is
bottom-of-funnel, and this is the one page written for somebody who has the
problem and has never heard of us. Two conventions apply to it and to nothing
else:

**It is edited over time, and deliberately not a dated log.** It describes a
problem in other people's tooling, and that moves. So it gets no
`.verified-note` and no visible date — the devlog convention is the opposite
of what this page needs, and applying it would freeze a page whose whole job
is to stay current.

**Its `dateModified` has nothing on the page to keep it honest.** Every other
piece of structured data on this site mirrors something a reader can see: the
docs pages' `dateModified` matches their visible *Checked* stamp, the FAQ
answers are the visible answers. This page's is the single exception, and it
is there because §5b.1 requires it. **Bump it whenever the body changes.**
Nobody reading the page can catch it if you don't.

**Its URL is permanent.** `/geomancer/why/` is short and angle-agnostic on
purpose: the search language lives in the `<title>` and `<h1>`, which can be
rewritten freely. A keyword baked into the path would lock the angle in
forever.

## The 404 page

`404.html` is served by GitHub Pages for any address that does not resolve,
which means it can render at `/geomancer/docs/typo/` as easily as at
`/nonsense`. **Every path in it is root-absolute (`/assets/site.css`, not
`../assets/site.css`) and must stay that way** — a relative path resolves
against the invented address, 404s in turn, and leaves the error page itself
unstyled with every link broken. It also carries no canonical tag, for the
same reason: the URL varies.

It is the one page whose header and footer are *not* copied verbatim from a
neighbour, because those copies use relative paths. When the header or footer
changes site-wide, this page needs the same change made with absolute paths.

## Adding a devlog entry

1. Copy `devlog/geomancer-devlog-1.html` to
   `devlog/<product>-devlog-<n>.html`.
2. Replace the `<article>` contents. Update `<title>`, the meta description,
   `og:title`, `og:description` and the canonical URL.
3. Set the entry date in `.entry-date`, and the verified date in the
   `.verified-note` paragraph.
4. Add a `<li>` to the top of `.entry-list` in `devlog/index.html`. Newest
   first.
5. **If the entry is about a product, add the same `<li>` to that product
   page's "Latest from the devlog" strip** — `geomancer/index.html` has one.
   The strip is a filtered view of the devlog, but with no build step the
   filtering is done by hand, so a product entry is listed in two places.
   Carry the `data-product` attribute across; it is the tag a generator
   would filter on if one ever arrives.
6. **Add the entry's URL to `sitemap.xml`.** See "Maintaining the sitemap"
   above. Nothing fails if you forget — the entry is simply never found.

That is four files per entry. It is fine at this size, and it is a
*different* cost from the one Rule 2's trigger watches: adding an entry is
new work each time, where changing the header is the same edit repeated
across every page. Repetition of the second kind is what earns a generator.
If writing entries ever becomes the thing that hurts, that is worth saying
out loud — but it is not the signal Rule 2 is listening for.

**Entries are dated logs.** Each one says when its figures were checked and
reports what was true that day. An entry does not get edited later because
the numbers moved — that is the point of the date. Write the entry, date it,
leave it alone.

## Adding or updating documentation

Documentation lives under the product directory, so each product owns its
own docs and a second product needs no restructure.

```
geomancer/docs/            the current release's documentation
geomancer/docs/water/      one page per module
geomancer/changelog/       releases and engine-version support
```

**The changelog sits beside `docs/`, not inside it.** It is cumulative and
always current, so it must not be caught up in a version snapshot — a
frozen 1.0 changelog would be nonsense.

### When a table gets a `<caption>`

A table gets a caption **when it sits under a shared `h2` alongside other
tables and has no heading of its own** — the caption is what tells them
apart. A table that already owns a heading has its caption; adding one
repeats the label.

That is why the water page has four captions and six tables, and the split is
deliberate rather than an oversight. `.doc-body h3` and `.table-wrap caption`
are both gold small caps, so a caption directly under a heading of the same
text renders as the same label printed twice.

*Provenance: this was written down because an audit read the 4-of-6 split as
an inconsistency and asked for the two missing captions. It was right when
written — the redundancy only appeared once `.doc-body h3` became gold small
caps in the same pass, which is what made a caption and a heading
indistinguishable. A finding can go stale inside the work that acts on it.*

### The version scheme

`geomancer/docs/` **always describes the current release.** That address
never moves, which is the whole point of it: it is the URL printed on the
store listing, inside the plugin, and in Discord, and it stays correct
without any of those being reprinted.

When a new version ships:

1. Copy `geomancer/docs/` to `geomancer/docs/<outgoing version>/` — for
   example `geomancer/docs/1.0/`. **Copy the current pages only: `index.html`
   and the module directories.** Do not copy previous version directories into
   the new one, or each release nests the whole archive history inside itself.
2. In the copy, add the `.doc-archived` banner to each page naming the
   version it documents and linking to the current one, and add
   `<meta name="robots" content="noindex">` to each `<head>`.
3. Update `geomancer/docs/` in place for the new release, and bump the
   `.doc-version` stamp on every page.
4. Add the release to `geomancer/changelog/`.

**An archived version is never edited again.** Same convention as a devlog
entry: it is a dated record of what was true for that release, and it stays
correct precisely because nobody goes back and touches it. Each page states
which release it describes and when it was last checked.

**That rule beats "if you change one, change them all."** The two collide the
first time the header or footer changes site-wide, because archived pages carry
their own copies. Archives are deliberately left behind: an archived page is a
snapshot, and a snapshot with next year's navigation in it is not one. The
`.doc-archived` banner is what tells the reader they are looking at an old page,
so a slightly old header is consistent rather than broken. **Only the current
docs are in scope for a site-wide change.**

The `noindex` in step 2 is deliberate. Archived pages are near-identical to
the current ones, and left indexable they compete with them — sending
people searching for help to documentation for a version they are not
running. Readers reach archives through the version links, not through
Google.

### The support sentence

One sentence describes how support works, and it appears on four surfaces:
`contact/index.html`, `geomancer/docs/index.html`, the Fab listing, and the
Discord `#geomancer` topic and pin.

> I check the inbox every weekday evening, so you'll have an answer within one working day.

*Provenance: the version ruled on 7 August reads "I check **it** every weekday
evening…" in Discord's `#welcome`, where the preceding sentence supplies the
antecedent. Everywhere else "it" has nothing to refer to, so the noun is stated.
That is an adaptation, not a re-ruling — flagged rather than assumed.*

**If it changes, it changes in all four places in the same sitting** — and the string must be identical, not merely equivalent. Two
different published response windows is worse than having none, because
each one makes the other look careless. The wording is deliberate: naming
*when the inbox is looked at* is a routine that can be kept indefinitely,
where a bare window is a promise that fails the first busy week.

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
| `Docs_Water_Panel.png` | `geomancer-docs-panel` | **not captured yet** |
| `Docs_Water_Generated.png` | `geomancer-docs-generated` | **not captured yet** |
| `Docs_Water_CarveGuard.png` | `geomancer-docs-carveguard` | **not captured yet** |

Capture the outstanding shots to exactly those filenames and the script
picks them up with no further changes. The last three are documentation
captures and fill the reserved frames in `geomancer/docs/water/`.

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

- [ ] Capture the outstanding shots and re-run the derive script.
- [ ] Update every `<img>` `width`/`height` to the values the script prints.
- [ ] Replace each `.frame-pending` on `geomancer/index.html` and the devlog
      entry with a real `<picture>`. Each reserved slot carries the exact
      markup and alt text to use in an HTML comment beside it.
- [ ] Set the entry date in `devlog/geomancer-devlog-1.html`.
- [ ] Set the figures-verified date in the same file.
- [ ] Set the date on the entry card in `devlog/index.html`.
- [ ] Settle the four invented sentences in `geomancer/why/` — confirm,
      rewrite or cut each — then remove that page's `.pending` banner. They
      are quoted in the banner itself, so this does not need the copy
      document open. This is the only banner on the site waiting on
      authorship rather than on a capture or a ruling.
- [ ] Remove the `.pending` banner from `geomancer/index.html`.
- [ ] Remove the `.pending` banner from `devlog/index.html`.
- [ ] Remove the `.pending` banner from `devlog/geomancer-devlog-1.html`.
- [ ] Re-verify the landscape carving section of `geomancer/docs/water/`
      against the shipped build, then remove that page's `.pending` banner.
- [ ] Remove the `.pending` banners from `geomancer/docs/` and
      `geomancer/changelog/` once their remaining bullets are closed. The
      engine-version support commitment is ruled and both pages now state it.
- [ ] Confirm the support sentence is identical on `contact/index.html`,
      `geomancer/docs/index.html`, the Fab listing and the Discord copy.
      One sentence, four surfaces — see "The support sentence" above.
- [ ] Search the repository for `PENDING` — it should return nothing.
- [ ] Check every link resolves.
- [ ] Confirm the devlog strip on `geomancer/index.html` matches
      `devlog/index.html`.
- [ ] **Settle the gallery layout on `geomancer/index.html` with the real
      images in place.** `.gallery` lays out 2-up at desktop widths, and the
      three figures leave the last one alone in its own row. Deliberately not
      fixed against the placeholders: the final composition depends on images
      that do not exist yet, at aspect ratios nobody knows, so solving it now
      means solving it twice. Gallery images are pinned to the frames' 16:9
      so the grid holds still until then. Decide it at the capture session.

Nothing on the site carries a release date, and nothing should. "When it's
ready" is the promise.

## What never goes on this site

Unreleased game titles and working names, revenue or pricing, release dates,
internal technical detail, internal file or folder paths, contributor names
without their consent, and AI-generated images presented as final art.

### HTML comments ship

A shipped HTML comment may reference files that ship in this repo
(`README.md`, `tools/derive-shots.py`). It must not reference files that do
not — those are internal documents and naming them is a disclosure.

**Grep before committing: a filename in a comment that is not in this repo is
the tell.** Two comments carrying an internal note's filename reached a public
branch this way, and neither needed it — the `.pending` banner is what
actually stops an unruled paragraph shipping, not a pointer to where the
options were written down.

---

© 2026 Pyraxis Entertainment. All rights reserved.
