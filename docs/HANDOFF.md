# Handoff: read this first

The one current note for whichever agent works next (Claude Code or Codex). Update **Now** before you
stop. The rules are in [`AGENTS.md`](../AGENTS.md).

## Now

- **Advanced OPC's other four paintings in color, November 17, 2026 (Claude Code; built,
  committed locally, not pushed).** Part 7 of Mo's "superb" goal. Mo picked "same pictures, in
  color" (A) for the research lens, Dr. Wang's mortar, the plate and the Buy vine scene: Codex
  repainted the October paintings, compositions kept (`paint_colour.sh`); built as
  `*-colour-v1.webp`; descriptions m702-m704 now say watercolor. The Buy bottle now stands at the
  foot of the colour grass with the lowest 20% of the painting in front (with October's 12% band
  the pale grass left the front layer empty). Built site, sequential: `qa_opc_ink` 313/313,
  `qa_home_ink` 290/290, `qa_nav` 326/326 (a rebuilt picture under an unpushed name showed stale
  until `.next/cache/images` was cleared). Before and after: https://claude.ai/artifact/FrBnkt5gyAf4xyBg2kB8r2
  (`reference/ink-pages/mockups/opc-colour/`). After this, every chapter painting on Advanced
  OPC is in color; its six question paintings are still grey ink (next), then Turmerific's, Nature
  Calm's and Green Bee Propolis's middles.
- **Advanced OPC's plants chapter: all nine plants, November 17, 2026 (Claude Code; live,
  `main` `23cf796`, production `dpl_B2d8YK6hdzrhcD4WDRC7yagccNuk`, demo alias on it; public
  checks green).** Part 6 of Mo's "superb" goal. "Inside every capsule, 13
  ingredients." showed six plants in grey ink. Of two California-color ideas mocked on the live
  page (A the same six in color, B all nine plant sources; review page
  https://claude.ai/artifact/NKKQJAoqfm5rx6TmoTXpuV) Mo picked **B** (Claude's pick): take
  `inside-nine-ah`, built as `plants-v1.webp` (art key `plants`); description m701 redrafted in
  all five catalogs (draft translations); `qa_opc_ink` checks the painting. Built site, sequential:
  `qa_opc_ink` 313/313, `qa_home_ink` 290/290, `qa_nav` 326/326. Three unused takes in
  `bigh-archive\opc-inside-unused-2026-11-17\`. Next on OPC: the research painting (a hand lens
  in grey ink), Dr. Wang's mortar, the plate and its painted sum.
- **Advanced OPC's grapes chapter: the gold is in the seeds, November 17, 2026 (Claude Code;
  live, `main` `7b7ca60`, production `dpl_CjX6BUsuwvf7ntEaV8aDyskvncxu`, demo alias on it).** Part 5 of Mo's "superb" goal. "A balance worth keeping."
  showed grey ink grapes lit gold in a yellow haze (a glow, and Asian ink-painting style). Of two
  California-color ideas mocked on the live page (A a bunch ripening green to violet, B a cut grape
  whose seeds turn to gold leaf; review page https://claude.ai/artifact/EvBkXxw7h84qguGVAxYPDM) Mo
  picked **B** (Claude's pick). The cut grape was painted larger so the seeds read on a computer
  (`why-seedsbig-ah`); `seeds()` in `build_opc.py` makes the plain-seed layer; no band of light on
  the seeds (it washed them pale on a phone). Picture description m700 redrafted in all five
  catalogs (draft translations). `qa_opc_ink`'s `spread` section checks plain seeds before, gold
  after, no band. Built site (`npm run build` + `npm start`, sequentially): `qa_opc_ink` 312/312,
  `qa_home_ink` 290/290, `qa_nav` 326/326; lint, type-check, prettier clean; built page looked at
  (1440 and 390 px, before and after the moment). Notes `reference/ink-pages/opc/README.md`; six unused takes in
  `bigh-archive\opc-why-unused-2026-11-17\`. Next part: the same page's "What's inside" (the row
  of six plants, still grey ink).
- **No small labels over product chapter headings, November 16, 2026 (Claude Code; live
  November 17, `main` `8f21216`, production `dpl_A2xcUN59edHPTs4Mg7hz5P4YnwsC`, demo alias on it;
  public checks all green).** Part 4 of Mo's "superb" goal. Shown before and after on the
  live pages (https://claude.ai/artifact/YGNkesKRfZiNmepcJ87L3P), Mo said yes to taking the small
  grey line off the chapter headings of Advanced OPC Formula, Turmerific and Nature Calm, as on
  NuriCell. `chapter-labels.ts` (`showsChapterLabels`: only Green Bee Propolis, whose numbered
  labels are its own chapter system); `why.tsx`, `inside.tsx`, `research.tsx`, `people.tsx`,
  `daily.tsx`. The three checkers check no label stands over a chapter's heading. Built site
  (`npm run build` + `npm start`, sequentially, November 17): `qa_opc_ink` 311/311,
  `qa_turmerific_ink` 267/267, `qa_nature_calm_ink` 271/271, `qa_nuricell_ink` 663/663,
  `qa_propolis_ink` 273/273, `qa_home_ink` 290/290, `qa_nav` 326/326; lint, type-check, prettier
  clean; built pages looked at (1440 and 390 px). Noted, not yet shown to Mo: OPC's lit grapes (Why
  chapter, approved October 16) sit in a pale yellow wash, a glow his later rule refuses (October
  19: gold leaf never glows); being mocked as the next part (`reference/ink-pages/mockups/opc-why/`).
- **Nature Calm's first screen, the high meadow, November 16, 2026 (Claude Code; live, `main`
  `903ecad`, production `dpl_Emko1rfYCh9LhKd4KRZ8Szt38zxX`, demo alias on it).** Part 3 of Mo's "superb" goal: the last product on the shared opening to leave bare
  paper. Of three calm California places mocked on the live page (A Tuolumne Meadows, B Tomales Bay
  at dawn, C Eastern Sierra aspens) Mo picked **A** (Claude's pick). Built with the shared
  `painted-opening.tsx` (`build_nature_calm_opening.py`, `nature-calm-opening-art.ts`, "Calm"'s
  baseline at 62.2% of the bottle's box, lift 0.1); `qa_nature_calm_ink` has a `meadow` section;
  the three checkers now check that Green Bee Propolis keeps its own opening. Review page
  https://claude.ai/artifact/PoveGP1zttXYJyDZdyYZxb; unused takes in
  `bigh-archive\nature-calm-opening-unused-2026-11-16\`. Built site (`npm run build` + `npm start`,
  sequentially): `qa_nature_calm_ink` 269/269, `qa_turmerific_ink` 265/265, `qa_opc_ink` 309/309,
  `qa_nuricell_ink` 663/663, `qa_propolis_ink` 273/273, `qa_home_ink` 290/290, `qa_nav` 326/326.
  Nature Calm's buy check (the lavender's front layer touches only the bottle) failed about one
  phone capture in five here and never on the live site: the taller opening puts the scene at a
  fractional pixel and the hidden-layer capture draws a few edge pixels differently; the check now
  counts a pixel only if it differs in two capture pairs (6/6 after). After this, every product page opens on
  a painted California place (NuriCell the coast, Propolis its own lockup). Next, one part at a
  time: the four pages' middle chapters (grey ink, every painting on the left, small grey labels
  over headings, the thin "How to take it").
- **Turmerific's first screen, the turmeric field, November 16, 2026 (Claude Code; live, `main`
  `1ebc6d2`, production `dpl_EhcG3kou5jueRNLF9wsBFq7fCxjy`, demo alias on it).** Part 2 of Mo's
  "superb" goal. Of three California places for
  turmeric mocked on the live page (A a Ventura County turmeric field with freshly dug roots and a
  eucalyptus windbreak, B a stucco garden wall with a lemon tree, C the Ojai bluffs at dusk) Mo
  picked **A** (Claude's pick). OPC's vineyard code became one shared piece,
  `painted-opening.tsx` + `painted-opening.module.css` (each product's art carries its rows, its
  name's baseline in the bottle's box and its lift); OPC renders pixel for pixel as before.
  Turmerific's art: `build_turmerific_opening.py`, `turmerific-opening-art.ts`, the name lifted
  0.41 of its size as in the mockup. `qa_turmerific_ink` has a `field` section; `qa_opc_ink`
  follows the shared names. Review page https://claude.ai/artifact/3oxar6sXLceaYD6Ka9ZxYC.
  Unused takes in `bigh-archive\turmerific-opening-unused-2026-11-16\`. Next: Nature Calm's first
  screen, then the middle chapters.
- **Product pages to "superb", November 16, 2026 (Claude Code; OPC opening and the stars live,
  `main` `7c8dff5`, production `dpl_EuVn9xcCePY3diXbwmoumwaaKmsB`, demo alias on it).** Mo's goal: every
  product page's words, design and paintings superb. Claude's honest scores after looking at all
  five on the public demo (1440 and 390 px, scrolled like a visitor): NuriCell 8.5; Green Bee
  Propolis 7, Nature Calm 7, Turmerific 6.5, Advanced OPC 6.5. What holds the four back: a plain
  first screen (bottle on bare paper: the same template on OPC, Turmerific and Nature Calm), grey
  ink middles while the rest of the site turned California colour, every painting on the left (Mo
  called that boring on NuriCell, October 19), small grey labels over headings (Mo found them
  strange three times on NuriCell), and the thin "How to take it" chapter with its painted sum
  (Mo found NuriCell's strange, October 27). The words are sound. **Part 1, built (local commit,
  not pushed):** Advanced OPC's first screen as a painted California vineyard (NuriCell's
  clear-day approach). Of A spring with mustard, B harvest with ripe grapes, C autumn colour, Mo
  picked **B** (Claude's pick). Codex paintings
  `reference/ink-pages/opc/originals/opening-{spring,harvest,autumn}-{a,b}h.png` (prompts
  `prompts/opening-*-1.txt`, `paint_opening.sh`; only `opening-harvest-ah` is used and kept, the
  other five are in `bigh-archive\opc-opening-unused-2026-11-16\`); mocked by
  script on the live page (`reference/ink-pages/mockups/opc-opening/`); review page
  https://claude.ai/artifact/Ta1qo8Jp8V8cMbkuoJe4e7. Built: `build_opc_opening.py`,
  `opc-opening.tsx`, `opc.module.css`, `opc-opening-art.ts`, `opening.tsx` and `product-ink.tsx`
  (OPC only); `qa_opc_ink` has a `vineyard` section and finds the bottle by its class (the
  bottle's box now holds the painting too). AGENTS.md "Advanced OPC opening"; notes
  `reference/ink-pages/opc/README.md`. Next, one part at a time: the same kind of first screen
  for Turmerific and Nature Calm, then each page's middle chapters. Built site (`npm run build` +
  `next start`, sequentially): `qa_opc_ink` 309/309 (new `vineyard` section, 2560 to 360),
  `qa_nuricell_ink` 663/663, `qa_turmerific_ink` 155/155, `qa_nature_calm_ink` 159/159,
  `qa_propolis_ink` 273/273, `qa_home_ink` 290/290, `qa_nav` 326/326 (the others before the last
  OPC-only change, which dropped mirrored side pieces for a painting as wide as the window); lint,
  type-check, prettier clean. Claude's score 8.5: from about 1920px wide the hills rise behind the
  name's foot; the 1536px painting is soft on a 2560 screen. **Fixed meanwhile (local commit,
  not pushed):** Nature Calm's Big Dipper stars
  sat in pale yellow halos (a fuzzy glow; the halo had also passed the gold detector): the build
  takes the halo back to paper and ships `stars-v2` (`dehalo` in `build_nature_calm.py`; README
  there). Built site: `qa_nature_calm_ink` 159/159. Noted for later: Nature Calm's thinnest moon
  crescents read like brackets "( )".

- **English launch pass, November 16, 2026 (Claude Code; live, `main` `5fff531`).** Mo's
  goal: the English site ready for launch, launch-quality words, nothing that reads as unfinished.
  Mo's answers the same day: no iMatrix (BiGH's own shop comes later, placeholders until then);
  show the bighnow.com prices; keep the fictional stories; Ask BiGH Science live through Support;
  build the form's email sending (Resend) for him to switch on. Done: prices on all five product
  pages; one shop file (`src/components/shop/shop.ts`: cart links, Log in, Sign up, prices); Ask
  BiGH Science live (dialog, Science strip, homepage line; the Support form's sixth topic,
  `/support?topic=science#write`); `/api/support` + `src/lib/support-mail.ts` (switched on by env
  vars); every "preview / in development / planned / design draft" line rewritten; legal pages
  `/privacy`, `/terms`, `/returns` (BiGH's 2016 texts) linked in the footer; a branded 404 (`[...rest]`
  catch-all, all languages); search basics (`src/lib/seo.ts`: titles, descriptions, canonical,
  hreflang, link previews `public/og/*-v1.jpg`, sitemap, robots closed until `SITE_INDEXING=on`,
  JSON-LD); the site icon (the old `icon.svg` was empty: blank tabs); American spelling; Nature
  Calm's grey misty lake repainted at Lake Tahoe with a little colour (Codex, two rounds). Every
  changed line keeps its translations (`reference/launch/copy_launch.py`; new drafts m1260-m1273).
  Launch-day switches and what is still Mo's: [`docs/launch-checklist.md`](launch-checklist.md).
  Checked on the built site (`npm run build` + `npm start`, localhost:3006), sequentially:
  `qa_home_ink` 290/290, `qa_nav` 326/326, `qa_fda` 248/248, `qa_support` 341/341,
  `qa_science_ink` 943/943, `qa_about` 460/460, `qa_nuricell_ink` 663/663, `qa_propolis_ink`
  273/273, `qa_opc_ink` 199/199, `qa_turmerific_ink` 155/155, `qa_nature_calm_ink` 159/159 (nav,
  science, about and the product pages ran before the footer's last change, a phone-only reorder
  re-checked by `qa_fda` and `qa_home_ink`); the launch checks 53/53 and the Support email path
  26/26 against a local stand-in for Resend (`reference/launch/test_support_mail.py`; the real
  Resend is untested until its key is set). Lint, type-check and prettier clean. **Live** on Mo's
  "Yes, push it": `main` `5fff531`, production `dpl_9k88cWZkpTZdPMoBKqskvSuFUCMx`, the demo alias on
  it; all 11 public checks green with the same counts (`docs/public-demo.md`). Mo, after: email
  "later"; keep Lake Tahoe; the disease-population studies stay, for his lawyer. A copy editor's pass (a subagent) found the slips fixed here and two
  things left for Mo (the checklist): disease-population studies on product pages, two OPC label
  quotes.

- **Handoff to Claude, November 16, 2026 (Mo is switching agents).**
  Codex has stopped editing. The California science set was published and verified November 14
  as recorded below; no implementation or deployment work remains pending from this task.
  Continue in this same folder on `studio`. The release is `f5cc4c6`; its public verification
  notes are in local commit `0bbc52c`. No tracked source changes were outstanding at handoff.
  Untracked earlier painting alternatives, draft review pages/scripts and extra screenshots are
  retained locally; they are not missing release files. Do not bulk-add or remove them.
  The separate A/B layout studies were never selected; the existing layout was deliberately kept.
  No new push, build or live-site verification was performed for this documentation-only handoff.

- **Published November 14, 2026 (Codex): all three California science topics.**
  Mo asked: "put all 3 on the actual webpage so I can see how they look on computer and phone."
  The real homepage now uses C's ranch workshop (`workshop-fuel-v2.webp`), its matching chimney
  close-up (`workshop-sparks-v1.webp`) and the three blue/sage neuron ages (`cell-*-v3.webp`).
  The existing desktop scroll story and phone swipe/tabs remain; no A/B layout was selected.
  `build_california.py` preserves the five originals' colour, framing and alpha (1448x1086).
  `science.module.css` gives the Illustrations label 28px of bare paper and white backs to the
  cell images inside the multiplied group, preventing transparent ages from stacking visibly.
  Build, lint, type-check and source formatting passed. Actual-page checks at 1440x1000,
  1024x768, 390x844 and 360x800 passed: all topics, seven age positions, decoded assets,
  labels clear, no overflow/page errors, and no younger cell leaking through the older one.
  Desktop/phone captures and moving states viewed: 9/10; the worker and gold cell parts remain
  small on phones. Evidence is in `reference/ink-pages/mockups/home-science-california/actual-page/`.
  Built-site checks completed: `qa_home_ink` **290/290**, `qa_nav` **326/326**, run sequentially;
  logs are beside the captures. `git diff --check` passed.
  Mo then explicitly authorized publishing to the live demo on November 14. `main` is now
  `f5cc4c6`, production `dpl_6VDnDcX8WQ7iQdLiQBZm1vLiaRuv` (Ready), and the stable demo alias
  points to it: https://bigh-website-demo.vercel.app/#science. The fetched `origin/main` had
  remained `05356fc`, so no runtime merge changes were needed. Fresh signed-out public checks
  passed at 1440 and 390px: HTTP 200, all topics, all three cell ages, seven slider positions,
  all five assets loaded, labels clear, no page errors or overflow. Public screenshots viewed,
  9/10 with the same phone limitations. Full public checks completed sequentially:
  `qa_home_ink` **290/290**, `qa_nav` **326/326**, no page or console errors. Results are
  recorded in `docs/public-demo.md` and `public-page/`. Release notes are committed locally on
  `studio`; no second push is needed for documentation. The published runtime remains `f5cc4c6`.
  Earlier unselected painting studies remain local and are not part of the release.

- **Scope correction, November 13, 2026 (Mo): all three homepage science topics.**
  Mo clarified that Mitochondria, Free radicals and Aging cells all need new section imagery,
  then asked for Mitochondria redesign ideas too. The current B implementation below is only
  partial completion of that request. Mo then answered 1 / A: improve the workshop painting and
  layout, rather than switching scenes. Two static layout studies now await a choice:
  A Picture first, B Guided painting (recommended), both using the closer repaint
  `california-workshop-c4.png`. This A/B choice is separate from the earlier scene choice.
  Captures at 1440px and 390px were viewed: no horizontal overflow, actual Ysabeau title font,
  9/10 visually; A needs more scrolling, B retains a long phone text section.
  Review: `reference/ink-pages/mockups/home-science-california/layouts/README.md`.
  Mo then asked again to see all three topics together as a set. A coordinated concept board
  now shows c4's workshop, the new `california-sparks-v1.png` and all three
  `california-neuron-{young,middle,old}-v1.png` paintings. The sparks retain the caught/escaped
  sparks and burned roof; the neuron retains the approved 6/3/1 gold convention with its
  illustration honesty label. Built-in image generation, no API spending.
  Latest review: `reference/ink-pages/mockups/home-science-california/full-set/README.md`.
  The board was opened and captured at 1440px and 390px on the built site's real paper and
  Ysabeau font; all six displayed images decoded, no horizontal overflow. Visual score 9/10;
  the small gold cell parts remain the phone limitation. Static board only, no new motion.
  Mo then asked for more Mitochondria image ideas. The latest comparison in `mito-ideas/`
  shows A the current c4 painting, B a closer worker/fire (`california-workshop-close-v1.png`,
  recommended), C an open ranch shed with hills and an oak (`california-workshop-shed-v1.png`).
  B and C are new built-in-tool paintings, with exact prompts saved beside the others. The
  matching Free radicals and Aging cells pictures sit under them for context. These letters
  identify painting compositions, not the earlier A/B layout studies. Viewed at 1440/390px:
  images decoded, no overflow, Ysabeau confirmed; 9/10 for B, whose fire reads more clearly on
  phones; C trades some foreground size for a stronger California setting. Mo then preferred
  **C**: "C matches with the next image of this section." The open shed's roof and chimney
  connect to Free radicals' close-up. `full-set/selected-c.py` renders the coordinated set with
  that painting, preserving the earlier board as `full-set-*.jpg`; latest: `selected-c-1440.jpg`
  and `selected-c-390.jpg`. This is a painting preference, not a choice of the earlier layouts.
  This concept round ended with C selected; the November 14 instruction above then authorized
  the full set on the actual page. Neither alternative layout was selected.

- **Selected and implemented locally November 13, 2026 (Codex): homepage science, B's California workshop.**
  Mo picked B after asking for looser painting: broad wet washes, broken edges and fewer details.
  The Mitochondria picture is now `workshop-fuel-v1.webp`, encoded from
  `california-workshop-c3.png` by `reference/ink-pages/home-science/build_california.py`.
  Original framing, colour and alpha are preserved; 1448x1086, 603 KB. Only the first topic's
  picture and source comments changed. Free radicals and Aging cells await their own review.
  Build, lint, type-check and changed-source formatting passed. Built-site screenshots at
  1440x1000 and 390x844, including arrivals, viewed: 9/10; the worker remains small on a phone.
  Built-site browser checks passed: `qa_home_ink` 290/290, `qa_nav` 326/326, both at
  localhost:3006. No push or demo change.
  Raw originals and prompts: `reference/ink-pages/home-science/`; review and built screenshots:
  `reference/ink-pages/mockups/home-science-california/` (`round2/` and `built/`).
  The previous completed release is below.
- **Live November 13, 2026 (Claude Code): About's "Curious about the science?" at a tide pool.**
  `main` `05356fc`, production `dpl_7a7wwtntaxeYgcBAvvHYqjA4ZLGU`, the demo alias on it; public
  checks: `qa_about` 460/460, `qa_home_ink` 290/290, `qa_nav` 326/326 (`docs/public-demo.md`). The last of About's three parts to take the
  site's California colour. Of three ideas on the real page (A the grey glasses in colour, B a
  tide pool with a guide, C a field notebook by a creek) Mo picked B, Claude's pick: a curious
  older woman looks into a Monterey tide pool with a hand lens while a park naturalist points to
  a sea star (`build_about_closing.py`, `closing-art.ts`, `about-ink.tsx` `TIDEPOOL`,
  `circle.module.css`). New description m1252 (draft translations; native check open). Review page
  https://claude.ai/artifact/HU3F7GX5FB222N6QCJQ4fy (`reference/ink-pages/mockups/about-closing/`);
  unused takes in `bigh-archive\about-closing-unused-2026-11-13\`. Checked on the built site
  before the push: `qa_about` 460/460, `qa_home_ink` 290/290, `qa_nav` 326/326. Claude's score
  8.5: on a phone the two people are small. The three parts Mo asked for on November 11 (Our
  experience, Our promise, this one) are now all in colour.
- **Live November 12, 2026 (Claude Code): About's "Our promise" dots, in colour.** `main`
  `57a87b5`, production `dpl_2Aj1fPozeJEpgdcFq7nm3nuefwDw`, the demo alias on it; public checks:
  `qa_about` 460/460, `qa_home_ink` 290/290, `qa_nav` 326/326 (`docs/public-demo.md`). The second of About's last three parts. Of three ideas on
  the real page (A the four dots in colour, B four California wildflowers, C one poppy counting
  from bud to bloom, Claude's pick) Mo compared B and C side by side, then said "Let's try A": four
  loose watercolour blooms in poppy orange, golden-hill straw, Pacific blue and sage green
  (`build_about_promise.py`, `promise-art.ts`, `circle.module.css`). Review page
  https://claude.ai/artifact/HFiZwnB5sG4DMnAnLp8qhn (`reference/ink-pages/mockups/about-promise/`).
  Built on the branch `about-promise` in a scratch worktree, rebased onto `main` `d4a87f4` and
  checked on the built site before the push: `qa_about` 460/460, `qa_home_ink` 290/290, `qa_nav`
  326/326. Claude's score 7.5: calm and in the page's colours, but the dots mean nothing on their
  own. The unused B and C originals are kept outside the repo. Next on About: "Curious about the
  science?" (the grey glasses).
- **Live November 12, 2026 (Claude Code): the Science zoom ends on a climber.** Mo found the last
  picture (the grandfather and grandchild walking away) "a little boring" and, after a first round
  that kept the pair (a gold-leaf kite, a swing), asked to think freely. Of a climber in Yosemite,
  a rower among gold-leaf ripples and swing dancing in Golden Gate Park he picked the climber. The
  zoom now goes inside the cell, the whole cell, her hand gripping warm granite, then her on a
  sunlit wall above Yosemite Valley (`zoom.tsx` `FOCUS`, `NEAR` per painting; `zoom.module.css`
  framing; `build_science.py` `calmer_blue`, the tall climber `lowered` 4%). `main` `d4a87f4`,
  production `dpl_j4dfeNFJytZ7TVF7MsUR2XfGeP9J` (the demo alias moved on to the promise dots); public checks
  `qa_science_ink` 943/943, `qa_home_ink` 290/290, `qa_nav` 326/326. New description m1251 (draft
  translations; native check open). Review page https://claude.ai/artifact/5X8EEbsSgLNV7qayf1zMVs
  (`reference/ink-pages/mockups/science-last/`); unused takes in
  `bigh-archive\science-last-unused-2026-11-12\`. Claude's score 8.5: nothing moves on the last
  picture; on a phone Half Dome is half cut off at the left edge.
- **Live November 12, 2026 (Claude Code): the homepage hummingbird's wings, too fast to see.**
  Mo: the beat was "so slow, it's like a butterfly". The wings now beat as a haze (each frame the
  wing blurred over most of a beat, a new one every screen frame) for about 3 s, fold onto the
  raised wings and rest (`build_wings.py` `HAZE_*`, `opening.module.css` `haze` / `fold`,
  `hummingbird-v4-near/-far.webp`). `main` `ff68f3e`, production
  `dpl_4JdX6cf6eJmb8pxzPuzJHm6BLFka`, the demo alias on it; public checks `qa_home_ink` 290/290,
  `qa_nav` 326/326. On `studio` the same change is `874fc2b`; `studio` has not merged `origin/main`
  (the About sequoia, `9e550a6`). Review page: https://claude.ai/artifact/3doPJvZQtKNgusd7BCa9QZ
  (`reference/ink-pages/mockups/home-bird-wings/fast/`). Claude's score 8.5: faint curved streaks
  in the blur up close; the wing pictures are 388 KB (were 226 KB).
- **Live November 12, 2026 (Claude Code): About's "Our experience" sequoia, a little coloured.**
  `main` `f46a497`, production `dpl_4XFanxGP5ZWDD7YBaxq7MJPjCuvp`, the demo alias on it; public
  checks: `qa_about` 460/460, `qa_home_ink` 290/290, `qa_nav` 326/326 (`docs/public-demo.md`). Mo asked for About's last three parts (Our
  experience, Our promise, "Curious about the science?") to take the site's California colour, one
  part at a time. For Our experience he set aside three new paintings (an orange tree, sourdough,
  a carousel) and kept the giant sequoia: "Maybe just make it a little bit colored." Of three
  colourings on the real page he picked 3: Codex's repaint in thin watercolour with its colour
  mixed 35% back toward grey, the gold leaf on the trunk at full colour
  (`build_about_experience.py`, `sequoia-soft-v1.webp`, `experience-art.ts`). The leaf takes the
  purpose oak's glint range (at the kit's range the band of light washed it to cream at rest). New
  description m1250 (draft translations); `qa_about`'s new `experience` group. Review page
  https://claude.ai/artifact/5ovTaXUGkaFShrw2jp7D8A. Built on the branch `about-sequoia` in a
  scratch worktree while another session worked in this folder; merged with `main` `dca5fc8` and
  checked on the built site before the push: `qa_about` 460/460, `qa_home_ink` 290/290, `qa_nav`
  326/326; lint, type-check and prettier clean. Claude's score 8.5: the gold leaf is small, so from
  a distance it reads as a little yellow spot. Next on About, one at a time: Our promise (the four
  grey ink dots), then "Curious about the science?" (the grey glasses).
- **Live November 11, 2026 (Claude Code): NuriCell's opening, room and sunshine.** `main`
  `dca5fc8`, production `dpl_CcuAH3FX7DL9qrb5mxenjeJ3SaUE`, the demo alias on it; a quick look at
  the public demo showed it at 1844, 1440 and 390 px and in Chinese; then the full public checks:
  `qa_nuricell_ink` 663/663, `qa_home_ink` 290/290, `qa_nav` 326/326 (`docs/public-demo.md`).
  Built on the branch `nuricell-sunlight` in a scratch worktree while another session's notes were
  uncommitted in this folder, then rebased onto `studio` `ee69a40` (the hummingbird release) and
  checked again on the built site before the push: `qa_nuricell_ink` 663/663, `qa_home_ink`
  290/290, `qa_nav` 326/326. Mo sent the live first screen with three notes:
  the big name sits right on the sea line, the words under the painting need room, and "some kind
  of reflection of the sun" in the upper right corner ("California sunshine"). Review page
  https://claude.ai/artifact/188m1vDatSxUdczs52ssHm: both ideas with the two spacing fixes, A light
  from the corner, B a small painted sun; Mo picked A. Built: from 960px "Nuri" and "Cell" lifted
  0.1 of their size (a strip of sky over the horizon; the bottle's middle now 0.1 name-sizes under
  the letters'), the words 0.13 name-sizes under the last grass (20px on a phone), and the sun's
  light pouring in from beyond the window's top right corner with its sparkle on the sea under it
  (two Codex layers in the painting's blend group, `nuricell-sun-art.ts`). AGENTS.md "NuriCell
  opening: room and sunshine"; pictures `reference/ink-pages/nuricell/build_nuricell_sun.py`;
  mockups and notes `reference/ink-pages/mockups/nuricell-opening/round7/`. `qa_nuricell_ink`'s
  `opening` and `clear_day` follow the new layout (the letters over the bottle's middle, the strip
  of sky, the words' room, the light reaching the corner and never ending inside the window, the
  corner warmer than the left, the sparkle on the sea, no scripts). `opening.tsx` gives every
  product's name halves a `data-half` hook (NuriCell's stylesheet lifts them). On the built site
  (`npm run build` + `next start`): `qa_nuricell_ink` 663/663, `qa_home_ink` 288/288, `qa_nav`
  326/326, `qa_opc_ink` 199/199, `qa_turmerific_ink` 155/155, `qa_nature_calm_ink` 159/159 (158/159
  in the chain: its Buy chapter's front layer 12px beside the bottle on a phone, untouched by this
  change; alone it passed), `qa_propolis_ink` 273/273; lint, type-check and prettier clean.
  Claude's score 8.5: the light is a second painting laid over the sky (a sharp eye may see where
  the two washes meet), and the old softness of the painting on a 2x screen stays. Mo saw the
  built page on the review page and said "Yes, go live".
- **Live November 11, 2026 (Claude Code): the homepage hummingbird's wings stay up.** Mo: the
  wings swung down by the belly ("normally I just see the upper wings move"). Each wing now fans
  about its shoulder from raised as painted out to about level with the shoulder, never through
  it (`build_wings.py` `RIG`, `hummingbird-v3-near/-far.webp`, `openingWings.box` in
  `assets.ts`); the rest pose and the phone menu's baked bird are unchanged. `main` `5b1e4f4`,
  production `dpl_CozxuDzGWSnBPKsUhATWQjNqyYUr`, the demo alias on it; public checks
  `qa_home_ink` 290/290 (a new check: the wings' box ends above the belly), `qa_nav` 326/326.
  Review page with before/after films: https://claude.ai/artifact/73RrLuccvfzBXFnusPv5vw
  (`reference/ink-pages/mockups/home-bird-wings/`). Claude's score 8.5: paused at the beat's
  lowest frame the far wing lies flat over the head like a little crest (a blur at speed).
- **Live November 11, 2026 (Claude Code): the Science page's Dr. Liu part, "the gold he
  studies".** `main` `dd73322`, production `dpl_D1uJztZ12Ww73KwpKS3W4THDwkk4`, the demo alias on
  it; a quick look at the public demo showed it on desktop, phone and in Chinese; then the full
  public checks: `qa_science_ink` 943/943, `qa_home_ink` 288/288, `qa_nav` 326/326
  (`docs/public-demo.md`). Mo saw the built part on the review page and said "Yes, go live".
  AGENTS.md's entry for it says "live" since the NuriCell sunshine notes (the edit waited
  uncommitted in the working copy at first, while another session had AGENTS.md staged).
  `dd73322` is `e0f04ab` plus `studio`'s notes (docs only) and the one commit, pushed as a
  fast-forward. Mo sent a screenshot of the part (he took it for About's; it is Science's) and
  found it "pretty plain or just a little boring": a small dark studio photograph on bare paper.
  He saw three ideas mocked on the real page, then two more (review page
  https://claude.ai/artifact/Une7FkzNpQuqCt4uyvdXQu), and picked C. His painted portrait
  (`liu-v1`, his real face) now sits in front of one huge cell (a Codex painting, `liu-cell-1`),
  its mitochondria slivers of gold that drift slowly while the painting is in the window (16 on
  the wide plate, 21 on a phone's; none with reduced motion or without script). From 960px the
  painting runs off the window's right edge and his words stand on its bare paper; a phone gets
  a tall painting over the words. One new line, "In gold: mitochondria. He has studied them since
  1994.", and the tags "Portrait painting · Illustration". AGENTS.md "Science, Dr. Liu";
  `people.tsx`, `people.module.css`, `liu-art.ts`; pictures `reference/ink-pages/science/build_liu.py`
  (README there, "Dr. Liu"); mockups and notes `reference/ink-pages/mockups/science-liu/`.
  `qa_science_ink` has a new `liu` section (ten window sizes, the drift, reduced motion, no
  script) and its `people`, `multiply`, `settled` and `languages` sections follow the new part.
  On the built site (`npm run build` + `next start`): `qa_science_ink` 943/943, `qa_home_ink`
  288/288, `qa_nav` 326/326; lint, type-check and prettier clean. A 7-second film of the drift is
  on the review page (the farthest sliver travels 11px on a desktop, 7px on a phone). Claude's score 8.5: only the slivers clear of him and of the plate's edges drift, the
  1536px painting is a little soft on a 2x screen, and the cell is the page's third. Still open:
  a native speaker's check of m1231-m1232 (`translations-science-liu.cjs`); Mo's word on how the
  drift feels on the live page. Seen again on the live Chinese page, an older gap: his headline
  and intro (and the path's words) are still English in every language.
  **A new rule from the same session (AGENTS.md, "Real people"):** for mockups Dr. Liu's picture
  may be redrawn by a picture model; nothing with a redrawn Dr. Liu goes on the public site until
  Mo says Dr. Liu approved it. Ideas D (at his microscope) and E (paper planes) were mocked that
  way; their paintings and shots are outside this public repo, in
  `bigh-archive\science-liu-2026-11-11\`.
- **Live November 10, 2026 (Claude Code): the Science opening starts inside the cell and pulls
  back to a grandfather and grandchild, hand in hand.** `main` `e0f04ab`, production
  `dpl_FgvoJMjUEeq3rntJo8Ku2eTb1tKN`, the demo alias on it from about 19:24 Pacific; a quick look
  at the public demo showed it on desktop, phone and in Chinese; then the full public checks:
  `qa_science_ink` 765/765, `qa_home_ink` 288/288, `qa_nav` 326/326 (`docs/public-demo.md`).
  A day after the zoom went live Mo asked for more or better ideas for the first screen, saw four
  on the real page (artifact `5rauLXYKSbXSi9VhTg9aem`: A start inside the cell, B the walker in
  dabs, C the gold dot, D the walker bigger) and said "Go with A". He saw A built and found its
  last view (one small walker) plain; of four last pictures on the real page he picked 1, "hand
  in hand"; he saw that built and said "Put it live". The first screen is the inside of one cell,
  its gold slivers adrift; scrolling pulls back to the cell seen whole, a grandfather's hand
  holding a child's, then the two of them on the trail, where "Why start with the cell?" now
  stands, with tall paintings of the hands and the pair for upright windows. AGENTS.md "Science
  opening: it starts inside the cell" and "Science opening, the last view: hand in hand";
  pictures and notes `reference/ink-pages/science/README.md` ("First-screen ideas", "The last
  view"). Built in a scratch worktree (branch `science-inside`) while other sessions worked in
  this folder; released as `origin/main` (NuriCell's clear day, About's oak) plus `studio`'s notes
  plus the two Science commits, a fast-forward. Before the push, on the combined built site:
  `qa_science_ink` 765/765, `qa_home_ink` 288/288, `qa_nav` 326/326, `check_science_art` 53/53;
  type-check and lint clean. Three calls were Claude's and Mo had seen them only in the films
  before the release: the whole cell shown between the inside view and the hands, "Why start with
  the cell?" moved onto the hills, and the gold's line at the first screen's foot. Asked how the
  motion feels when he scrolls the live page, Mo said "Feels right" (November 11, 2026). Still open: a
  native speaker's check of m1223-m1224 (`translations-science-inside.cjs`).
- **Live November 10, 2026 (Claude Code): About's purpose oak, on a sunny afternoon.** `main`
  `a3bfad5`, production `dpl_2ptufqJCHjqrP86VxnXgjem5sjGr`; the demo alias was on it from about
  18:45 Pacific until another session's Science release (`main` `e0f04ab`,
  `dpl_FgvoJMjUEeq3rntJo8Ku2eTb1tKN`, which contains this one) took it at about 19:24; public checks
  `qa_about` 453/453, `qa_home_ink` 288/288, `qa_nav` 326/326 (`docs/public-demo.md`). Mo found
  the purpose's oak "a little dark or scary" (black ink, bare roots hanging in empty paper, an
  empty swing). Of three painted ideas on the real page he picked A: the same valley oak in soft
  colour, a child on the swing, a grandmother pushing, a dog and a picnic, the roots inside warm
  earth, a patch of gold leaf among them (B was Monterey Bay with a gold kelp forest under a sea
  otter, C a San Francisco cable car over its hidden gold cable; review page
  https://claude.ai/artifact/8dvh62Mg1w7xtgNrYMz9Yp). He saw it built, then "Yes, go live". The
  words did not change. The gold leaf is plain gold at rest: the kit's band of light crosses it
  only as the painting comes up (on the kit's own range it stood on the patch when the painting was
  centred and washed it pale). AGENTS.md "About 'Our purpose'";
  `reference/ink-pages/about-purpose/README.md`. Built in a scratch worktree while other sessions
  used this folder; `main` moved twice on the way (NuriCell's clear day before the push, so the
  release was rebuilt and re-checked on top of it; the Science release after it). `studio` holds
  all three of the day's releases and their notes.
  Claude's score 8.5: the gold patch is small, "Made in California" also has oaks, the people lean
  a little storybook. Still open: a native speaker's check of m1230 (the painting's description);
  a look on a real iPhone. Noted, not asked for: the sequoia, the pool behind Dr. Liu, the promise
  dots and the glasses are still in the old grey ink; the sequoia is now the page's darkest
  painting. The takes not used are in `bigh-archive\about-purpose-unpicked-2026-11-10\`.
- **Live November 10, 2026 (Claude Code): NuriCell's opening, "A clear day".** `main`
  `4d846c7`, production `dpl_AMJsMctxNdcoQd7GydtpaVkgBSxY`, the demo alias on it; public checks
  `qa_nuricell_ink` 612/612, `qa_home_ink` 288/288, `qa_nav` 326/326 (`docs/public-demo.md`). Built
  in a scratch worktree (branch `nuricell-clear-day`) while another session worked in this folder,
  then fast-forwarded into `studio` and pushed. Mo asked for a better first screen for NuriCell,
  saw three ideas mocked on the real page and picked A. One loose ink-and-wash painting now stands behind the name and the
  bottle: a clear morning sky over the Pacific and a low grassy bluff. From 960px the name sits
  on the horizon and the real bottle stands on the bluff, a few blades of the painting's own grass
  in front of its foot; in one column the painting is drawn closer, so a phone has poppies either
  side of the bottle. The morning fog lifts once as the page opens (reduced motion: no fog).
  NuriCell only; no word changed. AGENTS.md "NuriCell opening: 'A clear day'". Checks on the built
  site (`next start`): `qa_nuricell_ink` 612/612 (its new `clear_day` section: 13 window sizes, five
  languages, the fog held and let go, reduced motion, no scripts), `qa_opc_ink` 199/199,
  `qa_nature_calm_ink` 159/159, `qa_propolis_ink` 273/273, `qa_turmerific_ink` 155/155,
  `qa_home_ink` 288/288, `qa_nav` 326/326; lint, type-check and prettier clean. Mo's review page:
  https://claude.ai/artifact/Ft8hXJ2FF8mKJvNyw7UG5s (photos of the built page, then the three
  mockups). Claude's score 8.5: it can read as a beach holiday, the 1536px painting is a little
  soft on a 2x screen, and the fog was judged from still frames. Mo saw the built page, said
  "Looks right", then "Yes, go live" (November 10). Still open: nothing but his word, if he has
  one, on how the fog moves on the live page. The takes not used (the first coast, the blue stroke, the two shades) are in
  `bigh-archive\nuricell-opening\`.
- **Live November 9, 2026 (Claude Code): About's two new chapters.** `main` `022a006`,
  production `dpl_H3nczVLAxKgViZsjP5oVzGKDFZPW`, the demo alias on it; public checks `qa_about`
  446/446, `qa_home_ink` 288/288, `qa_nav` 326/326 (`docs/public-demo.md`). Mo asked on
  November 4 for more on the About page and critiqued each part on the real page. Between Dr. Liu
  and Our experience now stand "Each plant, from where it grows best." (Mo picked B, the globe: a
  painted globe, the four plants round its rim, gold trails laid home to California; no place
  named, as Mo asked, since he is still finding out where the pine bark and grape seed come from)
  and "Proudly made in California." (Mo picked F, the valley at dawn: no bottles; GMP and its
  three rules under it). "Made in California." is back in the promise list, first of four.
  AGENTS.md has both rules. Draft translations m1200-m1222 (`translations-about-chapters.cjs`,
  not native-reviewed; the Chinese heading was shortened when it broke on phones). `qa_about`
  follows the new chapters (a `chapters` group). Built in a scratch worktree (branch
  `about-chapters`) and released alone on top of `main` `552f28c`; the unpicked ideas are in
  `bigh-archive\about-unpicked-2026-11-09\`. Still open: a native speaker's check of
  m1200-m1222; the real origins of the turmeric, grape seed and pine bark, if Mo ever wants them
  named.
- **Live November 9, 2026 (Claude Code): the Science opening as one slow zoom.** `main`
  `552f28c`, production `dpl_5v3Eviam3ztm49K4itgG98pQtrNR`, the demo alias on it; public checks
  `qa_science_ink` 723/723, `qa_home_ink` 288/288, `qa_nav` 326/326 (`docs/public-demo.md`). Mo
  found the first screen plain and the town at dusk unrelated to "cell"; he picked the zoom, saw a
  sample, said "Yes, build it", then "Yes, go live". A walker on golden hills (the h1 in the sky,
  "cell." in gold), the walker's hand, then one cell beside "Why start with the cell?"; the three
  lines follow. AGENTS.md "Science opening: one slow zoom". Built in a scratch worktree (branch
  `science-zoom`) while another session worked in this folder, rebased onto that session's
  homepage release (`7f2c1a0`) and pushed alone. Still open: Mo's word on how the motion feels
  (it was judged from still frames only); a native speaker's check of m1120-m1122.
- **Live November 9, 2026 (Claude Code): the homepage's "Small beginnings. Bigger
  possibilities." in the title face, all ink.** `main` `7f2c1a0`, production
  `dpl_3gCaVeVoio6hLxttywkcqBoay6EU` (the demo alias was on it until the Science release above,
  about 40 minutes later); public checks `qa_home_ink`
  288/288, `qa_nav` 326/326 (`docs/public-demo.md`). The line under the Big Sur close is a `<p>`,
  so it never got the headings' Ysabeau and read as heavy Switzer with a grey second line. Mo
  picked B (both lines in ink) over A (grey second line). Pushed alone: `studio` also holds
  About's two new chapters (next bullet), which are not live. AGENTS.md "Homepage 'Small
  beginnings…'"; mockups `reference/ink-pages/mockups/home-graphic/`. Next on the homepage, if
  Mo wants it: the plain Dr. Liu part.
- **Live November 6, 2026 (Claude Code): Science round 3, the science first, then the
  scientist.** `main` `8b422fa`, production `dpl_AiSfndGjtc21x1JVEoYQa1wUUc1a`, the demo alias on
  it; public checks `qa_science_ink` 642/642, `qa_home_ink` 288/288, `qa_nav` 326/326
  (`docs/public-demo.md`). Still open: a native speaker's check of m1100-m1117. Mo asked for the page to start broader (what science, and why) and to turn
  California, then gave Claude the whole job and said he would critique the built page. The page
  now opens "Our science starts in the cell." (a desk at a window over golden hills), then "Why
  start with the cell?" (San Francisco's houses at dusk, windows lighting in gold leaf), Dr. Liu,
  his path (Berkeley, Salzburg, Today; Okayama told in words), the formulas, "Read the research
  yourself.", Ask. AGENTS.md "Science round 3"; spec
  `docs/superpowers/specs/2026-11-04-science-california-design.md`; pictures
  `reference/ink-pages/science/` (README round 3). New lines have draft translations m1100-m1117
  (`translations-science-round3.cjs`, not native-reviewed; the path's words stay English, as
  before). Checks: `qa_science_ink` rewritten for the new order (opening, why, three places);
  `check_science_art.py` rewritten. Built in a scratch worktree (branch `science-ca`) while
  another session worked on About and the homepage in this folder. November 6, Mo's critique:
  keep the opening line; of three pictures for "Why start with the cell?" (A the town, B
  monarchs, C sunflowers, all shown on the real page) he kept A, the town; leave the formulas'
  bottles row as it is. So the page stays as built, and Mo said "Yes, put it live".
- **Live November 6, 2026 (Claude Code): the homepage's "In their own words." on a California
  back porch.** The three sample stories' still lifes (plum blossom in a vase, tea bowls) read as
  Asian. Mo picked A, the back porch with golden hills and a valley oak, over B, the kitchen table,
  then saw all three stories on the real page (Lisa's breakfast, Michael's book at dusk, Susan's
  honeycomb and the Brazilian shrub). AGENTS.md "Homepage 'In their own words.'"; pictures and
  `build_home_stories.py` in `reference/ink-pages/home-stories/`. Built in a scratch worktree from
  `origin/main` (this folder holds the unreleased Science round 3) and live as `main` `c75cabb`,
  production `dpl_E1qdSYVbqA9hMdrvji9JstGR6Cmp`, demo alias on it; studio has merged it
  (`cdf0d5e`), so the Science release no longer needs to merge it first.
- **Earlier, November 4, 2026, by Claude Code** (the homepage hummingbird's wings beat as
  it arrives, then rest: Mo picked A of three; live as `main` `d26efc2`, production
  `dpl_6A3SfC9jBUWzyLSe5xeWgCAkCqDz`, demo alias on it; every page check now ends a frozen run
  itself (`scripts/qa/stall_guard.py`) and Mo no longer waits for the public checks (AGENTS.md
  "Going live"); the homepage mitochondrion in "Tiny power plants." now fits the California
  colours: Mo loves its design but the page had turned California and colourful around it; of
  two recolourings of the same painting compared live as test pages (A California colour, B
  softer ink) he picked B, a third lighter, in warm sepia (`mito-soft-v1.webp`, AGENTS.md
  "Homepage 'Tiny power plants.'", `reference/ink-pages/home-mito/build_mito_colour.py`); live as
  `main` `9bff13c`, production `dpl_FWByV2YLyXQytJTrMAGFah39BBdH`, demo alias on it; the test
  pages `/home-a` and `/home-b` and A's picture are gone; the phone menu's foot: Mo picked E, the homepage's
  hummingbird at a California fuchsia, its wings at rest, in place of the crane at rest; live as
  `main` `d8ab9c4`, production `dpl_9AxZLkdKWLM84az4Nb26gzmmUdq4`; the footer's painting by the park sign: Mo
  picked A1, two California quail in a few wet washes, in place of the crane at rest; live as
  `main` `9fd7d87`, production `dpl_Hcfa9RqUPbimPg9AX1XRiPDJWLhP`, demo alias on it; the
  homepage's close: Mo picked 1B, the long
  view down the Big Sur coast in ink and wash, the close on `/`, test pages `/home-1` and `/home-3`
  removed; live as `main` `1e5aba5`, production `dpl_EeGZp3TbSWNMQaKzKi2mZ9upbAgj`, demo alias on
  it; the homepage's "Good questions" picture: a
  country mailbox, live as `main` `fdb95ca`, production `dpl_8Xrvxj6hWL2yY2Z65Ptq7zhAJXoT`, demo
  alias on it; the homepage's hummingbird: Allen's painted
  loose, its wings always beating, live as `main` `48819f9`, production
  `dpl_9uBeu3iVYejS9NJGW7DWGPhEJa3y`, demo alias on it; the smaller desktop sun, live as
  `main` `f0ababa`, production `dpl_6fgjwKxM2Y4KjtzSjjxHSNn3SzMT`, demo alias on it; the
  homepage's first screen as giant sequoias and a hummingbird, live as `main` `d5e6858`, production
  `dpl_FH3oK6Urx5Ws5sU4hw1S1X7jdxSV`, demo alias on it; About's poppy meadow live on its own as
  `main` `2ea851d`, production `dpl_76uqRyhhN2AYzkAdG4wLsbAqZATq`, demo alias on it; NuriCell
  chapter 6, "The same formula for about 20 years", live as `main` `f5356a4`, production `dpl_Ec1Gn8DoGjibsDfX4Kvyfc77LSka`, demo
  alias on it). October 27: About's two test openings live as `main` `f4783bb`
  (`dpl_G6ie8SS3BEEsh5jpJcTiXoReTE8o`); NuriCell pairs on the ranch, live on its own (`main`
  `4cd2231`); NuriCell research's Japanese hint no longer splits タップ (`main`
  `55c250a`); the go-live merge (everything waiting on `studio`
  put live together, `main` `641a751`; `studio` then equalled `main` but for notes); product
  questions put live on their own (`main` `c1f56aa`), NuriCell Dr. Liu (`6766ae1`) and the tablet
  menu's crane fix (`5fe0846`), each on its own; About's bigger circle merged into studio; the
  product openings' release notes. October 26: Science, one place per screen, put live on its own.
- **Waiting for Mo (November 4): About, two new chapters, a DRAFT on branch `about-chapters`
  (`c080a94`), NOT on `studio` and not for release.** Mo asked for more on About (scientists,
  ingredients from where they grow best, proudly made in California by GMP-certified makers) and
  for Claude's own ideas, to critique after. Built: "Each plant, from where it grows best." (four
  painted specimens and a key; only Brazil is on file, the other three places show "Place to
  confirm") and "Proudly made in California." (the five real bottles on a painted California
  morning, GMP in plain words); the promise row is three ("Honest about the research." is new).
  English only. Review page: artifact `Sju1s5FxENwBJ33trgL6Uq`; notes
  `reference/ink-pages/about-chapters/README.md` on that branch. Next: Mo's critique and the three
  missing places (turmeric, grape seed, pine bark), then translations.
- **Folder:** `C:\Users\mcbig\Documents\codes\bigh-website`, branch `studio`, tracking `origin/main`.
- **Live (October 28): the homepage's first screen is California.** Mo's colleagues
  loved the opening's watercolour and gold sun but read the misty peaks and red-crowned crane as
  Chinese. Of painted scenes (artifact `XcSw57ecBtwFxZzn7SmqdY`: Big Sur, golden hills, Yosemite)
  Mo asked how a scene ties to "Good health starts with your cells." and picked giant sequoias in
  the morning, then the sun moved into a clearing and, of three birds, Anna's hummingbird. **First
  screen only:** the crane stays in the closing painting, the footer and the phone menu. Branch
  `home-sequoia` (on `studio`), merged into `studio`: `opening-crane.tsx`, `opening.module.css`,
  `brush-route.ts` (`ground()`, the `opening-land` anchor), `assets.ts` (`opening`), pictures from
  `reference/ink-pages/home-california/build_home_opening.py`; `qa_home_ink`'s wingbeat checks
  replaced. Rule in `AGENTS.md`, DESIGN.md updated. Combined built site (with About's meadow):
  homepage 280/280, menu 326/326, About 403/403. On Mo's yes pushed as a fast-forward, `main`
  `d5e6858`, production `dpl_FH3oK6Urx5Ws5sU4hw1S1X7jdxSV`, demo alias on it; public demo
  homepage 280/280, menu 326/326 (`docs/public-demo.md`). **Next parts, one at a time (Mo's
  rule):** (1) the desktop sun, done: Mo picked A of three placements, three quarters of its
  size in the same spot (artifact `Qp6v64HkGMzrJEwraJxXcD`); built site homepage 280/280, menu
  326/326; on Mo's yes live as `main` `f0ababa` (production `dpl_6fgjwKxM2Y4KjtzSjjxHSNn3SzMT`,
  demo alias on it; public demo homepage 280/280, menu 326/326).; (2) the hummingbird's look and wings
  that never stop, built: Mo picked Allen's (over today's Anna's and a green female), then "more
  painting-like" (C, a few wet washes in the old crane's hand), then a beak of one dry brush
  stroke; its own painted wings beat about the shoulder, six blurred frames a beat at ten a
  second (`build_wings.py`, `hummingbird-v2*.webp`; artifact `QUXRzND98STrXfrwPd5iCQ`); built
  site homepage 286/286, menu 326/326; on Mo's yes live as `main` `48819f9` (production
  `dpl_9uBeu3iVYejS9NJGW7DWGPhEJa3y`, demo alias on it; public demo homepage 286/286, menu
  326/326); (3) "Good questions deserve clear answers": the
  inkstone and brush read as Chinese; Mo picked A of three (a country mailbox, its flag up in gold
  leaf, over a Gold Rush pan and a naturalist's notebook; artifact `UbRetC7irKBTVYyWPh8Gqj`), built
  on `studio` (`mailbox-v1.webp`, `reference/ink-pages/home-ask/`), built site homepage 286/286,
  menu 326/326; on Mo's yes live as `main` `fdb95ca` (production
  `dpl_8Xrvxj6hWL2yY2Z65Ptq7zhAJXoT`, demo alias on it; public demo homepage 286/286, menu 326/326); (4) "Our purpose" closing painting: pine on
  rocks, misty peaks, red-crowned cranes read as Chinese; of three California endings mocked on
  the real page (A Big Sur at evening, B an evening walk on the ridge, C a surfer at low tide;
  artifact `7APcgk8f6k1ZG8JERvP1yw`) Mo tried A and B live (test pages, `main` `c32fefb`), found the
  walk with people not Californian, and of three Californian walks (same artifact, v2) picked 1,
  the walk on the Big Sur coast: built on `studio` as the close on `/` (`purpose-coast-walk-v1.webp`,
  pelicans, test routes removed); on Mo's yes live as `main` `4d5f59e` (production
  `dpl_9mLMrnWT1LRA9hz1oN7PWJY4SxTD`, demo alias on it; public demo homepage 286/286, menu
  326/326). Mo then found it "a little bit simple" next to the old pine painting; of three richer
  Big Sur paintings (same artifact, v3) he tried 1 and 3 live (`/home-1`, `/home-3`, `main`
  `648e44d`) and found them "more picture like"; of the same places painted loosely (v4: A a loose
  watercolour, B ink and wash) he picked 1B, the long view in ink and wash: built on `studio` as
  the close on `/` (`purpose-ink-long-v1.webp`, its gold mask; phone frame 150% from 22.5%;
  `qa_home_ink` `PURPOSE_FRAME` set to its sun and walkers; the test routes, `purposeEndings` and
  the coast-walk and rich pictures removed; `studio` `6c1cb12`); built site homepage 286/286, menu
  326/326, the close at 1920, 1440, 1280, 768 and 390 px; live as `main` `1e5aba5`, production
  `dpl_EeGZp3TbSWNMQaKzKi2mZ9upbAgj`, demo alias on it; public demo homepage 286/286, menu 326/326,
  the close at the same five widths; (5) the footer's crane by the park sign: mocked November 3
  (artifact `EHcCHzYJaB9jpPDvAhAKLb`, `reference/ink-pages/footer-crane/README.md`): A California
  quail, B desert tortoise, C black bear cub, each looking at the sign's poppy; Mo asked for the
  quail and the bear more painting-like: round 2 (version 2) paints each in a wet wash (A1, C1) and
  in ink and wash (A2, C2); Mo picked A1, the wet-wash quail: built on `studio` November 3
  (`quail-sign-v1.webp` from `build_footer_quail.py`, one picture on every page with no "green
  spring" twin; `closing-quail.tsx` replaced `closing-crane.tsx`; `.look .rest` 235 tall and 58
  right of the sign, phones 190 and 42 and inside the column, so the sign keeps seven lines at
  390 px and eight at 360; `qa_fda` and `qa_home_ink` expect the quail); built site footer
  248/248, homepage 286/286, menu 326/326, About 403, NuriCell 457, Propolis 273, OPC 199, Science
  633, Support 341, Turmerific 155, Nature Calm 158/159 (the buy scene's front-layer pixel check
  on a phone: a flaky race at the lavender painting's edges, failing about 1 run in 8 on the live
  code built locally too; live demo 159/159); live as `main` `9fd7d87`, production
  `dpl_Hcfa9RqUPbimPg9AX1XRiPDJWLhP`, demo alias on it; public demo: `qa_fda` 248/248,
  `qa_home_ink` 286/286, `qa_nav` 326/326, Nature Calm 159/159, and the quail by the sign on the
  homepage and Green Bee Propolis at 1440 and 390 px wide. The crane's
  pictures (`crane-poppy-v1.webp` and its spring twin) stay in `public/` unused; (6) the phone
  menu's crane at rest: mocked November 3 on the real menu (artifact `MKzpasUKpvbnY6vPM9xce9`,
  `reference/ink-pages/menu-finale/`): A one quail, B the footer's two quail, C poppies, then on
  Mo's "Can we try with the hummingbird?" D Allen's perched on a twig and E the homepage's own
  bird at a California fuchsia (Codex painted the flower only); Mo picked E, then found its
  beating wings "annoying, like flys" at the menu's size, so its wings rest, raised as painted:
  built on `studio` November 3 (`menu-hummingbird-v1.webp` from `build_menu_finale.py`, the
  bird and its first wing frame baked into the fuchsia; no brush stroke under it;
  `nav-inscription.tsx` `.sheetBird` and `useBirdRoom`, the room's size unchanged; `qa_nav`
  says bird); live November 4 as `main` `d8ab9c4` (production
  `dpl_9AxZLkdKWLM84az4Nb26gzmmUdq4`; public `qa_nav` 326/326, `qa_home_ink` 286/286).
  `crane-rest-v2.webp` stays in `public/` unused. No crane is left on the site. (7) The homepage
  hummingbird's wings: Mo found the non-stop beat "a little annoying", like a fly, and picked A
  of three (A beat as it arrives, then rest; B short bursts; C always still; artifact
  `Ga3RJ98KD1gcuqsAFzwoG9`, `reference/ink-pages/mockups/home-bird-rest/`): 3 s at full speed
  while the bird blooms in, three slower beats, then the first frame, raised as painted
  (`opening.module.css` only); `qa_home_ink` reads the wing arriving and settled (built copy
  288/288); live November 4 as `main` `d26efc2`.
- **Live (October 28): About opens on the poppy meadow, thinning into the paper.**
  The ink circle reminded Mo of the film The Ring. He compared A (superbloom) and B (morning walk)
  live as test pages and picked A, then found its first screen and Our purpose "don't transition
  well" (the painting stopped in a straight line) and picked A of two painted ends (artifact
  `8fXZZqa9W5tFaPLY9cNnQo`): below the first screen the meadow thins out into bare paper, then the
  oak. Built on branch `about-meadow` (`2ea851d`, on top of `main` `f5356a4`) and merged into
  `studio`: the meadow replaces the circle on `/about` (`meadow.module.css`, `meadow-art.ts`); the
  circle, its hills, `let-the-circle-go.ts`, `before-hydration.tsx`, `/about-a`, `/about-b` and B's
  pictures are gone; `qa_about` checks the meadow (`meadow_layout`, `motion`); rule in `AGENTS.md`.
  Built site and public demo alike: About 403/403, homepage 282/282, menu 326/326. Put live on
  its own on Mo's yes as `main` `2ea851d` (a fast-forward from `f5356a4`), production
  `dpl_76uqRyhhN2AYzkAdG4wLsbAqZATq`, demo alias on it (`docs/public-demo.md`).
- **Live (October 28): NuriCell chapter 6, "The same formula for about 20 years" (Mo picked 2,
  October 27).** "How to take it" (egg cup, brushed 3 × 30 = 90) read as strange and the
  dose alone too thin for a chapter (the buy box and the first question say it). Three rounds of
  mockups (artifact `Nxd5q7PQPnw5JVNmhVoJQQ`, `reference/ink-pages/mockups/nuricell-daily/`); Mo
  picked round 3's 2 over a painted California day: a young redwood round (Codex,
  `originals/daily-rings-b1.png`), one ring about 20 in from the bark in gold leaf, its light mask
  made from the ring itself (`rings()` in `build_nuricell.py`); heading, a lead in ink and a note
  naming the four nutrients, words left and the round right from 960px. NuriCell only:
  `daily.tsx` takes a `story` (no label, no sum); OPC and Turmerific keep their sums. New strings
  m962-m965 in all four languages (not native-checked). `qa_nuricell_ink` has a `formula` section
  in place of `sum`; the shared sum's checks (dev-only `?ink-sum` fixtures, jp/cns captions) moved
  to `qa_opc_ink` (`sum`). No start year is on file ("about 20 years" is Mo's "almost
  20-something years"); Mo put it live with those words on October 28 (`main` `f5356a4`, pushed
  as a fast-forward of the tested commit). If a real start year turns up, change m962-m964.
  Open: native check m962-m965.
- **Live (October 27, on its own): NuriCell pairs on the ranch (Mo picked B).** Mo found
  "Why these four work together"'s white powder heaps look like drugs. Of three painted ideas (A two
  hands, B an old California ranch, C a gold trail map; artifact `H9XUk1ya3vXH7Ei7WvghnL`) he picked
  B: firewood and the stove (flipped so the wood comes first), the windmill pouring gold water into
  its tank, the Pony Express rider with a gold letter. Each plays once as it comes into view: the
  light runs up the fire, the wheel turns once while the water pours and light spreads across the
  tank, the light crosses the letter; Play again replays; reduced motion and no script show the
  paintings still. The wheel turns over a Codex repaint of the scene without it
  (`ranch-windmill-nowheel.png`). The heaps' pictures and code are gone. `nuricell-scenes.tsx`,
  `nuricell-inside.module.css`, generated `nuricell-pairs.ts` from
  `reference/ink-pages/nuricell-pairs/build_nuricell_pairs.py`; recording artifact
  `S6d2aNgCzBhZMUHdoQQebb`. Checked on the built site (`npm run build` + `next start`, scratch
  worktree): `qa_nuricell_ink` 450/450 (the scenes section rewritten), `qa_home_ink` 282/282,
  `qa_nav` 326/326; lint, type-check and Prettier clean. On Mo's yes, released alone: `091c05f`
  and `c7a760a` cherry-picked onto `origin/main` `55c250a` (chapter 6 above stayed out), the same
  three checks green on that build, pushed as `main` `4cd2231`; `studio` then merged it (no file
  changes). Public demo: `qa_nuricell_ink` 450/450 (run from the release's own copy: `studio`'s
  working copy then held chapter 6's checks), `qa_home_ink` 282/282, `qa_nav` 326/326.
- **Live (October 27): the footer crane by the park sign (Mo picked B "end of the trail", then
  pose C).** The crane leaves "Stay sharp. Live fully." and stands at rest in the grass at the FDA
  park sign's right, bending toward the sign's California poppy; the promise stands alone, a size
  smaller. Red crown on the homepage, gold elsewhere. On phones the sign narrows for it (about
  seven lines; the sign and crane a little smaller under 390 px). The homepage's brush line still
  ends as a stroke under the words. `closing-crane.tsx`, `ink.module.css` (`.look .rest`),
  `fda-statement.tsx`; picture `crane-poppy-v1.webp` from
  `reference/ink-pages/footer-crane/build_footer_crane.py`; mockups and the built shots
  `reference/ink-pages/mockups/footer-crane/`, artifact `Sa1u9LjcJRrHDxuKPPtvRy`. Built on
  `studio` as `c947fcf`; released in the go-live merge `641a751` with About's circle and NuriCell
  research (checks in `docs/public-demo.md`: on the public demo all 12 page checks green, `qa_fda`
  248/248, `qa_home_ink` 282/282). Open: on a phone the crane is small and its tail comes within
  about 17px of the window's edge.
- **Live (October 27): About, a bigger circle and no gold leaf (Mo picked A twice)** (released in
  the go-live merge `641a751`; public `qa_about` 404/404).
  The opening circle fills the first screen and "Be in Good Health." is written inside it (on a
  phone the title sits inside on three lines, the lead under the circle). The gold leaf that fell
  onto the circle is gone (Mo found its fall and shine cartoonish; the opening's gold is the sunlit
  hilltop). Layout B, a bigger circle with the words under it, was built at a temporary
  `/about-below` to compare and removed after Mo's pick. `circle.module.css`, `about-ink.tsx`,
  `let-the-circle-go.ts`; mockups and the built shots `reference/ink-pages/mockups/about-circle-size/`,
  artifact `CC6pZFonqYvRfZnJEB6g57`. Merged into studio October 27 on top of 598d10a and
  re-checked on the built site (`npm run build` + `next start`): `qa_about` 404/404 (new
  `circle_layout` section), `qa_home_ink` 282/282, `qa_nav` 326/326; lint and type-check clean.
  `qa_fda` stops at Turmerific, which never goes network-idle on a local `next start` (old, not
  this change).
- **Live (October 27): NuriCell research, Mo's pick A, "tap a book, read its study"**
  (mockup and the built page's shots `reference/ink-pages/mockups/nuricell-research/`, artifact
  `UFqCskQg1VCPiKy8ZTTVLk`; the draft rounds in `codes/bigh-archive/nuricell-research-mockup-2026-10-26/`).
  Mo asked for the research list to be more fun to read and found the small "The research" label
  odd. Each of the seven books in the painting is a button (a clip-path over the painting, grown
  around the far books): tap one and its study opens, the other books fade under a little paper
  (`books-mask-v1-*.png`, cut by `reference/ink-pages/nuricell/find_books.py`). The studies are six
  plain questions with short answers written from each paper's abstract; the two 2003 reviews
  share "Scientists disagree" and light two books. On a phone a tapped book brings its question up
  under the menu bar. No label, no "Show all"; without scripts every answer shows. The note is
  shorter in `nuricell.ts`. New words translated as drafts (m930-m961), including the chapter's
  heading, which was English in every language on all five product pages until now. On the built
  site at db2b938 (`npm run build` + `next start`): `qa_nuricell_ink` 443/443 (a new research
  section), `qa_questions` 403/403, `qa_home_ink` 282/282, `qa_nav` 326/326; the other four
  products' language checks 16/16 each on the build just before (without the product questions).
  Mo said to put it live on its own (October 27); it went out first in another session's go-live
  merge of studio (`main` `641a751`, production `dpl_EvL92fanN6vxLecZp21Hu8PWHkYy`, the demo alias
  on it), so the separate release copy was not pushed. On the public demo: `qa_nuricell_ink`
  443/443 (the research section 14/14); screenshots in English, Korean and Japanese matched the
  local build. Then the Japanese hint ("…研究です。タップすると読めます。") split タップ ("tap")
  across two lines on phones; Mo said to fix it and put it live (`main` `55c250a`). The hint now
  has `word-break: keep-all` before `auto-phrase`: Safari (WebKit 26.4) has no `auto-phrase`, so
  keep-all lets it break only after 、 and 。. Checked in Chromium and WebKit at 320, 360, 390, 430
  and 1280 px, locally and on the public demo: the line ends at 。 and タップ stays whole. Open:
  native check of m930-m961; the far books are small to tap on a phone (the questions are the easy
  tap); the Chinese hint can still break inside a word on phones ("点一 / 本", "读 / 到它"; not
  asked for). The site's other Japanese titles rely on `auto-phrase` alone, so on an iPhone they
  can break inside a word (not checked page by page).
- **Live (October 27): NuriCell Dr. Liu, "the view west"** (Mo picked idea A, the
  Berkeley story, then A2 of two mockups, then round 2 of A2; mockups and the built page's shots
  `reference/ink-pages/mockups/nuricell-liu/`, artifact `W7qmqUj4RNiCVLmtk94j5a`). His real
  portrait (liu-v1) stands on the Berkeley hills over the bay, the Golden Gate in the fog, painted
  in grey ink, dry grass in front of his foot. From 960px one painting runs across the chapter
  (as wide as the window, at most 1.8 × (window height - 140px), centred) and his name and words
  sit in its sky, ending above its land; phones get their own framing (`paintingPhone`, Next art
  direction in `ink-chapter.tsx`'s `FramedPicture`). No label over his name; a lead, one line on
  the 2002 study (told as published from Ames's lab: his years there were 1994-1997) and the note
  "An animal study, not a test of NuriCell." (m907-m910, drafts). Plates `liu-berkeley-v3`,
  `liu-berkeley-phone-v3` from `build_nuricell.py`'s `berkeley()` (Codex originals
  `liu-berkeley-west-ink-v2b`, `liu-berkeley-grass-v1`; v2a a spare). Nature Calm keeps its plain
  portrait and label. Built site (`npm run build` + `next start`, combined with the questions work
  at d15db52): `qa_nuricell_ink` 430/430, `qa_nature_calm_ink` 159/159; earlier build `qa_home_ink`
  282/282, `qa_nav` 315/316 (the tablet crane jump, since fixed in f9c1132). Mo said to put it
  live (October 27). Released on its own from a copy of live `main` with only its commits (the two
  mockup rounds, the code, the AGENTS rule, the deep-link fix, the docs), rebased once onto
  `5fe0846` (the tablet crane fix, pushed meanwhile), rebuilt and re-checked (`npm run build` +
  `next start`): lint and type check clean, `qa_nuricell_ink` 430/430, `qa_nature_calm_ink`
  159/159, `qa_home_ink` 282/282, `qa_nav` 326/326. Pushed `main` `6766ae1` (fast-forward),
  production `dpl_FQBFSg6uMe4kzy1KXVcj6ZHokg19`, demo alias on it. On the public demo, fresh
  browsers: `qa_nuricell_ink` 430/430, `qa_nature_calm_ink` 159/159, `qa_home_ink` 282/282,
  `qa_nav` 325/326 then 326/326 on a rerun (the settle film's frame timing over the network once);
  screenshots at 1440×900 and 390×844 matched the local build. The questions release and the
  go-live merge (`641a751`, which holds the demo now) went out on top of it minutes later; the
  page still serves the plates there. Open: native check of m907-m910; the hills read grey more
  than golden; on a 1280×800 laptop the section runs a little past the screen.
- **Live (October 27): the tablet menu's crane eases with the fold** (Mo said to fix the jump,
  then to push "only that fix"; before/after page `J5z9H46J76J8t2uM7nZqkf`). Released alone from
  live `main`: `main` `5fe0846` (the code of `f9c1132`), production `dpl_9WQV7zjP…`, demo alias
  → it; public `qa_nav` 326/326, `qa_home_ink` 282/282 (`docs/public-demo.md`). On a tablet the
  crane takes the room left under the menu's words (130px to 230px), so it changes size as Products folds. Left to the
  layout it followed only the slice of the fold where that room lies between its two sizes:
  folding Products away at 834x1112 it grew 54px in 0.12s (up to 13px a frame) and stopped dead;
  at 768x1024, 100px in 0.07s (25px a frame). Now `useCraneRoom` in `nav-inscription.tsx`
  works out the crane's end size as a part starts to fold and, on every change of the folds'
  size (a ResizeObserver, before the frame is drawn), holds it as far from its old size to its
  new one as the folds are through theirs; when the fold's transition ends the layout has it
  again. Biggest step now 4px a frame at 834x1112, 8px at 768x1024 and 1024x768; phones and
  1024x1366 unchanged. `qa_nav` films the fold at all three tablets and checks the size is let
  go after. Built site (`npm run build` + `next start`, studio `c947fcf` plus this): `qa_nav`
  326/326, `qa_home_ink` 282/282; lint and type-check clean. Separately, still open:
  `scripts/qa/qa_science_links.py` still clicks the Science drop-down switched off this morning.
- **Live (October 27, `main` `c1f56aa`): product questions, Mo's pick A, "a painting for each answer"**
  (mockups `reference/ink-pages/mockups/nuricell-questions/`, artifact `MceTcmgqxFuQPtLHrJ8xfE`;
  the built pages in `.../built/`, artifact `S4ttkdJhyASQLXjr8uYigt`). All five ink product pages
  (`questions.tsx`, shared): from 960px the questions on the left and the picked one's painting and
  answer on the right (the first picked as the page opens, the menu bar's pale wash behind it, a
  round "+" on the others; the old answer fades out before the new one fades in); on a phone each
  question opens in place with its painting. 28 Codex paintings, one per question, true to each
  label (capsule count and colour, 30 squares a month), cut to 3:2 by
  `reference/ink-pages/questions/build_questions.py` (README there: what was repainted and why).
  Propolis's old questions grid (heading left, list right) is gone; its heading keeps its own
  face. No new words. On the built site (`npm run build` + `next start`) on top of studio 598cab0:
  `qa_questions` 403/403 (new: all five pages, wide and phone, no script, four languages),
  `qa_nuricell_ink` 430/430, `qa_opc_ink` 185/185, `qa_propolis_ink` 273/273,
  `qa_turmerific_ink` 155/155, `qa_nature_calm_ink` 159/159, `qa_home_ink` 282/282, `qa_nav`
  315/316 (the known tablet crane jump). The product QA scripts now pick each question to read its
  answer (only the picked one is shown). Released on its own from live `main` on October 27 (on
  top of Dr. Liu's view west, `6766ae1`); the release and public checks are in
  `docs/public-demo.md`.
- **Live (October 26): Science, Mo's pick B, "one place per screen"** (Mo: "Science only, not the
  other sessions' unreleased work"). Released from a copy of live `main` with only the Science
  commits, rebased once onto `78ae1d6` (product openings, pushed meanwhile): `main` `e6e7e36`,
  production `dpl_DAZ7E1Tfs5ubFa8w4nfLvu3yod2t`, the demo alias points to it; public demo
  `qa_science_ink` 633/633, `qa_home_ink` 282/282, `qa_nav` 315/316 (the known tablet check)
  (`docs/public-demo.md`). On `main` the Science commits are `d9d0010`, `a2554f4`, `e6e7e36`
  (the same content as `studio`'s `8f7b99d`, `500873d`, `3a5cd0d`). `studio` merged
  `origin/main` again on October 27 (the go-live merge `641a751`). Before that: (mockups and the
  built page's shots `reference/ink-pages/mockups/science-path/2026-10-26/` and `.../built/`,
  artifact `9jBznqoXRwUacxeKv2P8AP`). Mo liked the paintings but found the sideways handscroll
  "feels like a draft". The page opens on the title and Dr. Liu (photo, name, intro; his numbers
  row is gone, his path tells it), then his path down the page: Okayama (painting left), Berkeley
  1994 (right, with the 2002 study), Salzburg 2025 (left), Today (wide, one line in the sky by the
  gold sun); then research, health explained, the formulas (moved down), Ask. Paintings cut from
  the old band by `build_science.py` (`PLACES`, phone cuts too); `path.tsx`; the handscroll's
  `journey.tsx` and `use-journey.ts` are deleted. Berkeley says 1994, not the mockup's 1994-2002
  (the faculty profile dates his time in Ames's lab 1994-1997). The path's words are English in
  every language, as the old stops were. `qa_science_ink` rewritten for the path (its journey,
  rooms and last-resort checks are gone). On the built site (`npm run build` + `next start`):
  `qa_science_ink` 633/633, `check_science_art.py` all pass, `qa_nav` 315/316 (the known tablet
  crane jump), `qa_home_ink` 282/282. `qa_science_links.py` crashes before checking anything: it still
  clicks the Science drop-down that became a plain link earlier on October 26 (not this change;
  not fixed).
- **Live (October 26): product openings, the words under the name, Mo's pick C "Title face"**
  (mockups `reference/ink-pages/mockups/nuricell-hero-left/`, artifact `1TNAN8z5fW6P14w7kv3QZz`).
  NuriCell, OPC, Nature Calm and Turmerific (the shared opening; Green Bee Propolis keeps its own):
  the headline in Ysabeau (560; Korean, Japanese and Chinese keep the title weight), the purpose a
  large lead in ink with no side line, and from 960px the two sit together and end where Add to cart
  ends (the refund line sits in a subgrid row of its own). Mo turned down Dr. Liu's photo there:
  pages without him would look lesser. On the built site (`npm run build` + `next start`) at 59585a0
  (on top of the lighthouse and What's inside): `qa_nuricell_ink` 429/429 (its opening check now
  tests the new look), `qa_opc_ink` 185/185, `qa_turmerific_ink` 155/155, `qa_nature_calm_ink`
  158/159 (its older front-layer pixel check, in the Buy chapter); a build before the last two small
  fixes (the dash kept with its word, the CJK weight) also passed `qa_propolis_ink` 273/273,
  `qa_home_ink` 282/282, `qa_nav` 315/316 (the known tablet crane jump). Released on its own from a
  copy of live `main` (`af7faf3`) with only this change cherry-picked: `main` `78ae1d6` (the same
  content as `studio`'s `59585a0`), production `dpl_92LiEZJuxbddWQY2mQNmcV8Jw2mG`; public demo
  `qa_nuricell_ink` 404/404, `qa_opc_ink` 185/185, `qa_nature_calm_ink` 159/159, `qa_turmerific_ink`
  155/155, `qa_propolis_ink` 273/273, `qa_home_ink` 282/282, `qa_nav` 315/316 (the known tablet
  crane jump). The Science release (`e6e7e36`) went on top minutes later and the demo alias moved
  there, with the new openings still in it (`docs/public-demo.md`). Open: on Turmerific at 1440x900
  the refund line ends on the window's bottom edge; on a phone its purpose runs six lines.
- **Live (October 26): NuriCell "Tiny power plants", Mo's pick B, the lighthouse** (`main`
  `610d70a`, released on its own from live `main`; public checks in `docs/public-demo.md`)
  (mockups and the built page `reference/ink-pages/mockups/nuricell-why/`, artifact
  `LiWF3jKo2tdLH4otM1SrRc`). Mo first picked A (a Gold Rush miner's lantern), saw it built beside
  the lighthouse sample, and switched to B the same day; the lantern's pictures are gone and its
  originals are in `codes/bigh-archive/nuricell-why-unused-2026-10-26/goldrush-built-a/`. A
  lighthouse on a California cliff replaces the paper lantern (it read as Asian); its lamp and
  beam still come on as you scroll. Codex paintings: the lit take (`why-lighthouse-a2`), then the
  unlit take as an edit of it, of which only the light is used (`build_nuricell.py`,
  `lantern()`). Below 960px it is drawn at 55% of the window (the template's 46%), so on a phone
  it spans the column. No label over the heading, one lead-in line with no indent, the 2% small
  beside a big 20% (stacked on phones); the section's six lines translated as drafts
  (m901–m906). On the built site: `qa_nuricell_ink` 429/429, `qa_home_ink` 282/282, `qa_nav`
  315/316 (the known tablet crane jump), `check_nuricell_art.py` all pass.
- **Live (October 26): NuriCell "What's inside", Mo's pick 1A** (mockups
  `reference/ink-pages/mockups/nuricell-inside/`, artifact `Bnhi2oV5MB9eoDusAmdiC2`; the built
  page recorded in `built.html`, artifact `UbeHphVKjW9BqEs2jXh8Fr`). The capsule painting's gold
  leaf rises out of the powder and settles where it is painted, then each flake keeps turning,
  catching the light (`nuricell-leaf.tsx`: one canvas over the painting without its leaf; the leaf
  as painted for reduced motion and no script). No label over the heading; "per serving of 3
  capsules" right under it; the label's other lines as a card; the research note said once at
  the chapter's end (NuriCell's synergy note now says what notes.science said). "Why these four
  work together" is three scenes (`nuricell-scenes.tsx`): each pair's two powder heaps and its
  gold (lit; kept in reserve; two halves made one), each with Play again. Pictures:
  `reference/ink-pages/nuricell/build_nuricell_gold.py` (capsule-ink, capsule-gold, capsule-leaf,
  `heap-*`). NuriCell only; the other four product pages are unchanged. On the built site
  (`npm run build` + `next start`): `qa_nuricell_ink` 404/404 (new sections plate, gold,
  scenes), `qa_home_ink` 282/282, `qa_propolis_ink` 273/273, `qa_opc_ink` 185/185,
  `qa_nature_calm_ink` 158/159 (its older front-layer pixel check), `qa_nav` 315/316 (the
  upright tablet's crane jump, recorded with the Science-link change above).
  The new words ("Also on the label", the card's lines, the merged note) are English in every
  language, like the rest of this chapter's product words. On Mo's yes Claude pushed `main` to
  `c944a72` (this, the Science link and the footer's copyright line below, merged with the
  homepage science peek `75fb88e`); production `dpl_4e5NFHzU2WD5VdsJAosxQVZZp6vf`, the demo alias
  points to it; public demo `qa_nuricell_ink` 404/404, `qa_home_ink` 282/282, `qa_fda` 232/232,
  `qa_nav` 315/316 (the tablet crane jump). "Tiny power plants" above was not pushed.
- **Live (October 26, with "What's inside"): the footer's copyright line comes last** (`75c6190`;
  AGENTS.md "Footer: the copyright line comes last").
- **Live (October 26, with "What's inside"): Science is a plain link in the menu bar** (Mo: the Science page
  is one page, and the drop-down's four doors into it made the site look short of content; keep
  the design for later). On the bar and in the phone's menu Science goes straight to `/science`,
  like About and Support; on the Science page its word carries the painted stroke. The drop-down
  is switched off, not deleted: `navScienceMenu` in `src/components/ink/nav/nav-data.ts`, and
  `SCIENCE_MENU` in `scripts/qa/qa_nav.py` (its drop-down checks skip; new Science-link checks
  run). `qa_home_ink`, `qa_science_ink`, `qa_about` and `home_snapshot.py` now expect the plain
  link. Built site (`npm run build` + `next start`): `qa_nav` 315/316, `qa_home_ink` 282/282,
  `qa_science_ink` 1279/1279, `qa_about` 353/353 (dev: `qa_nav` 315/316); lint and type-check
  clean. Mo's before/after page: https://claude.ai/artifact/DEE11nzfSvHRMeSgmFFfCC. The one
  failure was old, newly checked: the tablet menu's crane jumping as Products folds away (fixed
  later the same day, live October 27 in `5fe0846`: "the tablet menu's crane eases with the
  fold" at the top). Live in `c944a72`.
- **Live (October 24-25, latest): homepage science on phones, the tabs over the picture and a
  finger swipe** (Mo picked A on October 23, then asked to swipe from one topic to the next and
  said to put it live). Under 900px the three tabs sit right above the picture; the three topics
  (picture, line, words) sit side by side in a strip as wide as the window that snaps to one
  topic; the tabs glide it and follow the swipe; the age slider still drags sideways.
  `science.tsx` (`.slides`, `.slide`). Claude pushed `main` to `28a87db` (a fast-forward from
  `53913a3`); production `dpl_7vTcT4734Sht8EkW36E3sSwnyGa8`, the demo alias points to it; public
  demo `qa_home_ink` 282/282, `qa_nav` 440/440. That public test found a short drag sometimes
  left the strip 40 to 110px off a topic (11 of 48), so on October 25, on Mo's yes, Claude pushed
  the fix `3537053` (the strip glides to the nearest topic once it is still with no finger on it):
  `main` `4d27258`, production `dpl_6BGC8Py9pvpEnCqtW2yzj1guNNFb`, the demo alias points to it;
  public demo 0 of 48 short drags off a topic, touch test passed, `qa_home_ink` 282/282,
  `qa_nav` 440/440. Tested with synthesized touch in Chrome, not on a real phone.
- **Live (October 23): the homepage's flying crane between B and C** (Mo found C, half
  size, too small; of B, a size between and C on `reference/ink-pages/mockups/home-crane-size/` he
  picked the size between and said to push it in place of C). Desktop: 57.5% of the comp's crane,
  shrunk toward the point its brush line leaves from, then lifted 60 comp px and moved 50 left
  with its flight stroke. Phones: 63.4vw (66% of the old 96vw), the line unchanged.
  `opening.module.css`; `qa_home_ink`'s phone check now expects the bird at about 41% of the
  window. On the built site (`next start`), the crane's box at 1920x1080, 1440x900 and 390x844
  within 1px of the mockup. Claude pushed `main` to `116c22f` (a fast-forward from `eac92d8`);
  production `dpl_GihZFmN8MjwBSwmjk1SujhiXWgKr`, and the demo alias pointed to it; public demo
  `qa_home_ink` 282/282, `qa_nav` 440/440 (`docs/public-demo.md`).
- **Live (October 23): Free radicals shows the harm** (Mo picked A of three and said to put it
  live): the few sparks that slip past the chimney's screen burn black holes in the roof. See
  "Homepage science section" below. Claude pushed `main` to `eac92d8` (a fast-forward from
  `619e77d`); production `dpl_GNdZYehqzkfJc1Gbq1HUgjxeNgrW`, and the demo alias pointed to it;
  public demo `qa_home_ink` 282/282, `qa_nav` 440/440 (`docs/public-demo.md`). The crane push
  above is built on it.
- **Live (October 23): Switzer is served from the site itself** (Mo said to host it
  ourselves, saw the before/after, `reference/ink-pages/mockups/switzer-self-host/`, and said to
  push it). Fontshare's stylesheet kept dropping the
  connection (the bullet below). Its licence (ITF Free Font License 2.0) allows self-hosting but
  not sharing the files through a public repository, and this one is public, so
  `scripts/fetch-fonts.mjs` fetches the two official variable files (upright 42 KB, italic 33 KB,
  unchanged) from Fontshare's CDN before every `npm run build` and `npm run dev` into the
  git-ignored `public/fonts/switzer/`; if it cannot, the build stops. `globals.css` declares them
  as "Switzer" (so every existing stack and check still names it), the locale layout preloads the
  upright one (not on `/vn`), and `next.config.ts` caches `/fonts/*` for a year (a new file gets
  a new name). No page asks Fontshare for anything any more. Never commit the font files. On the
  built site (`npm run build` + `next start`): every page's first paragraph drawn in "Switzer
  Variable", the file 200 with the year-long cache, no request to Fontshare, `/vn` in Be Vietnam
  Pro without the preload; `qa_home_ink` 282/282, `qa_nav` 440/440, `qa_fda` 220/220, `qa_about`
  353/353, `qa_nuricell_ink` 355/355, `qa_propolis_ink` 273/273, `qa_opc_ink` 185/185,
  `qa_science_ink` 1279/1279, `qa_support` 341/341. Two that fail for older reasons:
  `qa_nature_calm_ink` 158/159 (the front-layer pixel check: on this computer the scene repaints
  hundreds of pixels between two identical screenshots, with Switzer or with it blocked; 159/159
  on the live site) and `qa_vn_font` 37/43 (the same six fail on the live site: the Ysabeau menu
  words and NuriCell's line heights). `qa_turmerific_ink` not run locally (it hangs on
  `next start`). Claude pushed `main` to `faf70af`, whose build failed (`MODULE_NOT_FOUND`:
  `.vercelignore` skipped all of `scripts/`; production stayed as it was), then let the one script
  through and pushed `619e77d`; its build log shows both files fetched (42 KB, 33 KB). Production
  `dpl_3zWtHArBcvgNMjpdAs1BnMwNXfK9`, the demo alias points to it; public demo: the font file 200
  with the year-long cache, no request to Fontshare, every page check passes (`qa_turmerific_ink`
  155/155 and `qa_nature_calm_ink` 159/159 included) but `qa_vn_font`'s six older failures
  (`docs/public-demo.md`).
- **Live (October 23): the homepage science powerhouse** (Mo picked D of six power
  plant ideas and said to put it live). See "Homepage science section" below. Claude pushed
  `main` to `5f800a8` (a fast-forward from `10ef0c5`); production
  `dpl_DMQiiuemFPhNiqRgyRX2HNMVuYvS`, the demo alias points to it; public demo `qa_home_ink` 282/282, `qa_nav` 440/440 (a first run's one failure was `ERR_NO_BUFFER_SPACE` on the checking computer)
  (`docs/public-demo.md`).
- **Live (October 22): the homepage's flying crane at half size (C)**. After B (below)
  went live, Mo asked to try C, then said to push C live in its place. Desktop: half the comp's
  crane, shrunk toward the point its brush line leaves from, then lifted 70 comp px and moved 60
  left with its flight stroke. Phones: 57.6vw (60% of the old 96vw), the line unchanged.
  `opening.module.css`; `qa_home_ink`'s phone check now expects the bird at about 37% of the
  window. Built in a scratch worktree (branch `home-crane-c`), then fast-forwarded here. On the
  built site (`next start`): `qa_home_ink` 282/282, `qa_nav` 440/440; desktop 1920 and 1440,
  phone, tablet, 2560 and Korean looked at (on a tablet, mid-wingbeat, the bird gets small).
  Claude pushed `main` to `10ef0c5` (a fast-forward from `28ee762`); production
  `dpl_CgS1YYUsbc1vtCWQeL69crspWZtJ`, the demo alias points to it; public demo `qa_home_ink`
  282/282, `qa_nav` 439/440 (the font host, below; `docs/public-demo.md`).
- **Fixed by the bullet at the top (October 23): the Switzer font host drops connections.** Switzer's stylesheet came from
  `api.fontshare.com`; from this computer the browser's request was reset
  (`net::ERR_CONNECTION_RESET`) in 5 of 6 loads of the demo and 3 of 6 of a local `next start`,
  and the page then falls back to another face (`qa_nav`'s "no console errors" fails on it).
  `curl` and a direct visit got 200. Not checked from another network. Self-hosting Switzer would
  remove the dependency; not done (not asked).
- **Live (October 22): the homepage science's "Aging cells" shows a brain cell**
  in place of the steam engine (Mo: an engine growing old did not relate to the age slider; he
  picked B, the cell up close, of two painted ideas; mockup
  `reference/ink-pages/mockups/home-science-cell/`). Its branches thin and its six gold power
  plants go out (6, 3, 1) as the age goes up. The first two topics keep the engine. Pictures
  `cell-<age>-v2.webp` from `reference/ink-pages/home-science/build_cell.py`; new caption lines
  `science.peekAge` (English only, like the others); DESIGN.md "The Science Stage Rule". Built in
  a separate worktree while another session pushed the crane, then merged here. On the built site
  (`next start`): `qa_home_ink` 282/282, `qa_nav` 440/440; laptop 1440 and 1280 and phone looked
  at, ages 35, 45 and 70 and the fade. Mo said to push it: Claude pushed `main` to `28ee762` (a
  fast-forward from `7ca818d`); production `dpl_C5C7DQ72sYC5jJTy6JH4zA8b3KAX`, the demo alias
  points to it; public demo `qa_home_ink` 282/282, `qa_nav` 440/440 (`docs/public-demo.md`).
- **Was live (October 22), replaced by C above: the homepage's flying crane smaller and higher** (Mo
  found it a little big, picked B of 80%, 65% and 50%, and said to push it; mockups
  `reference/ink-pages/mockups/home-crane-size/`). Desktop: 65% of the comp's crane, shrunk
  toward the point its brush line leaves from, then lifted 50 comp px and moved 40 left with its
  flight stroke. Phones: 69vw (72% of the old 96vw), the line unchanged. `opening.module.css`;
  `qa_home_ink`'s phone check now expects the bird at about 45% of the window. On the built site
  (`next start`): `qa_home_ink` 282/282, `qa_nav` 440/440; desktop 1920 and 1440, phone, tablet,
  2560 and Korean looked at. Claude pushed `main` to `7ca818d` (a fast-forward from `7895696`);
  production `dpl_GZa6NHXg59Qc8D1u9zJBUyXqqtW3`, the demo alias points to it; public demo
  `qa_home_ink` 282/282, `qa_nav` 440/440 (`docs/public-demo.md`).
- **Live (October 22): the homepage's brush line twice as heavy, and Sign up's stroke drawn
  bigger** (Mo said to push both). The line: Mo picked B of 1.5×, 2× and 2.5× (mockups
  `reference/ink-pages/mockups/home-brush-weight/`); the running line takes the whole weight, the
  bottle's ground and the closing stroke only a little, the crane's opening stroke none; the
  dry-brush streaks keep their old size (`WEIGHT` and `heavy` in `src/components/ink/brush.tsx`).
  On phones only the three rules and the closing stroke change. Sign up: Mo picked C of three
  fuller versions of the same painting (`35e26bb`, another session; DESIGN.md has the details),
  replacing the note below that the stroke stays as it is. Claude merged `main` (the steam
  train) into `studio` and pushed `main` to `7895696`; production
  `dpl_B9XcdfSd5XJS2R4L4UoondvxQcuk`, the demo alias points to it; public demo `qa_home_ink`
  282/282, `qa_nav` 440/440 (`docs/public-demo.md`). The smaller crane above went live after it.
- **Live (October 21): the homepage science steam train** (Mo said to put it live). See
  "Homepage science section" below. Claude pushed `main` to `7a042ce` (a fast-forward from
  `d9c8c34`); production `dpl_CJt1fJcyGvX3aocGj47Wi3AjVg7V`, the demo alias points to it; public
  demo `qa_home_ink` 282/282 and `qa_nav` 440/440 (`docs/public-demo.md`).
- **Live (October 21): two phone fixes** (Mo said to fix and push them). The homepage's
  warm sky was cut flat under the menu bar on phones (the opening's picture now clips only its
  sides, `opening.module.css`: a 12-level step, now under 1); and "✕ Close" was squeezed against
  the mark in the phone bar (from 400px down the bar's sides come out to 16px, the ✕ steps aside,
  the stroke is never shorter than clamp(78px, 26vw - 8px, 86px), CJK words at 17px: 15px or more
  to the mark from 360px in every language). Claude pushed `main` to `d9c8c34`; production
  `dpl_FF2NdyPy2e95UY2tYzJ96CcBzpjD`, the demo alias points to it (`docs/public-demo.md`). Not
  fixed: on a 320px phone, Japanese "メニュー" runs onto the stroke's dry tail, 8px from the mark.
- **Sign up's stroke kept, then drawn bigger (Mo, October 21).** He looked at three other strokes
  (clean, painted pill, dry brush; `reference/ink-pages/mockups/nav/2026-10-21-signup/`, originals
  `reference/nav/originals/codex-signup-*.png`) and kept the painting itself: at the size people
  see it, it reads as one quick brush gesture. Then he picked it a little fuller (C of three,
  `mockups/nav/2026-10-21-signup-fuller/`): the same painting drawn bigger, live since October 22
  (see above).
- **Live before that (October 21): the menu bar "Signed with one stroke"** (Mo picked A of three
  painted ideas and said to push it): the bar's words in Ysabeau (CJK keep their own letters), the
  painted rule under the bar from the first frame (laid once as the page opens), Sign up and the
  phone's Menu in paper on a black Codex-painted brushstroke (`inscription/swash-v1.webp`), a pale
  wash behind a pointed-at word (`inscription/wash-v1.webp`); `reference/nav/make_signed_strokes.py`
  cuts both. Ysabeau loads from the root layout (not preloaded: a preload would go unused on CJK
  pages). The Science eyebrow sits 22px under the rule from 1101px (`journey.module.css`).
  `qa_nav.py` updated (rule there from the start, the wash, text on the stroke). Claude pushed
  `main` to `849e26d` (a fast-forward); production `dpl_CuSdqu5hCtTLHH2tLy6m3ozDB38J`. Public
  demo then: all eleven page checks pass (`docs/public-demo.md`). Mockups,
  the three ideas and the built screenshots: `reference/ink-pages/mockups/nav/2026-10-21/`.
- **The homepage-science sketches seen here on October 21** (hiker and cell paintings, a README
  edit) were Claude Code's, for the science section (below). They were moved out of this folder
  the same day; the kept ones are committed with the steam train.
- **Live before that (October 19, latest then):** About's opening circle is now circle A, "heavy
  to dry" (a wet, heavy start that thins into dry streaks and lifts before it closes), and its
  gold leaf floats down onto the stroke like a real flake, then settles and catches the light; the
  spark of light that ran round the old circle is gone. Mo picked it from three new circles; Claude
  pushed `main` to `6e8aaca` (`ea13c93` plus that one commit). Production
  `dpl_6eTzh1tqkEpWqmBV1nM9w3YfxVJ7`. Public demo then: `qa_about` 353/353, `qa_home_ink`
  282/282, `qa_nav` 436/436.
- **Live before that (October 19):** all of `studio`, which Mo pushed as `ea13c93` (NuriCell layout
  B, About's oak, the redwood park sign in every page's footer and the homepage science section).
  Public demo then: `qa_home_ink` 282, `qa_nav` 436, `qa_fda` 220, `qa_about` 353,
  `qa_propolis_ink` 273, `qa_opc_ink` 185, `qa_nuricell_ink` 355, `qa_turmerific_ink` 155,
  `qa_nature_calm_ink` 159, `qa_science_ink` 1279, `qa_support` 341, all passing.
- **State:** `main` is `116c22f` (live: the powerhouse, Free radicals and the brain cell, the
  bigger Sign up stroke, the brush line's 2×, the crane at 57.5% and the self-hosted Switzer);
  `studio` adds only these release notes, so the next push is a fast-forward.
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
- **Homepage science section (Claude Code).** "Make sense of the science." shows, with a line
  under each picture tying it to the words: Mitochondria and Free radicals, an old powerhouse
  with its front left open (a worker feeding the gold fire, its steam turning the wheel, power
  out along the wire), Mo's pick D of six power plant ideas on October 22; for Free radicals its
  chimney opened up, the screen catching most sparks and the few that slip past burning black
  holes in the roof (Mo's pick A, October 23, after the caught sparks alone showed no harm;
  `build_plant.py`); Aging
  cells, a brain cell up close at three ages (`build_cell.py`). Before: the October 19
  hummingbird, apple and Joshua tree (decorative), a hiker with a window into a cell (dropped),
  the October 21 steam train. The caption lines (`science.peek`, `science.peekAge` in
  `content.ts`) are English in every language for now. Notes:
  `reference/ink-pages/home-science/README.md`; rule: DESIGN.md "The Science Stage Rule".
  On phones and tablets (under 900px) the tabs sit right above the picture and the three topics
  swipe sideways in a strip (DESIGN.md "The Scroll Story Rule"). Touch test:
  `scripts/qa/qa_home_ink.py` covers the tabs; finger swipes were tested through Chrome's
  DevTools protocol (`Input.dispatchTouchEvent`; `synthesizeScrollGesture` does nothing headless).
- **In progress:** None. **Next:** Mo's call.

## What's live

Public demo: <https://bigh-website-demo.vercel.app/>. It shows the production build of `main`
at `849e26d`, the same build as <https://bigh-website.vercel.app/> (everything below, with the
October 21 menu bar). `bighnow.com` is still the old WordPress site.

Every page is in Ink & Gold:

| Page                 | Its own idea                                                                             | Last public browser check             |
| -------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------- |
| Home                 | Crane; green spring watercolour in the paintings (Mo's pick C, Oct 16); buttons stay ink | `qa_home_ink` 282/282 (Oct 21)        |
| Menu bar             | "Inscription", signed with one stroke (Oct 21); all five bottles in Products             | `qa_nav` 440/440 (Oct 21)             |
| Footer               | FDA statement on a painted California trail sign                                         | `qa_fda` 220/220 (Oct 21)             |
| About                | Design C, "circle"                                                                       | `qa_about` 353/353 (Oct 21)           |
| NuriCell             | Paper lantern that lights; each painting in its own place (layout B, Oct 19)             | `qa_nuricell_ink` 355/355 (Oct 21)    |
| Green Bee Propolis   | Bold Signature desktop; Editorial pair mobile; gold flowing into the bee tree            | `qa_propolis_ink` 273/273 (Oct 21)    |
| Advanced OPC Formula | Grapes lit from inside                                                                   | `qa_opc_ink` 185/185 (Oct 21)         |
| Turmerific           | Gold soaking into the paper                                                              | `qa_turmerific_ink` 155/155 (Oct 21)  |
| Nature Calm          | Still lake whose gold gathers into one line                                              | `qa_nature_calm_ink` 159/159 (Oct 21) |
| Science              | Live: his path, one place per screen (Oct 26); local: round 3, the town's lamps (Nov 4)  | `qa_science_ink` 633/633 (Oct 26)     |
| Support              | "Pull up a chair" porch; the form is a preview and sends nothing                         | `qa_support` 341/341 (Oct 21)         |

Details of each go-live are in [`public-demo.md`](public-demo.md). Each page's notes, prompts and
spend are in `reference/ink-pages/<page>/`.

## Unfinished or waiting on Mo

- **Translations:** new lines are drafts and need a native speaker's check: NuriCell m594–m609,
  Science m650–m661 (some older Science lines are still English in four languages), OPC m700–m705,
  Turmerific m740–m744, Nature Calm m780–m784, About's oak m900, NuriCell's tidied "Tiny power
  plants" words and its lighthouse m901–m906 (m904, the picture's alt text, rewritten for the
  lighthouse). Support is English only for now
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
