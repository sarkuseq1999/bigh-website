# Science in Ink & Gold (the handscroll) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild `/science` in the site's Ink & Gold look as "the handscroll": Dr. Liu's path as one ink painting that travels sideways while the page scrolls down, then Dr. Liu, the formulas, the research, health explained and Ask BiGH Science as wide ink strips.

**Architecture:** A new client page `src/components/science/ink/` inside the kit's `InkPage` (shared menu bar, footer, bloom). The handscroll is a sticky "pin" (the painting's multiply blend group) followed, inside its section, by an empty "room" whose padding equals the painting's overflow, so the stylesheet alone gives the page its full height (tested October 14: a sticky box does not stay pinned through its parent's own bottom padding, but does through a following child's); a small hook turns scroll position into the painting's shift and the stop in view. Paintings are built by a Python script from GPT Image 2.5 originals into webp files plus a generated `science-art.ts`.

**Tech Stack:** Next.js 16 (App Router, `next/font`, `next/image`), React 19, CSS modules, next-intl via `useCopy`, Python 3 (Pillow, NumPy, OpenCV) for pictures, Playwright for Python for QA.

**Spec:** `docs/superpowers/specs/2026-10-14-science-ink-design.md` (read it first; this plan argues from it).

## Global Constraints

- Work only in the worktree `C:\Users\mcbig\Documents\codes\bigh-science-ink`, branch `science-ink`. Never push. Never touch the main checkout except its untracked `.claude/launch.json` (Task 2).
- Read the relevant guide in `node_modules/next/dist/docs/` before writing Next.js code (AGENTS.md: this Next.js has breaking changes).
- Files are LF. This checkout has `core.autocrlf=true`: never `git stash`; Python writes pass `newline="\n"`; `npx prettier --write <files>` restores LF.
- `DESIGN.md` applies: rice paper, sumi ink, gold leaf only for energy (the scroll's sun, the lamp's flame), sentence case, text 15px or larger, targets 44px or larger, the one breath (`--breath: 2.4s`, `--ease`), reduced motion complete and still.
- Dr. Liu is his real photograph (`/images/jiankang-liu.jpg`), never a generated face. Dr. Iris Wang appears in words only.
- Every word comes from `src/components/science/science-content.ts`; new strings are added there and marked `// DRAFT`.
- No brush line, no stations, no ensō, no lantern, no homepage/About/NuriCell painting on this page.
- New copy keys start at `m650` (the Propolis session adds keys from `m612`).
- Ports: dev `3050`, built (`next start`) `3051`.
- The homepage, About, NuriCell, the other product pages, the menu bar and the footer must not change.
- Commit after each task with a message ending in `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

- **Short laptop windows (1280x720, 1366x768) and long titles (Vietnamese, Korean):** the pinned box (title, painting, stops) must fit between the menu bar and the bottom of the window while it is pinned; the painting shrinks first. Test: Task 3 `journey` checks the pin's bottom at 1280x720 in `en` and `vn`.
- **Links into the middle of the page (`/science#research`, reload half way down):** the section's full height comes from the stylesheet (the room's padding = the painting's overflow), so anchors land where they will stay after the script runs. Test: Task 6 `deep_links`, measured 1.5s after load.
- **Turning a phone or resizing mid-scroll:** the shift is recomputed from the scroll position; no blank band, no jump to the start. Test: Task 3 `journey` resizes from 1440 to 1024 wide half way through and checks the painting still covers the band.
- **A painting losing its blend (a white box):** nothing between a painting's blend group and the page may make a stacking context (the footer crane's trap). Test: Task 3 and Task 4 `multiply`.
- **Reduced motion and no script:** nothing pins or moves; the whole scroll can still be seen (the band scrolls sideways under the visitor's own hand) and all five stops are readable. Test: Task 3 `still`.

---

## File structure

| File                                                         | Role                                                                     |
| ------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `reference/ink-pages/science/originals/*.png`, `*.json`      | GPT Image 2.5 originals and their settings (from the session scratchpad) |
| `reference/ink-pages/science/prompts/*.txt`                  | Their prompts                                                            |
| `reference/ink-pages/science/hf_science.py`                  | The paint helper used (copy, for the record)                             |
| `reference/ink-pages/science/build_science.py`               | Builds the webp pictures and `science-art.ts`                            |
| `reference/ink-pages/science/check_science_art.py`           | Checks the built pictures; writes a contact sheet                        |
| `reference/ink-pages/science/README.md`                      | What each picture is, the spend                                          |
| `reference/ink-pages/science/.gitignore`                     | `plates/`                                                                |
| `public/images/science/ink/*.webp`                           | Shipped pictures                                                         |
| `src/components/science/ink/science-art.ts`                  | Generated: picture sizes, the stops' places                              |
| `src/app/[locale]/science/page.tsx`                          | Route: Ysabeau, dialogs, products, `ScienceInk`                          |
| `src/components/science/ink/science-ink.tsx` + `.module.css` | The page: parts in order, title face                                     |
| `src/components/science/ink/opening.tsx`                     | The title block                                                          |
| `src/components/science/ink/journey.tsx` + `.module.css`     | The handscroll                                                           |
| `src/components/science/ink/use-journey.ts`                  | Scroll position to shift and stop                                        |
| `src/components/science/ink/people.tsx` + `.module.css`      | Dr. Liu and the formulas                                                 |
| `src/components/science/ink/strip.tsx` + `.module.css`       | One strip part (header row, painting, words)                             |
| `src/components/science/ink/explore.tsx` + `.module.css`     | Research (with the full list), health, ask                               |
| `src/components/science/science-content.ts`                  | Words (new DRAFT strings added)                                          |
| `reference/ink-pages/science/translations-science.cjs`       | Draft translations of the new strings                                    |
| `scripts/qa/qa_science_ink.py`                               | The page's QA                                                            |
| `reference/science-page/looks/film/`                         | Today's film page, retired                                               |

---

### Task 1: The paintings

**Files:**

- Create: `reference/ink-pages/science/{originals,prompts}/…`, `hf_science.py`, `build_science.py`, `check_science_art.py`, `README.md`, `.gitignore`
- Create (generated): `public/images/science/ink/*.webp`, `src/components/science/ink/science-art.ts`

**Interfaces:**

- Produces `scienceArt` (in `science-art.ts`):

  ```ts
  export const scienceArt = {
    scroll: { src, width, height, phone: { src, width, height },
              stops: { okayama, berkeley, y2002, salzburg, today } },   // fractions 0..1 of the width
    scrolls: { src, width, height, phone: { src, width, height } },
    health: { src, width, height, scenes: [{ src, width, height }, …3] }, // lamp, stones, poppies
    mugs: { src, width, height, phone: { src, width, height } },
  } as const;
  ```

- [ ] **Step 1: Move the originals and prompts into the repo**

The paintings are already painted (15 jobs, ledger `%LOCALAPPDATA%/HiggsfieldAPI/bigh-science-mock`). Copy them from the session scratchpad:

```bash
S="C:/Users/mcbig/AppData/Local/Temp/claude/C--Users-mcbig-Documents-codes-bigh-website/5f382547-0772-41e1-9474-8750b9995200/scratchpad/paint"
D="C:/Users/mcbig/Documents/codes/bigh-science-ink/reference/ink-pages/science"
mkdir -p "$D/originals" "$D/prompts"
for n in S-panel-1 S-panel-2 S-panel-3 R-scrolls S-health-poppy S-mugs A-scroll R-health R-tea; do
  cp "$S/originals/gpt25-$n.png" "$S/originals/gpt25-$n.json" "$D/originals/"
done
for n in S-panel-1 S-panel-2 S-panel-3 R-scrolls S-health-poppy S-mugs A-scroll R-health R-tea; do
  cp "$S/prompts/$n.txt" "$D/prompts/"
done
cp "$S/hf_science.py" "$D/hf_science.py"
printf 'plates/\n' > "$D/.gitignore"
ls "$D/originals" | wc -l
```

Expected: `18` (nine `.png`, nine `.json`). `A-scroll`, `R-health` and `R-tea` are kept because the panels and the two California edits were painted from them.

- [ ] **Step 2: Write the check first**

Create `reference/ink-pages/science/check_science_art.py`:

```python
"""Checks the Science page's built pictures (spec docs/superpowers/specs/2026-10-14-science-ink-design.md).

- every picture named in science-art.ts exists at its stated size;
- each picture's outer 3px strip is white (254.5 or whiter), so nothing shows a box when it
  multiplies onto the page;
- the scroll is a long band (at least 8 times as wide as tall), its five stops in order inside it;
- the health scenes are three, each narrower than the strip.
Writes plates/contact.jpg (the scroll with its stops marked, the strips, the scenes) to look at.

usage: python -X utf8 reference/ink-pages/science/check_science_art.py
"""

import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
TS = REPO / "src/components/science/ink/science-art.ts"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f"  ({detail})" if detail else ""))


def art():
    text = TS.read_text(encoding="utf-8")
    body = text[text.index("= {") + 2 : text.rindex("} as const")] + "}"
    body = re.sub(r"(\w+):", r'"\1":', body)
    body = re.sub(r",(\s*[}\]])", r"\1", body)
    return json.loads(body)


def picture(entry):
    path = REPO / "public" / entry["src"].lstrip("/")
    img = Image.open(path).convert("RGB")
    check(f"{entry['src']} size", img.size == (entry["width"], entry["height"]), f"{img.size}")
    a = np.asarray(img).astype(np.float32)
    edge = np.concatenate([a[:3].reshape(-1, 3), a[-3:].reshape(-1, 3), a[:, :3].reshape(-1, 3), a[:, -3:].reshape(-1, 3)])
    check(f"{entry['src']} white edge", edge.mean() >= 254.5, f"{edge.mean():.1f}")
    return img


data = art()
scroll = picture(data["scroll"])
picture(data["scroll"]["phone"])
check("scroll is a long band", scroll.width >= 8 * scroll.height, f"{scroll.width}x{scroll.height}")
stops = [data["scroll"]["stops"][k] for k in ("okayama", "berkeley", "y2002", "salzburg", "today")]
check("stops in order inside the band", all(0 < a < b < 1 for a, b in zip(stops, stops[1:])), str(stops))
for key in ("scrolls", "mugs"):
    picture(data[key])
    picture(data[key]["phone"])
health = picture(data["health"])
scenes = [picture(s) for s in data["health"]["scenes"]]
check("three health scenes", len(scenes) == 3)
check("each scene narrower than the strip", all(s.width < health.width * 0.6 for s in scenes))

sheet_w = 2400
rows = [scroll.resize((sheet_w, round(scroll.height * sheet_w / scroll.width)))]
draw = ImageDraw.Draw(rows[0])
for f in stops:
    x = round(f * sheet_w)
    draw.line([(x, 0), (x, rows[0].height)], fill=(200, 0, 0), width=3)
for img in (Image.open(REPO / "public" / data[k]["src"].lstrip("/")) for k in ("scrolls", "health", "mugs")):
    rows.append(img.convert("RGB").resize((sheet_w // 2, round(img.height * (sheet_w // 2) / img.width))))
rows.append(Image.new("RGB", (sheet_w, max(s.height for s in scenes) // 2), "white"))
x = 0
for s in scenes:
    small = s.resize((s.width // 2, s.height // 2))
    rows[-1].paste(small, (x, 0))
    x += small.width + 40
sheet = Image.new("RGB", (sheet_w, sum(r.height + 30 for r in rows)), "white")
y = 0
for r in rows:
    sheet.paste(r, (0, y))
    y += r.height + 30
(HERE / "plates").mkdir(exist_ok=True)
sheet.save(HERE / "plates/contact.jpg", quality=85)
print("contact sheet: reference/ink-pages/science/plates/contact.jpg")
print("ALL PASS" if all(results) else f"{results.count(False)} FAILED")
sys.exit(0 if all(results) else 1)
```

- [ ] **Step 3: Run it to see it fail**

Run: `python -X utf8 reference/ink-pages/science/check_science_art.py`
Expected: FAIL with `FileNotFoundError` for `science-art.ts`.

- [ ] **Step 4: Write the build script**

Create `reference/ink-pages/science/build_science.py`:

```python
"""Build the Science page's ink paintings (Mo, October 13-14, 2026; spec
docs/superpowers/specs/2026-10-14-science-ink-design.md).

Originals: reference/ink-pages/science/originals/gpt25-<take>.png (GPT Image 2.5 on rice paper;
prompts in prompts/). Output: public/images/science/ink/*.webp (lossless plates in plates/, not
committed) and src/components/science/ink/science-art.ts.

The handscroll is three 21:9 panels painted to one horizon with mist at their ends. Each panel's
paper is divided out; its inner ends fade to paper (a smoothstep over FADES px); the panels are
shifted to one horizon (DY, measured October 14: the sea's top row is 653 at panel 1's right and 696
at panel 2's left; the hills' top row is 498 at panel 2's right and 503 at panel 3's left) and laid
side by side, overlapping by OVERLAP px, with a darken blend, so ink stays ink and the mists join.
The band is then cropped to its ink and levelled to white. STOP_X: where each stop's place stands
on the joined canvas, read off its contact sheet (Okayama's castle, Berkeley's tower, the hills of
2002, Salzburg's fortress, the oaks under the sun).

The strips are cropped to their ink; phones get narrower crops (the scrolls' and the mugs' middle)
and the health strip's three scenes, cut where the ink is thinnest near its thirds.

usage: python -X utf8 reference/ink-pages/science/build_science.py
"""

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "reference/ink-pages/about"))
import build_about as bd  # noqa: E402

ba = bd.ba
OUT = REPO / "public/images/science/ink"
URL = "/images/science/ink"
TS = REPO / "src/components/science/ink/science-art.ts"
# Bump when a shipped picture changes after it has been pushed (the image optimizer caches by URL).
V = "v1"
TAKES = {
    "panel1": "S-panel-1",
    "panel2": "S-panel-2",
    "panel3": "S-panel-3",
    "scrolls": "R-scrolls",
    "health": "S-health-poppy",
    "mugs": "S-mugs",
}
OVERLAP = (300, 300)
DY = (0, -43, -48)
FADES = ((0, 420), (520, 420), (420, 0))
STOP_X = {"okayama": 756, "berkeley": 4108, "y2002": 4718, "salzburg": 5600, "today": 7088}
PHONE_H = 400  # the scroll's phone picture: 300px tall on screen, 1.33x
EDGE = 0.03

bd.ORIG = HERE / "originals"
bd.URL = URL
bd.V = V
bd.TAKES = TAKES
ba.OUT = OUT
ba.PLATES = HERE / "plates"


def faded(arr, left, right):
    """Fade an array's left and right ends to white (smoothstep over `left` / `right` px)."""
    w = arr.shape[1]
    x = np.arange(w, dtype=np.float32)
    k = np.ones(w, np.float32)
    if left:
        k = np.minimum(k, np.clip(x / left, 0, 1))
    if right:
        k = np.minimum(k, np.clip((w - 1 - x) / right, 0, 1))
    k = k * k * (3 - 2 * k)
    return arr * k[None, :, None] + 255.0 * (1 - k[None, :, None])


def handscroll():
    panels = [np.asarray(bd.divided(bd.load(TAKES[f"panel{i}"]))).astype(np.float32) for i in (1, 2, 3)]
    h, w, _ = panels[0].shape
    top = max(0, -min(DY))
    xs = [0, w - OVERLAP[0], 2 * w - OVERLAP[0] - OVERLAP[1]]
    canvas = np.full((h + top + max(0, max(DY)), xs[2] + w, 3), 255.0, np.float32)
    for arr, x, dy, (fade_l, fade_r) in zip(panels, xs, DY, FADES):
        y = top + dy
        region = canvas[y : y + h, x : x + w]
        canvas[y : y + h, x : x + w] = np.minimum(region, faded(arr, fade_l, fade_r))
    joined = Image.fromarray(np.clip(np.rint(canvas), 0, 255).astype(np.uint8))
    x0, y0, x1, y1 = bd.ink_box(np.asarray(joined), pad=0.02)
    band = bd.feathered(bd.levelled(joined.crop((x0, y0, x1, y1))), EDGE)
    art = bd.art_of(band, f"scroll-{V}", None)
    art["phone"] = bd.art_of(band, f"scroll-phone-{V}", round(band.width * PHONE_H / band.height))
    art["stops"] = {key: round((x - x0) / (x1 - x0), 4) for key, x in STOP_X.items()}
    return art


def strip(key, pad=0.04):
    flat = bd.divided(bd.load(TAKES[key]))
    return bd.levelled(flat.crop(bd.ink_box(np.asarray(flat), pad=pad)))


def middle(img, start, end):
    return img.crop((round(img.width * start), 0, round(img.width * end), img.height))


def finish(img, name, width):
    return bd.art_of(bd.feathered(img, EDGE), f"{name}-{V}", width)


def cut_near(img, frac, span=0.08):
    """The column with the least ink within `span` of `frac` of the width (smoothed)."""
    ink = 255.0 - np.asarray(img.convert("L")).astype(np.float32)
    profile = np.convolve(ink.mean(axis=0), np.ones(31) / 31, mode="same")
    a, b = round(img.width * (frac - span)), round(img.width * (frac + span))
    return a + int(np.argmin(profile[a:b]))


def scenes(img):
    cuts = [0, cut_near(img, 1 / 3), cut_near(img, 2 / 3), img.width]
    out = []
    for i, (a, b) in enumerate(zip(cuts, cuts[1:])):
        piece = img.crop((a, 0, b, img.height))
        # level 200: the scene's own ink, not the faint mist between scenes
        box = bd.ink_box(np.asarray(piece), level=200, pad=0.12)
        out.append(finish(piece.crop(box), f"health-scene-{i + 1}", 900))
    return out


def write_ts(art):
    head = [
        "// Generated by reference/ink-pages/science/build_science.py. Do not edit by hand: change",
        "// the script (or its TAKES) and run it again. The Science page's ink paintings (October 14,",
        "// 2026): GPT Image 2.5 on rice paper, the paper divided out so each multiplies onto the page's",
        "// own paper. scroll.stops: where each stop's place stands, as fractions of the scroll's width.",
        "",
    ]
    TS.parent.mkdir(parents=True, exist_ok=True)
    TS.write_text("\n".join(head) + f"export const scienceArt = {json.dumps(art, indent=2)} as const;\n", encoding="utf-8", newline="\n")
    prettier = REPO / "node_modules/prettier/bin/prettier.cjs"
    subprocess.run(["node", str(prettier), "--write", str(TS)], cwd=REPO, check=True, capture_output=True)
    print(TS.relative_to(REPO))


if __name__ == "__main__":
    scrolls = strip("scrolls")
    health = strip("health")
    mugs = strip("mugs")
    write_ts(
        {
            "scroll": handscroll(),
            "scrolls": {**finish(scrolls, "scrolls", 2400), "phone": finish(middle(scrolls, 0.3, 0.7), "scrolls-phone", 1000)},
            "health": {**finish(health, "health", 2400), "scenes": scenes(health)},
            "mugs": {**finish(mugs, "mugs", 2400), "phone": finish(middle(mugs, 0.22, 0.78), "mugs-phone", 1000)},
        }
    )
```

- [ ] **Step 5: Build and check**

Run: `python -X utf8 reference/ink-pages/science/build_science.py && python -X utf8 reference/ink-pages/science/check_science_art.py`
Expected: the webp list, `src/components/science/ink/science-art.ts`, then every line `PASS` and `ALL PASS`.

- [ ] **Step 6: Look at the contact sheet and both joins at full size**

Open `reference/ink-pages/science/plates/contact.jpg` with the Read tool. Then crop the two joins from `plates/scroll-v1.png` (the panels meet near 32% and 64% of its width) at full size and look at them: the seas must meet at one horizon in drifting mist and the hills fade into Salzburg's with no straight edge, no block of mist and no step. The red marks must stand under the castle, the tower, the hills right of the tower, the fortress and the oaks. If a mark is off, change `STOP_X` and run Step 5 again. If a join shows an edge, widen that end's `FADES` (or `OVERLAP`) by 100 px and run Step 5 again.

- [ ] **Step 7: Write the README**

Create `reference/ink-pages/science/README.md`:

```markdown
# The Science page's paintings (October 13-14, 2026)

GPT Image 2.5 ("Marketing Studio Image 2.5 Flare" on the Higgsfield API), 21:9, 2k, quality high,
with the homepage's resting crane as the brushwork reference. Mo gave $3 on October 13; 15 jobs
used (about $0.75, at most $1.05 before refunds). Ledger:
`%LOCALAPPDATA%/HiggsfieldAPI/bigh-science-mock/ledger-science-mock.jsonl`.

| Picture          | Original                              | Note                                                                                                                                     |
| ---------------- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| The handscroll   | `S-panel-1`, `S-panel-2`, `S-panel-3` | Three panels to one horizon, joined in their mist by `build_science.py`; style reference `A-scroll` (the mockup's single-picture scroll) |
| The research     | `R-scrolls`                           | A shelf of rolled scrolls; three lie pulled forward (the three key studies)                                                              |
| Health explained | `S-health-poppy`                      | An edit of `R-health`: California poppies instead of the plum branch (Mo, October 14)                                                    |
| Ask BiGH Science | `S-mugs`                              | An edit of `R-tea`: two mugs instead of the tea set (Mo, October 14)                                                                     |

Build: `python -X utf8 reference/ink-pages/science/build_science.py`, then
`python -X utf8 reference/ink-pages/science/check_science_art.py`.
```

- [ ] **Step 8: Commit**

```bash
git add reference/ink-pages/science public/images/science/ink src/components/science/ink/science-art.ts
git commit -m "feat(science): the handscroll and the three strip paintings, built for the page

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: The route, the page shell, Dr. Liu and the formulas

**Files:**

- Modify: `src/app/[locale]/science/page.tsx`
- Create: `src/components/science/ink/science-ink.tsx`, `science-ink.module.css`, `opening.tsx`, `people.tsx`, `people.module.css`
- Modify: `src/components/science/science-content.ts` (new DRAFT strings)
- Move: `src/components/science/{look-film.tsx,look-film.module.css,film-scene.ts,look-types.ts,science-page.tsx,science-page.module.css,site-chrome.tsx,site-chrome.module.css,research-library.tsx,research-library.module.css}` and `scripts/qa/qa_science_film.py` → `reference/science-page/looks/film/`
- Create: `scripts/qa/qa_science_ink.py`
- Modify (untracked, main checkout): `C:\Users\mcbig\Documents\codes\bigh-website\.claude\launch.json`

**Interfaces:**

- Produces `ScienceInk({ fontClass }: { fontClass: string })` in `science-ink.tsx`; `OpeningWords()` in `opening.tsx`; `Liu()` and `Formulas()` in `people.tsx`.
- Produces, in `qa_science_ink.py`: `check(name, ok, detail="")`, `opened(browser, w, h, path=PATH, reduced=False, js=True)` returning `(ctx, page, response, errors)`, `bring(page, selector, top=140)`, and a `SECTIONS` dict that later tasks extend.

- [ ] **Step 1: Add the preview entries**

Add these two objects to the `configurations` array of `C:\Users\mcbig\Documents\codes\bigh-website\.claude\launch.json` (keep everything else as it is):

```json
{"name": "bigh-science-ink", "runtimeExecutable": "npm", "runtimeArgs": ["--prefix", "C:/Users/mcbig/Documents/codes/bigh-science-ink", "run", "dev", "--", "--hostname", "localhost", "--port", "3050"], "port": 3050},
{"name": "bigh-science-ink-prod", "runtimeExecutable": "npm", "runtimeArgs": ["--prefix", "C:/Users/mcbig/Documents/codes/bigh-science-ink", "run", "start", "--", "--hostname", "localhost", "--port", "3051"], "port": 3051}
```

Check it parses: `python -X utf8 -c "import json; json.load(open(r'C:/Users/mcbig/Documents/codes/bigh-website/.claude/launch.json', encoding='utf-8')); print('ok')"` → `ok`.

- [ ] **Step 2: Write the failing QA (shell and people)**

Create `scripts/qa/qa_science_ink.py`:

```python
"""QA for the Science page in Ink & Gold, the handscroll (spec
docs/superpowers/specs/2026-10-14-science-ink-design.md; plan
docs/superpowers/plans/2026-10-14-science-ink.md).

Sections (all, or --only=a,b):
  shell       200 in the ink look, the menu bar marks Science, one h1, the parts' ids in order,
              no canvas, no console errors (1440x900, 390x844)
  people      Dr. Liu's real photo on its mount, his name, numbers and sources, "Read his story"
              opens his sheet; the five bottles with their credits, each linking to its page
  journey     (Task 3) the scroll pins, travels from Okayama to Today and lets go
  still       (Task 3) reduced motion and no script: nothing pins, every stop readable
  multiply    (Task 3, 4) every painting's blend group sits on the page with no stacking context
  strips      (Task 4) research, health and ask: painting, words, the full list, the explainers
  languages   (Task 5) kr, jp, cns, vn: 200, no errors, the new strings translated
  layout      (Task 6) sizes 1920 to 360: no sideways scroll, text 15px+, targets 44px+
  deep_links  (Task 6) #scientists, #research, #health, #ask land under the menu bar
Pictures: scripts/qa/out/science-ink/.

usage: python -X utf8 scripts/qa/qa_science_ink.py [base-url] [--only=shell,people,...]
"""

import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
BASE = ARGS[0] if ARGS else "http://localhost:3050"
ONLY = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--only=")), None)
REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "scripts/qa/out/science-ink"
OUT.mkdir(parents=True, exist_ok=True)
PATH = "/en/science"
PARTS = ["scientists", "liu", "formulas", "research", "health", "ask"]
PREFETCH_CSS = re.compile(r"was preloaded using link preload but not used")
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f"  ({detail})" if detail else ""), flush=True)


def opened(browser, w, h, path=PATH, reduced=False, js=True):
    ctx = browser.new_context(
        viewport={"width": w, "height": h},
        reduced_motion="reduce" if reduced else "no-preference",
        java_script_enabled=js,
    )
    page = ctx.new_page()
    errors = []
    page.on("console", lambda m: m.type == "error" and not PREFETCH_CSS.search(m.text) and errors.append(m.text))
    page.on("pageerror", lambda e: errors.append(str(e)))
    response = page.goto(BASE + path, wait_until="networkidle")
    if js:
        page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
    return ctx, page, response, errors


def bring(page, selector, top=140):
    page.evaluate(
        "([s, t]) => { const e = document.querySelector(s); window.scrollBy(0, e.getBoundingClientRect().top - t); }",
        [selector, top],
    )


def shell(browser):
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, response, errors = opened(browser, w, h)
        check(f"shell {w}: 200", response is not None and response.status == 200)
        check(f"shell {w}: ink look", page.locator('[data-look="ink"][data-page="science"]').count() == 1)
        check(f"shell {w}: Science carries the menu's stroke", page.locator('[data-nav-trigger="science"][data-ink="here"]').count() == 1)
        h1 = page.locator("h1")
        check(f"shell {w}: one h1, the title", h1.count() == 1 and "Meet the scientists" in h1.inner_text(), h1.first.inner_text() if h1.count() else "")
        ids = page.evaluate("() => [...document.querySelectorAll('main > section[id]')].map(s => s.id)")
        check(f"shell {w}: parts in order", ids == PARTS, str(ids))
        check(f"shell {w}: no canvas", page.locator("main canvas").count() == 0)
        font = page.evaluate("getComputedStyle(document.querySelector('h1')).fontFamily")
        check(f"shell {w}: title in Ysabeau", "ysabeau" in font.lower(), font)
        page.wait_for_timeout(1500)
        check(f"shell {w}: no console errors", not errors, "; ".join(errors[:3]))
        ctx.close()


def people(browser):
    ctx, page, _, errors = opened(browser, 1440, 900)
    bring(page, "#liu")
    page.wait_for_timeout(600)
    photo = page.locator('#liu img[src*="jiankang-liu"]')
    check("people: Dr. Liu's real photo", photo.count() == 1)
    check("people: the photo on its mount", photo.evaluate("i => getComputedStyle(i.closest('figure')).boxShadow") != "none")
    text = page.locator("#liu").inner_text()
    for word in ["Dr. Jiankang Liu", "280+", "1994", "2025", "Chief Scientific Advisor, BiGH"]:
        check(f"people: {word}", word in text)
    check("people: three sources", page.locator("#liu dl a[href^='https://']").count() == 3)
    page.get_by_role("button", name="Read his story").click()
    page.wait_for_timeout(800)
    check("people: his sheet opens", page.locator("dialog[open]").count() == 1)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    check("people: his sheet closes", page.locator("dialog[open]").count() == 0)
    bottles = page.locator("#formulas li")
    check("people: five bottles", bottles.count() == 5, str(bottles.count()))
    for name, slug in [("NuriCell", "nuricell"), ("Nature Calm", "nature-calm"), ("Advanced OPC Formula", "advanced-opc"),
                       ("Green Bee Propolis", "green-bee-propolis"), ("Turmerific", "turmerific")]:
        link = page.locator(f'#formulas a[href$="/products/{slug}"]')
        check(f"people: {name} links to its page", link.count() == 1)
    words = page.locator("#formulas").inner_text()
    check("people: Dr. Iris Wang in words", "Dr. Iris Wang developed Nature Calm" in words)
    check("people: no photo of Dr. Iris Wang", page.locator('img[alt*="Iris"]').count() == 0)
    check("people: no console errors", not errors, "; ".join(errors[:3]))
    ctx.close()


SECTIONS = {"shell": shell, "people": people}

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for name, run in SECTIONS.items():
            if ONLY is None or name in ONLY:
                run(browser)
        browser.close()
    failed = [r for r in results if not r[1]]
    print(f"\n{len(results) - len(failed)}/{len(results)} passed")
    sys.exit(1 if failed else 0)
```

- [ ] **Step 3: Run it against the dev server to see it fail**

Start the dev server with the preview tool (`preview_start {name: "bigh-science-ink"}`), then run:
`python -X utf8 scripts/qa/qa_science_ink.py http://localhost:3050 --only=shell,people`
Expected: FAIL on `ink look`, `one h1, the title`, `parts in order` (the film page is still there).

- [ ] **Step 4: Retire the film page**

```bash
mkdir -p reference/science-page/looks/film
for f in look-film.tsx look-film.module.css film-scene.ts look-types.ts science-page.tsx science-page.module.css site-chrome.tsx site-chrome.module.css research-library.tsx research-library.module.css; do
  git mv "src/components/science/$f" "reference/science-page/looks/film/$f"
done
git mv scripts/qa/qa_science_film.py reference/science-page/looks/film/qa_science_film.py
grep -rn "science/\(look-film\|film-scene\|look-types\|science-page\|site-chrome\|research-library\)" src || echo "no imports left"
grep -rln "images/science-page" src || echo "no film pictures referenced"
```

Expected: `no imports left` and `no film pictures referenced`. If the second prints files, keep `public/images/science-page/`; otherwise remove it (its originals stay in `reference/science-page/originals/`): `git rm -r -q public/images/science-page`.

Add one line to `reference/science-page/looks/README.md` under its list: `- film/ — "Scroll film" (Mo's pick, September 28, 2026), live until the ink handscroll replaced it (October 2026); its QA: film/qa_science_film.py.`

- [ ] **Step 5: Add the new words**

Append to `src/components/science/science-content.ts`:

```ts
// The ink page, "the handscroll" (Mo, October 13-14, 2026; spec
// docs/superpowers/specs/2026-10-14-science-ink-design.md). DRAFT lines.
export const ink = {
  // The opening's lead: the film's two lines, as one.
  lead: ["A life in cell science.", "From Okayama to Berkeley, and from the lab to BiGH."],
  formulasLabel: "The formulas", // DRAFT
  source: "Source", // DRAFT
  scrollHint: "Keep scrolling: the scroll unrolls", // DRAFT
  scrollStill: "Scroll sideways to see the whole painting", // DRAFT
  scrollAlt:
    "A long ink painting of Dr. Liu’s path: Okayama Castle, the ocean, the bell tower at Berkeley, Salzburg, and California hills under a gold sun", // DRAFT
  readStudy: "Read the study", // DRAFT
  scrollsAlt: "A shelf of rolled scrolls painted in ink; three lie pulled forward", // DRAFT
  healthAlt:
    "Three small ink paintings: an oil lamp with a gold flame, three balanced stones, and California poppies", // DRAFT
  sceneAlts: [
    "An oil lamp with a gold flame, painted in ink", // DRAFT
    "Three balanced stones, painted in ink", // DRAFT
    "California poppies, painted in ink", // DRAFT
  ],
  mugsAlt: "Two mugs on a low wooden table, steam rising, painted in ink", // DRAFT
  explainer: "Read a quick explainer",
  illustration: "Illustration",
};
```

- [ ] **Step 6: Write the route**

Replace `src/app/[locale]/science/page.tsx` with:

```tsx
import type { Metadata } from "next";
import { Ysabeau } from "next/font/google";
import { getTranslations, setRequestLocale } from "next-intl/server";
import { ProductPagesProvider } from "@/components/home/product-action";
import { SiteDialogs } from "@/components/ink/dialogs";
import { productPageLinks } from "@/components/product/catalog";
import { ScienceInk } from "@/components/science/ink/science-ink";
import copyKeys from "@/i18n/copy-keys.json";
import { redirect } from "@/i18n/navigation";

// Ysabeau, the homepage's title face (Mo, October 13, 2026), here for the Science page's titles as
// the other pages follow the homepage. Not preloaded, as on the homepage ([locale]/page.tsx).
const titles = Ysabeau({
  subsets: ["latin", "vietnamese"],
  variable: "--font-ysabeau",
  display: "swap",
  preload: false,
});

type Params = Promise<{ locale: string }>;

export async function generateMetadata({ params }: { params: Params }): Promise<Metadata> {
  const { locale } = await params;
  const translate = await getTranslations({ locale, namespace: "Copy" });
  return { title: `BiGH — ${translate(copyKeys["Science"])}` };
}

// The Science page in Ink & Gold, "the handscroll" (Mo, October 13-14, 2026; spec
// docs/superpowers/specs/2026-10-14-science-ink-design.md). /hken goes to Chinese: a [locale]
// page without this redirect fails the build's static render.
export default async function Page({ params }: { params: Params }) {
  const { locale } = await params;
  if (locale === "hken") redirect({ href: "/science", locale: "cns" });
  setRequestLocale(locale);

  return (
    <ProductPagesProvider pages={productPageLinks()}>
      <SiteDialogs>
        <ScienceInk fontClass={titles.variable} />
      </SiteDialogs>
    </ProductPagesProvider>
  );
}
```

- [ ] **Step 7: Write the page shell and the opening words**

Create `src/components/science/ink/science-ink.module.css`:

```css
/* The Science page in Ink & Gold, "the handscroll" (Mo, October 13-14, 2026; spec
   docs/superpowers/specs/2026-10-14-science-ink-design.md). Titles in Ysabeau, the homepage's title
   face; menus, words and pills stay in the kit's Switzer. The attribute outranks the kit's .look
   rule in either stylesheet order (as home-titles.module.css). */
.page[data-look="ink"] {
  --display-font: var(--font-ysabeau), var(--font-dm-sans), Arial, sans-serif;
}

.page[data-look="ink"] main :is(h1, h2, h3) {
  font-family: var(--display-font);
}

/* Small titles one step heavier in Latin scripts: Ysabeau's thin strokes read lighter than the
   words beside them (as on the homepage). */
.page[data-look="ink"] main h3:not(:lang(ko), :lang(ja), :lang(zh)) {
  font-weight: 600;
}

.opening {
  text-align: center;
}

.opening h1 {
  margin: 10px auto 0;
  max-width: 22ch;
  font-size: clamp(34px, 3.9vw, 58px);
  font-weight: 500;
  line-height: 1.04;
  letter-spacing: -0.012em;
  text-wrap: balance;
}

@media (min-width: 960px) {
  .opening h1 {
    max-width: none;
  }
}

.opening p:last-child {
  margin: 12px auto 0;
  max-width: 62ch;
}
```

Create `src/components/science/ink/opening.tsx`:

```tsx
"use client";

import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { ink, opening } from "../science-content";
import styles from "./science-ink.module.css";

/** The page's title block: "Science", the one h1, the film's two lines as its lead. */
export function OpeningWords() {
  const copy = useCopy();
  return (
    <header className={`${base.wrap} ${styles.opening}`}>
      <p className={base.caption}>{copy(opening.eyebrow)}</p>
      <h1 id="science-title">{copy(opening.title)}</h1>
      <p className={base.body}>{ink.lead.map((line) => copy(line)).join(" ")}</p>
    </header>
  );
}
```

Create `src/components/science/ink/science-ink.tsx` (the handscroll and the strips arrive in Tasks 3 and 4; until then the opening section holds only its words):

```tsx
"use client";

import { InkPage } from "@/components/ink/ink-page";
import { OpeningWords } from "./opening";
import { Formulas, Liu } from "./people";
import styles from "./science-ink.module.css";

/** The Science page: the handscroll, Dr. Liu, the formulas, the research, health explained and
 *  Ask BiGH Science, on the kit's paper with the shared menu bar and footer. */
export function ScienceInk({ fontClass }: { fontClass: string }) {
  return (
    <InkPage current="science" className={`${fontClass} ${styles.page}`}>
      {() => (
        <>
          <section id="scientists" aria-labelledby="science-title" style={{ paddingTop: 110 }}>
            <OpeningWords />
          </section>
          <Liu />
          <Formulas />
          <section id="research" />
          <section id="health" />
          <section id="ask" />
        </>
      )}
    </InkPage>
  );
}
```

The three empty sections keep the menu's anchors working until Task 4 fills them; Task 4 replaces them.

- [ ] **Step 8: Write Dr. Liu and the formulas**

Create `src/components/science/ink/people.module.css`:

```css
/* Dr. Liu and the formulas (spec, "The page" rows 2 and 3). */
.liu {
  padding-top: clamp(96px, 10vw, 150px);
}

.liuGrid {
  display: grid;
  gap: 36px;
}

@media (min-width: 960px) {
  .liuGrid {
    grid-template-columns: 300px minmax(0, 1fr);
    gap: 72px;
    align-items: center;
  }
}

/* The one shadow (DESIGN.md): the real photograph on its paper mat. */
.mount {
  width: min(300px, 70vw);
  margin: 0;
  padding: 14px 14px 16px;
  background: #fbf9f4;
  box-shadow:
    0 1px 2px rgba(28, 27, 25, 0.1),
    0 10px 28px -12px rgba(28, 27, 25, 0.28);
}

.mount img {
  display: block;
  width: 100%;
  height: auto;
}

.name {
  margin: 8px 0 0;
  font-size: clamp(40px, 3.6vw, 52px);
  font-weight: 500;
  line-height: 1.04;
}

.headline {
  margin: 14px 0 0;
  color: var(--ink);
  font-size: 21px;
  line-height: 1.4;
}

.intro {
  margin-top: 10px;
  max-width: 640px;
}

.numbers {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 190px));
  gap: 32px;
  margin: 30px 0 0;
}

.numbers dt {
  font-family: var(--display-font);
  font-size: clamp(44px, 4vw, 60px);
  font-weight: 500;
  line-height: 1;
  letter-spacing: -0.02em;
  color: var(--ink);
}

.numbers dd {
  margin: 10px 0 0;
  color: var(--muted);
  font-size: 15px;
  line-height: 1.4;
}

.numbers dd a {
  display: inline-block;
  margin-top: 4px;
  color: var(--ink);
}

.story {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 48px;
  margin-top: 22px;
  padding: 0;
  border: 0;
  background: none;
  font: inherit;
  font-size: 19px;
  cursor: pointer;
}

.formulas {
  padding-top: clamp(96px, 10vw, 150px);
}

.head {
  display: grid;
  gap: 18px;
}

@media (min-width: 960px) {
  .head {
    grid-template-columns: minmax(0, 1.15fr) minmax(0, 0.85fr);
    gap: 72px;
    align-items: end;
  }
}

.title {
  margin: 12px 0 0;
  font-size: clamp(32px, 3.4vw, 50px);
  font-weight: 500;
  line-height: 1.06;
  text-wrap: balance;
}

.bottles {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 40px 20px;
  margin: 56px 0 0;
  padding: 0;
  list-style: none;
}

@media (min-width: 960px) {
  .bottles {
    grid-template-columns: repeat(5, minmax(0, 1fr));
    align-items: end;
  }
}

.bottles li {
  text-align: center;
}

.bottleLink {
  display: block;
  color: var(--ink);
  text-decoration: none;
}

.bottleLink img {
  display: block;
  width: auto;
  height: clamp(150px, 14vw, 200px);
  margin: 0 auto;
  transition: transform var(--breath) var(--ease);
}

.bottles li[data-lead] .bottleLink img {
  height: clamp(170px, 16.5vw, 240px);
}

.bottleLink:hover img {
  transform: translateY(-4px);
}

.bottleName {
  display: block;
  margin-top: 20px;
  font-family: var(--display-font);
  font-size: 24px;
  font-weight: 600;
  line-height: 1.15;
}

.credit {
  margin: 8px 0 0;
  color: var(--muted);
  font-size: 15px;
  line-height: 1.45;
}

@media (prefers-reduced-motion: reduce) {
  .bottleLink img {
    transition: none;
  }
}
```

Create `src/components/science/ink/people.tsx`:

```tsx
"use client";

import Image from "next/image";
import { ArrowRight, ArrowUpRight } from "lucide-react";
import { useProductPage } from "@/components/home/product-action";
import { useSiteDialogs } from "@/components/ink/dialogs";
import base from "@/components/ink/ink.module.css";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { formulas, formulasLine, ink, iris, liu, liuNumbers } from "../science-content";
import styles from "./people.module.css";

const BOTTLE = { width: 1230, height: 1278 };

/** Dr. Liu: his real photograph on its mat, his record with its sources, his story sheet. */
export function Liu() {
  const copy = useCopy();
  const dialogs = useSiteDialogs();
  return (
    <section id="liu" className={styles.liu} aria-labelledby="liu-name">
      <div className={`${base.wrap} ${styles.liuGrid}`}>
        <figure className={styles.mount}>
          <Image
            src={liu.photo.src}
            width={liu.photo.width}
            height={liu.photo.height}
            alt={copy(liu.name)}
            sizes="(max-width: 959px) 70vw, 300px"
          />
        </figure>
        <div>
          <p className={base.caption}>{copy(liu.role)}</p>
          <h2 id="liu-name" className={styles.name}>
            {copy(liu.name)}
          </h2>
          <p className={styles.headline}>{copy(liu.headline)}</p>
          <p className={`${base.body} ${styles.intro}`}>{copy(liu.intro)}</p>
          <dl className={styles.numbers}>
            {liuNumbers.map((n) => (
              <div key={n.value}>
                <dt>
                  {n.value}
                  {n.suffix}
                </dt>
                <dd>
                  {copy(n.label)}{" "}
                  <a href={n.url} target="_blank" rel="noreferrer">
                    {copy(ink.source)} <ArrowUpRight size={14} aria-hidden="true" />
                  </a>
                </dd>
              </div>
            ))}
          </dl>
          <button
            type="button"
            className={`${base.textLink} ${styles.story}`}
            onClick={dialogs.openScientist}
          >
            {copy(liu.button)} <ArrowRight size={18} aria-hidden="true" />
          </button>
        </div>
      </div>
    </section>
  );
}

/** The five formulas: who developed each one, each bottle linking to its own page. */
export function Formulas() {
  const copy = useCopy();
  const pageOf = useProductPage();
  return (
    <section id="formulas" className={styles.formulas} aria-labelledby="formulas-title">
      <div className={base.wrap}>
        <header className={styles.head}>
          <div>
            <p className={base.caption}>{copy(ink.formulasLabel)}</p>
            <h2 id="formulas-title" className={styles.title}>
              {copy(formulasLine)}
            </h2>
          </div>
          <p className={base.body}>{copy(iris.text)}</p>
        </header>
        <ul className={styles.bottles}>
          {formulas.map((formula, index) => {
            const href = pageOf(formula.name);
            const body = (
              <>
                <Image
                  src={formula.image}
                  width={BOTTLE.width}
                  height={BOTTLE.height}
                  alt=""
                  sizes="(max-width: 959px) 40vw, 240px"
                />
                <span className={styles.bottleName}>{copy(formula.name)}</span>
              </>
            );
            return (
              <li key={formula.name} data-lead={index === 0 ? "" : undefined}>
                {href ? (
                  <Link href={href} className={styles.bottleLink}>
                    {body}
                  </Link>
                ) : (
                  <div className={styles.bottleLink}>{body}</div>
                )}
                <p className={styles.credit}>{copy(formula.credit)}</p>
              </li>
            );
          })}
        </ul>
      </div>
    </section>
  );
}
```

- [ ] **Step 9: Run the static checks and the QA**

Run: `npm run type-check && npx eslint src/components/science src/app && npx prettier --write src/components/science src/app/[locale]/science scripts/qa/qa_science_ink.py`
Expected: no errors.

Run: `python -X utf8 scripts/qa/qa_science_ink.py http://localhost:3050 --only=shell,people`
Expected: every line `PASS` except `shell … title in Ysabeau` may need a reload of the dev server after the route change (restart the preview if the route still shows the film: a new or replaced route needs a restart, per memory).

- [ ] **Step 10: Look at it**

Take screenshots at 1440x900 and 390x844 of the top of the page and of `#liu`/`#formulas` (Playwright, viewport shots, not full page) and look at them full size: the title one line at 1440, the photo on its mat, the bottles in one row at 1440 and two by two on the phone.

- [ ] **Step 11: Commit**

```bash
git add -A src/app/[locale]/science src/components/science scripts/qa/qa_science_ink.py reference/science-page public/images/science-page
git commit -m "feat(science): the ink page's route and shell, Dr. Liu and the formulas; the film page retires to reference/

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: The handscroll

**Files:**

- Create: `src/components/science/ink/journey.tsx`, `journey.module.css`, `use-journey.ts`
- Modify: `src/components/science/ink/science-ink.tsx` (the opening section becomes `<Journey motion={motion} />`)
- Modify: `scripts/qa/qa_science_ink.py` (sections `journey`, `still`, `multiply`)

**Interfaces:**

- Consumes: `scienceArt.scroll` (Task 1), `OpeningWords` (Task 2), `pathStops` and `ink` from `science-content.ts`.
- Produces: `Journey({ motion }: { motion: boolean })`; `useJourney(section: RefObject<HTMLElement | null>, motion: boolean, at: readonly number[]): void`. DOM contract the QA reads: `section#scientists[data-now]` (index of the stop in view), `[data-pin]` (the sticky blend group), `[data-band]`, `img[data-painting]`, `li[data-stop="0..4"]`; CSS custom properties `--x` and `--walked` on the section.

- [ ] **Step 1: Write the failing QA sections**

Add to `scripts/qa/qa_science_ink.py`, before `SECTIONS`:

```python
STACKING = """el => {
  // Each element from the blend group's parent up to the page root that makes a stacking context
  // (a white box where the paper should show: the footer crane's trap).
  const found = [];
  for (let e = el.parentElement; e && !e.matches('[data-look="ink"]'); e = e.parentElement) {
    const s = getComputedStyle(e);
    const why = [];
    if (s.transform !== 'none') why.push('transform');
    if (Number(s.opacity) < 1) why.push('opacity');
    if (s.filter !== 'none') why.push('filter');
    if (s.maskImage && s.maskImage !== 'none') why.push('mask');
    if (s.isolation === 'isolate') why.push('isolation');
    if (s.mixBlendMode !== 'normal') why.push('blend');
    if (s.position !== 'static' && s.zIndex !== 'auto') why.push('z-index');
    if (['fixed', 'sticky'].includes(s.position)) why.push(s.position);
    if (s.willChange && s.willChange !== 'auto') why.push('will-change');
    if (/paint|layout|strict|content/.test(s.contain)) why.push('contain');
    if (why.length) found.push((e.tagName + '.' + e.className).slice(0, 60) + ': ' + why.join(','));
  }
  return found;
}"""

STATE = """() => {
  const s = document.querySelector('#scientists');
  const band = s.querySelector('[data-band]').getBoundingClientRect();
  const img = s.querySelector('[data-painting]').getBoundingClientRect();
  const pin = s.querySelector('[data-pin]').getBoundingClientRect();
  return { now: Number(s.dataset.now), pinTop: pin.top, pinBottom: pin.bottom,
           imgLeft: img.left, imgRight: img.right, bandLeft: band.left, bandRight: band.right,
           innerHeight, scrollY, sectionBottom: s.getBoundingClientRect().bottom };
}"""


def journey(browser):
    for w, h, lang in [(1440, 900, "en"), (1280, 720, "en"), (1280, 720, "vn"), (390, 844, "en")]:
        ctx, page, _, errors = opened(browser, w, h, path=f"/{lang}/science")
        page.wait_for_timeout(1200)
        start = page.evaluate(STATE)
        check(f"journey {w}x{h} {lang}: starts at Okayama", start["now"] == 0, str(start["now"]))
        check(f"journey {w}x{h} {lang}: pin fits the window", start["pinBottom"] <= h + 1, f"{start['pinBottom']:.0f} > {h}")
        travel = page.evaluate("() => { const s = document.querySelector('#scientists'); return s.offsetHeight - s.querySelector('[data-pin]').offsetHeight; }")
        check(f"journey {w}x{h} {lang}: room to travel", travel > w, f"{travel}px")
        seen = []
        for step in range(0, 11):
            page.evaluate(f"window.scrollTo(0, {travel * step / 10})")
            page.wait_for_timeout(250)
            st = page.evaluate(STATE)
            seen.append(st["now"])
            if 0 < step < 10:
                check(f"journey {w}x{h} {lang} {step}/10: pinned", abs(st["pinTop"] - start["pinTop"]) < 2, f"{st['pinTop']:.0f}")
                check(f"journey {w}x{h} {lang} {step}/10: painting covers the band", st["imgLeft"] <= st["bandLeft"] + 1 and st["imgRight"] >= st["bandRight"] - 1)
        check(f"journey {w}x{h} {lang}: stops in order, Okayama to Today", seen == sorted(seen) and seen[0] == 0 and seen[-1] == 4, str(seen))
        end = page.evaluate(STATE)
        check(f"journey {w}x{h} {lang}: the painting's end in view at the end", abs(end["imgRight"] - end["bandRight"]) < 3, f"{end['imgRight']:.0f} vs {end['bandRight']:.0f}")
        page.evaluate(f"window.scrollTo(0, {travel + 400})")
        page.wait_for_timeout(300)
        after = page.evaluate(STATE)
        check(f"journey {w}x{h} {lang}: lets go after Today", after["pinTop"] < start["pinTop"] - 100, f"{after['pinTop']:.0f}")
        page.evaluate(f"window.scrollTo(0, {travel * 0.5})")
        page.wait_for_timeout(300)
        page.screenshot(path=str(OUT / f"journey-{w}x{h}-{lang}-half.png"))
        if w == 1440:
            page.set_viewport_size({"width": 1024, "height": 768})
            page.wait_for_timeout(600)
            st = page.evaluate(STATE)
            check("journey resize 1440→1024 half way: painting still covers the band", st["imgLeft"] <= st["bandLeft"] + 1 and st["imgRight"] >= st["bandRight"] - 1)
        check(f"journey {w}x{h} {lang}: no console errors", not errors, "; ".join(errors[:3]))
        ctx.close()


def still(browser):
    for label, kwargs in [("reduced motion", {"reduced": True}), ("no script", {"js": False})]:
        for w, h in [(1440, 900), (390, 844)]:
            ctx, page, _, _ = opened(browser, w, h, **kwargs)
            page.wait_for_timeout(800)
            pin = page.evaluate("getComputedStyle(document.querySelector('[data-pin]')).position")
            check(f"still {label} {w}: nothing pins", pin == "static", pin)
            room = page.evaluate("document.querySelector('#scientists [data-room]').offsetHeight")
            check(f"still {label} {w}: no travel room", room == 0, str(room))
            visible = page.evaluate("[...document.querySelectorAll('#scientists li[data-stop] p')].map(p => getComputedStyle(p).visibility === 'visible' && getComputedStyle(p).display !== 'none' && p.getBoundingClientRect().height > 0)")
            check(f"still {label} {w}: all five stops readable", visible == [True] * 5, str(visible))
            band = page.evaluate("getComputedStyle(document.querySelector('[data-band]')).overflowX")
            check(f"still {label} {w}: the band scrolls sideways", band == "auto", band)
            shown = page.evaluate("getComputedStyle(document.querySelector('[data-painting]')).filter")
            check(f"still {label} {w}: the painting crisp", shown in ("none",), shown)
            page.screenshot(path=str(OUT / f"still-{label.replace(' ', '-')}-{w}.png"))
            ctx.close()


def multiply(browser):
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, _, _ = opened(browser, w, h, reduced=True)
        pin = page.locator("[data-pin]")
        check(f"multiply {w}: the pin is the scroll's blend group", pin.evaluate("e => getComputedStyle(e).mixBlendMode") == "multiply")
        found = pin.evaluate(STACKING)
        check(f"multiply {w}: nothing between the pin and the paper", not found, "; ".join(found))
        for img in page.locator("main figure[data-picture] img, main [data-scene] img").all():
            found = img.evaluate(STACKING)
            check(f"multiply {w}: {img.get_attribute('src')[:50]} sits on the paper", not found, "; ".join(found))
        ctx.close()
```

and extend `SECTIONS`:

```python
SECTIONS = {"shell": shell, "people": people, "journey": journey, "still": still, "multiply": multiply}
```

Run: `python -X utf8 scripts/qa/qa_science_ink.py http://localhost:3050 --only=journey,still,multiply`
Expected: FAIL (`[data-pin]` not found).

- [ ] **Step 2: Write the hook**

Create `src/components/science/ink/use-journey.ts`:

```ts
"use client";

import { useEffect, type RefObject } from "react";

/**
 * The handscroll's travel (spec, "The handscroll"). The room after the pinned box (journey.module.css)
 * is as tall as the painting's overflow, so the page is already as tall as the travel before any
 * script runs;
 * this hook only reads the scroll position. While the pinned box is stuck under the menu bar, one
 * pixel scrolled down moves the painting one pixel left. Writes on the section: --x (px moved),
 * --walked (px of the line inked, up to the stop in view) and data-now (that stop's index). The stop
 * in view is the one nearest a reading point that moves from 15% to 85% of the band as the painting
 * travels, so the first stop is current at the start and the last at the end. On a short window it
 * also shrinks the painting (--band-h) until the pinned box fits under the menu bar. Reduced motion:
 * nothing runs; the stylesheet shows the still scroll.
 */
export function useJourney(
  section: RefObject<HTMLElement | null>,
  motion: boolean,
  at: readonly number[],
) {
  useEffect(() => {
    const root = section.current;
    const pin = root?.querySelector<HTMLElement>("[data-pin]");
    const band = root?.querySelector<HTMLElement>("[data-band]");
    const painting = root?.querySelector<HTMLImageElement>("[data-painting]");
    if (!root || !pin || !band || !painting || !motion) return;
    let travel = 0;
    let width = 0;
    let start = 0;
    let frame = 0;
    let now = -1;

    const update = () => {
      frame = 0;
      const p = Math.min(1, Math.max(0, (window.scrollY - start) / Math.max(1, travel)));
      const x = p * travel;
      const read = x + (0.15 + 0.7 * p) * band.clientWidth;
      let best = 0;
      at.forEach((f, i) => {
        if (Math.abs(f * width - read) < Math.abs(at[best] * width - read)) best = i;
      });
      root.style.setProperty("--x", `${x.toFixed(1)}px`);
      root.style.setProperty("--walked", `${Math.max(0, at[best] * width - x).toFixed(1)}px`);
      if (best !== now) {
        now = best;
        root.dataset.now = String(best);
      }
    };
    const schedule = () => {
      if (!frame) frame = requestAnimationFrame(update);
    };
    const fit = () => {
      // The pinned box must fit between the menu bar and the window's foot: a long title (vn, kr)
      // or a short window takes the room from the painting, never from the words.
      root.style.removeProperty("--band-h");
      const pinTop = parseFloat(getComputedStyle(pin).top) || 0;
      const over = pin.getBoundingClientRect().height + pinTop + 12 - window.innerHeight;
      if (over > 0) {
        const h = Math.max(180, painting.getBoundingClientRect().height - over);
        root.style.setProperty("--band-h", `${h}px`);
      }
    };
    const measure = () => {
      fit();
      width = painting.getBoundingClientRect().width;
      travel = Math.max(0, width - band.clientWidth);
      const pinTop = parseFloat(getComputedStyle(pin).top) || 0;
      const padTop = parseFloat(getComputedStyle(root).paddingTop) || 0;
      start = root.getBoundingClientRect().top + window.scrollY + padTop - pinTop;
      update();
    };
    const resize = new ResizeObserver(() => measure());
    resize.observe(band);
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", measure);
    measure();
    return () => {
      resize.disconnect();
      window.removeEventListener("scroll", schedule);
      window.removeEventListener("resize", measure);
      if (frame) cancelAnimationFrame(frame);
      root.style.removeProperty("--x");
      root.style.removeProperty("--walked");
      root.style.removeProperty("--band-h");
    };
  }, [section, motion, at]);
}
```

- [ ] **Step 3: Write the handscroll's styles**

Create `src/components/science/ink/journey.module.css`:

```css
/* The handscroll (Mo, October 13-14, 2026; spec "The handscroll"). The pinned box holds the title,
   the painting and its stops; it is the painting's blend group (multiply), so the painting can move
   inside it (transform) without a white box. The room after it is as tall as the painting's
   overflow (padding % = the containing block's width = the band's width): one pixel scrolled down,
   one pixel of painting, with the page's full height set before any script runs. A sticky box does
   not stay pinned through its parent's own bottom padding (tested October 14), hence a child. */
.journey {
  --pin-top: 76px;
  --band-h: clamp(220px, 38svh, 300px);
  position: relative;
  padding-top: var(--pin-top);
}

.room {
  padding-bottom: max(0px, calc(var(--band-h) * var(--ratio) - 100%));
}

@media (min-width: 960px) {
  .journey {
    --pin-top: 96px;
    --band-h: clamp(240px, calc(100svh - 440px), 430px);
  }
}

.pin {
  position: sticky;
  top: var(--pin-top);
  display: grid;
  gap: 22px;
  mix-blend-mode: multiply;
}

/* The painting's window: its two ends fade into the paper, so it unrolls from mist. */
.band {
  position: relative;
  overflow: hidden;
  -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 6%, #000 94%, transparent 100%);
  mask-image: linear-gradient(90deg, transparent 0, #000 6%, #000 94%, transparent 100%);
}

.painting {
  display: block;
  width: auto;
  max-width: none;
  height: var(--band-h);
  transform: translate3d(calc(-1 * var(--x, 0px)), 0, 0);
}

/* The stops under their places, moving with the painting (from 960px). */
.track {
  position: relative;
  overflow: hidden;
  min-height: 170px;
}

.rail {
  position: absolute;
  top: 7px;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--hair);
}

.rail span {
  position: absolute;
  top: -1px;
  left: 0;
  width: var(--walked, 0px);
  height: 3px;
  background: var(--ink);
}

.stops {
  position: relative;
  width: calc(var(--band-h) * var(--ratio));
  margin: 0;
  padding: 0;
  list-style: none;
  transform: translate3d(calc(-1 * var(--x, 0px)), 0, 0);
}

.stops li {
  position: absolute;
  top: 0;
  left: calc(var(--at) * 100%);
  width: 230px;
  margin-left: -115px;
  text-align: center;
}

.dot {
  display: block;
  width: 15px;
  height: 15px;
  margin: 0 auto 14px;
  border: 1.5px solid var(--muted);
  border-radius: 50%;
  background: #fff;
}

.mark {
  display: block;
  color: var(--muted);
  font-size: 17px;
  font-weight: 500;
}

.stopTitle {
  margin: 4px 0 0;
  color: var(--muted);
  font-size: 22px;
  line-height: 1.2;
}

.stopText {
  margin: 6px 0 0;
  color: var(--muted);
  font-size: 15px;
  line-height: 1.45;
  visibility: hidden;
}

.stopText a {
  color: var(--ink);
}

/* The stop in view: its dot inked, its words in ink, its sentence shown. */
.journey[data-now="0"] [data-stop="0"],
.journey[data-now="1"] [data-stop="1"],
.journey[data-now="2"] [data-stop="2"],
.journey[data-now="3"] [data-stop="3"],
.journey[data-now="4"] [data-stop="4"] {
  --stop-ink: var(--ink);
}

.stops li .mark,
.stops li .stopTitle {
  color: var(--stop-ink, var(--muted));
}

.journey[data-now="0"] [data-stop="0"] .stopText,
.journey[data-now="1"] [data-stop="1"] .stopText,
.journey[data-now="2"] [data-stop="2"] .stopText,
.journey[data-now="3"] [data-stop="3"] .stopText,
.journey[data-now="4"] [data-stop="4"] .stopText {
  visibility: visible;
}

.journey[data-now="0"] [data-stop="0"] .dot,
.journey[data-now="1"] [data-stop="1"] .dot,
.journey[data-now="2"] [data-stop="2"] .dot,
.journey[data-now="3"] [data-stop="3"] .dot,
.journey[data-now="4"] [data-stop="4"] .dot {
  width: 19px;
  height: 19px;
  margin-top: -2px;
  margin-bottom: 12px;
  border-color: var(--ink);
  background: var(--ink);
}

.dots {
  display: none;
}

.foot {
  display: flex;
  justify-content: space-between;
  gap: 16px;
}

.hint {
  color: var(--muted);
  font-size: 17px;
}

/* Phones and tablets: the stops do not travel; five dots show where you are, and the stop in view
   shows its words under them. */
@media (max-width: 959px) {
  .track {
    min-height: 0;
    overflow: visible;
  }

  .rail {
    display: none;
  }

  .stops {
    width: auto;
    transform: none;
  }

  .stops li {
    position: static;
    display: none;
    width: auto;
    margin: 0;
    text-align: left;
  }

  .stops li .dot {
    display: none;
  }

  .journey[data-now="0"] [data-stop="0"],
  .journey[data-now="1"] [data-stop="1"],
  .journey[data-now="2"] [data-stop="2"],
  .journey[data-now="3"] [data-stop="3"],
  .journey[data-now="4"] [data-stop="4"] {
    display: block;
  }

  .dots {
    display: flex;
    gap: 10px;
    align-items: center;
  }

  .dots i {
    width: 12px;
    height: 12px;
    border: 1.5px solid var(--muted);
    border-radius: 50%;
    background: #fff;
  }

  .journey[data-now="0"] .dots i:nth-child(1),
  .journey[data-now="1"] .dots i:nth-child(2),
  .journey[data-now="2"] .dots i:nth-child(3),
  .journey[data-now="3"] .dots i:nth-child(4),
  .journey[data-now="4"] .dots i:nth-child(5) {
    border-color: var(--ink);
    background: var(--ink);
  }
}

/* Reduced motion, and a page whose script never runs: nothing pins or moves. The band scrolls
   sideways under the visitor's own hand, and all five stops are read in a row (a list on phones).
   :global([data-look]) outranks the kit's bloom rules whatever order they load in. */
@media (prefers-reduced-motion: reduce), (scripting: none) {
  .room {
    display: none;
  }

  .pin {
    position: static;
  }

  .band {
    overflow-x: auto;
    overscroll-behavior-x: contain;
  }

  .painting,
  .stops {
    transform: none;
  }

  :global([data-look="ink"]) .painting[data-bloom] {
    -webkit-mask: none;
    mask: none;
    filter: none;
  }

  .rail,
  .dots,
  .hint {
    display: none;
  }

  .stops {
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 24px;
    width: auto;
  }

  .stops li,
  .journey .stops li {
    position: static;
    display: block;
    width: auto;
    margin: 0;
  }

  .stops li .stopText {
    visibility: visible;
  }

  .stops li .mark,
  .stops li .stopTitle {
    color: var(--ink);
  }
}

@media (max-width: 959px) and (prefers-reduced-motion: reduce),
  (max-width: 959px) and (scripting: none) {
  .stops {
    grid-template-columns: 1fr;
  }
}
```

- [ ] **Step 4: Write the handscroll**

Create `src/components/science/ink/journey.tsx`:

```tsx
"use client";

import { useRef, type CSSProperties } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { ink, pathStops } from "../science-content";
import { OpeningWords } from "./opening";
import { scienceArt } from "./science-art";
import { useJourney } from "./use-journey";
import styles from "./journey.module.css";

const ART = scienceArt.scroll;
const AT = [
  ART.stops.okayama,
  ART.stops.berkeley,
  ART.stops.y2002,
  ART.stops.salzburg,
  ART.stops.today,
] as const;

/**
 * The handscroll (Mo, October 13-14, 2026): the title, then Dr. Liu's path as one ink painting
 * that travels sideways while the page scrolls down (Okayama, the ocean, Berkeley, Salzburg,
 * California under a gold sun), its five stops under their places. Phones get a shorter picture
 * (the same painting, 400px tall). Reduced motion and no script: the still scroll.
 */
export function Journey({ motion }: { motion: boolean }) {
  const copy = useCopy();
  const section = useRef<HTMLElement>(null);
  useJourney(section, motion, AT);
  return (
    <section
      ref={section}
      id="scientists"
      className={styles.journey}
      data-now="0"
      aria-labelledby="science-title"
      style={{ "--ratio": ART.width / ART.height } as CSSProperties}
    >
      <div className={styles.pin} data-pin="">
        <OpeningWords />
        <div
          className={styles.band}
          data-band=""
          tabIndex={motion ? undefined : 0}
          aria-label={motion ? undefined : copy(ink.scrollStill)}
        >
          <picture>
            <source
              media="(max-width: 959px)"
              srcSet={ART.phone.src}
              width={ART.phone.width}
              height={ART.phone.height}
            />
            {/* eslint-disable-next-line @next/next/no-img-element -- wider than next/image serves (3840px) */}
            <img
              className={styles.painting}
              data-painting=""
              src={ART.src}
              width={ART.width}
              height={ART.height}
              alt={copy(ink.scrollAlt)}
              fetchPriority="high"
              decoding="async"
              data-bloom="waiting"
            />
          </picture>
        </div>
        <div className={`${base.wrap} ${styles.foot}`} style={{ maxWidth: "none" }}>
          <div className={styles.dots} aria-hidden="true">
            <i />
            <i />
            <i />
            <i />
            <i />
          </div>
          <p className={styles.hint} aria-hidden="true">
            {copy(ink.scrollHint)}
          </p>
          <p className={base.caption}>{copy(ink.illustration)}</p>
        </div>
        <div className={styles.track}>
          <div className={styles.rail} aria-hidden="true">
            <span />
          </div>
          <ol className={styles.stops}>
            {pathStops.map((stop, i) => (
              <li key={stop.mark} data-stop={i} style={{ "--at": AT[i] } as CSSProperties}>
                <i className={styles.dot} aria-hidden="true" />
                <span className={styles.mark}>{copy(stop.mark)}</span>
                <h3 className={styles.stopTitle}>{copy(stop.title)}</h3>
                <p className={styles.stopText}>
                  {copy(stop.text)}{" "}
                  {stop.url ? (
                    <a href={stop.url} target="_blank" rel="noreferrer">
                      {copy(stop.link)}
                    </a>
                  ) : null}
                </p>
              </li>
            ))}
          </ol>
        </div>
      </div>
      <div className={styles.room} data-room="" aria-hidden="true" />
    </section>
  );
}
```

In `science-ink.tsx`, replace the opening `<section id="scientists" …>…</section>` with `<Journey motion={motion} />`, change `{() => (` to `{(motion) => (`, add `import { Journey } from "./journey";`, and remove the now-unused `OpeningWords` import.

- [ ] **Step 5: Run the QA**

Run: `npm run type-check && npx eslint src/components/science && npx prettier --write src/components/science scripts/qa/qa_science_ink.py`
Run: `python -X utf8 scripts/qa/qa_science_ink.py http://localhost:3050 --only=shell,journey,still,multiply`
Expected: every line `PASS`. If `pin fits the window` fails at 1280x720 vn, the `fit()` step is not reaching the painting: check `--band-h` on the section in the browser.

- [ ] **Step 6: Look at it like a visitor**

Open the page in a real browser window at 1440x900 (Playwright headed or the preview tool) and scroll from the top to Dr. Liu slowly. Then look at the `journey-*-half.png` and `still-*.png` shots full size. It must read as one painting unrolling: no white box, no seam, the dots under their places, the line inking up to the stop in view, the sun at the end. Score it out of 10 and write the score and the two weakest things in the commit message body.

- [ ] **Step 7: Commit**

```bash
git add src/components/science/ink scripts/qa/qa_science_ink.py
git commit -m "feat(science): the handscroll travels from Okayama to Today as the page scrolls

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: The research, health explained and Ask BiGH Science

**Files:**

- Create: `src/components/science/ink/strip.tsx`, `strip.module.css`, `explore.tsx`, `explore.module.css`
- Modify: `src/components/science/ink/science-ink.tsx` (the three empty sections become `<Research />`, `<Health />`, `<Ask />`)
- Modify: `scripts/qa/qa_science_ink.py` (section `strips`)

**Interfaces:**

- Consumes: `scienceArt.scrolls`, `.health`, `.mugs` (Task 1); `research`, `health`, `ask`, `ink` from `science-content.ts`; `researchItems` from `@/components/home/research-data`; `useSiteDialogs().openArticle(index)`.
- Produces: `Strip(props)` in `strip.tsx`; `Research()`, `Health()`, `Ask()` in `explore.tsx`.

- [ ] **Step 1: Write the failing QA section**

Add to `scripts/qa/qa_science_ink.py`, before `SECTIONS`:

```python
def strips(browser):
    for w, h in [(1440, 900), (390, 844)]:
        ctx, page, _, errors = opened(browser, w, h)
        for part in ["research", "health", "ask"]:
            bring(page, f"#{part}")
            page.wait_for_timeout(500)
            check(f"strips {w} {part}: its title", page.locator(f"#{part} h2").count() == 1)
            pics = page.locator(f"#{part} img")
            shown = [p for p in pics.all() if p.is_visible()]
            check(f"strips {w} {part}: a painting shows", len(shown) >= 1, str(len(shown)))
            for img in shown:
                ok = img.evaluate("i => i.complete && i.naturalWidth > 0")
                check(f"strips {w} {part}: {img.get_attribute('alt')[:40]} loaded", ok)
        if w == 390:
            scenes = page.locator("#health [data-scene] img")
            check("strips 390 health: one scene over each article", scenes.count() == 3 and all(s.is_visible() for s in scenes.all()))
        text = page.locator("#research").inner_text()
        for title in ["Mitochondrial nutrients and the aging cell", "Dr. Liu on lipoic acid and the aging brain", "Healthy aging has many moving parts"]:
            check(f"strips {w} research: {title}", title in text)
        check(f"strips {w} research: the honesty line", "do not establish the effects of a finished BiGH product" in text)
        rows_before = page.locator("#research details").count()
        page.get_by_role("button", name=re.compile(r"See all 36 sources")).click()
        page.wait_for_timeout(500)
        rows_after = page.locator("#research details").count()
        check(f"strips {w} research: the full list opens (36)", rows_before == 0 and rows_after == 36, f"{rows_before} → {rows_after}")
        page.get_by_role("button", name=re.compile(r"Show fewer sources")).click()
        page.wait_for_timeout(300)
        check(f"strips {w} research: and closes", page.locator("#research details").count() == 0)
        buttons = page.locator("#health button")
        check(f"strips {w} health: three explainers", buttons.count() == 3)
        buttons.nth(1).click()
        page.wait_for_timeout(700)
        check(f"strips {w} health: an explainer sheet opens", page.locator("dialog[open]").count() == 1)
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)
        ask = page.locator("#ask").inner_text()
        for word in ["Ask BiGH Science", "In development", "not accepting submissions"]:
            check(f"strips {w} ask: {word}", word in ask)
        check(f"strips {w} ask: three numbered steps", page.locator("#ask ol > li").count() == 3)
        check(f"strips {w}: no console errors", not errors, "; ".join(errors[:3]))
        ctx.close()
```

and add `"strips": strips` to `SECTIONS` (after `people`).

Run: `python -X utf8 scripts/qa/qa_science_ink.py http://localhost:3050 --only=strips`
Expected: FAIL (`#research h2` not found).

- [ ] **Step 2: Write the strip**

Create `src/components/science/ink/strip.module.css`:

```css
/* One part below Dr. Liu (spec, "The page"): the header row (title left, lead right), one wide
   painting with soft ends, then the part's words. */
.strip {
  padding-top: clamp(96px, 10vw, 150px);
}

.head {
  display: grid;
  gap: 18px;
}

@media (min-width: 960px) {
  .head {
    grid-template-columns: minmax(0, 1.15fr) minmax(0, 0.85fr);
    gap: 72px;
    align-items: end;
  }
}

.title {
  margin: 12px 0 0;
  font-size: clamp(32px, 3.4vw, 50px);
  font-weight: 500;
  line-height: 1.06;
  text-wrap: balance;
}

.figure {
  position: relative;
  margin: 40px 0 0;
}

.art {
  display: block;
  width: 100%;
  height: auto;
  max-height: 380px;
  object-fit: contain;
  -webkit-mask-image: linear-gradient(90deg, transparent 0, #000 5%, #000 95%, transparent 100%);
  mask-image: linear-gradient(90deg, transparent 0, #000 5%, #000 95%, transparent 100%);
}

.figure figcaption {
  margin-top: 6px;
  text-align: right;
}

/* A strip with phone scenes instead (health): the wide painting from 960px only. */
.figure[data-wide-only] {
  display: none;
}

@media (min-width: 960px) {
  .figure[data-wide-only] {
    display: block;
  }
}
```

Create `src/components/science/ink/strip.tsx`:

```tsx
"use client";

import { getImageProps } from "next/image";
import type { ReactNode } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { ink } from "../science-content";
import styles from "./strip.module.css";

type Pic = { readonly src: string; readonly width: number; readonly height: number };

/**
 * One part below Dr. Liu: the header row, one wide painting (its phone crop under 960px, or no
 * painting under 960px at all with `wideOnly`, where the part shows its own scenes), then `children`.
 * The painting multiplies onto the page's paper (the kit's .ink) and blooms in as it arrives.
 */
export function Strip({
  id,
  label,
  title,
  lead,
  art,
  phone,
  alt,
  wideOnly = false,
  children,
}: {
  id: string;
  label: string;
  title: string;
  lead: string;
  art: Pic;
  phone?: Pic;
  alt: string;
  wideOnly?: boolean;
  children: ReactNode;
}) {
  const copy = useCopy();
  const common = { alt: copy(alt), sizes: "(max-width: 959px) 92vw, 1176px" };
  const wide = getImageProps({ ...common, src: art.src, width: art.width, height: art.height });
  const narrow = phone
    ? getImageProps({ ...common, src: phone.src, width: phone.width, height: phone.height })
    : null;
  return (
    <section id={id} className={styles.strip} aria-labelledby={`${id}-title`}>
      <div className={base.wrap}>
        <header className={styles.head}>
          <div>
            <p className={base.caption}>{copy(label)}</p>
            <h2 id={`${id}-title`} className={styles.title}>
              {copy(title)}
            </h2>
          </div>
          <p className={base.body}>{copy(lead)}</p>
        </header>
        <figure
          className={styles.figure}
          data-picture=""
          data-wide-only={wideOnly ? "" : undefined}
        >
          <picture>
            {narrow ? <source media="(max-width: 959px)" srcSet={narrow.props.srcSet} /> : null}
            {/* eslint-disable-next-line @next/next/no-img-element -- art direction through getImageProps */}
            <img
              {...wide.props}
              alt={common.alt}
              className={`${base.ink} ${styles.art}`}
              loading="lazy"
              data-bloom="waiting"
            />
          </picture>
          <figcaption className={base.caption}>{copy(ink.illustration)}</figcaption>
        </figure>
        {children}
      </div>
    </section>
  );
}
```

Before writing it, read `node_modules/next/dist/docs/` for `getImageProps` (art direction with `<picture>`) and adjust the call if the installed version's signature differs.

- [ ] **Step 3: Write the three parts**

Create `src/components/science/ink/explore.module.css`:

```css
/* The research, health explained and Ask BiGH Science: the words under each strip. */
.cols {
  display: grid;
  gap: 32px;
  margin: 36px 0 0;
  padding: 0;
  list-style: none;
}

@media (min-width: 960px) {
  .cols {
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 48px;
  }
}

.col {
  padding-top: 18px;
  border-top: 1px solid var(--hair);
}

.meta {
  margin: 0;
  color: var(--muted);
  font-size: 15px;
}

.colTitle {
  margin: 8px 0 0;
  font-size: 26px;
  line-height: 1.15;
}

.text {
  margin: 10px 0 0;
  color: var(--muted);
  font-size: 17px;
  line-height: 1.55;
}

.links {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  margin-top: 14px;
}

.go {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 44px;
  padding: 0;
  border: 0;
  background: none;
  color: var(--ink);
  font: inherit;
  font-size: 17px;
  cursor: pointer;
}

.tag {
  padding: 3px 12px;
  border: 1.5px solid var(--hair);
  border-radius: 999px;
  color: var(--muted);
  font-size: 15px;
}

.after {
  display: flex;
  flex-wrap: wrap;
  gap: 18px 28px;
  align-items: center;
  margin-top: 40px;
}

.note {
  max-width: 620px;
  margin: 0;
  color: var(--muted);
  font-size: 15px;
  line-height: 1.45;
}

.number {
  display: block;
  font-family: var(--display-font);
  font-size: 40px;
  font-weight: 500;
  line-height: 1;
}

.status {
  padding: 8px 18px;
  border: 1.5px solid var(--ink);
  border-radius: 999px;
  color: var(--ink);
  font-size: 17px;
}

/* Health on phones: each scene over its article (the wide strip shows from 960px). */
.scene {
  display: block;
  width: min(100%, 360px);
  height: auto;
  margin: 0 auto 18px;
}

@media (min-width: 960px) {
  .scene {
    display: none;
  }
}

/* The full list of sources. */
.groups {
  margin-top: 40px;
}

.group + .group {
  margin-top: 40px;
}

.groupTitle {
  margin: 0;
  font-size: 26px;
}

.row {
  border-bottom: 1px solid var(--line);
}

.row summary {
  display: grid;
  grid-template-columns: 4.5em minmax(0, 1fr) 28px;
  gap: 16px;
  align-items: baseline;
  min-height: 56px;
  padding: 14px 0;
  cursor: pointer;
  list-style: none;
}

.row summary::-webkit-details-marker {
  display: none;
}

.row[open] .plus {
  transform: rotate(45deg);
}

.plus {
  transition: transform calc(var(--breath) / 3) var(--ease);
}

.rowBody {
  padding: 0 0 18px 4.5em;
}

@media (prefers-reduced-motion: reduce) {
  .plus {
    transition: none;
  }
}
```

Create `src/components/science/ink/explore.tsx`:

```tsx
"use client";

import { ArrowRight, ArrowUpRight, Minus, Plus } from "lucide-react";
import Image from "next/image";
import { useState } from "react";
import { researchItems } from "@/components/home/research-data";
import { useSiteDialogs } from "@/components/ink/dialogs";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { ask, health, ink, research } from "../science-content";
import { scienceArt } from "./science-art";
import { Strip } from "./strip";
import styles from "./explore.module.css";

const KEY = research.key.map((url) => researchItems.find((item) => item.url === url)!);

/** The research: the scroll rack, the three key studies, then all 36 sources on request. */
export function Research() {
  const copy = useCopy();
  const [all, setAll] = useState(false);
  return (
    <Strip
      id="research"
      label={research.eyebrow}
      title={research.title}
      lead={research.text}
      art={scienceArt.scrolls}
      phone={scienceArt.scrolls.phone}
      alt={ink.scrollsAlt}
    >
      <ul className={styles.cols}>
        {KEY.map((item) => (
          <li key={item.url} className={styles.col}>
            <p className={styles.meta}>
              {copy(item.year)} · {copy(item.category)} · {item.journal}
            </p>
            <h3 className={styles.colTitle}>{copy(item.title)}</h3>
            <p className={styles.text}>{copy(item.text)}</p>
            <div className={styles.links}>
              <a className={styles.go} href={item.url} target="_blank" rel="noreferrer">
                {copy(ink.readStudy)} <ArrowUpRight size={16} aria-hidden="true" />
              </a>
              {research.byLiu.includes(item.url) ? (
                <span className={styles.tag}>{copy(research.tag)}</span>
              ) : null}
            </div>
          </li>
        ))}
      </ul>
      <div className={styles.after}>
        <button
          type="button"
          className={`${base.pill} ${base.pillGhost}`}
          aria-expanded={all}
          aria-controls="research-all"
          onClick={() => setAll(!all)}
        >
          {all ? copy(research.hideAll) : copy(research.seeAll, { count: researchItems.length })}
          {all ? <Minus size={18} aria-hidden="true" /> : <Plus size={18} aria-hidden="true" />}
        </button>
        <p className={styles.note}>{copy(research.note)}</p>
      </div>
      <div id="research-all" className={styles.groups} hidden={!all}>
        {all
          ? research.groups.map((group) => (
              <div key={group.type} className={styles.group}>
                <h3 className={styles.groupTitle}>{copy(group.title)}</h3>
                <p className={styles.text}>{copy(group.text)}</p>
                {researchItems
                  .filter((item) => item.type === group.type)
                  .map((item) => (
                    <details key={item.url} className={styles.row}>
                      <summary>
                        <span className={styles.meta}>{copy(item.year)}</span>
                        <span>
                          {copy(item.title)}
                          {research.byLiu.includes(item.url) ? (
                            <span className={styles.tag} style={{ marginLeft: 10 }}>
                              {copy(research.tag)}
                            </span>
                          ) : null}
                        </span>
                        <Plus className={styles.plus} size={22} aria-hidden="true" />
                      </summary>
                      <div className={styles.rowBody}>
                        <p className={styles.text}>{copy(item.text)}</p>
                        <a className={styles.go} href={item.url} target="_blank" rel="noreferrer">
                          {copy("Read original source")}{" "}
                          <ArrowUpRight size={16} aria-hidden="true" />
                        </a>
                      </div>
                    </details>
                  ))}
              </div>
            ))
          : null}
      </div>
    </Strip>
  );
}

/** Health explained: one painting of three scenes over the three articles (on phones, each scene
 *  over its own article); each opens the kit's short explainer sheet. */
export function Health() {
  const copy = useCopy();
  const dialogs = useSiteDialogs();
  return (
    <Strip
      id="health"
      label={health.eyebrow}
      title={health.title}
      lead={health.text}
      art={scienceArt.health}
      alt={ink.healthAlt}
      wideOnly
    >
      <ul className={styles.cols}>
        {health.doors.map((door, index) => {
          const scene = scienceArt.health.scenes[index];
          return (
            <li key={door.topic} className={styles.col} data-scene="">
              <Image
                className={`${base.ink} ${styles.scene}`}
                src={scene.src}
                width={scene.width}
                height={scene.height}
                alt={copy(ink.sceneAlts[index])}
                sizes="360px"
              />
              <p className={styles.meta}>{copy(door.topic)}</p>
              <h3 className={styles.colTitle}>{copy(door.title)}</h3>
              <p className={styles.text}>{copy(door.preview)}</p>
              <button
                type="button"
                className={styles.go}
                onClick={() => dialogs.openArticle(index)}
              >
                {copy(ink.explainer)} <ArrowRight size={16} aria-hidden="true" />
              </button>
            </li>
          );
        })}
      </ul>
    </Strip>
  );
}

/** Ask BiGH Science: two mugs on a table, the three steps, its status. */
export function Ask() {
  const copy = useCopy();
  return (
    <Strip
      id="ask"
      label={ask.eyebrow}
      title={ask.title}
      lead={`${copy(ask.lead)} ${copy(ask.text)}`}
      art={scienceArt.mugs}
      phone={scienceArt.mugs.phone}
      alt={ink.mugsAlt}
    >
      <ol className={styles.cols}>
        {ask.steps.map((step, index) => (
          <li key={step} className={styles.col}>
            <span className={styles.number}>{index + 1}</span>
            <p className={styles.text}>{copy(step)}</p>
          </li>
        ))}
      </ol>
      <div className={styles.after} style={{ paddingBottom: "clamp(96px, 10vw, 150px)" }}>
        <span className={styles.status}>{copy(ask.status)}</span>
        <p className={styles.note}>{copy(ask.note)}</p>
      </div>
    </Strip>
  );
}
```

Note: `Strip` passes `lead` through `copy()`; `Ask` hands it text that is already translated, which `copy()` returns unchanged (no key matches). In `science-ink.tsx` replace the three empty sections with `<Research />`, `<Health />`, `<Ask />` and import them from `./explore`.

The full list is rendered only when open: before it opens the page has no `details` rows, which the QA checks.

- [ ] **Step 4: Run the QA**

Run: `npm run type-check && npx eslint src/components/science && npx prettier --write src/components/science scripts/qa/qa_science_ink.py`
Run: `python -X utf8 scripts/qa/qa_science_ink.py http://localhost:3050 --only=shell,strips,multiply`
Expected: every line `PASS`.

- [ ] **Step 5: Look at it**

Viewport screenshots of `#research`, `#health` (and the open full list) and `#ask` at 1440x900, 1024x768 and 390x844; look at each full size. The three health scenes stand over their three columns from 960px; on the phone each scene sits over its article; no painting shows a box; the gold appears only in the lamp's flame.

- [ ] **Step 6: Commit**

```bash
git add src/components/science/ink scripts/qa/qa_science_ink.py
git commit -m "feat(science): the research, health explained and Ask BiGH Science as ink strips

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 5: Words in five languages

**Files:**

- Create: `reference/ink-pages/science/translations-science.cjs`
- Modify (generated by it): `src/i18n/copy-keys.json`, `messages/{en,cns,kr,vn,jp}.json`
- Modify: `scripts/qa/qa_science_ink.py` (section `languages`)

**Interfaces:**

- Consumes: the `ink` strings from Task 2.
- Produces: copy keys `m650` upward for the strings below.

- [ ] **Step 1: Write the failing QA section**

Add to `scripts/qa/qa_science_ink.py`, before `SECTIONS`:

```python
NEW_STRINGS = {
    "kr": ["계속 스크롤하세요", "연구 보기"],
    "jp": ["スクロールを続けると", "研究を読む"],
    "cns": ["继续向下滚动", "阅读研究"],
    "vn": ["Tiếp tục cuộn", "Đọc nghiên cứu"],
}


def languages(browser):
    for lang, words in NEW_STRINGS.items():
        ctx, page, response, errors = opened(browser, 1440, 900, path=f"/{lang}/science")
        check(f"languages {lang}: 200", response is not None and response.status == 200)
        text = page.locator("main").inner_text()
        for word in words:
            check(f"languages {lang}: {word}", word in text)
        overflow = page.evaluate("document.documentElement.scrollWidth - innerWidth")
        check(f"languages {lang}: no sideways scroll", overflow <= 0, str(overflow))
        check(f"languages {lang}: no console errors", not errors, "; ".join(errors[:3]))
        ctx.close()
```

and add `"languages": languages` to `SECTIONS`.

Run: `python -X utf8 scripts/qa/qa_science_ink.py http://localhost:3050 --only=languages`
Expected: FAIL on the new words.

- [ ] **Step 2: Write the translations**

Create `reference/ink-pages/science/translations-science.cjs`:

```js
// Adds the Science ink page's new strings (October 14, 2026) to the five catalogs. DRAFT
// translation, not native-reviewed: the site's understated voice, no new claims. Keys start at
// m650 (the Propolis session adds keys from m612). hken.json stays {} (/hken redirects to /cns).
// Run from the repo root:
//   node reference/ink-pages/science/translations-science.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  ["The formulas", "配方", "포뮬러", "Các công thức", "処方"],
  ["Source", "来源", "출처", "Nguồn", "出典"],
  [
    "Keep scrolling: the scroll unrolls",
    "继续向下滚动：画卷徐徐展开",
    "계속 스크롤하세요: 두루마리가 펼쳐집니다",
    "Tiếp tục cuộn: bức tranh cuộn sẽ mở ra",
    "スクロールを続けると、絵巻が広がります",
  ],
  [
    "Scroll sideways to see the whole painting",
    "左右滚动可查看整幅画",
    "옆으로 스크롤하면 그림 전체를 볼 수 있습니다",
    "Cuộn ngang để xem toàn bộ bức tranh",
    "横にスクロールすると絵の全体が見られます",
  ],
  [
    "A long ink painting of Dr. Liu’s path: Okayama Castle, the ocean, the bell tower at Berkeley, Salzburg, and California hills under a gold sun",
    "一幅描绘刘建康博士求索之路的水墨长卷：冈山城、大海、伯克利的钟楼、萨尔茨堡，以及金色太阳下的加州山丘",
    "류젠캉 박사의 여정을 그린 긴 수묵화: 오카야마성, 바다, 버클리의 종탑, 잘츠부르크, 그리고 금빛 해 아래 캘리포니아 언덕",
    "Bức tranh thủy mặc dài về hành trình của TS. Liu: thành Okayama, đại dương, tháp chuông ở Berkeley, Salzburg và những ngọn đồi California dưới mặt trời vàng",
    "劉建康博士の歩みを描いた長い水墨画：岡山城、海、バークレーの時計塔、ザルツブルク、金色の太陽の下のカリフォルニアの丘",
  ],
  ["Read the study", "阅读研究", "연구 보기", "Đọc nghiên cứu", "研究を読む"],
  [
    "A shelf of rolled scrolls painted in ink; three lie pulled forward",
    "水墨画：书架上摆满卷轴，其中三卷被抽出放在前面",
    "먹으로 그린 두루마리 선반. 세 개가 앞으로 꺼내져 있습니다",
    "Kệ những cuộn giấy vẽ bằng mực; ba cuộn được kéo ra phía trước",
    "巻物の並ぶ棚の水墨画。三本が手前に引き出されています",
  ],
  [
    "Three small ink paintings: an oil lamp with a gold flame, three balanced stones, and California poppies",
    "三幅小水墨画：一盏燃着金色火焰的油灯、三块叠放平衡的石头、加州罂粟花",
    "작은 수묵화 세 점: 금빛 불꽃의 기름등잔, 균형 잡힌 돌 세 개, 캘리포니아 양귀비",
    "Ba bức tranh mực nhỏ: ngọn đèn dầu với ngọn lửa vàng, ba hòn đá cân bằng và hoa anh túc California",
    "三つの小さな水墨画：金色の炎の油灯、積み重ねた三つの石、カリフォルニアポピー",
  ],
  [
    "An oil lamp with a gold flame, painted in ink",
    "水墨油灯，金色火焰",
    "금빛 불꽃의 기름등잔을 먹으로 그린 그림",
    "Ngọn đèn dầu với ngọn lửa vàng, vẽ bằng mực",
    "金色の炎の油灯の水墨画",
  ],
  [
    "Three balanced stones, painted in ink",
    "水墨画：三块叠放平衡的石头",
    "균형 잡힌 돌 세 개를 먹으로 그린 그림",
    "Ba hòn đá cân bằng, vẽ bằng mực",
    "積み重ねた三つの石の水墨画",
  ],
  [
    "California poppies, painted in ink",
    "水墨加州罂粟花",
    "캘리포니아 양귀비를 먹으로 그린 그림",
    "Hoa anh túc California, vẽ bằng mực",
    "カリフォルニアポピーの水墨画",
  ],
  [
    "Two mugs on a low wooden table, steam rising, painted in ink",
    "水墨画：矮木桌上两只冒着热气的马克杯",
    "낮은 나무 탁자 위 김이 오르는 머그잔 두 개를 먹으로 그린 그림",
    "Hai chiếc cốc bốc hơi trên chiếc bàn gỗ thấp, vẽ bằng mực",
    "低い木の机に湯気の立つマグカップが二つ、水墨画",
  ],
];
const path = "src/i18n/copy-keys.json";
const keys = JSON.parse(fs.readFileSync(path, "utf8"));
const locales = ["en", "cns", "kr", "vn", "jp"];
const catalogs = locales.map((l) => JSON.parse(fs.readFileSync("messages/" + l + ".json", "utf8")));
let next = Math.max(650, Math.max(...Object.values(keys).map((k) => Number(k.slice(1)))) + 1);
const added = [];
for (const row of entries) {
  const key = keys[row[0]] ?? "m" + next++;
  keys[row[0]] = key;
  added.push(key + " " + row[0]);
  row.forEach((value, i) => {
    catalogs[i].Copy[key] = value;
  });
}
fs.writeFileSync(path, JSON.stringify(keys, null, 2) + "\n");
locales.forEach((l, i) =>
  fs.writeFileSync("messages/" + l + ".json", JSON.stringify(catalogs[i], null, 2) + "\n"),
);
console.log(added.join("\n"));
console.log("next id m" + next);
```

Check the Chinese and Japanese rendering of Dr. Liu's name against the existing catalogs before running: `grep -n "刘建康\|劉建康\|류젠캉" messages/*.json | head` (key `m198` names him); use the same spelling.

- [ ] **Step 3: Run it**

Run: `node reference/ink-pages/science/translations-science.cjs`
Expected: twelve lines `m650 The formulas` … `m661 Two mugs …` (or lower keys for any string that already had one) and `next id m662`.

- [ ] **Step 4: Run the QA**

Restart the dev server (catalog changes), then run:
`python -X utf8 scripts/qa/qa_science_ink.py http://localhost:3050 --only=languages,shell`
Expected: every line `PASS`.

- [ ] **Step 5: Commit**

```bash
git add reference/ink-pages/science/translations-science.cjs src/i18n/copy-keys.json messages scripts/qa/qa_science_ink.py
git commit -m "feat(science): the ink page's new words in five languages (drafts for a native check)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Every size, the built site, the gates and the review

**Files:**

- Modify: `scripts/qa/qa_science_ink.py` (sections `layout`, `deep_links`)
- Modify: `docs/science-page.md` (a new top section)
- Any polish the review finds, in `src/components/science/ink/`

**Interfaces:**

- Consumes: everything above.
- Produces: the finished branch, screenshots for Mo.

- [ ] **Step 1: Write the last QA sections**

Add to `scripts/qa/qa_science_ink.py`, before `SECTIONS`:

```python
SIZES = [(1920, 1080), (1536, 864), (1440, 900), (1280, 720), (1024, 768), (900, 1000), (768, 1024), (390, 844), (360, 740)]

SMALL_TEXT = """() => [...document.querySelectorAll('main *')].filter(e => {
  if (!e.childNodes.length || ![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return false;
  const s = getComputedStyle(e); const r = e.getBoundingClientRect();
  return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && parseFloat(s.fontSize) < 15;
}).map(e => e.tagName + ' ' + e.textContent.trim().slice(0, 30))"""

SMALL_TARGETS = """() => [...document.querySelectorAll('main a, main button, main summary')].filter(e => {
  const r = e.getBoundingClientRect(); const s = getComputedStyle(e);
  return r.width > 0 && s.visibility !== 'hidden' && (r.height < 44 && !e.closest('p, dd'));
}).map(e => e.tagName + ' ' + e.textContent.trim().slice(0, 30) + ' ' + Math.round(e.getBoundingClientRect().height))"""


def layout(browser):
    for w, h in SIZES:
        ctx, page, _, errors = opened(browser, w, h)
        height = page.evaluate("document.documentElement.scrollHeight")
        for y in range(0, height, h):
            page.evaluate(f"window.scrollTo(0, {y})")
            page.wait_for_timeout(120)
        page.wait_for_timeout(800)
        overflow = page.evaluate("document.documentElement.scrollWidth - innerWidth")
        check(f"layout {w}x{h}: no sideways scroll", overflow <= 0, str(overflow))
        small = page.evaluate(SMALL_TEXT)
        check(f"layout {w}x{h}: text 15px or larger", not small, "; ".join(small[:4]))
        targets = page.evaluate(SMALL_TARGETS)
        check(f"layout {w}x{h}: targets 44px or larger", not targets, "; ".join(targets[:4]))
        check(f"layout {w}x{h}: no console errors", not errors, "; ".join(errors[:3]))
        ctx.close()


def deep_links(browser):
    for w, h in [(1440, 900), (390, 844)]:
        for part in ["scientists", "research", "health", "ask"]:
            ctx, page, _, _ = opened(browser, w, h, path=f"{PATH}#{part}")
            page.wait_for_timeout(1500)
            top = page.evaluate(f"document.getElementById('{part}').getBoundingClientRect().top")
            heading = page.evaluate(f"document.querySelector('#{part} h1, #{part} h2').getBoundingClientRect().top")
            bar = page.evaluate("document.querySelector('header').getBoundingClientRect().bottom")
            check(f"deep_links {w} #{part}: lands at its part", -5 <= top <= bar + 60 or part == "scientists", f"top {top:.0f}")
            check(f"deep_links {w} #{part}: heading clear of the menu bar", heading >= bar - 1, f"{heading:.0f} vs {bar:.0f}")
            ctx.close()
```

and add `"layout": layout, "deep_links": deep_links` to `SECTIONS`.

- [ ] **Step 2: Run the whole QA on dev; fix what fails**

Run: `python -X utf8 scripts/qa/qa_science_ink.py http://localhost:3050`
Expected: every line `PASS`. Fix each failure in the page's code (never by loosening a check that guards a visible fault); run again until clean.

- [ ] **Step 3: The built site**

Stop the dev preview, then:

```bash
npm run build
```

Start `bigh-science-ink-prod` with the preview tool (port 3051), then run:

```bash
python -X utf8 scripts/qa/qa_science_ink.py http://localhost:3051
python -X utf8 scripts/qa/qa_home_ink.py http://localhost:3051
python -X utf8 scripts/qa/qa_about.py http://localhost:3051
python -X utf8 scripts/qa/qa_nuricell_ink.py http://localhost:3051
python -X utf8 scripts/qa/qa_nav.py http://localhost:3051
python -X utf8 scripts/qa/qa_fda.py http://localhost:3051
python -X utf8 scripts/qa/qa_science_links.py http://localhost:3051
```

Expected: all pass (each script prints its own `n/n passed`; the other pages' counts must equal their counts on `origin/main`). Also `npm run type-check`, `npx eslint src`, `npm run format:check` (only the three known CRLF files may fail).

- [ ] **Step 4: Screenshots, scored**

Viewport shots (never full-page: the pinned part breaks them) at 1440x900, 1280x720, 1024x768 and 390x844: the opening, the scroll at a quarter, half and the end, Dr. Liu, the formulas, each strip, the footer. Look at each at full size, scrolled like a visitor. Score each screen out of 10 (bar: 9); fix and re-shoot anything under 9, or write down honestly why it stays (for example, the glossy bottles).

- [ ] **Step 5: A fresh review**

Dispatch `impeccable-finish-reviewer` with the spec, this plan, the approved mockups in `reference/ink-pages/mockups/science-ink/` and the screenshots; fix the material findings; run Steps 2-4 again on what changed.

- [ ] **Step 6: Docs**

Add a new top section to `docs/science-page.md`:

```markdown
## Now: the handscroll, in Ink & Gold (October 14, 2026)

Mo picked idea A, "the handscroll" (October 13), and approved the whole page (October 14). Spec:
`docs/superpowers/specs/2026-10-14-science-ink-design.md`; plan:
`docs/superpowers/plans/2026-10-14-science-ink.md`; mockups: `reference/ink-pages/mockups/science-ink/`.
Code: `src/components/science/ink/`; paintings: `reference/ink-pages/science/` (build script, originals,
prompts, spend). QA: `scripts/qa/qa_science_ink.py`. The film page it replaced is in
`reference/science-page/looks/film/`. Open: a native check of the draft translations (m650 upward);
most older Science lines are still English on the other languages (as before this page).
```

- [ ] **Step 7: Commit**

```bash
git add -A src/components/science scripts/qa/qa_science_ink.py docs/science-page.md
git commit -m "feat(science): every size and the built site checked; docs

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

Then show Mo the screenshots (artifact `https://claude.ai/artifact/Rvr98DEWPLUWDighZgVSGv`, a new version) with the scores, and ask: push the branch for a Vercel preview (yes or no). Nothing is pushed without her yes.
