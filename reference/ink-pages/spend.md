# Ink pages: picture spend

GPT Image 2.5 through `reference/home-v2/r4/hf_unquoted.py`, about $0.05 a picture (billed $0.07,
$0.02 refunded on reconcile). Check open.higgsfield.ai/billing for the real total.

## About redesign, "The name, on a folded letter" (Mo's $5, October 6, 2026)

Ledger: `C:/Users/mcbig/AppData/Local/HiggsfieldAPI/bigh-about-letter/ledger-nav-gpt.jsonl` (cap 30 jobs).
Mockup round before this plan: 13 jobs in `bigh-about2` (about $0.65).

| Job | Picture | Kept | Note |
| --- | ------- | ---- | ---- |
| word-v1 | The written name BiGH, gold dot (ref: ref-word.png) | yes | Same hand as the mockup, calmer; legible; round gold dot clear of the stem. Faint pale halos at stroke edges go white when the paper is divided out. |
| letter-b-v1 | Chapter letter B (ref) | yes | Clean B, one stroke each, dry brush only at the tail; no specks. |
| letter-i-v1 | Chapter letter i with gold dot (ref) | yes | Reads as an i (the mockup's blob is fixed): one long stroke, round torn-edge gold dot well above. Stem top is a flat, ragged brush entry. |
| letter-g-v1 | Chapter letter G (ref) | yes | Open bowl, firm bar, the word's down-stroke spur; calm. |
| letter-h-v1 | Chapter letter H (ref) | yes | Legible, crossbar past the right stroke. Weakest letter: blunt, frayed upright tops with a few tiny specks. Passes; not retaken. |
| band-v1 | Grey wash band under the opening | yes | Soft grey, both ends fade out, bloom edges top and bottom, no black. |
| pool-v1 | Pale pool behind Dr. Liu's photo | yes | Irregular blooms, no rim, darker lower left; median tone 220/255 after division. |
| rings-v1 | Tree rings, one gold ring | no | Hand-painted and 20+ rings, but the gold ring sits only ~3 rings in from the bark (brief: ~10). |
| rings-v2 | Retake: + "gold ring about halfway between bark and heart, about ten rings outside it" | yes | ~8-9 rings outside the gold, many inside; wavering, hand-painted; continuous thin gold leaf. |
| dots-v1 | Four watercolor dots | yes | Four separate dots, clearly deep, dark, mid, pale. |

10 jobs of the 30 cap, about $0.50 (at most $0.70 before refunds). 9 first takes + 1 retake.

## About B and C, built side by side (October 7, 2026)

Ledger: `C:/Users/mcbig/AppData/Local/HiggsfieldAPI/bigh-about-bc/` (this plan caps it at 30 jobs).
Mockup rounds before this plan: 7 jobs in `bigh-about2` (about $0.35).

| Job | Picture | Kept | Note |
| --- | ------- | ---- | ---- |
| book-v1 | Open book, gold-leaf ribbon (ref: ref-book.png) | yes | Reads at a glance; fanned pages, hinted lines of text (nothing legible), soft splash washes like the mockup; one torn-leaf gold ribbon over the gutter and past the edge; plain paper, no red. |
| seedling-v1 | Oak seedling, roots, gold-leaf acorn (ref: ref-seedling.png) | yes | Lobed oak leaves in grey wash, acorn on the stem as in the mockup, dotted soil line, fine roots; the gold acorn is crackled leaf among the roots; calm, plain paper. |
| desk-v1 | Desk: brush on rest, microscope, books (ref: ref-desk.png) | yes | Microscope entirely ink and grey wash, no brass or gold (gold pixels 0.003% after division); brush on its rest, three old books, soft splash washes; plain paper. Mottled wash on the metal is a little busy but matches the mockup. |
| sequoia-v1 | Giant sequoia trunk, sapling, misty trees, gold touch (ref: ref-sequoia.png) | no | Majestic and calm, gold leaf on the trunk, sapling beside it; but the trunk and crown wash run off the top edge (212 columns under 235 in row 0 after division): the crop would cut the tree and fail the white-edge check. |
| sequoia-v2 | Retake: + whole tree inside, crown fading out well below the top edge | no | Superseded by v3: its gold mask covered 0.04% of the picture (check floor 0.1%). Whole tree inside with paper above; trunk rises into a misty crown (reads as rising, not a stump, at full size); small torn gold leaf on the trunk; sapling and misty redwoods behind; calm. |
| palms-v1 | Two fan palms, gold sun, rolling hills (ref: ref-vignettes.png) | yes | One picture only (not the strip's four); two slender fan palms, crackled gold-leaf sun low beside them, low rolling hills touched with gold; no beach; quiet. |
| bee-v1 | Leafy branch, one bee (ref: ref-vignettes.png) | yes | Delicate grey-wash branch, one bee in flight; calm, plain paper. The bee has soft ochre stripes (paint, not leaf) as in the approved mockup; no gold leaf. |
| moon-v1 | Gold-leaf crescent, grey cloud (ref: ref-vignettes.png) | yes | Crackled gold-leaf crescent over a soft grey cloud wash; calm, centred, plain paper. |
| letter-v1 | Letter in an envelope, fountain pen (ref: ref-vignettes.png) | no | Reads well and calm, but adds gold the prompt never asked for (a gold-leaf wax seal on the envelope, gold bands on the pen) and leafy sprigs around it (no other objects). |
| letter-v2 | Retake: + no gold or colour, no seal, no plants | yes | Open envelope, letter half out, fountain pen across it, all grey ink (gold pixels 0.0); no seal, no plants; calm, plain paper. |
| lamp-v1 | Desk lamp, open journal, gold-leaf light, sprig (ref: ref-lamp.png) | yes | Close to the mockup: lamp bending over the journal, its light a pale pool of crackled gold leaf on the pages, sprig beside it, soft splash washes; calm, plain paper. |
| enso-v1 | Enso, gold touch at the start (ref: ref-enso.png) | no | Calm, real brushwork, but not one readable stroke: wet black on both sides of the gold (left and bottom) and dry over the top, its two ends overlapping at 3 o'clock instead of an open gap, so the page's clockwise sweep from the gold would paint it backwards; the gold (a crumpled leaf shape) sits on the black ink, where lifting it would smudge. |
| enso-v2 | Retake: + one clockwise pass from a wet head at 11 o'clock, gold on bare paper beside it, a clear gap | yes | One confident stroke, open (a clear gap at 12 o'clock between the dry tail and the wet head), small torn gold-leaf fleck on the paper at the head. The model still brushed it counter-clockwise (head at 12, down the left, dry up the right), so build_bc.py ships it mirrored left to right: the page's clockwise sweep from the gold then follows the brush, wet to dry. Gold ends up at 1 o'clock, not 11 as in the mockup. |
| hills-v1 | Band of low California hills, gold glow on one hilltop (ref: ref-hills.png) | yes | Low, rounded, layered hills in pale grey wash, both ends feathering out, a faint gold-leaf glow along the right hilltop; no peaks, trees or buildings; reads as rolling hills, not the homepage's mountains. |
| glasses-v1 | Round reading glasses on an open notebook, gold hinge (ref: ref-glasses.png) | yes | Close to the mockup: round frames resting on the notebook, pseudo-cursive grey strokes (nothing legible at full size), a small gold-leaf band at the hinge; calm, plain paper. |
| sequoia-v3 | Retake 2: + the gold a clearly visible torn patch about a fifth of the trunk's width | yes | Whole tree inside, misty crown, good bark; the leaf barely grew: its outline is 0.092% of the picture, so its gold mask (0.06%) still fails check_bc.py's 0.1% floor. Kept as the best take; no retakes left for it. |

16 jobs of the 30 cap, about $0.80 (at most $1.12 before refunds). 12 first takes + 4 retakes (sequoia x2, letter, enso). Style references cropped from the approved mockups as the plan says, then the page text ("What you can count on.", "Our p", "What our work is for.") and a stray seedling leaf were inpainted out of ref-vignettes, ref-sequoia and ref-hills so no take would copy them.

## NuriCell ink page (October 9, 2026)

Ledger: `C:/Users/mcbig/AppData/Local/HiggsfieldAPI/bigh-nuricell-mock/` (cap 70). Mockup rounds 1-11:
65 jobs (about $3.25, at most $4.55 before refunds), Mo's $5. Kept mockup paintings (finals):
P7-capsule, P7-stepping-books, P11-liu-face-bold (Dr. Liu, from his real photo; Mo's call, October 9),
P7-egg-capsules, P7-sum, P5-stroke.

| Job              | Picture                                                 | Kept | Note           |
| ---------------- | ------------------------------------------------------- | ---- | -------------- |
| lantern-lit-v1   | Lantern lit by gold leaf (ref: crane-rest-v2 brushwork) | no   | One tall lantern hanging from an ink cord that reaches the top edge; rims are loose dry-brush ink, ribs fine grey lines, body crackled gold leaf glowing rim to rim with a soft gold haze on the paper; no landscape or other objects, paper on every side. The body is more detailed and symmetrical than the crane (reads as ink-and-gold watercolour, not a few loose strokes), but it is plainly painted, not rendered. Not chosen: the retake (v2) is the looser painting; kept on disk as a spare. |
| lantern-unlit-v1 | Edit of the lit take: unlit, no gold                    | no   | Same lantern in the same place (shift 0 px down, 1 px sideways against the lit take), cord, rims, ribs and leaf crackle kept as pale cool-grey wash; zero gold or warm haze left (gold pixels 0.0%); the paper is a hair cooler than the lit take (R 241 vs 245); worth watching in Task 2's crossfade. Not chosen with its lit take; kept on disk as a spare. |
| lantern-lit-v2   | Retake of the lit take: loose body (ref: crane-rest-v2 brushwork) | yes | One lantern, cord to the top edge, a short knot at the top rim; bold dry-brush rims, body a few broad wet strokes of gold-leaf wash with uneven ragged sides, only six hand-brushed grey ribs (not parallel, slightly tilted), crackle only hinted, soft gold haze; no landscape or other objects, paper on every side (about 525 px left and right, 190 px below). Clearly looser than v1; the glow is still strong and steady (row-to-row brightness std 9.5 vs 12.3 for v1), slightly less saturated than v1 (warmth 115 vs 126) and the haze a little fainter. |
| lantern-unlit-v2 | Edit of lit-v2: unlit, no gold (same prompt as v1) | yes | Same lantern in the same place (shift 0 px down, 1 px sideways against lit-v2), brushy rims, six loose ribs and mottled wash kept as pale cool-grey; gold pixels 0.0%, no warm haze; reads as a real ink wash. The paper is a hair cooler than the lit take (R 241.5 vs 245.8), as in v1. |

Choice: the v2 pair (`gpt25-lantern-lit-v2.png` and `gpt25-lantern-unlit-v2.png`). Looks like a loose ink painting first (v1's 13 even ribs and uniform crackle read as a detailed illustration), strong steady glow second (v2 holds it, a little paler), register third (a tie: 0 px and 1 px for both pairs). All four originals are kept.

4 jobs, about $0.20 (at most $0.28 before refunds): 2 first takes + 1 retake pair (lit-v2, unlit-v2). Ledger after: 69 of 70.
