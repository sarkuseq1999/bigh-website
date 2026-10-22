"""Write one prompt file per Sign up stroke job (two pictures of each kind)."""

from pathlib import Path

HERE = Path(__file__).parent
TAIL = (
    " Centred, filling about 70% of the picture's width, with plenty of white paper all round. Pure"
    " white background, no paper texture, no shadow, no other marks, no text, no letters, no words,"
    " no seal, no stamp, no signature. Flat even lighting, photographed straight from above,"
    " landscape picture."
)
KINDS = {
    "pill": (
        "A single short horizontal shape painted in black sumi ink with a soft, wet, round brush on"
        " plain white paper: a pill-shaped ink wash about two and a half times as wide as it is"
        " tall, with gently rounded ends, filled almost solid black, the wet ink pooling slightly"
        " darker along its edges with a faint soft bleed into the paper's fibres. A slightly uneven,"
        " hand-painted outline, never a perfect vector shape. No dry-brush streaks, no splatter."
    ),
    "clean": (
        "One short, confident horizontal stroke of black sumi ink made with a wide flat brush on"
        " plain white paper, in a single straight pass: about two and a half times as wide as it is"
        " tall, an even, dense black body with clean edges that show only a slight paper-tooth"
        " roughness. Both ends finish with a brief tapered lift; the right end shows a few fine"
        " dry-brush streaks. Calm and controlled: not a blob, no round pressed head, no splatter."
    ),
    "dry": (
        "One fast horizontal stroke of black sumi ink made with a half-dry, stiff brush on plain"
        " white paper, in a single sweep: about three times as wide as it is tall, dense black in its"
        " middle band, breaking into many fine parallel bristle streaks of flying white along its top"
        " and bottom edges and at both ends, with paper showing between the streaks. Energetic but"
        " light, the solid middle wide enough to write a word on. No round blob, no splatter."
    ),
}
for kind, text in KINDS.items():
    for n in (1, 2):
        folder = HERE / f"{kind}{n}"
        folder.mkdir(exist_ok=True)
        (folder / "prompt.txt").write_text(text + TAIL, encoding="utf-8", newline="\n")
print("ok")
