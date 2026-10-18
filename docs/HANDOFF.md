# Handoff: read this first

The one current note for whichever agent works next (Claude Code or Codex). Update **Now** before you
stop. The rules are in [`AGENTS.md`](../AGENTS.md).

## Now

- **Last updated:** October 18, 2026, by Codex.
- **Folder:** `C:\Users\mcbig\Documents\codes\bigh-website`, branch `studio`, tracking `origin/main`.
- **State:** Mo approved Bold Signature A with the original purchase card and explicitly asked to
  apply it live to the demo. The approved source is local commit `5a8ed9f`.
- **Demo:** <https://bigh-website-demo.vercel.app/products/green-bee-propolis> now points to preview
  deployment `dpl_Dyn8ybDmMjwUGrbfCXyW5XfgfJMN` (`bigh-website-393kqxd0f-sarkuseq1999s-projects.vercel.app`), in the existing `bigh-website` project.
  Only the demo alias was updated; no production promotion, GitHub push or access-setting change.
- **In progress:** None. The heavy Switzer title keeps Green left, the real bottle centred and
  Bee / Propolis right. The original outlined One bottle card has the capsule, overlapping 45-day
  badge, daily count, centred Add to cart without an arrow, and refund line. The real site's
  existing copy, translations and honest checkout-preview notice remain.
- **Local checks:** Build, lint, TypeScript and changed-file formatting passed. Propolis:
  269/269 passed; homepage: 282/282 checks passed; menu: 436/436 checks passed.
  Desktop and phone screenshots and the tree's gold state were inspected. Visual assessment:
  9/10; the existing introductory paragraph remains fairly long on a small phone.
- **Public verification:** A fresh unauthenticated browser confirmed the updated hero and card,
  HTTP 200, loaded assets, responsive layout, chapter navigation and checkout-preview behavior.
  The public Propolis suite finished with 269/269 passed; desktop and phone
  homepage/menu navigation checks passed without browser errors.
- **Release scope:** Only tracked website code, public assets, translations and build configuration
  were uploaded. Notes, credentials, QA output and local comparison artifacts were excluded.
  Changes from the previous public version are confined to Propolis and its opt-in chapter links.
- **Next:** Mo can review the public demo. Continue the unrelated launch items below only when asked.
- **Local previews:** Built page on `http://localhost:3012/products/green-bee-propolis` during this
  task. The comparison artifacts at `http://localhost:3009/` and `http://localhost:3010/` are preserved.

## What's live

Public demo: <https://bigh-website-demo.vercel.app/>. It shows the preview build of `5a8ed9f`
(approved Bold Signature Propolis opening and original purchase card, live October 18).

Every page is in Ink & Gold:

| Page                 | Its own idea                                                                             | Last public browser check             |
| -------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------- |
| Home                 | Crane; green spring watercolour in the paintings (Mo's pick C, Oct 16); buttons stay ink | `qa_home_ink` 282/282 (Oct 16)        |
| Menu bar             | "Inscription", all five bottles in the Products drop-down                                | `qa_nav` 436/436 (Oct 16)             |
| Footer               | FDA statement on a painted California trail sign                                         | `qa_fda` 220/220 (Oct 16)             |
| About                | Design C, "circle"                                                                       | `qa_about` 343/343 (Oct 16)           |
| NuriCell             | Paper lantern that lights                                                                | `qa_nuricell_ink` 359/359 (Oct 16)    |
| Green Bee Propolis   | Bold Signature opening; real bottle between the name; gold flowing into the bee tree     | `qa_propolis_ink` 269/269 (Oct 18)    |
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
