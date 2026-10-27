<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.

<!-- END:nextjs-agent-rules -->

# BiGH website: the shared rulebook

Two agents build this site: **Claude Code** (the main builder) and **Codex** (the picture studio, and
sometimes a builder). Both read this file. `CLAUDE.md` only points here. Mo owns the site and decides.

## Start here

- **Folder:** `C:\Users\mcbig\Documents\codes\bigh-website`, branch `studio` (it tracks `origin/main`).
  Both apps open this folder. In Codex, work in this folder itself (Local), not in a separate worktree.
- **Read first:** [`docs/HANDOFF.md`](docs/HANDOFF.md) (what's live, what's unfinished, how to run).
  Then [`DESIGN.md`](DESIGN.md) (the Ink & Gold look) and [`PRODUCT.md`](PRODUCT.md) (facts, promises,
  honesty rules). `BRAND-CHEATSHEET.md` still holds product facts and Dr. Liu's story; its design notes
  describe the September site that Ink & Gold replaced.
- **Run:** `npm run dev -- --hostname localhost --port 3007`, then open http://localhost:3007.

## Taking turns

1. **One agent at a time.** Never let Claude Code and Codex edit this folder at once.
2. **Starting a turn:** run `git status` and `git log --oneline -5`, then read `docs/HANDOFF.md`.
3. **Ending a turn** (Mo says "finish up for handoff"): commit the work locally on `studio`, update the
   "Now" part of `docs/HANDOFF.md`, and tell Mo in one or two lines what is done and what is not.
   Never leave uncommitted changes for the other agent.
4. **New rules go in the repo.** When Mo states a lasting rule or design decision, write it into this
   file (or `DESIGN.md` for the look) in the same turn. Private memory is invisible to the other agent.
5. **One job, one agent.** Don't split one page between the two agents.
6. **Other folders are old task copies.** `C:\Users\mcbig\Documents\codes\bigh-*` and Codex's own
   worktrees hold finished or abandoned work. Don't work in them, and ask Mo before deleting any.

## Mo's standing rules

- **Ask before:** every push (the GitHub repo is public, and a push to `main` is a live production
  build), any spending, and anything that messages a customer.
- **Look before you show.** Take real screenshots (desktop and phone, and the moving states), look at
  them at full size, scrolled like a visitor, and score the work honestly out of 10. Show Mo only at 8
  or above (9 for the homepage or a page's centrepiece). Say the score and what still holds it back.
  Anything that would look like a mistake to a first-time visitor is a defect, even if it was built on
  purpose. Never write a check that asserts an oddity into place.
- **Check the built site.** `next build` orders CSS differently from `next dev`, so a page is only done
  after it is checked on `npm run build` + `npm start`.
- **Show pictures on a page Mo can open on a phone** (Claude: an Artifact link). Label choices A/B/C and
  recommend one. Don't flood Mo with options.
- **Words:** understated and concrete, no hype; short lines ("a website, not an article"); keep the
  honesty labels (illustrations, fictional samples, research limits).
- **Only add what was asked for.** No speculative features or integrations.

## Design rules Mo has stated

These sit on top of `DESIGN.md`.

- **Shared theme, own design.** Every page shares only the theme: rice paper, sumi ink, one gold leaf
  for energy, Switzer (Ysabeau for titles), the menu bar, the footer, honesty labels, the slow pace.
  Each page needs its own layout, its own new paintings and its own signature moment. Never reuse the
  homepage's paintings or its page-long brush line as a page's main structure. Test: "Would someone
  think this is the homepage?" If yes, redesign. Offer 2-3 concepts as picture mockups before building.
- **Even rhythm.** Every section uses the same pairing (one painting and its words, sides alternating).
  One picture per screen, and each chapter brings its own picture. A signature object lives only in
  the chapter where it means something. The brand name appears once per screen. No fake paper folds.
- **Don't park every painting on one side.** Mo found NuriCell's chapters boring with every
  painting on the left (October 19, 2026) and picked B, "each painting gets its own spot", over a
  plain left-right zigzag. From 960px: lantern right, the capsule in the middle of its four
  ingredients, the books running in from the page edge, Dr. Liu right, the brushed 3 × 30 = 90
  across the page, the bottle left. Phones keep one column. NuriCell only for now
  (`nuricell.module.css`); the other four product pages still put every painting on the left.
- **NuriCell Dr. Liu: the view west (Mo picked A2, October 26, 2026).** Mo wanted the Dr. Liu
  chapter "more fun" and better designed. Of three ideas (A the Berkeley story, B a magazine cover,
  C a line in his own words) he picked A, then A2 of two mockups, then asked for it improved. His
  real portrait (liu-v1, never redrawn) stands on the Berkeley hills over the bay, the Golden Gate
  in the fog, painted in the site's grey ink (round 1's colour watercolour looked borrowed), dry
  grass in front of his foot. From 960px one painting runs across the chapter and his name and
  words sit in its sky; phones get their own framing (him larger, the bridge beside him). No label
  over his name; the lead says he studied two of NuriCell's nutrients together at UC Berkeley; the
  2002 study is told as published, with "An animal study, not a test of NuriCell." NuriCell only:
  Nature Calm keeps the plain portrait. `people.tsx`, `nuricell.module.css`, `build_nuricell.py`
  (`berkeley()`); mockups `reference/ink-pages/mockups/nuricell-liu/`.
- **NuriCell "What's inside": moving gold, a tidier top, the pairs as scenes (Mo picked 1A,
  October 26, 2026).** Mo liked the plate's layout but wanted the gold to move, found the small
  grey "What's inside" label odd and the three grey notes under the plate messy, and the
  "Why these four work together" columns dull. The gold leaf now rises out of the powder and
  settles where it is painted, then each flake keeps turning slowly, catching the light like
  real gold leaf (picked over a never-ending updraft). The label is gone (the heading says it);
  "per serving of 3 capsules" sits right under the heading (the heading says "every capsule",
  the amounts are for 3); the other ingredients are one label card; the research note is said
  once, at the chapter's end. The pairs are three little scenes: each pair's two powder heaps
  from the painting and its gold doing what the pair does together (lit, kept in reserve, two
  halves made one), picked over a scroll story and a pick-a-partner game. NuriCell only
  (`nuricell-leaf.tsx`, `nuricell-scenes.tsx`; pictures `build_nuricell_gold.py`). Mockups:
  `reference/ink-pages/mockups/nuricell-inside/`.
- **NuriCell "Tiny power plants": a California lighthouse and fewer words (Mo picked B, October
  26, 2026).** Mo asked for another kind of lamp and found the words too much and not well ordered,
  the grey "Why cellular health matters" line on top strange. Of three California lights (A a Gold
  Rush miner's lantern, B a coast lighthouse, C a San Francisco gas street lamp) he first picked A
  (the paper lantern read as Asian), then saw A built beside the B sample and switched to B the
  same day. Its light still comes on as you scroll (the lamp room dark, then lit, with its beam).
  On phones and tablets it stands taller than the template's paintings (55% of the window, not
  46%) so its lamp is more than a dot. The label over the heading is gone, the three paragraphs are
  one lead-in line on the heading's left edge (no indent), and the brain's 2% is set small and grey
  beside a big 20% (stacked, small first, on phones). NuriCell only (`why.tsx`,
  `nuricell.module.css`; pictures `build_nuricell.py`, Codex paintings). Mockups:
  `reference/ink-pages/mockups/nuricell-why/`.
- **Product openings, the words under the name: "Title face" (Mo picked C, October 26, 2026).**
  Mo found the bottom-left of NuriCell's first screen weak and unfinished (grey words, a thin side
  line, ending above the buy box). He turned down Dr. Liu's photo there: the opening is shared, and
  pages without him (Turmerific and Propolis have no scientist chapter) would look lesser. So a fix
  for the shared opening uses only what every product has. The headline is in Ysabeau; the purpose
  is a large lead in ink that runs under the bottle, with no side line; from 960px the two sit
  together at the foot of their side and end where Add to cart ends. All four products on the
  shared opening (`opening.tsx`, `product-ink.module.css`); Green Bee Propolis keeps its own
  approved opening. Mockups: `reference/ink-pages/mockups/nuricell-hero-left/`.
- **About, "Our purpose" and the circle (October 19, 2026).** Mo found the seedling too slight for
  the purpose and its mission line too small to read. He picked a big painted valley oak (a rope
  swing above the ground, a gold light in the roots you can't see); it stands larger than the
  page's other paintings on purpose. The mission line sits a step under the heading, in ink, not
  the grey body size. Later the same day Mo found the opening circle "too round, not artistic
  enough" and the spark of gold light that ran round it "fake". He picked circle A, "heavy to
  dry" (a wet, heavy start that thins into dry streaks and lifts before it closes), and the gold
  leaf floating down onto it like a real flake, settling, then catching the light. Gold leaf
  behaves like real gold: no glow, no spark, no twinkling stars, never red.
- **Green Bee Propolis opening:** keep the real bottle between the product-name text on desktop
  (Mo, October 16, 2026). Refine that composition; do not replace it with all the words beside the
  bottle. On October 18, Mo selected mobile option B, Editorial pair: Green / Bee / Propolis
  stacked on the left beside the real bottle, then the short description and original purchase
  card. Put the longer explanation and provenance below the purchase controls on mobile only.
  Preserve the approved desktop appearance.
  Mo approved Bold Signature A on October 18: heavy Switzer (750), Green left, the real bottle
  centred, Bee / Propolis right. Keep the original outlined One bottle card with the capsule,
  overlapping 45-day badge, daily count, and a centred Add to cart without an arrow.
  Preserve the approved desktop opening, mobile B and purchase card. (Its Weathered Taupe A
  footer sign of October 18 was replaced on October 19 by the site-wide redwood park sign.)
- **FDA footer sign: the redwood park sign, on every page (Mo, October 19, 2026).** The brown
  trail sign (October 13) and the taupe sign (October 18) looked drawn (pen outlines, wood grain)
  next to the homepage's soft ink wash. After trying painted signs on real pages, Mo liked the
  one-brushstroke sign with a California poppy and asked for the feel of California's park signs,
  then picked the redwood park sign: a muted redwood plank with rounded corners, a cream carved
  border and cream letters, sage grass and the poppy, painted loosely with no pen outlines. Keep
  its brown muted (ink, not orange) and its letters at 4.5:1 or more. Mockups:
  `reference/ink-pages/mockups/fda-sign/`.
- **Footer: the copyright line comes last (Mo, October 26, 2026).** "© 2026 BiGH. Be in Good
  Health." and "Back to top" are the page's very last line, under the park sign (© left, Back to
  top right; on phones Back to top above, © last). The grey preview note that sat under the sign
  ("Educational content is for general information…") is gone; the product window still says
  ordering is not open.
- **California, not Asian.** BiGH is a California/USA brand. Keep the ink style, but no Chinese
  characters, seals, stamps, scrolls-as-culture or herbal cabinets, and no Asian-tradition names like
  "kintsugi". Anchor ideas in California and American imagery: poppies, oaks, golden hills, state-park
  signs, botanist specimens.
- **Paintings, not photos.** Loose sumi-e brushwork, like the homepage crane: "the more it looks like a
  painting, the better." Watercolour backgrounds only. No photo-real scenes and no detailed drawings.
- **Never redraw the product.** Paint the background with an empty spot, then stand the real approved
  bottle PNG from `public/images/products/` in it, unchanged. A soft ground wash and a front layer (a
  sprig in front of the base) seat it in the painting. Never ship a generated bottle or label.
- **Real people.** Dr. Liu's face is never generated: use his real photo, in colour (a living person in
  black and white reads as deceased). When editing a painting with his photo in it, give the edit model
  the empty frame and paste the real photo back afterwards. Dr. Iris Wang appears in words only.
- **Never use:** lab glassware (reads as "chemicals you eat"), red or rust clustered dots or fuzzy glows
  (read as germs), a gold halo behind a product, a decorative picture that only repeats its sentence.
  Every picture must add information.
- **Never boring at rest.** Judge a design at first glance, before any hover. If it looks like a
  template or the old design at rest, it fails.
- **Menus show everything at once** on desktop (a row of all five bottles, not a list that swaps one
  picture on hover).
- **Menu bar: "Signed with one stroke" (Mo picked A, October 21, 2026).** Mo found the bar plain
  ("simple, it does its job") and picked A of three painted ideas over B (a two-line title page)
  and C (the words on one pale brushstroke): the bar's words in Ysabeau, the title face (Chinese,
  Japanese and Korean keep their own letters); the painted rule under the bar from the first frame,
  laid once as the page opens; Sign up and the phone's Menu written in paper on a real black
  brushstroke; a pale ink wash behind a pointed-at word. Drop-downs, the settle and the menu sheet
  stay as they were. Mockups: `reference/ink-pages/mockups/nav/2026-10-21/`; strokes cut by
  `reference/nav/make_signed_strokes.py` from two Codex paintings.
- **Menu bar: Science is a plain link for now (Mo, October 26, 2026).** The Science page is one
  page, and the drop-down's four doors into it made the site look short of content. Science goes
  straight to `/science` on the bar and in the phone's menu, like About and Support. Keep the
  drop-down's design: it is switched off, not deleted (`navScienceMenu` in
  `src/components/ink/nav/nav-data.ts`, `SCIENCE_MENU` in `scripts/qa/qa_nav.py`). Turn it back
  on only when Mo says the Science page has grown enough.
- **Science: his path one place per screen (Mo picked B, October 26, 2026).** Mo liked the
  Science page's paintings but found the sideways handscroll "feels like a draft", and asked for
  an order that is logical and easy. The page opens on the title and Dr. Liu (photo, name, intro;
  no numbers row, his path tells them), then his path going down, one place per screen: Okayama
  (painting left), Berkeley 1994 (right; the 2002 study is told there), Salzburg 2025 (left),
  Today (wide, its words in the sky by the gold sun). Then the research, health explained, the
  formulas, Ask. The paintings are cut from the old handscroll's band (`build_science.py`,
  `PLACES`); phones get tighter cuts in one column. Berkeley says 1994, not 1994-2002: the
  faculty profile dates his time in Bruce Ames's laboratory 1994-1997. Mockups:
  `reference/ink-pages/mockups/science-path/2026-10-26/`.
- **Homepage brush line: twice as heavy (Mo picked B, October 21, 2026).** Mo asked for the
  page-long line a little thicker and picked B (2×) over A (1.5×) and C (2.5×). The running line
  takes the whole weight; the two heavy accents (the ground under the big bottle, the closing
  stroke under "Stay sharp.") only a little more, so they never turn into slabs; the crane's
  opening stroke none, on phones too. The dry-brush streaks keep their old size, so the heavier
  line never reads as two lines or a hollow tube. `WEIGHT` in `src/components/ink/brush.tsx`.
  Mockups: `reference/ink-pages/mockups/home-brush-weight/`.
- **Homepage crane: between B and C, 57.5% (Mo picked it, October 23, 2026).** Mo liked the
  opening but found the flying crane a little big. Of three sizes (A 80%, B 65%, C 50%) he put B
  live, then C, then found C too small and picked a size between them. The crane is 57.5% of the
  comp's size, shrunk toward the point its brush line leaves from, then lifted 60 comp px and
  moved 50 left, its flight stroke with it, so it reads as farther off in the sky and the
  headline leads. Phones: 66% of the old crane (63.4vw, the bird about 41% of the window), clear
  of the window's left edge, its line unchanged. `opening.module.css`. Mockups:
  `reference/ink-pages/mockups/home-crane-size/`.
- **Homepage "Aging cells": a brain cell up close (Mo picked B, October 22, 2026).** Mo found the
  steam engine growing old did not relate to the age slider and asked for a cell that ages. One
  brain cell, up close: its branches thin and its six gold power plants go out (6, 3, 1) as the
  age goes up, still at work when old. Picked over A (the whole cell, whose gold was too small on
  a phone). DESIGN.md "The Science Stage Rule";
  mockup: `reference/ink-pages/mockups/home-science-cell/`.
- **Homepage "Mitochondria" and "Free radicals": inside the powerhouse (Mo picked D, October 22,
  2026).** Mo asked for a power plant instead of the steam train and picked D of six painted ideas:
  an old powerhouse with its front left open like a storybook (a worker feeds the gold fire, its
  steam turns the wheel, power runs out along the wire), and for Free radicals its chimney opened
  up, the screen on top catching the sparks. Grey ink, few parts, the crane's hand. On October 23
  Mo asked Free radicals to show harm ("free radicals harm us") and picked A of three: the few
  sparks that slip past the screen burn black holes in the roof (black ink only, never red).
  DESIGN.md "The Science Stage Rule"; mockups: `reference/ink-pages/mockups/home-science-plants/`
  and `home-science-harm/`.
- **Homepage science on phones: tabs over the picture, swipe, a peek (Mo, October 23-26, 2026).** In
  one column the three tabs sat about 500px above the picture, out of sight. Mo picked A (the tabs
  right above the picture, the words after it), then asked to swipe with a finger from one topic to
  the next: the three topics (picture, line, words) sit side by side in a strip as wide as the
  window that snaps to one topic; the tabs glide it and follow the swipe. On October 26 Mo asked
  how people would know they can swipe and picked A of three hints (over a one-time nudge and three
  dots): the next topic's painting peeks in, paler, at the window's right edge. DESIGN.md "The
  Scroll Story Rule"; `science.tsx` (`.slides`).
- **References:** Timeline (timeline.com) is Mo's favourite site: borrow its calm, one idea per screen,
  not its small labels. Keep labels and targets large for older readers.

## Pictures: where they go

| What                                  | Where                                                                                   |
| ------------------------------------- | --------------------------------------------------------------------------------------- |
| Approved product bottles (never edit) | `public/images/products/<product>.png` (see `docs/brand-assets.md`)                     |
| Pictures the site shows               | `public/images/<page>/…` or `public/images/products/<slug>/ink/`, as `<name>-v<N>.webp` |
| Raw generated originals (kept)        | `reference/ink-pages/<page>/originals/`                                                 |
| Prompts (one `.txt` per picture)      | `reference/ink-pages/<page>/prompts/`                                                   |
| Mockups shown to Mo                   | `reference/ink-pages/mockups/<page>/`                                                   |
| Page notes and spend                  | `reference/ink-pages/<page>/README.md`                                                  |
| Lossless working plates               | `reference/ink-pages/<page>/plates/` (git-ignored)                                      |
| Unused originals                      | `C:\Users\mcbig\Documents\codes\bigh-archive\` (outside the public repo)                |

- Each page has a build script (`reference/ink-pages/<page>/build_<page>.py`) that turns originals into
  the site's webp files. Paintings ship with their paper divided out and multiply onto the page.
- **Replacing a picture:** give it a new file name (`-v2`). The image optimizer caches by name.
- **Codex pictures:** Codex's own copy lands in `~/.codex/generated_images/`, outside this repo, where
  Claude can't find it. Always save the keeper into the page's `originals/` folder, with its prompt in
  `prompts/` under the same name.
- **Claude sending a picture job to Codex:** run it in the background from the target folder:
  `codex exec --skip-git-repo-check -C "<folder>" -s workspace-write -c model_reasoning_effort="low" -o "<folder>/last-message.txt" "Use your built-in image generation tool to make ONE picture: <prompt>. Copy the PNG into the current folder as <name>.png."`
  Tested October 16, 2026: one picture in 48 seconds. It uses Mo's ChatGPT plan allowance, not API
  credit. Every picture order must carry the design rules above.
- **Paid generators** (Higgsfield GPT Image 2.5, about $0.05 a picture, through each page's
  `hf_<page>.py` helper with a ledger and a cap): ask Mo for a budget first.
- **Never `git add -A`.** Large picture folders and logs sit in the tree. Add files by name.

## Run, check, ship

- **Dev:** `npm run dev -- --hostname localhost --port 3007` (Claude: preview "bigh-website").
- **Built site:** `npm run build`, then `npm start -- --hostname localhost --port 3006` (Claude: preview
  "bigh-website-prod").
- **Browser checks:** `scripts/qa/` (Playwright for Python), run as
  `python -X utf8 scripts/qa/<script>.py <base-url>`. Page scripts: `qa_home_ink`, `qa_nav`, `qa_fda`,
  `qa_about`, `qa_nuricell_ink`, `qa_propolis_ink`, `qa_opc_ink`, `qa_turmerific_ink`,
  `qa_nature_calm_ink`, `qa_science_ink`, `qa_support`. Run the ones for the pages you touched, plus
  `qa_home_ink` and `qa_nav`.
- **Code checks:** `npm run lint`, `npm run type-check`, and `npx prettier --check <changed files>`.
- **Going live (only on Mo's yes):** `git fetch`, merge `origin/main`, rebuild and re-check, then
  `git push origin studio:main`. If the push is blocked for the agent, give Mo the exact command to
  paste. Vercel builds production from `main`; then point the demo alias (below), run the checks
  against the public demo, and add an entry to `docs/public-demo.md`.
- **Preview share links:** only one `?_vercel_share=` link works at a time; making a new one kills the
  old one.

## Code traps

- **Switzer's font files are never committed** (Mo, October 23, 2026: host it ourselves). Its
  licence allows self-hosting but not sharing the files through a public repository, and this one
  is public. `scripts/fetch-fonts.mjs` fetches the official files from Fontshare before every
  `npm run build` / `npm run dev` into the git-ignored `public/fonts/switzer/`; run builds through
  npm, not `next build` alone, or the site ships without them. Never subset or convert them.
  `.vercelignore` skips `scripts/` except this one file; a build script Vercel must run needs
  the same exception (October 23: the first push failed with `MODULE_NOT_FOUND`).
- **Homepage CSS specificity:** `src/components/home/homepage.module.css` resets `.site p`,
  `.site button` and `.site h2` (specificity 0,1,1). A single-class CSS-module rule such as
  `.cta { background: … }` loses to them silently. Scope component rules under the component's root
  class (for example `.portraits .cta`).
- **Line endings:** files are LF, but this checkout has `core.autocrlf=true`. `git stash` and
  `git checkout` rewrite touched files with CRLF, and `npm run format:check` then fails on all of them.
  Don't stash to compare states. Python on Windows writes CRLF unless you pass `newline="\n"`.
  `prettier --write` restores LF.
- **New route folder:** restart the dev server, or it 404s.
- **Hidden browser pane:** animation frames pause, so pane screenshots of moving pages come out blank.
  Use Playwright.
- **Bash heredocs eat backslashes** in generated code. Write scripts to files instead.

## Public demo address

Mo requested a public demo without login or share tokens after colleagues could not open earlier preview links.

- Use `https://bigh-website-demo.vercel.app/` as the single demo address. Do not send a new deployment URL or tokenized share link for routine updates.
- After publishing and checking a new deployment, point this alias at it with `vercel alias set <deployment-hostname> bigh-website-demo.vercel.app --scope sarkuseq1999s-projects` (Claude can also use the Vercel MCP `assign_alias`).
- Verify the plain demo URL in a fresh unauthenticated browser after every alias update, including the new feature.
- The demo alias has a domain-specific public-access exception. Keep the project’s general Vercel Authentication setting intact. A project-wide removal was rejected by automatic approval review; the narrower demo exception succeeded.
- See `docs/public-demo.md` for the current deployment and access details.

## Fresh start

This is a brand-new website using the existing tech stack. Do not carry over old design, content, or
product assumptions unless Mo explicitly asks.

- `old-storage/` is the archived previous website. Do not use it as design guidance or reuse its
  layouts, colors, fonts, images, wording, or animations unless asked.
- `reference/` holds reference materials for the new website.

## Higgsfield video and animation connection

For Higgsfield video or animation requests, first read
`C:/Users/mcbig/.codex/skills/higgsfield-api/SKILL.md`.
The API helper and encrypted credential live outside this website repository. Video defaults to no
sound unless Mo asks for it.
