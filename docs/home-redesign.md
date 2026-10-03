# Homepage redesign (from September 28, 2026)

Mo: "Now that the About and Science and NuriCell page all look really good, I want you to do the
same or even higher caliber re-design for the Home page. The contents don't really have to change,
but the overall design and feel ... change any image or videos if needed. Check your own work with
screenshots and don't stop until it reaches 8.8 out of 10. Give me 2 to 3 options. Use all design
references necessary, also outside sources. This home page is the centerpiece of this website."

## Final: Ink & Gold, the crane (October 2, 2026)

Mo picked the crane ("This Crane one is amazing."). It is now the homepage itself at `/` in every
language: `src/app/[locale]/page.tsx` renders `HomeDialogs` around `LookInk`
(`src/components/home-v2/look-ink/`). There is no `?look=` and no switcher any more.

- Removed: the cell opening (code, `mito-cell` picture and plate, its comp spec) and the eight test
  looks (daylight, night, words, sunrise, pop, iris, everyday, botanical): their components, pictures,
  clips, reference folders and QA scripts, plus `home-v2.tsx` and the look switcher. All of it is in
  the backup `C:\Users\mcbig\Documents\codes\bigh-archive\home-redesign-all-looks-2026-10-02.zip`.
- Kept: `chrome.tsx`, `content.ts`, `dialogs.tsx`, `reference/home-v2/ink/` (prompts, originals,
  plates, `build_assets.py`, `translations.cjs`), `reference/home-v2/r4/`, `hf_run.py`, `.impeccable/`.
- New words: ten strings (m575-m584: the four section labels, Dr. Liu's role, "20+ years", the
  mitochondrion's alt text, "Illustrations", "BiGH products", "Choose a story") added by
  `node reference/home-v2/ink/translations.cjs`. Their translations are DRAFTS, not native-reviewed.
- Checks: `python -X utf8 scripts/qa/qa_home_ink.py` (runs against `/` and `/kr`), `npm run build`.
- The brush line is drawn on desktop only; phones keep the opening's own line (lead's decision).

## Where

- Worktree `C:\Users\mcbig\Documents\codes\bigh-home`, branch `home-redesign` (from origin/main
  ee25ce5). Other sessions own the other worktrees; never touch them.
- Dev server: `http://localhost:3014` (English lives at `/`, Korean at `/kr`). Looks:
  `/?look=daylight`, `/?look=night`, `/?look=words`, and `/?look=current` = today's homepage.
  If the server is down (curl fails), start it once in the background:
  `npm --prefix C:/Users/mcbig/Documents/codes/bigh-home run dev -- --hostname localhost --port 3014`.
- Nothing is committed or pushed without Mo's yes. The GitHub repo is public.

## Shared pieces (do not edit; ask the lead if one must change)

| File                                     | What                                                                                                                                                          |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `src/components/home-v2/content.ts`      | Every accepted word on the homepage, per block, plus facts, products, stories, research, science topics. Use `copy()` on every string.                        |
| `src/components/home-v2/chrome.tsx`      | `HomeHeader` (props `overlay`, `tone`, `solidAfter`) and `HomeFooter`; same as About/Science. Tune with the look's CSS tokens.                                |
| `src/components/home-v2/dialogs.tsx`     | `useHomeDialogs()` → `openProduct(i)`, `openScientist()`, `openAsk()`, `openSupport()`, `openArticle(i)`.                                                     |
| `src/components/home/product-action.tsx` | `ProductAction`: NuriCell links to `/products/nuricell`, the rest open the product dialog. Every product picture and button must use it (Mo clicks pictures). |
| `src/components/home-v2/home-v2.tsx`     | Look picker. The switcher at the bottom is review-only.                                                                                                       |

Tokens every look sets on its root: `--ink --muted --paper --paper-deep --line --accent --gutter
--wide --display-font --sans --display-weight`. The header/footer/dialog read them
(`--chrome-bg --chrome-ink --chrome-line --footer-bg --footer-ink --footer-muted --footer-line
--dialog-bg --dialog-ink` override).

Blocks every look must carry, with these section ids: `top` (opening), `scientists`, `cellular`,
`products`, `stories`, `science`, `research`, `purpose`, then the footer. Order may change when the
story reads better, but every block's words and working controls stay: product selection, three
science topics (and the aging illustration's honesty label), research filters + show all, story
selection, the dialogs.

## Mo's rules (collected)

- **Timeline (timeline.com) is her number one reference**: calm, one short idea per screen,
  generous space, rounded full-bleed photography, the product inside the headline words (#006).
  Borrow the vibe, not the clothes.
- **Large navigation and labels for older readers** (#045): labels ≥ 15 px, body ≥ 18 px on
  desktop, buttons ≥ 48 px tall, good contrast. No tiny letter-spaced capitals.
- **Switzer everywhere** ("Swiss"), loaded in the locale layout. Display weight ~440–480,
  tight tracking (−0.02 to −0.035 em on big type), no italics, sentence-case labels. Mo called
  serif and Fraunces attempts "vibe coded".
- **Never paste flat vector shapes on a photoreal render** ("very fake"). Effects on a render
  are a second render or a shader on its own pixels.
- **No red dots, rust particle clusters or blobby glows** (they read as germs). Warm gold light
  and lime only.
- **No photo-real invented people for the customer stories**; stories use hands-only scenes,
  objects and the real bottles, labeled "Fictional sample" / "Illustrative photo".
- **Say "animal study", never "rats".** Keep the honesty lines: "Illustration, not a
  measurement" on the aging visual, the fictional-sample note, the research note, the footer note.
- **Credits:** NuriCell "Formulated by Dr. Jiankang Liu." Nature Calm: Dr. Liu and Dr. Iris Wang.
  Dr. Iris Wang: text only, never a photograph.
- **Mo's Design Vault picks for this build** (pulled to
  `C:\Users\mcbig\Documents\design-vault-pulls\2026-09-28-picked\`, read `notes.md`): #055 the
  "$10,000" hero (slow subtle text-free looping video on warm cream, big headline left, pill
  buttons, a stats card overlapping the hero), #046/#047 full-screen immersive heroes with one
  central object and a short key phrase, #054 one lively main subject, #006 the pill inside the
  headline words, #044 testimonials mixing media tiles and short quote cards, #005 scientists
  introduced simply, #013 footer with one clear slogan, #042 circles as a visual index.
- **Outside references studied** (screenshots in the lead's scratchpad `ref/`): Timeline home,
  Oura ("Subtle. Power." — a tiny product in a real landscape, huge centered words), Neko Health
  (pale calm world, big rounded image panels with tabbed text), NewLimit (Swiss rules, thin-line
  science diagrams), Altos Labs, Function Health, Eight Sleep, AG1, Seed.
- The site's own pages Mo likes set the bar: `/about` (Glass: paper, huge title, glass battery),
  `/science` (Scroll film: leaf under a lens, dive into the cell, dark cinematic), and
  `/products/nuricell` (Chapters: Big name with the bottle between "Nuri" and "Cell", dark bulb
  chapter, capsule cutaway, 3D bottle).

## The quality bar: 8.8 / 10

Score like a senior designer at a top studio, against Timeline, Oura and the site's own
Science/About/NuriCell pages. "Vibe coded" tells to hunt down: a generic hero with gradient blobs;
every section the same centered stack; cards-with-icons grids; tiny letter-spaced eyebrows
everywhere; inconsistent picture styles (the current page mixes a deep-space render, a studio
headshot, a cobalt still life and a lime block); AI-looking pictures (garbled text, warped
labels, extra fingers); too many words per screen; decoration without meaning; weak phone layout.

What earns it: one strong idea for the whole page; one art direction for every picture; confident
type scale with real contrast between sizes; rhythm (full-bleed moments between calm ones,
overlaps, alignment to one grid); motion that tells the story and is smooth at 60 fps; details
(hover states, focus rings, captions, image cropping) that feel finished; a phone layout designed,
not squeezed.

## Pictures and video

- Reuse approved assets where they fit: `public/images/products/*.png` (approved transparent
  bottles, Sept 18), `public/images/science/*` (glass cell, aged cell, lime droplet),
  `public/images/about/glass-battery-lifted.webp`, `public/images/science-page/*`,
  `public/media/hero/*` (deep-space motion Mo chose on Sept 22), `public/images/stories/v2/*`
  (still-life pieces, hands-only moments + loops), `public/images/jiankang-liu.jpg` (512×768, the
  only Dr. Liu photo; keep it small or soften it).
- New stills: Gemini (`mcp__gemini__gemini-generate-image`), one call at a time. Keep originals +
  the prompt in `reference/home-v2/<look>/originals/` with a `.json` sidecar; ship webp in
  `public/images/home-v2/<look>/` (≤ 2400 px wide, aim < 400 KB). Look at every result at 100 %
  and reject artifacts. Never generate product labels: composite the approved bottle PNGs.
- Video: prefer animating stills in code (depth parallax / light shader, like
  `src/components/about/look-glass-scene.ts` and `src/components/home/science-glass.tsx`). At most
  two generated clips per look (`mcp__gemini__gemini-generate-video`, no audio), encoded small with
  ffmpeg (H.264, ≤ 3 MB, a poster frame).

## Motion and performance

GSAP 3.15 (+ ScrollTrigger), Lenis, three r184 and motion are installed. Load heavy scene code
with a dynamic import inside an effect so each look pays only for itself. Respect
`prefers-reduced-motion` (a still, complete page). Phones: lighter scenes or stills. Traps: plain
object `fromTo` with x/y (use `.set` + `.to`); `html { scroll-behavior: smooth }` (the locale
layout sets `data-scroll-behavior`); a component that renders a still first and the moving version
later must mount the moving part as its own component; `scroll-padding-top: 150px`.

## Checks

- Static: `npx tsc --noEmit`, `npx eslint src/components/home-v2`, `npx prettier --check
src/components/home-v2` (LF files; Python writes need `newline="\n"`; never `git stash`).
- Browser: Playwright for Python with the real GPU
  (`--use-gl=angle --use-angle=d3d11 --enable-gpu --ignore-gpu-blocklist`). Each look gets
  `scripts/qa/qa_home_<look>.py <base>`: 200, no console errors, every block id present, header
  links, a dialog opens and closes, product/story/topic/filter controls work, no horizontal scroll
  at 390 px, every image loaded, label sizes ≥ 15 px. Pictures to `scripts/qa/out/home-<look>/`.
- Look at screenshots yourself: desktop 1440×900 and phone 390×844, viewport shots down the page
  (full-page shots break svh layouts), plus mid-motion frames. A helper:
  `python -X utf8 <scratchpad>/shoot.py URL OUTDIR [--w --h --step --max --wait --mobile]` and
  `sheet.py OUT.png COLS WIDTH imgs...` for contact sheets.
