"""Have Codex paint the Questions pictures (one per question, every product page), a few at a time.

usage: python -X utf8 paint_questions.py [name ...]   (no names: every subject in prompts/subjects.txt)
Each prompt is prompts/_style.txt with the subject and format filled in, saved as prompts/<name>.txt;
the picture lands in originals/<name>.png, Codex's last message in originals/<name>.log. Runs on
Mo's ChatGPT plan (codex exec), not paid credits.
"""

import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "originals"
STYLE_REF = HERE.parent / "home-science" / "originals" / "style-crane.png"
AT_ONCE = 8
OUT.mkdir(exist_ok=True)

FORMATS = {"4:3": "Landscape format, 4:3.", "16:9": "Wide landscape format, 16:9."}
style = (HERE / "prompts" / "_style.txt").read_text(encoding="utf-8").strip()
wanted = set(sys.argv[1:])
codex = shutil.which("codex")

queue = []
for line in (HERE / "prompts" / "subjects.txt").read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    name, fmt, subject = line.split("|", 2)
    if wanted and name not in wanted:
        continue
    prompt = style.replace("{SUBJECT}", subject).replace("{FORMAT}", FORMATS[fmt])
    (HERE / "prompts" / f"{name}.txt").write_text(prompt + "\n", encoding="utf-8", newline="\n")
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
    queue.append((name, cmd))

running = []
while queue or running:
    while queue and len(running) < AT_ONCE:
        name, cmd = queue.pop(0)
        (OUT / f"{name}.png").unlink(missing_ok=True)
        running.append((name, subprocess.Popen(cmd, stdin=subprocess.DEVNULL,
                                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)))
        print("started", name, flush=True)
    for name, proc in list(running):
        if proc.poll() is not None:
            running.remove((name, proc))
            ok = (OUT / f"{name}.png").exists()
            print(name, "exit", proc.returncode, "png" if ok else "MISSING", flush=True)
    time.sleep(2)
