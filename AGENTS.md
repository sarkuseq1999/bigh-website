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
   file (or `DESIGN.md` for the look, `docs/DESIGN-DECISIONS.md` for a page's design decision) in
   the same turn. Private memory is invisible to the other agent.
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
- **One part at a time** (Mo, October 28, 2026: "the quality really kind of matters. We should
  not rush it"). When several parts need redesigning, mock up one part on the real page, show
  it, discuss it with Mo, build it, and only then start the next. Don't bundle parts.

## Design rules Mo has stated

Mo's page-by-page design decisions (what he picked for each part of each page, and why) live in
[`docs/DESIGN-DECISIONS.md`](docs/DESIGN-DECISIONS.md). They sit on top of `DESIGN.md` and are
as binding as this file. **Read it before you design, redesign, repaint or mock up any part of
a page**, and before you touch a page's paintings, layout or words; search it for the page and
part you are working on. Routine fixes that change nothing visible can skip it. New design
decisions go there, in the same turn.

## The English launch (Mo, November 16, 2026)

Mo's goal: make the English site ready for launch, with launch-quality words everywhere and nothing
that reads as unfinished. The switches for launch day are in [`docs/launch-checklist.md`](docs/launch-checklist.md).

- **Our own shop, not iMatrix.** BiGH will use its own back office and cart (bigh-backend); never link
  the old iMatrix cart (`backoffice.office2office.com`, `aeg.imatrixoffice.com`). Everything the site
  needs from the shop lives in `src/components/shop/shop.ts` (cart links, Log in, Sign up, prices);
  until a link is set its button stays a polite placeholder.
- **Prices:** the bighnow.com prices (NuriCell and Nature Calm $80, Advanced OPC Formula $65,
  Turmerific $50, Green Bee Propolis $36), shown on each product page's card and buy chapter.
- **Customer stories stay fictional for now**, labeled "Illustrative stories: the people and names
  below are fictional, not real customers." Never "Design draft". Real words replace them later.
- **Ask BiGH Science is live, through the Support form** (topic "A health or science question";
  its buttons open `/support?topic=science#write`). BiGH's team answers, with the scientists it works
  with when a question needs them. Never promise a personal answer from Dr. Liu; never medical advice.
- **The Support form sends email through Resend** (`/api/support`) once its environment variables are
  set; until then it keeps its placeholder line.
- **Legal pages** `/privacy`, `/terms`, `/returns`: BiGH's own 2016 documents, wording kept; linked
  in the footer's last line.
- **American spelling** in every visible line (color, flavor, watercolor), except a label's own words
  quoted as printed ("Optimised"). Counts one to nine in words, 10 and up in figures.
- **Search stays closed until launch day** (`SITE_INDEXING=on` opens it).

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
  `qa_home_ink` and `qa_nav`, one at a time (two at once, or a build beside them, can fail the
  filmed-timing checks; rerun a failed script alone before calling it a defect). Each page script
  imports `stall_guard.py`: if nothing prints for 10 minutes (`QA_STALL_MINUTES`), it prints
  `FAIL frozen: …` with the last line it printed and stops with exit code 3. A browser can freeze
  without an error (November 4, 2026: `qa_nav` sat idle for 55 minutes on the public demo).
- **Code checks:** `npm run lint`, `npm run type-check`, and `npx prettier --check <changed files>`.
- **Going live (only on Mo's yes):** `git fetch`, merge `origin/main`, rebuild and re-check, then
  `git push origin studio:main`. If the push is blocked for the agent, give Mo the exact command to
  paste. Vercel builds production from `main`; then point the demo alias (below), run the checks
  against the public demo, and add an entry to `docs/public-demo.md`.
  **Mo doesn't wait for the public checks** (November 4, 2026: "I could just work on the next
  thing"). Once the alias points at the new build and a quick look shows the change on the plain
  demo address, tell Mo it is live and that the full checks are running; run them in the
  background and go on with the next thing. Tell Mo only if one fails (and fix it first); write the
  `docs/public-demo.md` entry with the counts when they finish.
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
