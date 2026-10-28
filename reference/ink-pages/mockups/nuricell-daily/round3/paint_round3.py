"""Codex paints round 3 of NuriCell's daily chapter: what the section says instead of the dose.

  1  A good day for your cells: one California day (move, eat well, friends, sleep)
  2  The same formula for about 20 years: a young redwood's rings

usage: python -X utf8 paint_round3.py <repo> <out-dir> [name ...]
Uses the Questions pictures' shared style words and the homepage crane as the style reference.
Runs on Mo's ChatGPT plan (codex exec), not paid credits.
"""

import shutil
import subprocess
import sys
import time
from pathlib import Path

REPO, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
Q = REPO / "reference/ink-pages/questions"
STYLE_REF = REPO / "reference/ink-pages/home-science/originals/style-crane.png"
style = (Q / "prompts/_style.txt").read_text(encoding="utf-8").strip()

FIGURE = (
    "people are tiny, simple, faceless figures of a few brush strokes each, grown-ups in their fifties "
    "or sixties, never detailed"
)
WIDE = (
    "Very wide panorama: the whole scene is one long, low band across the middle of the picture, about "
    "three times as wide as it is tall, with plain empty paper above and below it. Landscape format, 3:2."
)
SUBJECTS = {
    "day-a1": (
        "One California day told across one long hillside, read from left to right, morning to night. "
        "Far left, early morning: a lone figure walking up a trail on a golden grassy hill, a low "
        "rising sun beside them with a thin transparent pale gold watercolour tint, the only colour in "
        "the picture. Left of centre: a valley oak with a small wooden outdoor table under it, a bowl "
        "and a cup on the table, breakfast. Right of centre: two or three friends sitting together on "
        "a bench at the hill's edge, looking out over a soft valley in the afternoon. Far right, "
        "night: a small farmhouse with one window lit, a thin crescent moon in a darker grey wash of "
        f"sky. The sky's wash deepens slowly from pale on the left to darker grey on the right. "
        f"The {FIGURE}. The four moments are spaced evenly along the band, joined by the same "
        "rolling hill line."
    ),
    "day-a2": (
        "Four small separate scenes of one California day, side by side in a row from left to right, "
        "each a loose vignette that fades into bare paper, with clear empty paper between them and "
        "about the same size: (1) morning, a lone figure walking up a trail on a golden grassy hill, "
        "a low rising sun with a thin transparent pale gold watercolour tint, the only colour in the "
        "picture; (2) breakfast, a plain bowl, a cup and a small dish holding exactly three plain white "
        "capsules on a wooden table by a window; (3) afternoon, two friends sitting together on a "
        "bench under a valley oak; (4) night, a small farmhouse with one window lit under a thin "
        f"crescent moon. The {FIGURE}."
    ),
    "rings-b1": (
        "The cut end of a young California redwood log, seen straight on, filling the middle of the "
        "picture: about twenty-five growth rings painted as loose, slightly uneven concentric circles "
        "of wet grey wash, a little wider apart near the centre, under a thin transparent muted "
        "warm-brown watercolour tint; the thick fibrous bark around the edge in dry-brush black with "
        "flying white; one small sword fern sprig lying beside it on the ground. The rings must be "
        "clearly countable and the centre clear."
    ),
    "rings-b2": (
        "A section of a young California redwood log lying on the forest floor, its cut end turned "
        "three-quarters toward us, filling the left two thirds of the picture: about twenty-five "
        "growth rings painted as loose, slightly uneven concentric circles of wet grey wash under a "
        "thin transparent muted warm-brown watercolour tint, the fibrous bark in dry-brush black. "
        "Behind it, very faint pale grey washes of tall straight redwood trunks fading into mist, and "
        "a few sword ferns at its foot. The rings must be clearly countable and the centre clear."
    ),
}
FORMATS = {"day-a1": WIDE, "day-a2": WIDE, "rings-b1": "Square format, 1:1.", "rings-b2": "Landscape format, 3:2."}
codex = shutil.which("codex")
wanted = sys.argv[3:] or list(SUBJECTS)

running = []
for name in wanted:
    subject = SUBJECTS[name]
    prompt = style.replace("{SUBJECT}", subject).replace("{FORMAT}", FORMATS[name])
    (OUT / f"{name}.txt").write_text(prompt + "\n", encoding="utf-8", newline="\n")
    order = (
        "Use your built-in image generation tool to make exactly ONE picture, with the attached "
        f"picture as the style reference: {prompt} Copy the generated PNG into the current folder "
        f"as {name}.png. Reply with its full path."
    )
    cmd = [
        codex, "exec", "--skip-git-repo-check", "-C", str(OUT), "-s", "workspace-write",
        "-c", 'model_reasoning_effort="low"', "-o", str(OUT / f"{name}.log"),
        "-i", str(STYLE_REF), "--", order,
    ]
    (OUT / f"{name}.png").unlink(missing_ok=True)
    running.append((name, subprocess.Popen(cmd, stdin=subprocess.DEVNULL,
                                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)))
    print("started", name, flush=True)

while running:
    for name, proc in list(running):
        if proc.poll() is not None:
            running.remove((name, proc))
            ok = (OUT / f"{name}.png").exists()
            print(name, "exit", proc.returncode, "png" if ok else "MISSING", flush=True)
    time.sleep(2)
