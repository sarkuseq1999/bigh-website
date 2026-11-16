"""Launch copy pass (November 16, 2026): American spelling and the English launch rewrites.

The site keys every translated line by its English source text (src/i18n/copy-keys.json maps the
English to a message id, messages/<locale>.json hold the words). Changing an English line in a
component therefore also needs its source key renamed and its English message changed, or every
language loses its translation. This script does that, so the edits in the components and the
catalogs stay in step:

1. SPELLING: American spelling in every quoted string in src/ (colour -> color, watercolour ->
   watercolor, flavour -> flavor), and in the matching source keys and English messages. Paths and
   CSS custom properties are left alone. Translations are unchanged (spelling only).
2. RENAMES: an English line rewritten for launch keeps its id; its English message changes, and so
   do the other languages' where a new draft translation is given (draft, not native-reviewed),
   so no language keeps a line the English no longer says (for example "in development").
3. ADDS: new lines get the next free ids, with draft translations.

The component edits for RENAMES and ADDS are made by hand; this script only checks that each new
English line is present in src/ and stops if it is not. Re-running is safe.

Run from the repo root:  python -X utf8 reference/launch/copy_launch.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KEYS = ROOT / "src/i18n/copy-keys.json"
LOCALES = ["en", "cns", "kr", "vn", "jp"]

SPELL = [
    (re.compile(r"\bwatercolours\b"), "watercolors"),
    (re.compile(r"\bwatercolour\b"), "watercolor"),
    (re.compile(r"\bWatercolour\b"), "Watercolor"),
    (re.compile(r"\bcolours\b"), "colors"),
    (re.compile(r"\bcolour\b"), "color"),
    (re.compile(r"\bColour\b"), "Color"),
    (re.compile(r"\bflavours\b"), "flavors"),
    (re.compile(r"\bflavour\b"), "flavor"),
]
STRING = re.compile(r'"(?:[^"\\\n]|\\.)*"')


def spell(text: str) -> str:
    for pattern, value in SPELL:
        text = pattern.sub(value, text)
    return text


def spell_string(match: re.Match[str]) -> str:
    literal = match.group(0)
    # Paths, file names and CSS custom properties keep their spelling.
    if re.search(r"/|\.(webp|png|jpe?g|svg|css)\b|^\"--", literal):
        return literal
    return spell(literal)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


# Rewrites of existing lines: (old English, new English, {locale: draft translation}).
RENAMES: list[tuple[str, str, dict[str, str]]] = []
# New lines: (English, {locale: draft translation}).
ADDS: list[tuple[str, dict[str, str]]] = []

exec((Path(__file__).parent / "copy_entries.py").read_text(encoding="utf-8"))  # fills both lists


def main() -> int:
    changed_files = 0
    for path in (ROOT / "src").rglob("*"):
        if path.suffix not in {".ts", ".tsx"} or path.name == "copy-keys.json":
            continue
        text = path.read_text(encoding="utf-8")
        new = STRING.sub(spell_string, text)
        if new != text:
            path.write_text(new, encoding="utf-8", newline="\n")
            changed_files += 1

    keys: dict[str, str] = load(KEYS)
    catalogs = {loc: load(ROOT / f"messages/{loc}.json") for loc in LOCALES}

    renamed = {}
    for source, key in keys.items():
        renamed[spell(source)] = key
    keys = renamed
    for key, value in list(catalogs["en"]["Copy"].items()):
        catalogs["en"]["Copy"][key] = spell(value)

    src_text = "\n".join(
        p.read_text(encoding="utf-8") for p in (ROOT / "src").rglob("*") if p.suffix in {".ts", ".tsx"}
    )
    report = [f"spelling: {changed_files} source files"]

    for old, new, translations in RENAMES:
        if new not in src_text and json.dumps(new, ensure_ascii=False)[1:-1] not in src_text:
            print(f"MISSING in src (edit the component first): {new}")
            return 1
        key = keys.pop(old, None) or keys.get(new)
        if not key:
            print(f"NO KEY for: {old}")
            return 1
        keys[new] = key
        catalogs["en"]["Copy"][key] = new
        for loc, value in translations.items():
            catalogs[loc]["Copy"][key] = value
        report.append(f"{key} renamed: {new[:70]}")

    used = {int(v[1:]) for v in keys.values() if v.startswith("m") and v[1:].isdigit()}
    nxt = 1260
    for english, translations in ADDS:
        if english in keys:
            key = keys[english]
            report.append(f"{key} kept: {english[:70]}")
        else:
            if english not in src_text and json.dumps(english, ensure_ascii=False)[1:-1] not in src_text:
                print(f"MISSING in src (edit the component first): {english}")
                return 1
            while nxt in used:
                nxt += 1
            key = f"m{nxt}"
            used.add(nxt)
            keys[english] = key
            report.append(f"{key} added: {english[:70]}")
        catalogs["en"]["Copy"][key] = english
        for loc, value in translations.items():
            catalogs[loc]["Copy"][key] = value

    save(KEYS, keys)
    for loc in LOCALES:
        save(ROOT / f"messages/{loc}.json", catalogs[loc])
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
