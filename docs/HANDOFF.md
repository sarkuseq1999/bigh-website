# Handoff: read this first

The one current note for whichever agent works next (Claude Code or Codex). Update **Now** before you
stop. The rules are in [`AGENTS.md`](../AGENTS.md).

## Now

- **Last updated:** October 18, 2026, by Claude Code.
- **Folder:** `C:\Users\mcbig\Documents\codes\bigh-website`, branch `studio`, tracking `origin/main`.
- **State:** `main` has caught up with the demo. Mo pasted the push (`studio:main` at `5b7ba74`);
  Vercel built production `dpl_E8PnPqm45gWJu2fdZG8KGLCgjmMS`, which now serves
  `bigh-website.vercel.app`. The demo alias was moved to that same production build.
- **What it carries:** Codex's Propolis work (Bold Signature desktop, Editorial pair mobile,
  Weathered Taupe A footer sign). No other page changed.
- **Checks:** lint, type check, formatting, build; built site `qa_propolis_ink` 273,
  `qa_fda` 220, `qa_home_ink` 282, `qa_nav` 436, `qa_science_ink` 1279, all passing. Public demo:
  `qa_propolis_ink` 273/273, `qa_fda` 220/220, `qa_home_ink` 282/282, `qa_nav` 436/436,
  `qa_science_ink` 1279/1279. Desktop and phone screenshots of both public addresses inspected.
- **Customers:** `bighnow.com` is still the old WordPress site (checked October 18). Nothing in
  this repo reaches it yet.
- **In progress:** None. **Next:** Mo's call.

## What's live

Public demo: <https://bigh-website-demo.vercel.app/>. It shows the production build of `main`
at `5b7ba74`, the same build as <https://bigh-website.vercel.app/> (Propolis: Bold Signature
desktop, Editorial pair mobile, Weathered Taupe A sign). `bighnow.com` is still the old WordPress site.

Every page is in Ink & Gold:

| Page                 | Its own idea                                                                             | Last public browser check             |
| -------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------- |
| Home                 | Crane; green spring watercolour in the paintings (Mo's pick C, Oct 16); buttons stay ink | `qa_home_ink` 282/282 (Oct 18)        |
| Menu bar             | "Inscription", all five bottles in the Products drop-down                                | `qa_nav` 436/436 (Oct 18)             |
| Footer               | FDA statement on a painted California trail sign                                         | `qa_fda` 220/220 (Oct 18)             |
| About                | Design C, "circle"                                                                       | `qa_about` 343/343 (Oct 16)           |
| NuriCell             | Paper lantern that lights                                                                | `qa_nuricell_ink` 359/359 (Oct 16)    |
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
