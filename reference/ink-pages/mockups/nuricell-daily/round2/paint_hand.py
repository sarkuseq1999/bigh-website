"""Codex paints NuriCell How-to-take-it idea D (a hand holding three capsules), a few takes at once.

usage: python -X utf8 paint_hand.py <repo> <out-dir>
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

HAND = (
    "a relaxed adult hand with exactly five fingers (four fingers and a thumb), painted in a few loose, "
    "wet strokes of pale grey wash with a darker dry-brush accent along one edge, no knuckle lines, "
    "no fingernails, no skin texture"
)
CAPS = (
    "exactly three plain white capsules, three, not more and not fewer, each a simple two-piece "
    "capsule shape left as bare paper with a soft grey edge and a faint seam; they are the clearest "
    "thing in the picture"
)
SUBJECTS = {
    "daily-hand-d1": (
        f"An open hand, palm up, reaching in from the lower right edge of the picture, seen from a little "
        f"above: {HAND}. Resting together in the middle of the palm: {CAPS}. Nothing else."
    ),
    "daily-hand-d2": (
        f"A loosely cupped hand seen from the side at table height, held out as if offering what it holds: "
        f"{HAND}. In the cup of the palm: {CAPS}. Below the hand, one long pale grey wash suggests a table "
        f"top, fading into the paper. Nothing else."
    ),
    "daily-hand-d3": (
        f"An open hand, palm up, reaching in from the right edge of the picture, held just above a plain "
        f"breakfast plate with a slice of toast on it that is only a pale wash suggestion: {HAND}. Resting "
        f"together in the palm: {CAPS}. Nothing else."
    ),
}
FORMAT = "Landscape format, 4:3."
codex = shutil.which("codex")

running = []
for name, subject in SUBJECTS.items():
    prompt = style.replace("{SUBJECT}", subject).replace("{FORMAT}", FORMAT)
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
