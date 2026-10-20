# Handoff: read this first

The one current note for whichever agent works next (Claude Code or Codex). Update **Now** before you
stop. The rules are in [`AGENTS.md`](../AGENTS.md).

## Now

- **Last updated:** October 19, 2026, by Claude Code (About's new circle live).
- **Folder:** `C:\Users\mcbig\Documents\codes\bigh-website`, branch `studio`, tracking `origin/main`.
- **Live (October 19, latest):** About's opening circle is now circle A, "heavy to dry" (a wet,
  heavy start that thins into dry streaks and lifts before it closes), and its gold leaf floats
  down onto the stroke like a real flake, then settles and catches the light; the spark of light
  that ran round the old circle is gone. Mo picked it from three new circles; Claude pushed `main`
  to `6e8aaca` (`ea13c93` plus that one commit). Production `dpl_6eTzh1tqkEpWqmBV1nM9w3YfxVJ7`;
  the demo alias points to it. Public demo: `qa_about` 353/353, `qa_home_ink` 282/282, `qa_nav`
  436/436 (`docs/public-demo.md`).
- **Live before that (October 19):** all of `studio`, which Mo pushed as `ea13c93` (NuriCell layout
  B, About's oak, the redwood park sign in every page's footer and the homepage science section).
  Public demo then: `qa_home_ink` 282, `qa_nav` 436, `qa_fda` 220, `qa_about` 353,
  `qa_propolis_ink` 273, `qa_opc_ink` 185, `qa_nuricell_ink` 355, `qa_turmerific_ink` 155,
  `qa_nature_calm_ink` 159, `qa_science_ink` 1279, `qa_support` 341, all passing.
- **State:** `studio` is `main` plus two notes commits (and `qa_support`'s allowance fix), not
  pushed; the next push is a fast-forward.
- **Turmerific on a local server:** the page never finishes loading under `next start` (its
  `soak-v1.webp` sprite and three link prefetches stay open, filling HTTP/1.1's six connections),
  so `qa_turmerific_ink` and the end of `qa_fda` time out locally. The live site shows the same open
  requests but finishes over HTTP/2, and both checks pass there. Not fixed; worth a look.
- **NuriCell layout B (Mo picked from mockups, October 19):** from 960px the lantern hangs right of
  its words, the capsule stands in the middle of its four ingredients, the books run in from the
  page edge, Dr. Liu stands right, the brushed 3 × 30 = 90 goes across the page. Phones keep one
  column. NuriCell only; Mo said leave the other four product pages as they are for now.
- **About (Mo picked both from mockups, October 19):** "Our purpose" shows a big painted valley
  oak (rope swing, gold light in the roots) in place of the seedling, larger than the page's other
  paintings on purpose; the mission line is a step under the heading, in ink. The opening circle's
  gold leaf lands as a spark of gold light runs once round the stroke, then glints now and then.
  The oak was painted with Codex's image tool (no API spend); notes in `reference/ink-pages/spend.md`.
  Its description is a draft translation (m900).
- **About checks (live):** on the built release copy `qa_about` 353/353, `qa_home_ink` 282/282,
  `qa_nav` 436/436; on the public demo the same plus `qa_nuricell_ink` 355/355. Desktop, phone and
  the four other languages inspected; the circle filmed frame by frame on dev, the built site and
  the demo. `qa_about`'s allowance for Next's "preloaded but not used" CSS warning now accepts
  Vercel's `?dpl=…` on CSS addresses (it counted that harmless warning on the first public run).
  A local `next start` once hung on one image resize under heavy load (NuriCell's unlit lantern at
  640px): restarting the server cleared it; Vercel's own image service served it fine.
- **Customers:** `bighnow.com` is still the old WordPress site (checked October 18). Nothing in
  this repo reaches it yet.
- **Homepage science section (live; Mo picked from mockups, October 19, Claude Code):** each of "Make
  sense of the science."'s three topics has its own painting (a hummingbird at California sage, a
  cut apple kept fresh by a Meyer lemon, a Joshua tree at three ages on the age slider), so the
  mitochondrion shows only in "Tiny power plants." Mo chose the Joshua tree over a second oak,
  since About now has the oak. The slider shows one whole tree at a time, never two blended.
  Built on branch `home-science` in a separate worktree while another session worked here, then
  replayed onto this `studio` and fast-forwarded in. Built site `qa_home_ink` 282/282 and
  `qa_nav` 436/436, desktop (with motion) and phone screenshots. Notes:
  `reference/ink-pages/home-science/README.md`; rule: DESIGN.md "The Science Stage Rule".
- **In progress:** None. **Next:** Mo's call.

## What's live

Public demo: <https://bigh-website-demo.vercel.app/>. It shows the production build of `main`
at `ad3561e`, the same build as <https://bigh-website.vercel.app/> (the October 18 Propolis work
plus NuriCell layout B). `bighnow.com` is still the old WordPress site.

Every page is in Ink & Gold:

| Page                 | Its own idea                                                                             | Last public browser check             |
| -------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------- |
| Home                 | Crane; green spring watercolour in the paintings (Mo's pick C, Oct 16); buttons stay ink | `qa_home_ink` 282/282 (Oct 19)        |
| Menu bar             | "Inscription", all five bottles in the Products drop-down                                | `qa_nav` 436/436 (Oct 19)             |
| Footer               | FDA statement on a painted California trail sign                                         | `qa_fda` 220/220 (Oct 18)             |
| About                | Design C, "circle"                                                                       | `qa_about` 343/343 (Oct 16)           |
| NuriCell             | Paper lantern that lights; each painting in its own place (layout B, Oct 19)             | `qa_nuricell_ink` 355/355 (Oct 19)    |
| Green Bee Propolis   | Bold Signature desktop; Editorial pair mobile; gold flowing into the bee tree            | `qa_propolis_ink` 273/273 (Oct 18)    |
| Advanced OPC Formula | Grapes lit from inside                                                                   | `qa_opc_ink` 185/185 (Oct 16)         |
| Turmerific           | Gold soaking into the paper                                                              | `qa_turmerific_ink` 155/155 (Oct 16)  |
| Nature Calm          | Still lake whose gold gathers into one line                                              | `qa_nature_calm_ink` 159/159 (Oct 16) |
| Science              | Dr. Liu's life as a handscroll                                                           | `qa_science_ink` 1279/1279 (Oct 18)   |
| Support              | "Pull up a chair" porch; the form is a preview and sends nothing                         | `qa_support` 341/341 (Oct 16)         |

Details of each go-live are in [`public-demo.md`](public-demo.md). Each page's notes, prompts and
spend are in `reference/ink-pages/<page>/`.

## Unfinished or waiting on Mo

- **Translations:** new lines are drafts and need a native speaker's check: NuriCell m594–m609,
  Science m650–m661 (some older Science lines are still English in four languages), OPC m700–m705,
  Turmerific m740–m744, Nature Calm m780–m784, About's oak m900. Support is English only for now
  (its keys start at m618).
- **Support form:** sends nothing yet. Real email needs an email service and domain setup (Mo's call
  and spend).
- **Capsule colours:** unknown for Turmerific (painted gold) and Nature Calm (painted pale). Ask Mo.
- **Turmerific:** a liver question for the FAQ waits on Mo's research.
- **Green spring on other pages:** only the homepage has the watercolour tint. Mo hasn't been asked.
- **Homepage:** a font for Chinese, Japanese and Korean titles is still open.
- **Not connected yet:** Sign up (placeholder until Mo gives the link), the store and checkout.
- **Customer stories** are labelled fictional samples until real reviews exist.
- **Dr. Liu** hasn't seen his NuriCell painting yet.

## How this was checked (this setup)

- `studio` was cut from the newest `origin/main` (`bf4cb84`). `npm ci` installed cleanly.
- `npm run build` passed (after moving an old, git-ignored experiment, `scripts/qa/out/editorial-build/`,
  out to `C:\Users\mcbig\Documents\codes\bigh-archive\main-folder-leftovers-2026-10-16\`; its stray
  `homepage.tsx` broke the type check).
- On the built site (:3006): `qa_home_ink` 282/282, `qa_opc_ink` 185/185, `qa_nav` 436/436.
- Codex, run read-only in this folder, answered from this rulebook: branch `studio`, read this note
  first, originals and prompts in `reference/ink-pages/<page>/`, commit and update **Now** before
  switching.

## How to run the preview

```sh
npm ci                                              # after a pull that changed package.json
npm run dev -- --hostname localhost --port 3007     # dev server: http://localhost:3007
npm run build                                       # production build
npm start -- --hostname localhost --port 3006       # built site: http://localhost:3006
python -X utf8 scripts/qa/qa_home_ink.py http://localhost:3006
```

Claude Code: the previews "bigh-website" (:3007) and "bigh-website-prod" (:3006). Locales live at
`/`, `/kr`, `/jp`, `/cns`, `/vn`.

## Old folders

About 30 other copies sit in `C:\Users\mcbig\Documents\codes\bigh-*` (one per past task), plus one in
Codex's own worktrees folder. All their finished work is on `main`. A few hold leftovers that never
went live: old demo-notes commits (`support-page`, `home-gold-word`, `product-turmerific`), the
rejected About B design (`about-b`), the About comparison preview (`about-compare`), a June experiment
(`for-real`, with unsaved files) and unsaved files in `bigh-home`, `bigh-main-preview` and
`.claude/worktrees/hero-section-redesign`. Don't work in them. Ask Mo before deleting any.
