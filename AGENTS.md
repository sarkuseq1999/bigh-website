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
- **One part at a time** (Mo, October 28, 2026: "the quality really kind of matters. We should
  not rush it"). When several parts need redesigning, mock up one part on the real page, show
  it, discuss it with Mo, build it, and only then start the next. Don't bundle parts.

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
  ingredients, the books running in from the page edge, Dr. Liu right, the redwood round right
  (October 27, 2026; it replaced the brushed 3 × 30 = 90), the bottle left. Phones keep one
  column. NuriCell only for now
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
- **NuriCell research: tap a book, read its study (Mo picked A, October 26, 2026).** Mo asked for
  the research list to be more fun to read and found the small "The research" label over its
  heading strange. Each of the seven books in the painting is a button: tap one and its study
  opens, its book stays dark and the other books fade under a little paper (pointing at a book
  previews it). Each study is a plain question with a short, honest answer (animal studies say
  rats or animals first); the two 2003 reviews share one question, "Scientists disagree", and
  light two books. No label over the heading, no "Show all"; without scripts every answer shows.
  `nuricell-research.tsx`; masks `books-mask-v1-*.png` from `reference/ink-pages/nuricell/find_books.py`.
  Mockups: `reference/ink-pages/mockups/nuricell-research/`.
- **NuriCell "What's inside": moving gold, a tidier top, the pairs as scenes (Mo picked 1A,
  October 26, 2026).** Mo liked the plate's layout but wanted the gold to move, found the small
  grey "What's inside" label odd and the three grey notes under the plate messy, and the
  "Why these four work together" columns dull. The gold leaf now rises out of the powder and
  settles where it is painted, then each flake keeps turning slowly, catching the light like
  real gold leaf (picked over a never-ending updraft). The label is gone (the heading says it);
  "per serving of 3 capsules" sits right under the heading (the heading says "every capsule",
  the amounts are for 3); the other ingredients are one label card; the research note is said
  once, at the chapter's end. The pairs became three little scenes (picked over a scroll story
  and a pick-a-partner game); their powder heaps were replaced on October 27 (next rule).
  NuriCell only (`nuricell-leaf.tsx`; pictures `build_nuricell_gold.py`). Mockups:
  `reference/ink-pages/mockups/nuricell-inside/`.
- **NuriCell pairs: on the ranch, no powder (Mo picked B, October 27, 2026).** Mo found the
  pairs' white powder heaps with gold on top "a little strange, like drugs". Of three painted
  ideas (A two hands passing gold leaf, B an old California ranch, C a gold trail map with four
  camps) he picked B. Each pair is a Codex painting of two ranch things that need each other,
  gold marking the energy: firewood and the stove with a gold fire (acetyl-L-carnitine +
  alpha-lipoic acid, painted flipped so the wood comes first), the windmill pouring gold water
  into its tank (alpha-lipoic acid + creatine), the Pony Express rider and his horse with a gold
  letter (choline + acetyl-L-carnitine). The pair's names sit under each painting; the words
  are unchanged. Each plays once as it comes into view (Play again replays it): the light runs
  up the fire, the wheel turns once while the water pours and light spreads across the tank,
  the light crosses the letter. Gold behaves like gold leaf (no glow, no sparkle). No powder,
  pills, capsules, tins or lab glass in these paintings: anything that could read as drugs.
  The wheel turns over Codex's painting of the same scene without it. NuriCell only
  (`nuricell-scenes.tsx`, `nuricell-pairs.ts`; pictures
  `reference/ink-pages/nuricell-pairs/build_nuricell_pairs.py`). Mockups:
  `reference/ink-pages/mockups/nuricell-pairs/`.
- **NuriCell chapter 6: "The same formula for about 20 years" (Mo picked 2, October 27, 2026).**
  Mo found "How to take it" (the egg cup and the brushed 3 × 30 = 90) strange, then found "3
  capsules a day" too thin for a chapter: the buy box right under it and the first question say
  it too. Of round 3's two ideas (1 a painted California day with a line per moment, 2 the
  formula's years) he picked 2: the cut end of a young California redwood (a Codex painting), the
  ring about 20 rings in from the bark laid in gold leaf (with the kit's light mask). The heading
  "The same formula for about 20 years.", a lead in ink ("Dr. Liu chose its four nutrients. We
  haven't changed them since.") and a note naming the four. No label, no sum; from 960px the
  words left and the round right, phones the round over its words. "About 20 years" is Mo's
  "almost 20-something years"; no start year is on file, and Mo put it live with "about 20 years"
  (October 28). If a real start year turns up, change the words (m962-m964) to match. NuriCell only
  (`daily.tsx` `story`, `nuricell.ts`); OPC and Turmerific keep the sum. Picture `rings()` in
  `build_nuricell.py`; mockups `reference/ink-pages/mockups/nuricell-daily/` (round3).
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
- **NuriCell opening: "A clear day" (Mo picked A, November 10, 2026; live the same day, `main`
  `4d846c7`).** Mo asked again for a better first screen for NuriCell (the 18
  ideas of October 23-24 were all turned down). Three ideas were mocked on the real page, each
  keeping the big "Nuri [bottle] Cell" he had asked to keep and giving the bottle a world to stand
  in: A a clear day (a painting), B blue and gold (one blue brush stroke behind the name, a strip of
  gold leaf under the bottle), C morning shade (an oak branch's shadow, no paint). He picked A: one
  loose ink-and-wash painting behind the name and the bottle, a clear California morning sky over
  the Pacific and a low grassy bluff with a few poppies and two stones. From 960px the name sits on
  the horizon and the real bottle stands on the bluff; in one column the bottle stands on the bluff
  under the name. As the page opens the morning fog lifts, once (reduced motion: no fog). The words
  and the buy box stay on bare paper under the grass. The painting fills the window's width at
  every size (two side pieces join it in a window wider than 1600px). Paint the coast loosely: ink
  brush first, light washes, small poppies as single dabs (the first take, flat washes and big
  poppies, read as a greeting card). No words about fog or a clear head near it: the lifting fog
  must never become a promise ("clears brain fog"). NuriCell only: Advanced OPC, Turmerific and
  Nature Calm keep the plain opening, Green Bee Propolis its own. `nuricell-opening.tsx`,
  `nuricell.module.css`, `opening.tsx`; picture `reference/ink-pages/nuricell/build_nuricell_opening.py`
  (a Codex painting, `paint_opening.sh`); mockups `reference/ink-pages/mockups/nuricell-opening/round6/`.
- **About, "Our purpose" and the circle (October 19, 2026).** Mo found the seedling too slight for
  the purpose and its mission line too small to read. He picked a big painted valley oak (a rope
  swing above the ground, a gold light in the roots you can't see); it stands larger than the
  page's other paintings on purpose (repainted in soft colour, with people, on November 10:
  "About 'Our purpose'" below). The mission line sits a step under the heading, in ink, not
  the grey body size. Later the same day Mo found the opening circle "too round, not artistic
  enough" and the spark of gold light that ran round it "fake". He picked circle A, "heavy to
  dry" (a wet, heavy start that thins into dry streaks and lifts before it closes), and the gold
  leaf floating down onto it like a real flake, settling, then catching the light. Gold leaf
  behaves like real gold: no glow, no spark, no twinkling stars, never red. On October 26 Mo
  found that leaf's fall and shine cartoonish and picked A of three ideas: no gold on the circle
  at all (the opening's gold is the sunlit hilltop below it), over the hilltop warming to gold
  and a still leaf. He also found the circle too small on a big screen ("not immersive enough").
  Of two bigger layouts built on the real page he picked A: the circle fills the first screen
  and the title is written inside it (on a phone the lead sits under it), over B, a bigger
  circle with the words under it, which hardly grew on a short laptop. Mockups:
  `reference/ink-pages/mockups/about-circle-size/`. (The circle left the page on October 28:
  next rule.)
- **About opening: the poppy meadow, thinning into the paper (Mo picked A, then A, October
  27-28, 2026).** The big circle reminded Mo of the film The Ring ("a little scary"). Of three
  painted ideas (A a poppy superbloom, B a morning walk, C the name painted) he compared A and B
  on the live site and picked A: golden California hills in spring poppies fill the first screen,
  the words in the painting's empty sky, the poppies' gold arriving from the foot of the screen
  as the page opens (gold leaf: no glow, no shine). He then found the first screen and Our purpose
  "don't transition well" (the painting stopped in a straight line on its biggest poppies) and
  picked A of two painted ends over B, morning fog: below the first screen the meadow thins out,
  fewer and smaller poppies, a few last ones and dry grass, then bare paper, then the oak. Never
  end the meadow in a straight line or a gradient fade. The painting's paper is cut to
  transparency (no multiply). `meadow.module.css`, `meadow-art.ts`; pictures
  `reference/ink-pages/about-opening/build_about_opening.py` (Codex painting plus Codex's
  continuation of its foot, `join_foot.py`). Mockups: `reference/ink-pages/mockups/about-opening/`
  and `about-opening-join/`.
- **About "Our purpose": the oak on a sunny afternoon (Mo picked A, November 10, 2026; live the
  same day).** Mo found the purpose's oak "a little dark or
  scary": black ink right after the sunny meadow, bare roots hanging in empty paper, and an empty
  swing (the words say "a full life", and nobody was in the picture). Of three painted ideas on the
  real page (A the same oak on a sunny afternoon, B Monterey Bay above and below the water, a
  gold-leaf kelp forest under a sea otter, C a San Francisco cable car over its hidden gold cable)
  he picked A: the valley oak in the soft colour of the valley at dawn, a child on the swing, a
  grandmother pushing, a dog and a picnic, the roots inside a slice of warm earth, a patch of gold
  leaf among them. A picture of a full life has people in it. Never an empty swing, bare roots
  hanging in empty paper, or black ink here. It still stands larger than the page's other
  paintings. Its gold leaf is plain gold at rest: the kit's band of light crosses it only as the
  painting comes up (on the kit's own range the band stood on the patch when the painting was
  centred and washed it pale, like a hole in the paint). `purpose-art.ts`, `about-ink.tsx`,
  `circle.module.css`; picture `reference/ink-pages/about-purpose/build_about_purpose.py` (Codex
  painting `oak-1-b`, `paint.sh`); mockups `reference/ink-pages/mockups/about-purpose/`.
- **About "Our ingredients": the globe (Mo picked A, the map, November 6, then B, the globe,
  November 9, 2026; on the draft branch `about-chapters`, not live).** Mo liked the idea of "Each
  plant, from where it grows best." but not its first design (four specimens beside a two-by-two
  key). He picked a painted world map with each plant at its place and gold trails home to
  California, then said not to name places at all (he is still finding out where the pine bark
  and grape seed come from): the part should only give the feeling that each plant comes from the
  region of the world best for its natural growth. Of two no-place designs (A the same map, the
  plants in the seas; B a globe) he picked B: a painted globe over the real land, California
  facing you, the four plants standing just past its rim all round it, and a trail of gold-leaf
  dabs from each over the globe to California, laid one plant after another, once, as it comes
  into view. Each plant carries the kind of place it thrives in ("Sunny slopes"), never a
  country. On phones the trails start at the globe's rim and the plants are listed under it.
  `plants-map.tsx`; pictures `reference/ink-pages/about-plants/` (`render_globe.py`, `globe-1-a`);
  mockups `reference/ink-pages/mockups/about-plants/` (`no-places/`).
- **About "Proudly made in California.": the valley at dawn (Mo picked F, November 9, 2026; on
  the draft branch `about-chapters`, not live).** Mo did not want the five bottles in the draft's
  painting ("I'd rather not have the product bottle there"). Of five no-bottle ideas on the real
  page (A a fruit-crate label, B a record book written in as you scroll, C California painted
  over its outline, D a clipboard ticked in gold on a sunlit wall, F the Central Valley at dawn;
  a Gold Rush pan was tried and dropped) he picked F: one painting across the chapter, the
  Central Valley in first light with some fields in gold leaf, the heading in its empty sky and
  the three GMP rules in a row under it. "Made in California" goes back into the promise list.
  `made-mockups.tsx` (`ValleyIdea`); pictures `reference/ink-pages/about-made/` (`valley-1-b`);
  mockups `reference/ink-pages/mockups/about-made/`.
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
- **Footer: two California quail by the park sign (Mo picked A1, November 3, 2026).** On
  October 26 Mo asked for better ideas for "Stay sharp. Live fully." and its crane and picked B,
  "end of the trail" (pose C): the painting leaves the promise and stands in the grass at the FDA
  park sign's right, looking at the sign's California poppy; the promise stands alone, a size
  smaller. On November 3 the red-crowned crane there read as Chinese, like the opening's crane
  and the old close's cranes. Of three California animals (A California quail, the state bird; B
  a desert tortoise; C a black bear cub) he picked A, then asked for the quail "a little more
  painting like" and picked A1 of two looser takes (A2 ink and wash): two quail painted in a few
  wet washes in the opening hummingbird's hand, no outlines, one keeping watch, the other bending
  toward the poppy. A painting with its own thin colour, the same on every page (no tinted twin).
  On phones the sign narrows for it (seven lines at 390 px, about seven under 390) and the quail
  stay inside the column. The homepage's brush line still ends as a stroke under the words.
  `closing-quail.tsx`, `ink.module.css` (`.look .rest`), `fda-statement.tsx`; picture
  `reference/ink-pages/footer-crane/build_footer_quail.py` (Codex paintings, `paint.sh`).
  Mockups: `reference/ink-pages/mockups/footer-crane/` (`animals/` for the quail).
- **Phone menu's foot: the hummingbird at a California fuchsia (Mo picked E, November 3,
  2026).** The crane at rest at the foot of the phone and tablet menu (the footer's old finale in
  miniature) was the last crane on the site. Of five ideas put into the real menu (A one quail, B
  the footer's two quail, C poppies; then, on "Can we try with the hummingbird?", D Allen's
  perched on a twig and E the homepage's own bird at a California fuchsia) he picked E, then
  found its beating wings "annoying, like flys" at the menu's size: here the wings never beat.
  They rest on their first frame, raised as painted (the homepage's rest with reduced motion),
  baked with the body into one picture. The bird is the homepage's own, never redrawn; only the
  fuchsia is a new painting (Codex), its coral calmed so the bird leads. No brush stroke under it
  (one cut through the grass like a bar). Its room keeps the crane's: on phones a set size from
  the window's height (130-230px), on tablets the room left under the words. The homepage's
  opening bird beats its wings only as it arrives (November 4). `nav-inscription.tsx` (`.sheetBird`, `useBirdRoom`),
  picture `menu-hummingbird-v1.webp` from `reference/ink-pages/menu-finale/build_menu_finale.py`;
  mockups `reference/ink-pages/mockups/menu-finale/`.
- **Homepage opening: giant sequoias and a hummingbird (Mo picked, October 28, 2026).** Mo's
  colleagues loved the opening's watercolour and gold sun but said the whole read as
  Chinese, "made in China": the misty peaks with pines and the red-crowned crane. Of California
  scenes painted on the real page (A Big Sur sunset, B golden hills, C Yosemite) Mo asked how a
  scene relates to "Good health starts with your cells." and picked D: a grove of giant sequoias
  (they live more than 3,000 years) in the morning sun, the sun in a clearing beside one giant
  trunk, the gold sun the same gold as "cells.". The crane goes: of three birds he picked Anna's
  hummingbird (California's year-round hummingbird; for its size it burns energy faster than
  almost any animal, its flight muscles packed with mitochondria) over a golden eagle and a grey
  sandhill crane. Keep the stroke that leaves the bird and runs down the page (Mo likes it).
  **First screen only** (Mo, October 28): the crane stayed below it at first; the closing
  painting's cranes left on November 2 ("Homepage close", below), the footer's crane and the
  phone menu's on November 3 ("Footer: two California quail" and "Phone menu's foot", above).
  No crane is left on the site. Built: the painting covers the whole opening
  (`opening-sequoias-v1.webp`), the sun in the clearing (at most 1000 px into the column), the
  hummingbird in the crane's frame (Anna's as a still until October 29, below), the line pinned
  to the painting's forest floor (`opening-land`, `ground()` in `brush-route.ts`). Then Mo found
  the desktop sun "a little too big or too close to the tree" and picked A of three placements
  (A smaller, same spot; B smaller in the clearing's middle; C low behind the firs): the desktop
  sun is three quarters of its size (218 comp px), shrunk about its own centre; phones keep
  theirs. Mockups `reference/ink-pages/mockups/home-sun/`.
  **The bird: Allen's, painted loose, wings beating as it arrives (Mo, October 29 and November
  4).** Mo asked for other
  hummingbirds and wings "always moving", like a dragonfly's. Of today's Anna's, a green female
  Anna's and Allen's (copper, like the redwood bark; it nests almost only on the California
  coast) he picked Allen's, then asked for it "more painting-like" and picked C, painted in a
  few wet washes in the old crane's hand (fresh Codex paintings: edits of a detailed bird keep
  its speckle), then found the beak "too realistic": the beak is one dry grey brush stroke, no
  shine. Its orange is calmed toward the redwood's copper so the gold sun leads. The wings are
  its own painted wings, lifted out and beaten about the shoulder, six blurred frames a beat at
  ten beats a second (`hummingbird-v2-near/-far.webp`, `build_wings.py`), the far wing behind
  the body; paused once the opening leaves the window, resting raised with reduced motion. On
  November 4 Mo found the non-stop beat "a little annoying", like a fly (as in the phone menu the
  day before), and picked A of three (A beat as it arrives, then rest; B short bursts; C always
  still): the wings beat at full speed for 3 s while the bird blooms in, slow over three beats,
  then rest on their first frame, raised as painted. Never a beat that runs on. The
  bird is lined up on the first hummingbird's bill and tail, so the line still leaves from under
  its tail. Mockups `reference/ink-pages/mockups/home-bird/`.
  `opening-crane.tsx`, `opening.module.css`; pictures `build_home_opening.py` in
  `reference/ink-pages/home-california/` (README); mockups
  `reference/ink-pages/mockups/home-california/`.
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
  `reference/ink-pages/mockups/science-path/2026-10-26/`. (Round 3 below changed the order and
  the paintings; the path's one place per screen stays.)
- **Science round 3: start with the science, then the scientist (Mo, November 4, 2026; built
  for his critique, which kept the page as built; live November 6, `main` `8b422fa`).** Mo: the design was good but "the way I put it together
  could be better"; start broader, with what kind of science BiGH focuses on (cell science) and
  the reason behind it; keep the water paint but shift from Asian to California. He then gave
  Claude the whole job ("do the best you can ... I will come and critique"), so no options were
  mocked; the built page is the proposal. Order: the opening "Our science starts in the cell."
  (the two questions, how cells make energy and what changes with age, naming Dr. Liu on the
  first screen; a desk at an open window over golden hills, a brass microscope on it); "Why start
  with the cell?" (about 37 trillion cells, each making its own energy: San Francisco's houses at
  dusk whose windows light a few at a time in gold leaf, once, as it arrives; three numbered lines
  opening the existing explainer sheets; it keeps the `#health` address the footer links to);
  Dr. Liu; his path (Berkeley with the Okayama doctorate in its words, Salzburg, Today: Okayama's
  castle read as Asian); "Every formula has a scientist behind it."; "Read the research
  yourself." (bound journals on a library table, three open); Ask BiGH Science (camp mugs on a
  redwood picnic table). No labels over headings. Gone: the scrolls, the balanced stones and oil
  lamp, the tea-set mugs, "Make sense of the science." (the homepage's own heading). Every
  painting is Codex ink and wash, painted loose (the tidy first takes read as illustrations).
  Spec `docs/superpowers/specs/2026-11-04-science-california-design.md`; pictures
  `reference/ink-pages/science/` (README, `build_science.py`, `paint.sh`).
  November 6: Mo kept the opening line ("Our science starts in the cell.") and asked for other
  pictures for "Why start with the cell?" to compare. Shown on the real page, each lighting in
  gold leaf a piece at a time: A the town (as built), B monarchs wintering at Pacific Grove (each
  warms its own flight muscles before it can fly; Claude's pick), C a Sacramento Valley sunflower
  field at sunrise. A microscope view of cheek cells was tried and left out (the gold cells looked
  like chips). Mo picked A, the town stays. He also left the formulas' row of five bottles as it
  is ("Every formula has a scientist behind it."). Mockups `reference/ink-pages/mockups/science-why/`;
  the unused takes are in `bigh-archive\science-why-unused-2026-11-06\`.
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
- **Homepage "Tiny power plants.": the mitochondrion in softer ink (Mo picked B, November 4,
  2026).** Mo loves the cell's design, but its heavy black and blue-grey ink no longer fitted the
  page once the opening turned California and colourful. Of two recolourings of the same painting,
  every stroke kept (A California colour: a redwood copper skin, pale sage inside; B softer ink),
  compared live as test pages `/home-a` and `/home-b`, he picked B: the ink a third lighter and
  warmed to sepia, the blackest strokes a deep warm brown-grey. The gold folds are unchanged (the
  gold layer). Its own colour, so no green-spring tint. Keep the design; change only the paint.
  `mito-soft-v1.webp` from `reference/ink-pages/home-mito/build_mito_colour.py` (`softer`);
  `assets.ts` `mito`, `cellular.tsx`. Mockups: `reference/ink-pages/mockups/home-mito/`.
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
- **Homepage "Good questions": a country mailbox (Mo picked A, October 30, 2026).** The inkstone
  and brush read as Chinese. Of three California pictures on the real page (A a country mailbox, B
  a Gold Rush pan and pick, C a naturalist's notebook) Mo picked A: the rounded rural mailbox on its
  post, its raised flag in gold leaf, poppies and dry grass at its foot, in a few wet washes. You
  send a question, an answer comes back. Same small size and centred pause as before; the words
  and button did not change. The switched-off Science drop-down carries it too. `mailbox-v1.webp`,
  `build_home_ask.py` in `reference/ink-pages/home-ask/`; mockups
  `reference/ink-pages/mockups/home-ask/`.
- **Homepage "In their own words.": breakfast on the back porch (Mo picked A, November 6,
  2026).** The three sample stories' still lifes were painted as East Asian ink still
  lifes (plum blossom in a narrow vase, tea bowls, a low table, a sliced pear) and read as Asian.
  Of two California mornings on the real page (A the back porch, B the kitchen table with a lemon
  tree in the window) Mo picked A: coffee in an enamel mug, orange juice, a bowl of oranges,
  poppies in a jam jar, a brown paper lunch bag and the car keys on a weathered porch table, golden
  hills and a valley oak beyond. Ink and thin watercolour in the mailbox's and the Big Sur close's
  hand, its own colour (no green-spring twin). Michael's and Susan's stories follow on the same
  porch (dusk with a book and reading glasses; a piece of honeycomb and a sprig of the Brazilian
  shrub). The real bottle stays out of the paintings (it read as an ad in a customer's story). The
  paintings are framed whole, and from 900px the window's edge falls at 6% of the painting (it was
  14%), so nothing in it is cut in half. `story-porch-{morning,dusk,afternoon}-v1.webp` from
  `build_home_stories.py` in `reference/ink-pages/home-stories/` (`paint.sh`, `shoot_stories.py`);
  `assets.ts` `storyPaintings`, `stories.module.css`. Mockups
  `reference/ink-pages/mockups/home-stories/`.
- **Homepage close: the long view down the Big Sur coast, in ink and wash (Mo picked 1B,
  November 2, 2026).** "Our purpose is simple." sat over an old pine on its rock, misty peaks and
  two red-crowned cranes: Chinese. Of three California endings on the real page (A Big Sur at
  evening, B an evening walk on a golden ridge, C a surfer at low tide) Mo tried A and B live as
  test pages, then found the walk with people "doesn't give the vibe of California" (bare golden
  hills could be anywhere). Of three Californian walks (1 on the Big Sur coast, 2 among a valley
  oak and poppies, which echoed About, 3 under palms) he picked 1 and put it live, then found it
  "a little bit simple" next to the old pine painting ("that one looks really good, like a
  picture"). Of three richer Big Sur paintings he tried 1 (the long view with Bixby Bridge) and 3
  (McWay Falls) live and found them "more picture like": photos with a watercolour filter. Of the
  same two places painted loosely (A a loose watercolour, B ink and wash) he picked 1B: an older
  couple and their dog on the cliff-top trail, headland after headland fading down the coast,
  Bixby Bridge small in the haze, drawn with an ink brush and light colour laid over it, the old
  pine painting's way of painting. Richness comes from brushwork and ink, never from photographic
  detail. Morning sequoias to evening coast, one full day. The sun is the opening's own gold leaf
  set on the horizon at the head of the glitter; five brown pelicans fly in where the cranes flew.
  The painting is 2:1 (at the old 7:3 the land rose into the words); on phones the frame is 150%
  of the window from 22.5% across, so the walkers and the whole sun both show. `purpose.tsx`,
  `purpose.module.css`; pictures `build_home_purpose.py` (`ink-long`) in
  `reference/ink-pages/home-purpose/`; mockups `reference/ink-pages/mockups/home-purpose/` (round 4).
- **Homepage "Small beginnings. Bigger possibilities.": the title face, all ink (Mo picked B,
  November 9, 2026).** The line under the Big Sur close is a `<p>`, so the homepage's title face
  (Ysabeau, given to h1-h3) never reached it: it read as heavy Switzer with a grey second line,
  the page's only one, like a leftover. Of two looks on the real page (A the title face with the
  grey second line, B both lines in ink) Mo picked B. The words did not change. Any display line
  that is not a heading takes `font-family: var(--display-font)` itself. `purpose.module.css`
  (`.graphic`); mockups `reference/ink-pages/mockups/home-graphic/`.
- **Product questions: a painting for each answer (Mo picked A, October 26, 2026).** Mo found the
  questions part plain ("more fun, better to look at"; the words stay) and picked A, "a picture for
  each question", over B (one breakfast-table painting with numbered marks). All five product
  pages: from 960px the questions on the left and the picked one's painting and answer on the
  right, the first picked as the page opens, the menu bar's pale wash behind it and a round "+" on
  the others; on a phone each question opens in place with its painting. Every painting shows its
  own answer and is true to the label (the right number of capsules, their colour, 30 squares a
  month); all are 3:2, so the answers line up. `questions.tsx`; paintings and their build script
  `reference/ink-pages/questions/`; mockups `reference/ink-pages/mockups/nuricell-questions/`.
- **Science opening: one slow zoom, from a walker to one cell (Mo picked it, November 9, 2026;
  live the same day, `main` `552f28c`).** Mo found round 3's first screen plain and boring (a small painting boxed
  on one side, small black words, nothing moving, the word "cell" beside a desk), and doubted that
  the town at dusk "correlates to the topic" (it only made sense after its caption). Of three
  ideas for the opening (A the same window filling the screen, B a zoom, C one big cell) with
  three for "Why start with the cell?" (1 lead with the number, 2 the cell as a map of the three
  lines, 3 the zoom lands on the cell) he took B with 3, saw a sample, and said "Yes, build it".
  A walker on golden California hills fills the first screen, the h1 in the painting's sky,
  "cell." in the homepage's gold leaf. As the page scrolls the view moves in on the walker's hand
  in the dry grass, then on one cell of it, where "Why start with the cell?" and its lead stand;
  the three numbered lines follow below. The cell is a loose wet wash with a dark blue nucleus,
  its mitochondria about twenty-five slender slivers of gold, and a line under it says so ("In
  gold: its mitochondria, where the cell makes most of its energy."). The first cell came out as a
  schoolbook diagram with fat gold beans that read as peanuts, and the first hand as a realistic
  illustration (knuckles, nails): never those; paint both loose. The gold is flat like leaf: no
  glow. The stage is pinned while its track (4.4 windows) scrolls; reduced motion and no script
  get no pinning, the hills then the cell beside its words. The desk at the window and the town
  with its lamps are gone (their originals stay). `#health` now stands at the zoom's last view.
  Keep in mind Mo's October 21 note on the homepage (a hiker with a round window into a cell was
  "hard to relate to", the cell "a ball with worms in it"): here the hand is the step between,
  and the heading beside the cell names it. `zoom.tsx`, `zoom.module.css`, `why.tsx` (the lines);
  pictures `zoom()` in `build_science.py` (Codex paintings, `prompts/zoom-*.txt`); mockup
  `reference/ink-pages/mockups/science-zoom/`.
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
