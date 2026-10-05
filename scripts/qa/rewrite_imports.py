"""Rewrite import specifiers after the ink kit move (October 5, 2026). Exact strings only."""

import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) / "src"
INK = "@/components/ink"
RULES = {
    # files that stayed in home-v2/look-ink
    "components/home-v2/look-ink": {
        '"./look-ink.module.css"': f'"{INK}/ink.module.css"',
        '"./motion"': f'"{INK}/motion"',
        '"../chrome"': f'"{INK}/chrome"',
        '"../dialogs"': f'"{INK}/dialogs"',
        '"./brush"': f'"{INK}/brush"',
        '"./closing-crane"': f'"{INK}/closing-crane"',
    },
    # files that moved into ink/
    "components/ink": {
        '"./content"': '"@/components/home-v2/content"',
        '"./assets"': '"@/components/home-v2/look-ink/assets"',
        '"./look-ink.module.css"': '"./ink.module.css"',
        '"./brush-route"': '"@/components/home-v2/look-ink/brush-route"',
    },
    "app": {
        '"@/components/home-v2/dialogs"': f'"{INK}/dialogs"',
        '"@/components/home-v2/chrome"': f'"{INK}/chrome"',
    },
}

changed = []
for folder, mapping in RULES.items():
    for file in (ROOT / folder).rglob("*.ts*"):
        text = file.read_text(encoding="utf-8")
        new = text
        for old, replacement in mapping.items():
            new = new.replace(f"from {old}", f"from {replacement}")
        if new != text:
            file.write_text(new, encoding="utf-8", newline="\n")
            changed.append(str(file.relative_to(ROOT)))
print("\n".join(changed))
