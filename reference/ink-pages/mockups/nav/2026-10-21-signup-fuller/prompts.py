"""One prompt per fuller version of today's Sign up stroke (two pictures of each kind). Each job gets
today's original as its reference picture."""

from pathlib import Path

HERE = Path(__file__).parent
HEAD = (
    "The attached picture is a black sumi ink brushstroke. Paint ONE new stroke in the same hand and"
    " the same style: a wet, round, loaded start at the left, rough paper-tooth edges, solid deep"
    " black ink, and dry bristle streaks where the brush lifts at the right. But make it FULLER: "
)
TAIL = (
    " Horizontal, centred, filling about 70% of the picture's width, with plenty of white paper all"
    " round. Pure white background, no paper texture, no shadow, no other marks, no text, no"
    " letters, no seal, no stamp. Flat even lighting, photographed straight from above, landscape"
    " picture."
)
KINDS = {
    "body": (
        "its body stays as thick as its round start all the way along instead of thinning, about"
        " three and a half times as wide as it is tall, and the dry streaks at the right end are"
        " short."
    ),
    "chunky": (
        "shorter and chunkier, about two and a half times as wide as it is tall: a big round loaded"
        " start, a thick, full body, and a short fringe of dry streaks at the right end."
    ),
    "rich": (
        "a heavier, wetter load of ink: the body swells a little in the middle, the ink pools a"
        " little darker at the start, and the right end fans into a fuller brush of dry streaks"
        " (many of them, close together, not a few sparse spikes). About three times as wide as it"
        " is tall."
    ),
}
for kind, text in KINDS.items():
    for n in (1, 2):
        folder = HERE / f"{kind}{n}"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "prompt.txt").write_text(HEAD + text + TAIL, encoding="utf-8", newline="\n")
print("ok")
