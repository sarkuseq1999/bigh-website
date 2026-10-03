# Homepage redesign, round 2 (September 29, 2026)

Read `docs/home-redesign.md` first: everything there still applies (where things are, shared
files you must not edit, Mo's rules, checks) unless this page says otherwise.

## What Mo said about round 1

"Those designs are mostly using what we already have ... re-organize them ... What I actually
wanted is to use design reference from me, but also from other sources, other websites ... make
me something stunning, great design, great look and feel. Let's not use anything that we currently
have ... generate images, make videos ... I need this home page to pop, show me what you are
capable of." Then: "this time I want you to get at least a 9 out of 10 ... screenshot to check it
and to grade it."

## What changes

- **The bar is 9.0 / 10**, overall and for the opening; no block under 8.7. Scored like a senior
  designer at a top studio, from your own screenshots (desktop 1440×900 and 1280×720, phone
  390×844, mid-motion frames), against the references below. The lead re-scores from his own
  screenshots and sends work back until it is really there. Don't report early.
- **No existing site imagery.** Do not use the current homepage, About, Science or product-page
  pictures, renders or videos (`public/images/**`, `public/media/**`, including the glass cell,
  deep-space cell, story stills and loops, and the round-1 look assets). Do not import round-1 look
  code or `home/science-glass.tsx`. Every picture and motion is new, made for your look.
- **Kept (they are facts, not design):** the approved product bottle PNGs in
  `public/images/products/*.png` (never generate a bottle or a label; composite these), the BiGH
  logo (through the shared header/footer), Dr. Jiankang Liu's only photo
  `public/images/jiankang-liu.jpg` (512×768; you may present it any way that keeps it sharp and
  true to him), and every word in `content.ts`. The shared header/footer/dialogs stay.
- The science block still needs the three topics and the aging honesty label
  ("Illustration, not a measurement"); build your own version of it in your look's world.
- **Type**: Switzer stays the brand face (Mo's pick) but use it with far more range: size
  contrast, weight contrast (Switzer has thin to black), confident tracking. Labels ≥ 15 px, body ≥
  18 px, nav as shared.

## References to study (screenshots in the lead's scratchpad `ref/`)

`ext2_a.png`, `ext2_b.png` (new: Superpower's portrait against a huge warm sun; Prenuvo's people +
neon machine; Tally Health's people holding giant bright capsules; Rhode; Ultrahuman's product on
a plinth; Isomorphic Labs' pastel glass sculpture; Calico; Graza's bold color; Apple's product
film; Awwwards picks; Igloo), `ext_timeline.png`, `ext_neko.png`, `ext_bio.png` (Oura, NewLimit,
Altos, AG1), `ext_eight_fn.png`, and Mo's Design Vault pulls
(`C:\Users\mcbig\Documents\design-vault-pulls\2026-09-28-picked\`, esp. #046/#047 full-screen
immersive heroes, #054 "lively, fun, alive" main subject, #055 the "$10,000" hero, #006 object in
the headline, #044 testimonials with media). Open the live sites too (Playwright) when a motion
matters: superpower.com, tallyhealth.com, isomorphiclabs.com, ouraring.com, timeline.com.

## Making pictures and video

- Stills: `mcp__gemini__gemini-generate-image` (Google's newest image model, 2K/4K). ONE call at a
  time across the whole team: if a call fails with "fetch failed" or a rate error, wait 30 s and
  retry once. Write prompts like a photographer's brief (lens, light, film stock, composition).
  Don't ask for "empty space on the left for text" — it paints a blank panel; describe where the
  subject sits instead. Inspect every result at 100 %: reject AI tells (hands, teeth, text, warped
  objects, plastic skin, repeated patterns). Keep originals + prompt `.json` in
  `reference/home-v2/<look>/originals/`; ship webp in `public/images/home-v2/<look>/`
  (≤ 2400 px, aim < 350 KB), made by a script in `reference/home-v2/<look>/`.
- Bottles in scenes: generate the scene with a clear, lit, empty spot (a plinth, a ledge, a sunlit
  table, a hand-sized clearing) matching the bottles' soft front light, then composite the real PNG
  with a contact shadow, ambient occlusion and a colour match (Pillow or CSS). Never generate text
  or packaging.
- People: lifestyle scenes may show generated people (mid-life and older, real-looking, never
  glamour); keep faces natural, avoid close-up hands. Never pair a generated person with a
  testimonial quote: the stories stay hands/objects/scenes + "Fictional sample". Footer already says
  lifestyle imagery is illustrative.
- Video: `mcp__gemini__gemini-generate-video` is Veo 2 (text only, 720p, ~8 s, about $2.80 a clip).
  At most TWO clips per look, only for atmosphere (water, light, leaves, sky, abstract light) where
  the exact subject doesn't matter; poll with `gemini-check-video`; encode H.264 ≤ 3 MB with a
  poster. Most motion should be code: depth parallax on stills (make a depth map), light shaders,
  masks, scroll-linked camera moves, WebGL. Log every paid call (what, cost) in
  `reference/home-v2/<look>/spend.md`. Look budget: about $12 total (images + video).
- No red/rust dot clusters or blobby glows (they read as germs); no flat vector shapes pasted on
  photoreal pictures.

## Ownership

Only create/edit `src/components/home-v2/look-<look>/**`, `public/images/home-v2/<look>/**`,
`public/media/home-v2/<look>/**`, `reference/home-v2/<look>/**`, `scripts/qa/qa_home_<look>.py`.
Same dev server `http://localhost:3014/?look=<look>`. Keep files compiling. Pass dialog tokens with
`:global(body):has(.look)`. No commits, no new npm packages (ask the lead; three, gsap, lenis and
motion are installed).

## Update (September 29, later): generation moves to Higgsfield

Gemini hit Mo's monthly spending cap: do not call `gemini-generate-image` or
`gemini-generate-video` again. Mo gave **$15 for the whole round** on Higgsfield. Use ONLY the
wrapper `reference/home-v2/hf_run.py` (it quotes the live price first, refuses anything over the
per-job cap, your look's $4.50 budget or the $13.50 round budget, runs one job at a time across
all looks, downloads to `reference/home-v2/<look>/originals/`, writes a `.json` sidecar and logs
`spend.md`). Never call the Higgsfield helper directly; never try GPT Image 2.5 (no up-front price).

```bash
# stills (photo-real people and scenes; best value)
python -X utf8 reference/home-v2/hf_run.py image --look <look> --name <name>   --model higgsfield-ai/soul/v2/standard --aspect 16:9 --prompt "..."          # $0.004
# other still models: alibaba/qwen-image-3/text-to-image ($0.04; --resolution 2k $0.075),
# xai/grok-imagine-image-2.0 ($0.06–0.08), ideogram/v4.0 ($0.06), z-image/turbo ($0.015)
# animate one of your stills (5 s, no sound)
python -X utf8 reference/home-v2/hf_run.py video --look <look> --name <name>   --image reference/home-v2/<look>/originals/<still>.png --prompt "..." --duration 5  # ~$0.23
python -X utf8 reference/home-v2/hf_run.py ledger     # spent so far
python -X utf8 reference/home-v2/hf_run.py resume --receipt <receipt.json>  # finish a timed-out job
```

Jobs can wait 10–15 minutes in Higgsfield's queue: run them in the background and keep building.
Soul 2 aspect ratios: 16:9, 9:16, 4:3, 3:4, 1:1, 2:3, 3:2. Soul 2 is superb at photo-real people
and light (the lead's test: `reference/home-v2/sunrise/originals/lead-test-soul2.png`, a silver-haired
woman in profile against a huge sun). Look at every result at 100 % and reject AI tells. Video:
prompt calm, subtle motion ("gentle breeze in hair, sun shimmer, slow push in, subject still"),
then encode H.264 ≤ 3 MB with ffmpeg and a poster; loop it cleanly (crossfade the ends).
