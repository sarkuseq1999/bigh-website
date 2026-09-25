# "Make sense of the science." — design rounds (September 24, 2026)

After Mo accepted Still life for the customer stories ("okay for this section; we'll polish later"), she asked to work on the next section. Her approved homepage plan (September 21, BRAND-CHEATSHEET.md) puts **education** after the customer stories, then a closing invitation. The section sits directly after the stories and replaces the older "Stay curious." preview. That preview's markup is saved in `reference/science-section/2026-09-24-previous-learn-section.tsx.txt`, and its styles are still in `homepage.module.css`.

The older research list ("Curiosity, with references.") and the "Our purpose is simple." block are not in Mo's approved plan. They remain below the new section because the menu links point to them (`#research`, `#about`). Mo agreed the eight-section flow; moving the two blocks to the Science and About pages still needs her yes.

All looks use Mo's accepted copy: the headline, the introduction, three article titles with their previews, and "Explore the science" (it scrolls to the research list for now). The full articles are not written yet, so each article opens the existing short explainer dialog. New design lines (analogies, short facts, sentences with objects, chapter names, labels) are drafts, and their translations are drafts too.

## Decision and refinement (September 24): the Glass cell

**Mo chose round 2's Glass cell.** She said "the 3D mitochondria is really pretty, very, very well done," and asked for two things. Visitors must always know which topic they are on (1 mitochondria, 2 free radicals, 3 aging cells). Each topic's picture should match its topic more closely. The review bar is gone, and the section always shows the Glass cell (`science-glass.tsx`). Kitchen table and Picture words are kept in `reference/science-section/round-2/` with their images.

- **Topic tabs** sit at the top of the sticky stage: **1 Mitochondria · 2 Free radicals · 3 Aging cells**. The current tab is filled, a slim meter shows the progress, and tapping a tab jumps to its topic. On phones only the current tab shows its name.
- **1 Mitochondria:** gold energy packets travel out of the glass along dotted streams, like power leaving a power plant. A pinned label points to the folds: "Inner folds: where energy is made."
- **2 Free radicals** (third version, September 24, after Mo sent a screenshot of the white vector stars on the render: "This looks very fake, not good at all"): nothing is pasted on top of the render any more. The whole scene is drawn _inside_ the glass by the WebGL shader, so it shares the render's light, and it plays as a loop with a step caption under the cell:
  1. "Making energy also makes a few free radicals": embers, each a white-hot core in a deep-orange rim with a warm bloom, appear at the golden folds and drift a little. The glass wavers slightly around each one (a small refraction).
  2. "Too many can damage the cell, starting with the mitochondria": one ember drifts to the lower wall, flashes, and a rust-brown burn with a ragged edge blooms in the glass.
  3. "Antioxidants keep them in balance": three antioxidant droplets, a second GPT Image 2.5 render of pale lime glass on a transparent ground (`reference/science-section/originals/sci3-droplet.png`), glide from the clear ends of the cell and catch the remaining embers, one of them just short of the wall. Each catch is a soft lime ring. The burn then fades (the cell repairs) and the droplets drift back.

  Labels read "Free radicals" (with a leader to where the embers start) and "Antioxidants". The side facts stay: "Mitochondria are one of the main sources of free radicals", "Your body also makes its own antioxidants" and "More antioxidants are not automatically better". On phones the caption replaces the side list.

- **3 Aging cells:** the **age slider** from 20 to 80 (drag it, use the arrow keys, or sweep a mouse over it; the first visit demonstrates it once, 20→45) now turns the young render into a second render of the _same_ cell grown old (`reference/science-section/originals/sci3-aged.png`, generated from the young one as a reference, so it lines up within a pixel): the glass frosted and crazed, the folds fewer and thinner, the gold faded to a dusty amber-grey, dark specks of oxidation inside. The shader blends the two in a straight line from 20 to 80, each patch of the glass a little ahead or behind on a soft noise, so every year changes something and nothing is fully old before 80; from 60 to 80 the whole cell dims and cools a little further, so 80 reads as gone where 60 still keeps some gold. (The first version of this blend finished early, and Mo saw the same dead look from 60 to 80.) The energy flowing out (topic 1's streams) slows and dims with age, and the halo fades. The caption reads "Drag to change the age · Illustration, not a measurement." The dotted rings of time are gone.

Why the earlier versions looked fake: flat vector shapes (stars, circles, a brown blob) on a photoreal render read as stickers, whatever their motion. Anything that shares the picture must be lit like the picture, so the effects are now either a second render in the same style (droplets, the aged cell) or changes to the render's own pixels (embers, burn, patina).

Is one mitochondrion right for all three topics? Mo asked twice ("the free radical doesn't work with mitochondria or work with something else?"), and yes, it is. Free radicals are mostly _made by_ mitochondria while they make energy, and they damage the mitochondria first (their membranes and their own DNA), then other parts of the cell; antioxidants, made by the body and partly from food, neutralize them. It makes one connected story:

1. Mitochondria make most of the cell's usable energy.
2. Doing that also makes reactive oxygen species (a kind of free radical). Mitochondria are one of their main sources, and cells' antioxidant defenses keep them in balance.
3. Declining mitochondrial function is one of the recognized hallmarks of aging (the Cell reviews already cited in the research list).

Honest limits, both already in the copy: free radicals also come from elsewhere, and aging has many causes. The aging picture is labeled an illustration.

The new strings come from `reference/science-section/translations-glass.cjs` and `translations-glass2.cjs` (drafts). Checks: type-check, ESLint, Prettier and Impeccable's detector (0 findings) pass. 21 of 21 checks passed locally and again on the public demo, in English and Korean at 1440 and 390 wide:

- topics 1-2-3 on scroll, each with the matching tab and picture;
- the slider's first-visit demo, the End key (age 80, fully aged glow) and dragging back to 20;
- the free-radical scene lighting steps 1, 2 and 3;
- tab jumps and each topic's explainer;
- reduced motion;
- no sideways scroll and no errors.

Third version checks (September 24): type-check, ESLint, Prettier and Impeccable's detector pass; 21 of 21 checks passed locally and on the public demo (`bigh-website-b4jkeuau4-sarkuseq1999s-projects.vercel.app`), in English and Korean at 1440 and 390 wide. Phone fit was measured at 360 x 700 and 390 x 844 in English and Korean: the caption and the slider now sit in room reserved under the cell (a longer step 2 had run into the title), the slider's hint wraps inside its column (it had widened the column and pushed the input and the "80" tick off screen), and on short screens the cell gives up width so topic 3 fits one screen. Higgsfield plan credits: 11.75 spent (aged render 9, droplet 2.75), 37 left.

Mo's second round of notes (September 24, evening): 60 and 80 looked the same, fixed as above; and "why is Explore the science so far down?": the sticky stage was a full-screen box, so on a tall screen the closing button came a screen's worth of paper below the last words. The stage now ends where its words end, and the button follows about 80 px after them. The stage still sticks for the whole track.

Bugs caught during the build:

- a bare `[data-scorch]` selector that CSS Modules rejected, which broke the page (static checks passed, but the browser check caught it);
- gold sparks invisible against the gold folds;
- catch rings rendering in the corner before their moment, because `fromTo` only animates the end values it is given;
- the "80" tick wrapping in Korean.

- WebGL is ready.
- Scrolling moves through topics 1, 2 and 3, each with its matching tab and picture, and the age reaches 80.
- Tabs jump to a topic and back.
- The topic's explainer opens and closes.
- Reduced motion shows the still cell and all three topics.
- There is no sideways scroll and there are no errors.

One Korean fix was made on the way: the "80" tick wrapped onto two lines.

## Round 2 — the three looks compared (`?science=1`, `2`, `3`)

Mo called round 1 "plain" and "vibe coded" and asked for stunning options, using any tool (GSAP, three.js). Mid-build she named **Timeline** (timeline.com) as her favorite overall design, to be used as a reference. Timeline's science page was studied on September 24 (screenshots in the session, not saved to the repo). Its moves are one short idea per screen, full-bleed rounded photography with focus changes on scroll, a centered translucent "battery" with a small list beside it, and the product set inside headline words. The looks borrow the vibe, not the clothes: BiGH's palette and Instrument Serif stay.

1. **Glass cell** (`science-glass.tsx`, three.js + GSAP ScrollTrigger). The layout follows Timeline's "cellular batteries" frame. A mitochondrion rendered as warm-gold glass stays centered while three chapters scroll past (sticky stage, 340svh track). Each chapter has a three-line fact list beside the cell, and the article title, preview and link below it.
   - The WebGL shader gives the still render real depth: a depth map (`glass-cell-depth.png`, a smooth dome built from the silhouette) shifts nearer parts as the cell turns toward the pointer, or sways on its own. It also makes the golden folds breathe.
   - Chapter 2 sends gold sparks out, each caught by a lime ring (free radicals and defenses). Chapter 3 ripples rings of time.
   - The render's white ground multiplies into the paper. The shader and the WebP both clip near-white to pure white, so no box shows.
   - The rail jumps between chapters. With reduced motion or no WebGL, the still image and all three chapters show in order.
2. **Kitchen table** (`science-table.tsx`, GSAP ScrollTrigger). The layout follows Timeline's science story. One sunlit overhead photo fills the screen, with a thin margin and rounded corners. As you scroll, the camera glides from the bulb to the apple halves and lemon, then to the tree-ring board.
   - Focus follows the subject: a pre-blurred copy of the photo (`kitchen-table-soft.webp`) is masked around the subject, so the frame softens while the camera travels and sharpens on arrival.
   - Morning light drifts over the table.
   - One sentence at a time sits centered on a paper wash above the subject: the analogy, then the article title as a link, then the preview.
   - Labels ("Air only", "With lemon juice", "One ring a year") are pinned to the photo.
   - On phones the photo becomes a band under the words, so nothing is cropped off.
3. **Picture words** (`science-words.tsx`, GSAP ScrollTrigger). The layout follows Timeline's "supplement [pill] that changes how cells age" headline, which Mo saved as Design Vault #006. The real objects sit inside large centered sentences: "Your cells run on tiny [bulb] power plants." · "A cut apple [apple] browns in the air. / A squeeze of lemon [lemon] slows it down." · "Like the rings of a tree, [tree slice] your cells change with time."
   - Scrolling pops each object in. The bulb switches on, the apple browns, and the tree slice turns. The lemon sways gently.
   - Pointing at an object shows a round close-up (the macro photos) that follows the pointer.

Round-2 images are GPT Image 2.5 on Mo's Higgsfield plan (35 credits; 48.75 left, the plan ends September 27):

- the glass cell (2k max);
- the overhead table (21:9, 4k max);
- four macro close-ups (2k high).

Picture words reuses round 1's cut-outs. A Seedance loop of the glass cell was refused as "nsfw", a false positive, and the credits were refunded. The cell is animated in code instead, which is also sharper than a 720p video. Originals and prompt sidecars are in `reference/science-section/originals/` (`sci2-*`). The strings come from `reference/science-section/translations-round2.cjs`.

Verification:

- Type-check, ESLint, Prettier and Impeccable's detector (0 findings) pass.
- The same 29 checks passed on the local server and again on the public demo, in English and Korean at 1440 and 390 wide:
  - Glass cell: WebGL is ready, chapters change 0→1→2 on scroll, the three facts show, and the rail jumps.
  - Kitchen table: the camera moves, chapters change, and each chapter shows only its own labels.
  - Picture words: the bulb is on and the apple browned after scrolling, and the close-up shows on hover.
  - Every explainer link opens and closes.
  - Reduced motion shows all three chapters, with no WebGL.
  - There is no sideways scroll and there are no errors.
- Screenshots were inspected at each step. Fixes during the build:
  - the cell was too orange, with a faint box around it;
  - the cell's box collapsed to zero width;
  - on desktop, the camera couldn't center the bulb, so focus landed on the apples (focus now follows the subject);
  - apples were cropped on phones;
  - link arrows wrapped awkwardly;
  - the preview covered the words.

## Round 1 — declined ("plain, vibe coded")

Kitchen science (objects that changed as you scrolled, in rounded panels), Myth or fact (a three-card flip game), and Chat (BiGH answering like a message thread). The code and images are kept in `reference/science-section/round-1/`. The round-1 strings remain in the catalogs because Picture words and Kitchen table reuse several of them. The cut-outs (bulb, apple, lemon, tree slice) were reused in round 2. It verified at 30 of 30 checks before being declined. Mo's reason was the look, not function.
