"""Have Codex paint the Questions mockups' pictures, several at once.

usage: python -X utf8 paint.py [name ...]   (no names: every subject in prompts/subjects.txt)
Each prompt is _style.txt with the subject and format filled in, saved as prompts/<name>.txt; the
picture lands in art/<name>.png, Codex's last message in art/<name>.log.
"""

import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
ART = HERE / "art"
STYLE_REF = HERE.parents[1] / "home-science" / "originals" / "style-crane.png"
ART.mkdir(exist_ok=True)

FORMATS = {"4:3": "Landscape format, 4:3.", "16:9": "Wide landscape format, 16:9."}
style = (HERE / "prompts" / "_style.txt").read_text(encoding="utf-8").strip()
wanted = set(sys.argv[1:])
codex = shutil.which("codex")

jobs = []
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
        codex, "exec", "--skip-git-repo-check", "-C", str(ART), "-s", "workspace-write",
        "-c", 'model_reasoning_effort="low"', "-o", str(ART / f"{name}.log"),
        "-i", str(STYLE_REF), "--", order,
    ]
    jobs.append((name, subprocess.Popen(cmd, stdin=subprocess.DEVNULL,
                                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)))
    print("started", name, flush=True)

for name, proc in jobs:
    code = proc.wait()
    ok = (ART / f"{name}.png").exists()
    print(name, "exit", code, "png" if ok else "MISSING", flush=True)
