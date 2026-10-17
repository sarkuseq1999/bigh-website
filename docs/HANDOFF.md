# Handoff: read this first

The one current note for whichever agent works next (Claude Code or Codex). Update **Now** before you
stop. The rules are in [`AGENTS.md`](../AGENTS.md).

## Now

- **Last updated:** October 16, 2026, by Codex.
- **Folder:** `C:\Users\mcbig\Documents\codes\bigh-website`, branch `studio`, tracking `origin/main`.
- **State:** `studio` contains the setup commits plus a local Green Bee Propolis design proposal.
  The public demo still shows `bf4cb84`; nothing from this design turn has been pushed.
- **In progress:** None. The Propolis refinement is complete locally and ready for Mo's review.
- **Next:** Mo reviews the local proposal. It uses Ysabeau titles, a name beside the real bottle,
  alternating chapter paintings, chapter links and clearer research rows on phones. The existing
  copy, paintings, gold animation, menu and footer remain. Notes and A/B mockups:
  `reference/ink-pages/propolis/README.md`. Publishing requires Mo's yes.
- **Local checks:** Production build, lint, TypeScript and changed-file formatting passed.
  Propolis: 217/217, homepage: 282/282, menu: 436/436. The last change only opts the new Propolis
  shortcuts into heading-aware scrolling; its mouse, keyboard and touch checks passed in the final
  production build, as did a smoke check of the existing homepage chapter link.
- **Visual review:** Built desktop, phone and moving tree states inspected. Codex's assessment is
  9/10; the remaining limit is dense research copy on small phones. Before/after and A/B captures
  are in `reference/ink-pages/mockups/propolis-refinement/`. The built preview is running at
  `http://localhost:3006/products/green-bee-propolis`; the screenshot gallery is at
  `http://localhost:3008/` (this PC only). The dev server is stopped.
- **Phone sharing:** Automatic approval review rejected exposing the unpublished gallery on the
  local network. The gallery was instead bound to loopback. No public deployment or alias changed.

## What's live

Public demo: <https://bigh-website-demo.vercel.app/>. It shows the production build of `main` at
`bf4cb84` (Advanced OPC Formula in Ink & Gold, live October 16).

Every page is in Ink & Gold:

| Page                 | Its own idea                                                                             | Last public browser check             |
| -------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------- |
| Home                 | Crane; green spring watercolour in the paintings (Mo's pick C, Oct 16); buttons stay ink | `qa_home_ink` 282/282 (Oct 16)        |
| Menu bar             | "Inscription", all five bottles in the Products drop-down                                | `qa_nav` 436/436 (Oct 16)             |
| Footer               | FDA statement on a painted California trail sign                                         | `qa_fda` 220/220 (Oct 16)             |
| About                | Design C, "circle"                                                                       | `qa_about` 343/343 (Oct 16)           |
| NuriCell             | Paper lantern that lights                                                                | `qa_nuricell_ink` 359/359 (Oct 16)    |
| Green Bee Propolis   | Gold flowing into the cracks of a bee tree; name on one line                             | `qa_propolis_ink` 204/204 (Oct 16)    |
| Advanced OPC Formula | Grapes lit from inside                                                                   | `qa_opc_ink` 185/185 (Oct 16)         |
| Turmerific           | Gold soaking into the paper                                                              | `qa_turmerific_ink` 155/155 (Oct 16)  |
| Nature Calm          | Still lake whose gold gathers into one line                                              | `qa_nature_calm_ink` 159/159 (Oct 16) |
| Science              | Dr. Liu's life as a handscroll                                                           | `qa_science_ink` 1279/1279 (Oct 16)   |
| Support              | "Pull up a chair" porch; the form is a preview and sends nothing                         | `qa_support` 341/341 (Oct 16)         |

Details of each go-live are in [`public-demo.md`](public-demo.md). Each page's notes, prompts and
spend are in `reference/ink-pages/<page>/`.

## Unfinished or waiting on Mo

- **Translations:** new lines are drafts and need a native speaker's check: NuriCell m594–m609,
  Science m650–m661 (some older Science lines are still English in four languages), OPC m700–m705,
  Turmerific m740–m744, Nature Calm m780–m784. Support is English only for now (its keys start at m618).
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
