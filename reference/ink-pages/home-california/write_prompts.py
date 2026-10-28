"""Write the Codex picture orders for the California homepage opening ideas (October 28, 2026).

Mo's colleagues found the homepage opening lovely but Chinese-feeling (misty peaks with pines, the
red-crowned crane). Three California scenes keep the gold sun, the watercolour and the layout:
A Big Sur sunset, B golden hills, C Yosemite; and the crane becomes a sandhill crane.

Take 1 of each scene gets the live opening attached as a guide to the hand and colours; take 2
paints from words alone. One .txt per picture in prompts/, named as the picture. The attached
pictures are made here too, into plates/refs/ (git-ignored): the live green-spring landscape set
where it sits in the opening on a 3:2 sheet, and the live crane's original.

    python -X utf8 reference/ink-pages/home-california/write_prompts.py
"""

from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PROMPTS = HERE / "prompts"
REFS = HERE / "plates" / "refs"
STYLE = (PROMPTS / "_style.txt").read_text(encoding="utf-8")

REF = (
    "ATTACHED: our current opening painting. Copy ONLY its hand and colours (the soft wet "
    "watercolour, pale blue-grey far, sage green near, lots of bare paper and mist) and its "
    "layout (scene on the right, bare paper on the left). Do NOT copy its mountains or its pine "
    "trees: paint a completely different place, described below.\n\n"
)

SCENES = {
    "big-sur": """THE PLACE: California's Big Sur coast in the late afternoon, looking along the coast.
- The open Pacific Ocean fills the left and middle: one long, flat, calm sea horizon across the picture at about 40% down. The sea is only a few soft horizontal strokes of pale blue-grey near the horizon that fade to bare paper toward the bottom left.
- Directly below the sun's spot (about 69% across), a narrow path of warm sunlight on the water: pale warm gold-ochre watercolour broken by small horizontal gaps of paper, running from the horizon down toward us and fading out.
- On the RIGHT: the Big Sur coast. Several headlands step away into the distance one behind the other, the far ones pale blue-grey in sea haze (the farthest reaching to about 75% across), the nearest a big cliff of sage-green coastal scrub and golden dry grass filling the lower right corner, white surf as bare paper at its foot.
- Highway 1: a thin pale road cut into the side of the near headland, curving along the cliff, crossing a canyon on a small, elegant, single open-arch concrete bridge (like Bixby Creek Bridge), seen small at middle right.
- No trees at all.""",
    "golden-hills": """THE PLACE: California's golden summer foothills in the late afternoon.
- The hills are soft, low and rounded, rolling (never steep or pointed), covered in dry golden grass painted in pale, muted straw-ochre washes (not bright yellow), with soft sage-green shadows in the folds.
- Far: two pale blue-grey ranges of low, rounded hills along the horizon at about 40% down, across the full width.
- On the RIGHT: nearer rolling hills, the nearest filling the lower right corner. On the near hill stands one big, old, spreading valley oak: a wide, dark, rounded crown much wider than it is tall, dark sage and ink, on a short stout trunk, its shadow pooled on the grass. Two or three small oaks dotted on the farther hills.
- A few weathered wooden ranch fence posts with a sagging wire run along the near hill.
- Toward the left the hills sink, flatten and pale out into bare paper.""",
    "yosemite": """THE PLACE: Yosemite Valley in California's Sierra Nevada, early morning.
- On the RIGHT: El Capitan, a huge sheer wall of smooth pale-grey granite with a rounded top, rising straight up from the valley floor (a smooth monolith, not jagged).
- Farther away, at about 60-70% across, just below the sun's spot: the unmistakable silhouette of Half Dome, a rounded granite dome with one side sliced off flat and vertical, pale blue-grey in the distance.
- A thin ribbon waterfall (Bridalveil Fall) drops down a cliff at the far right.
- The valley floor at the lower right: dark green forest of tall straight conifers (sugar pines and incense cedars: tall narrow spires, never twisted pines), with low morning mist lying in the valley between the trees.
- Toward the left the valley fades into pale mist and bare paper.""",
}

# D (October 28, Mo picked "2" after asking how a scene relates to "Good health starts with your
# cells."): giant sequoias, which live more than 3,000 years, in the morning sun: long life, and
# energy starting rather than ending (A's Pacific sun can only be a setting one). The trunks must
# rise out of the picture to read as giants, so this one is painted as the whole first screen,
# not as the landscape band: it says where the sun, the bird and the words go.
GROVE = """THE PLACE: a grove of giant sequoias in California's Sierra Nevada, early on a clear morning.

COMPOSITION (the picture is the whole first screen of a website, edge to edge):
- On the RIGHT, from about 80% across to the right edge: two or three enormous giant sequoia trunks, straight and massive, with deeply furrowed, fluted cinnamon-brown bark, rising from the forest floor at the bottom edge and running up out of the top of the picture. The nearest trunk is very wide (about 12% of the picture's width). Their first branches are very high; toward the top of the picture the trunks fade into bright morning haze, so the top 15% is nearly bare.
- Lower down, from about 50% to 80% across and below 50% down: the forest floor at the grove's edge, low and soft: green ferns, a few small young conifers, a fallen log, in pale morning mist, fading out toward the left.
- Soft, very pale shafts of warm morning light slant down from the upper left into the grove between the trunks.
- The sky, from 20% to 80% across and from the top down to about 48%, stays open pale paper: a gold sun will be placed at about 70% across and 30% down, and a flying bird at about 25-50% across and 20-40% down. Keep those places clear: no trunks, no branches there.
- Everything left of 48% across and below 48% down stays bare paper (big words will be set there), with at most a very faint wash.
- The bottom edge fades softly into bare paper.

STYLE:
A loose watercolour-and-ink painting on plain warm white paper, wide format (landscape, 3:2, 1536 x 1024). The hand of a quick, confident watercolour: wet soft edges, colour bleeding into the paper, a few dry-brush streaks, very few strokes and lots of bare paper. Soft, calm colours: the sequoia bark a muted cinnamon-brown (never bright red or orange), sage and fern greens, pale blue-grey shadows, a warm morning haze; dark ink only in a few small accents. The more it looks like a painting, the better. Not photo-real, not a detailed drawing, not a storybook illustration.

It is an American, California scene in the spirit of the California plein-air watercolour painters, NOT an Asian ink painting: no misty pointed peaks, no twisted pine trees clinging to rocks, no pagodas, no characters, no seals or stamps.

Never: no sun disc, no birds, no people, no animals, no buildings, no signs, no text, letters or numbers anywhere, no signature, no seal or stamp, no frame or border, no gold leaf."""

# D, round 2 (October 28): Mo found D's sun cramped (the mockup had pushed it left, between the
# crane and two far trunks Codex put where the sun was asked to go) and asked whether the crane
# still suits. A clearing is edited into sequoia-2 so the sun can go home, and two American birds
# are painted over the live crane's original, in its place and hand: Anna's hummingbird (Claude's
# pick: it burns energy faster for its size than almost any animal, its flight muscles packed with
# mitochondria) and the golden eagle. Each flies like the crane, so the page's stroke can still
# leave from its tail where the crane's feet were.
CLEARING = """EDIT the attached painting. Keep it exactly as it is, the same paper, hand and colours, with ONE change: remove the two farther tree trunks that stand between about 66% and 83% across (the pale, misty one at about 70-74% and the brown one at about 75-82%, behind the big front trunk). In their place, open bright morning haze: pale warm light and bare paper, with only a few faint, distant small conifer tips low down (below about 50% down). This makes a clear opening in the grove from about 58% to 83% across, from the top down to about 50% down. Keep the big front trunk on the right, the faint far trunks at the very right edge, the young conifers, the ferns, the fallen log and the slanting light exactly as they are. No sun disc, no birds, no text, no signature, no frame."""

HUMMINGBIRD = """EDIT the attached painting. Replace the crane with an Anna's hummingbird, California's year-round hummingbird, painted in exactly the same loose watercolour hand on the same paper, with nothing else in the picture.
- It flies toward the upper right, as the crane does: the body angled up to the right, the long, thin, straight bill pointing right, both wings raised high in a fast beat, their tips a little blurred with dry-brush strokes, the tail fanned out behind.
- Size and place: smaller than the crane. From its tail tip at about 18% across and 82% down to its bill tip at about 68% across and 42% down; its raised wings reach up to about 15% down.
- Colours, muted and soft: a green back and crown (sage to bottle green), a soft grey-white breast and belly, the male's throat and crown a muted rose-magenta (not bright red), dark grey wing feathers.
- Few strokes, wet soft edges, like the crane. Not a detailed illustration, not a cartoon, not a greeting card.
No flowers, no branches, no other birds, no text, no signature, no seal, no frame."""

EAGLE = """EDIT the attached painting. Replace the crane with a golden eagle, painted in exactly the same loose watercolour hand on the same paper, with nothing else in the picture.
- It soars toward the right in a calm glide: long, broad wings spread wide and almost flat, lifted in a very shallow V, the long dark primary feathers at the wing tips spread like fingers; the head forward to the right with a golden-buff nape and a hooked bill; the tail spread behind.
- Size and place: its wingspan about as wide as the crane's wings, centred where the crane's body was; its tail tip at about 20% across and 75% down.
- Colours, muted and soft: warm dark brown washes (not black), the golden-buff nape, a grey-yellow bill and feet tucked up.
- Few strokes, wet soft edges, like the crane. Calm and gliding, not fierce: no open beak, no talons out. Not a detailed illustration, not a logo.
No other birds, no text, no signature, no seal, no frame."""

# Mo picked the hummingbird (October 28). Its first takes have big, broad, feathery wings, like
# the crane's they were painted over; a hummingbird's are long, narrow and pointed, a blur in a
# fast beat. Two edits of hummingbird-1 change only the wings; one fresh take over the crane's
# original describes the whole bird again with the right wings.
WINGS = """EDIT the attached painting. Keep the hummingbird's body, head, bill, tail, colours, size and place exactly as they are, the same paper and the same loose watercolour hand. Change ONLY the wings: they are wrong for a hummingbird (too big, too broad and too feathery, like a large bird's). Paint true hummingbird wings: long, narrow, pointed and swept back like thin blades, each about as long as the body, both raised up and back in a fast beat, with no separate feathers drawn; their edges softened into a few quick dry-brush motion streaks, so they read as a blur of speed. Pale grey and soft dark grey. Nothing else in the picture: no flowers, no text, no signature, no frame."""

HUMMINGBIRD_3 = HUMMINGBIRD.replace(
    "both wings raised high in a fast beat, their tips a little blurred with dry-brush strokes, the tail fanned out behind.",
    "both wings raised up and back in a fast beat: true hummingbird wings, long, narrow and pointed like thin swept-back blades, each about as long as the body, no separate feathers drawn, their edges softened into a few quick dry-brush motion streaks so they read as a blur of speed; the tail fanned out behind.",
)

CRANE = """EDIT the attached painting. Keep the bird's exact pose, size, position and wing shapes, the same brush hand and the same paper. Change only the species: make it a North American SANDHILL CRANE.
- Its whole body, neck and wings are soft mid-grey and pale warm-grey watercolour washes (not white).
- The long flight feathers at the wing tips and along the wings' trailing edge are a darker slate grey (not solid black).
- The neck is grey (no black neck). A pale whitish cheek and throat. A small bright red patch on the forehead and crown only.
- A dark grey bill. Dark grey legs trailing straight behind, as now.
Nothing else in the picture: plain paper. No text, no signature, no seal, no frame."""


def refs():
    REFS.mkdir(parents=True, exist_ok=True)
    land = Image.open(ROOT / "public/images/home-v2/ink/spring/landscape.webp").convert("RGB")
    sheet = Image.new("RGB", (1536, 1024), "white")
    sheet.paste(land.resize((1536, 659)), (0, 1024 - 659))
    sheet.save(REFS / "current-opening.png")
    crane = Image.open(ROOT / "reference/home-v2/ink/originals/gpt25-crane-paint-a.png").convert("RGB")
    crane.resize((1536, 1020)).save(REFS / "current-crane.png")


def main():
    refs()
    for name, scene in SCENES.items():
        (PROMPTS / f"{name}-1.txt").write_text(REF + scene + "\n\n" + STYLE, encoding="utf-8", newline="\n")
        (PROMPTS / f"{name}-2.txt").write_text(scene + "\n\n" + STYLE, encoding="utf-8", newline="\n")
    for take in (1, 2):
        (PROMPTS / f"sandhill-crane-{take}.txt").write_text(CRANE + "\n", encoding="utf-8", newline="\n")
    # Two takes with the live opening attached (the take 1s of A to C were the better ones), one without.
    for take in (1, 2):
        (PROMPTS / f"sequoia-{take}.txt").write_text(REF + GROVE + "\n", encoding="utf-8", newline="\n")
    (PROMPTS / "sequoia-3.txt").write_text(GROVE + "\n", encoding="utf-8", newline="\n")
    for take in (1, 2):
        for name, text in (("sequoia-2-clear", CLEARING), ("hummingbird", HUMMINGBIRD), ("golden-eagle", EAGLE)):
            (PROMPTS / f"{name}-{take}.txt").write_text(text + "\n", encoding="utf-8", newline="\n")
        (PROMPTS / f"hummingbird-wings-{take}.txt").write_text(WINGS + "\n", encoding="utf-8", newline="\n")
    assert HUMMINGBIRD_3 != HUMMINGBIRD
    (PROMPTS / "hummingbird-3.txt").write_text(HUMMINGBIRD_3 + "\n", encoding="utf-8", newline="\n")
    print(sorted(p.name for p in PROMPTS.glob("*.txt")))


if __name__ == "__main__":
    main()
