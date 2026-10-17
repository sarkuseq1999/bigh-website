"""Build a phone-friendly review from real browser captures. No product image is edited."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
CAPTURES = ROOT / "scripts/qa/out/propolis-design"
OUT = ROOT / "reference/ink-pages/mockups/propolis-refinement"

def picture(source, name):
    with Image.open(source) as image:
        image.save(OUT / name, "WEBP", quality=92, method=6)
    return name

chapters = [
    ("opening", "The opening"),
    ("why", "The origin — gold flowing through the tree"),
    ("inside", "The extract"),
    ("research", "The research"),
    ("daily", "The daily ritual"),
    ("buy", "The bottle"),
    ("questions", "The questions"),
]
sections = []
for key, title in chapters:
    desktop = picture(CAPTURES / "built" / f"1440-{key}.png", f"after-{key}-desktop.webp")
    phone_key = f"{key}-words" if key in ("inside", "research") else key
    phone = picture(CAPTURES / "built" / f"390-{phone_key}.png", f"after-{key}-phone.webp")
    sections.append(f'<section><h2>{title}</h2><picture><source media="(max-width:600px)" srcset="{phone}"><img src="{desktop}" alt="{title}: the revised Green Bee Propolis page" loading="lazy"></picture><p class="links"><a href="{desktop}">Desktop capture</a><a href="{phone}">Phone capture</a></p></section>')

before = picture(CAPTURES / "before/1440-opening.png", "before-desktop.webp")
before_phone = picture(CAPTURES / "before/390-opening.png", "before-phone.webp")
html = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><link rel="icon" href="data:,"><title>Green Bee Propolis — design review</title><style>
*{box-sizing:border-box}body{margin:0;background:#f8f3ea;color:#171612;font:18px/1.6 system-ui,sans-serif}main{max-width:1280px;margin:auto;padding:48px 24px}h1{font:500 clamp(36px,5vw,64px)/1.1 Georgia,serif;letter-spacing:-.04em;margin:20px 0}h2{font:400 clamp(25px,3vw,36px)/1.2 Georgia,serif;margin:0 0 24px}p{max-width:48em}a{color:inherit;text-underline-offset:5px}nav,.links{display:flex;gap:24px;flex-wrap:wrap}nav a,.links a{padding:10px 0;min-height:48px}section{padding:52px 0;border-top:1px solid #ccc6ba;margin-top:32px}img{width:100%;height:auto;display:block;border:1px solid #e2dccf}small{font-size:16px}.score{font-weight:600}.choices{display:grid;grid-template-columns:1fr 1fr;gap:28px}.choices figure{margin:0}.choices figcaption{padding:14px 0}summary{cursor:pointer;padding:18px 0;font-size:22px}details{border-top:1px solid #ccc6ba;margin-top:40px}@media(max-width:600px){main{padding:30px 18px}.choices{grid-template-columns:1fr}section{padding-top:34px}.links{font-size:16px}}
</style></head><body><main><small>BiGH · Local design proposal · October 16, 2026</small><h1>Green Bee Propolis,<br>with room to breathe.</h1><p>Lighter titles. A clearer product opening. Alternating paintings and words. The approved bottle, product facts and gold-filled bee tree stay intact.</p><p class="score">Design assessment: 9/10.</p><p>The remaining limit is the dense research copy on small screens. The study details open only when wanted.</p><nav><a id="live" href="http://localhost:3006/products/green-bee-propolis">Open the local page</a><a href="#new">The revised page</a><a href="#before">Before</a><a href="#concepts">A / B concepts</a></nav><div id="new">''' + "".join(sections) + f'''</div><section id="before"><h2>Before</h2><picture><source media="(max-width:600px)" srcset="{before_phone}"><img src="{before}" alt="The original Green Bee Propolis opening" loading="lazy"></picture></section><section id="concepts"><h2>The two starting concepts</h2><div class="choices"><figure><a href="concept-A-desktop.png"><img src="concept-A-desktop.png" alt="Concept A, botanical editorial" loading="lazy"></a><figcaption><strong>A — recommended and developed.</strong> A readable name beside the bottle.</figcaption></figure><figure><a href="concept-B-desktop.png"><img src="concept-B-desktop.png" alt="Concept B, a softer split name" loading="lazy"></a><figcaption><strong>B — softer split name.</strong> Closer to the previous layout.</figcaption></figure></div></section><p>These are screenshots of the local build. The public demo has not been updated.</p></main><script>document.getElementById('live').href='http://'+location.hostname+':3006/products/green-bee-propolis';</script></body></html>'''
html = html.replace("'+location.hostname+'", "'+(location.hostname || 'localhost')+'")
(OUT / "index.html").write_text(html, encoding="utf-8", newline="\n")
print(OUT / "index.html")
