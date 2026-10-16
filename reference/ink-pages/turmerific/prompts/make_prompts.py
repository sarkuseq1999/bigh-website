"""Writes Turmerific's painting prompts: `_<name>.txt` holds the subject, `<name>.txt` the full prompt
(the shared style first). Run from anywhere: python -X utf8 reference/ink-pages/turmerific/prompts/make_prompts.py
"""

from pathlib import Path

HERE = Path(__file__).parent


def write(name, text):
    (HERE / name).write_text(text.strip() + "\n", encoding="utf-8", newline="\n")


STYLE = (HERE / "_style.txt").read_text(encoding="utf-8").strip()

# Ink paintings (sumi ink, gold leaf only where stated).
INK = {
    "why-soak-lit": (
        "A short, knobbly piece of fresh turmeric root lying on its side on the left of the middle, its thin skin a few "
        "dry-brush strokes of warm brown-grey ink with the faint rings of the root, its freshly cut end facing us. In "
        "front of it, a little to the right and lower, lies one round slice cut from the root, flat on the paper, seen a "
        "little from above: a ragged ring of brown-grey skin around a cut face of bright, real gold leaf. From that "
        "slice, the gold has soaked out into the rice paper: a large, soft watercolour bloom of warm golden-ochre wash "
        "and gold leaf spreading outward through the paper's fibres around and below the slice, its edges feathered and "
        "irregular like wet watercolour bleeding into absorbent paper, a slightly darker golden rim where the wet edge "
        "dried, fading to pale gold and then to bare paper. The root's own cut end is gold leaf too. The bloom covers "
        "about half of the picture. Nothing else. Calm, warm, luminous."
    ),
    "why-drops-lit": (
        "A short, knobbly piece of fresh turmeric root lying diagonally in the lower left, its thin skin a few dry-brush "
        "strokes of warm brown-grey ink with the faint rings of the root, its freshly cut end pointing up and to the "
        "right, the cut face bright, real gold leaf. From that cut end, a long, gentle, curving trail of many tiny round "
        "droplets of real gold leaf drifts upward and to the right across the paper, like a slow stream of tiny golden "
        "beads: close together and a little larger near the root, then smaller, sparser and fainter as they travel "
        "toward the upper right corner. Each droplet a single small round dab of gold, some with a faint golden halo "
        "where it touched the wet paper. Nothing else. Calm, light, luminous."
    ),
    "inside-scoop": (
        "A small, simple wooden spoon lying on the paper, its handle reaching to the lower left, painted in a few warm "
        "grey-brown strokes. Its bowl is heaped with fine golden curcumin powder, painted as soft, granular washes of "
        "golden ochre with real gold leaf catching the light on top, and a little powder has spilled from it in a soft, "
        "fine trail on the paper in front. Beside the spoon on the right, lying on the same level, two "
        "dietary-supplement capsules side by side: small, smooth, elongated oblong pills, each made of two rounded "
        "halves that meet in the middle, like vitamin capsules, never coffee pods; translucent warm golden-yellow, with "
        "a fine grey outline and a small soft shadow. Nothing else. Simple, quiet, precious. The powder is fine and "
        "golden, never brown, never like dirt or soil."
    ),
    "research-glasses": (
        "An open notebook lying flat, seen from a little above, its two pages a slightly lighter shape of paper with "
        "soft grey edges and a soft grey fold in the middle, filling most of the picture. On the pages, a few rows of "
        "loose, faint grey brush marks only suggest handwriting: nothing legible, no letters, no numbers. A pair of "
        "folded reading glasses rests on the right page, painted in a few confident dark strokes for the frames and "
        "pale grey washes for the lenses. One long, slender turmeric leaf (lance-shaped, with fine parallel veins) lies "
        "across the left page as a bookmark, in soft grey-green wash. No gold. Calm, thoughtful, unhurried."
    ),
    "daily-glass": (
        "A simple, clear drinking glass of water standing upright, seen from the front at table height, painted in a "
        "few confident grey strokes for its rim and sides, the water a pale, cool grey-blue wash with a bright "
        "highlight left as bare paper and a soft shadow on the paper. In front of the glass, a little to the right, "
        "lying on the same level, exactly two dietary-supplement capsules side by side: small, smooth, elongated oblong "
        "pills, each made of two rounded halves that meet in the middle, like vitamin capsules, never coffee pods; "
        "translucent warm golden-yellow in a soft wash with a touch of real gold leaf, a fine grey outline and a small "
        "soft shadow. Nothing else: no plate, no food, no table. Quiet morning calm. The capsules are the only gold."
    ),
}
for name, body in INK.items():
    write(f"_{name}.txt", body)
    write(f"{name}.txt", STYLE + "\n\n" + body)

# The painted sum: a row of numbers, so no "fills the picture" line and numbers allowed.
SUM_STYLE = STYLE.replace(
    " The subject fills most of the picture (about 85% of its height and width): bold, generous, never small in the "
    "middle of empty paper.",
    "",
).replace("no text, no letters, no numbers, ", "no text, no letters, ")
SUM = (
    "Brush calligraphy of numbers only, written in one row across the middle of the paper in sumi ink by a master's "
    "steady, controlled hand: the number 2, then a small multiplication sign (×), then the number 30, then a small "
    "equals sign (=), then the number 60. It reads exactly: 2 × 30 = 60. Leave clear space between every numeral "
    "and sign; nothing touches. Each numeral bold, refined and perfectly legible (clear Western numerals, never "
    "stylised into other shapes), with wet strokes and a little dry-brush at the ends; the two signs smaller and "
    "lighter. Nothing else on the paper: no other characters, no words, no gold."
)
write("_daily-sum.txt", SUM)
write("daily-sum.txt", SUM_STYLE + "\n\n" + SUM)

# Buy scenes: soft watercolour colour allowed; an empty space where the real bottle will stand.
COLOR_STYLE = (
    "A loose watercolour and ink painting on one plain sheet of warm, light rice paper with fine fibres, seen flat, "
    "evenly lit, no frame, no table, no text, no letters, no numbers, no signature, no red seal, no stamp. It must look "
    "hand-painted, expressive and artistic, with the confident, loose brushwork of the reference picture (copy only its "
    "brushwork, never its subject: no bird, no crane, no reeds, no water): wet washes bleeding softly into the paper, "
    "dry-brush where the brush runs out, simplified forms that suggest rather than describe, lots of white paper. "
    "Never a photograph, never a 3D render, never a detailed botanical illustration. Soft, transparent colour only "
    "where stated; everything else sumi ink from deep black to pale grey washes, plus real gold leaf only where "
    "stated. Only the things named below are painted: no buildings, no people, no animals, no extra objects."
)
write("_style-color.txt", COLOR_STYLE)
BUY = {
    "buy-plant": (
        "A turmeric plant in flower, painted large. From the lower left and lower right, its long, broad, lance-shaped "
        "leaves rise and arch outward in a loose fan, in fresh sage-green and soft grey-green washes with darker ink "
        "strokes for the midribs, some leaves overlapping, their tips curving gently. Rising from the back on the "
        "right, above the leaves, one turmeric flower spike: a soft cone of overlapping pale green bracts that turn a "
        "delicate rose pink toward the top, with a few small pale yellow flowers peeking out between the lower bracts. "
        "At the foot of the plant, a soft, pale grey wash shadow on the ground across the lower part of the picture. In "
        "the middle of the lower half, between the leaves, an EMPTY space of plain paper, about a third of the picture "
        "wide and half of its height tall, where an object will stand later: nothing is painted there except the soft "
        "ground wash at its bottom; no pot, no vase, no bottle, no jar. A few fallen round slices of turmeric root, "
        "their cut faces real gold leaf, lie on the ground wash at the front, either side of that empty space. Fresh, "
        "calm, generous."
    ),
    "buy-california": (
        "California golden hills in the late afternoon. Soft, rolling hills of dry golden grass fill the lower half, "
        "painted in warm ochre and pale gold washes with darker ink strokes along their curves, a little real gold leaf "
        "where the low sun catches the grass on the ridges. On a far ridge on the left, one lone valley oak with a "
        "broad, rounded crown in loose dark ink strokes, small in the distance. Above, a pale, warm sky of bare paper "
        "with the faintest wash. In the foreground across the bottom, a few tall blades of golden grass in quick "
        "strokes, and a soft pale ground wash. In the middle of the lower half, an EMPTY space of plain paper and soft "
        "ground wash, about a third of the picture wide and half of its height tall, where an object will stand later: "
        "nothing is painted there; no tree, no rock, no bottle, no jar, no post. Wide, warm, quiet."
    ),
}
for name, body in BUY.items():
    write(f"_{name}.txt", body)
    write(f"{name}.txt", COLOR_STYLE + "\n\n" + body)

# The unlit Why takes are edits of the lit ones, so the two stay in register.
write(
    "why-soak-unlit.txt",
    "Edit the reference painting. Keep everything exactly as it is: the same piece of turmeric root and the same round "
    "slice in the same places, the same brushwork, the same warm rice paper, the same framing and size. Change only "
    "this: take away all the gold. The cut end of the root and the cut face of the slice become pale, plain cream "
    "paper with a faint grey wash, and the large golden watercolour bloom around and below the slice is gone "
    "completely: plain, clean rice paper there. No gold, no yellow, no ochre anywhere.",
)
write(
    "why-drops-unlit.txt",
    "Edit the reference painting. Keep everything exactly as it is: the same piece of turmeric root in the same place, "
    "the same brushwork, the same warm rice paper, the same framing and size. Change only this: take away all the "
    "gold. The root's cut end becomes pale, plain cream paper with a faint grey wash, and every one of the tiny golden "
    "droplets is gone completely: plain, clean rice paper where they were. No gold, no yellow, no ochre anywhere.",
)

if __name__ == "__main__":
    print(sorted(p.name for p in HERE.glob("*.txt")))
