"""Build the review page Mo opens on his phone: review.html, every screenshot embedded.

Usage: python -X utf8 build_review.py
Reads review.json (the ideas, their lines and notes) and shots/*.jpg.
"""
import base64
import json
from io import BytesIO
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "shots"
data = json.loads((HERE / "review.json").read_text(encoding="utf-8"))


def embed(name: str, width: int) -> str:
    img = Image.open(SHOTS / name).convert("RGB")
    if img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    buf = BytesIO()
    img.save(buf, "JPEG", quality=82, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def idea(item: dict) -> str:
    key = item["key"]
    pick = '<span class="pick">My pick</span>' if item.get("pick") else ""
    rows = []
    for i, topic in enumerate(["Mitochondria", "Free radicals"]):
        rows.append(
            f"""<figure class="pair">
  <figcaption><b>{topic}</b><span>{item["lines"][i]}</span></figcaption>
  <div class="views">
    <img class="desk" src="{embed(f"{key}-1440-{i}.jpg", 1200)}" alt="{item["name"]}, {topic}, on a computer">
    <img class="phone" src="{embed(f"{key}-390-{i}.jpg", 600)}" alt="{item["name"]}, {topic}, on a phone">
  </div>
</figure>"""
        )
    notes = "".join(f"<li>{n}</li>" for n in item["notes"])
    return f"""<section id="idea-{item["letter"].lower()}">
  <header><span class="letter">{item["letter"]}</span><h2>{item["name"]}</h2>{pick}</header>
  <p class="say">{item["say"]}</p>
  {"".join(rows)}
  <ul class="notes">{notes}</ul>
</section>"""


html = f"""<title>Science Paintings Redo</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Ysabeau:wght@400;500&family=Inter:wght@400;500;600&display=swap">
<style>
/* Layout: one column of ideas; each idea = name, one line, then two real-page screenshots
   (computer wide, phone beside it). The screenshots are the content; the page stays quiet. */
:root {{
  --paper: #f6f3ea; --ink: #1c1a17; --soft: #5f5a50; --line: #d9d3c4; --gold: #9a7420; --card: #fffdf7;
  --display: "Ysabeau", "Iowan Old Style", Georgia, serif;
  --body: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --paper: #191713; --ink: #f1ece0; --soft: #b3ab9b; --line: #3a362e; --gold: #d9b45a; --card: #23201a; color-scheme: dark }} }}
:root[data-theme="dark"] {{
  --paper: #191713; --ink: #f1ece0; --soft: #b3ab9b; --line: #3a362e; --gold: #d9b45a; --card: #23201a; color-scheme: dark }}
body {{ background: var(--paper); color: var(--ink); font: 17px/1.55 var(--body); }}
main {{ max-width: 1120px; margin: 0 auto; padding-block: 32px 72px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: flex; flex-direction: column; gap: 56px; }}
h1 {{ font: 500 clamp(30px, 6vw, 46px)/1.1 var(--display); margin: 0 0 12px; text-wrap: balance; }}
.lead {{ color: var(--soft); max-width: 62ch; margin: 0; }}
.why {{ margin: 18px 0 0; padding: 0 0 0 20px; max-width: 62ch; }}
.why li {{ margin: 4px 0; }}
section {{ display: flex; flex-direction: column; gap: 18px; border-top: 1px solid var(--line); padding-top: 28px; }}
section header {{ display: flex; align-items: baseline; gap: 14px; flex-wrap: wrap; }}
.letter {{ font: 500 34px/1 var(--display); color: var(--gold); }}
h2 {{ font: 500 clamp(24px, 4.6vw, 32px)/1.15 var(--display); margin: 0; }}
.pick {{ font: 600 13px/1 var(--body); letter-spacing: .04em; text-transform: uppercase; color: var(--paper);
  background: var(--ink); border-radius: 999px; padding: 7px 12px; }}
.say {{ margin: 0; max-width: 62ch; }}
.pair {{ margin: 0; display: flex; flex-direction: column; gap: 10px; }}
.pair figcaption {{ display: flex; flex-direction: column; gap: 2px; }}
.pair figcaption b {{ font-weight: 600; }}
.pair figcaption span {{ color: var(--soft); }}
.views {{ display: grid; grid-template-columns: minmax(0, 3.1fr) minmax(0, 1fr); gap: 12px; align-items: start; }}
.views img {{ width: 100%; height: auto; display: block; border: 1px solid var(--line); border-radius: 6px; background: var(--card); }}
.notes {{ margin: 0; padding-left: 20px; color: var(--soft); max-width: 62ch; }}
.notes li {{ margin: 3px 0; }}
.now .views {{ grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); }}
@media (max-width: 640px) {{
  .views {{ grid-template-columns: minmax(0, 1fr); }}
  .views .phone {{ max-width: 300px; }}
  .now .views {{ grid-template-columns: minmax(0, 1fr); }}
}}
</style>
<main>
  <div>
    <h1>{data["title"]}</h1>
    <p class="lead">{data["lead"]}</p>
    <ul class="why">{"".join(f"<li>{w}</li>" for w in data["why"])}</ul>
  </div>
  {"".join(idea(i) for i in data["ideas"])}
  <section class="now">
    <header><h2>For comparison: the page today</h2></header>
    <div class="views">
      <img src="{embed("now-1440-0.jpg", 1200)}" alt="Today's Mitochondria painting">
      <img src="{embed("now-1440-1.jpg", 1200)}" alt="Today's Free radicals painting">
    </div>
  </section>
</main>
"""
(HERE / "review.html").write_text(html, encoding="utf-8", newline="\n")
print("review.html", round(len(html) / 1024), "KB")
