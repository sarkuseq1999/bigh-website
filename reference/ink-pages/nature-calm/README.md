# Nature Calm in Ink & Gold

October 16, 2026. Branch `nature-calm-ink` (worktree `codes/bigh-nature-calm-ink`), from `origin/main`
934d313. NuriCell's ink template (`docs/superpowers/specs/2026-10-09-nuricell-ink-design.md`) with
Nature Calm's own paintings in every chapter and its own signature moment in "Why it matters".

## Mo's picks (October 16: "All A")

| Chapter        | Painting                                                                                        | Take(s)                                  |
| -------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------------- |
| Opening        | The real bottle between "Nature" and "Calm" (the name set to fit; phones stack it)              | (no painting)                            |
| Why it matters | **Still water.** A lake ruffled by wind, its gold reflection scattered; as you arrive the water stills and the light gathers into one line (the lantern's cross-fade, this painting's own meaning) | `why-water-still` (lit), `why-water-ripple` (unlit, its edit) |
| What's inside  | A sugar pine cone: many scales, one calm natural form; three beads of gold resin                 | `inside-cone`                            |
| The research   | The Big Dipper: seven gold stars over one dark ridge (seven studies, the stars you steer by)     | `research-stars-v2` (v1's stars too small) |
| The people     | Dr. Liu: NuriCell's painting of him, reused (Mo's A; nothing new generated)                     | (NuriCell's `liu-v1`)                    |
| How to take it | A glass of water, three capsules, the moon's phases above, the full moon in gold (one bottle, one month); no painted sum (3 × 30 = 90 is NuriCell's) | `daily-moon`                             |
| Buy            | The real bottle standing between lavender rows (a California farm), stalks in front of its foot | `buy-lavender`                           |

Round 1 also painted, not chosen: `why-storm-clear` + `why-storm-dark` (an oak, the storm passes),
`inside-cairn`, `research-lighthouse`, `daily-plate`, `buy-beach`, `buy-oak`, `research-stars` (v1).
Their originals (54 MB) are kept out of the public repo in
`codes/bigh-archive/nature-calm-ink-unused-originals-2026-10-16/`; `originals/` holds the six takes the page
uses. Capsules are painted pale (their real colour unconfirmed).

## Rules learned on the way

- A **pale wash dies on the page**: the still lake's water is only 7% darker than its paper, and
  once divided out and multiplied onto the page it vanished (the "after" read as a gold line hanging
  from a hill). The build deepens the wash on both Why layers equally and keeps the whole sheet; the
  standard paper lift (220/245) is replaced by a gentle one (200/252) for wash paintings.
- The kit's **gold detector takes browns and ochres for gold** (the pine cone's scales, an ochre
  hill): the leaf on these takes sits at hue 38-60, so a stricter detector cuts the masks.
- The dev server caches optimized pictures by URL (`.next/dev/cache/images`): a rebuilt file under
  the same name is served stale until that folder is cleared (or the name versioned).
- With the bottle at NuriCell's size (90% of the scene's width) the glass itself is 47% of it: a
  scene must keep its subject at the sides, the foot and above the cap. The lavender rows do.

## Files

- `hf_nature_calm.py`: GPT Image 2.5 jobs (ledger `%LOCALAPPDATA%/HiggsfieldAPI/bigh-nature-calm-ink`,
  cap 42 jobs; Mo's $3). Prompts in `prompts/` (`_style.txt` + `_<name>.txt` → `<name>.txt`; edits
  carry no style preamble and take the painting they edit as their reference).
- `build_nature_calm.py`: originals → `public/images/products/nature-calm/ink/` and
  `src/components/product/ink/nature-calm-art.ts`.
- `translations-nature-calm.cjs`: draft translations m780-m784 (not native-reviewed).
- QA: `scripts/qa/qa_nature_calm_ink.py`.
