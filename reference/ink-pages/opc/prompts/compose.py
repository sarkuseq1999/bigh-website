"""Join _style.txt (or _style-land.txt for a landscape) and _<name>.txt into <name>.txt, the prompt
hf_opc.py sends. usage: python -X utf8 reference/ink-pages/opc/prompts/compose.py <name> [land]"""

import io
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
name = sys.argv[1]
land = len(sys.argv) > 2 and sys.argv[2] == "land"
style = HERE / ("_style-land.txt" if land else "_style.txt")
text = style.read_text(encoding="utf-8").strip() + "\n\n" + (HERE / f"_{name}.txt").read_text(encoding="utf-8").strip() + "\n"
with io.open(HERE / f"{name}.txt", "w", encoding="utf-8", newline="\n") as f:
    f.write(text)
print(HERE / f"{name}.txt")
