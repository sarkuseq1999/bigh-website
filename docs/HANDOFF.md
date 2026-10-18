# Handoff: read this first

The one current note for whichever agent works next (Claude Code or Codex). Update **Now** before you
stop. The rules are in [`AGENTS.md`](../AGENTS.md).

## Now

- **Last updated:** October 18, 2026, by Codex.
- **Folder:** `C:\Users\mcbig\Documents\codes\bigh-website`, branch `studio`, tracking `origin/main`.
- **State:** Mo selected mobile B, Editorial pair, for Green Bee Propolis. Source commit `6933d63`
  is live on the existing public demo. The desktop Bold Signature opening is unchanged.
- **Demo:** <https://bigh-website-demo.vercel.app/products/green-bee-propolis>, preview deployment
  `dpl_7QhgdKVpsi3m8DuASqXNVy2ER88G` (`bigh-website-f1unv5zvc-sarkuseq1999s-projects.vercel.app`).
  Only the demo alias changed; no production promotion, GitHub push or access-setting change.
- **Mobile design:** Bold Green / Bee / Propolis on the left beside the authentic bottle; the
  short description and original One bottle card follow. The long explanation and provenance
  come after the purchase controls. No product facts, images, prices or checkout behavior changed.
- **Checks:** Build, lint, TypeScript and formatting passed; Propolis 273/273 passed locally.
  Both the built site and public demo passed all 10 responsive viewport checks (360 through 1440).
  At 360 and 390, bottle/card/button positions match the reviewed B preview within 3px and the
  full button fits the first screen. At 960, 1024 and 1440, desktop comparisons found zero changed
  pixels. Images, card badge spacing, chapter links and the honest checkout notice passed.
- **Visual review:** Actual mobile and tablet screenshots inspected; 9/10. This is the selected
  compact composition; the existing long explanation remains available below the controls.
- **Scope:** Runtime source changes since the prior demo are only `propolis-opening.tsx` and
  `propolis.module.css`. No other product or shared navigation component changed. Focused checks
  were used for this mobile-only request; the previous full homepage/menu checks remain recorded.
- **In progress:** None. **Next:** Mo can review the updated demo.
- **Local previews:** Built update at `http://localhost:3014/products/green-bee-propolis` during
  this task. The three isolated mobile options remain at `http://localhost:3013/`; earlier
  comparison files are preserved. Local URLs are for this PC only.

## What's live

Public demo: <https://bigh-website-demo.vercel.app/>. It shows the preview build of `6933d63`
(selected Editorial pair on mobile; approved Bold Signature desktop retained, live October 18).

Every page is in Ink & Gold:

| Page                 | Its own idea                                                                             | Last public browser check             |
| -------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------- |
| Home                 | Crane; green spring watercolour in the paintings (Mo's pick C, Oct 16); buttons stay ink | `qa_home_ink` 282/282 (Oct 16)        |
| Menu bar             | "Inscription", all five bottles in the Products drop-down                                | `qa_nav` 436/436 (Oct 16)             |
| Footer               | FDA statement on a painted California trail sign                                         | `qa_fda` 220/220 (Oct 16)             |
| About                | Design C, "circle"                                                                       | `qa_about` 343/343 (Oct 16)           |
| NuriCell             | Paper lantern that lights                                                                | `qa_nuricell_ink` 359/359 (Oct 16)    |
| Green Bee Propolis   | Bold Signature desktop; Editorial pair mobile; gold flowing into the bee tree            | 10 responsive public views (Oct 18)   |
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
