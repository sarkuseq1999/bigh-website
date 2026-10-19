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
- **Green Bee Propolis opening:** keep the real bottle between the product-name text on desktop
  (Mo, October 16, 2026). Refine that composition; do not replace it with all the words beside the
  bottle. On October 18, Mo selected mobile option B, Editorial pair: Green / Bee / Propolis
  stacked on the left beside the real bottle, then the short description and original purchase
  card. Put the longer explanation and provenance below the purchase controls on mobile only.
  Preserve the approved desktop appearance.
  Mo approved Bold Signature A on October 18: heavy Switzer (750), Green left, the real bottle
  centred, Bee / Propolis right. Keep the original outlined One bottle card with the capsule,
  overlapping 45-day badge, daily count, and a centred Add to cart without an arrow.
  Mo approved Weathered Taupe A for the Propolis FDA footer sign on October 18: use the
  unchanged blank artwork with the exact selectable disclaimer in charcoal. Keep this treatment
  scoped to Propolis; preserve the approved desktop opening, mobile B and purchase card.
- **FDA footer sign trial (October 19):** Mo found the taupe sign still too much like a drawing
  (pen outlines, wood grain) next to the homepage's soft ink wash. To compare two painted signs on
  real pages, sign A (ink-wash trail sign) is on Advanced OPC and sign C (one-brushstroke board,
  one California poppy) is on Green Bee Propolis, in place of the taupe sign. Not chosen yet; the
  other pages keep the brown sign. Mockups: `reference/ink-pages/mockups/fda-sign/`.
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
