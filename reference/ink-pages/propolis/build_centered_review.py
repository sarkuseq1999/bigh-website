"""Create a local, responsive review of the bottle-between-words opening from browser captures."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "reference/ink-pages/mockups/propolis-centered"
CAPTURES = ROOT / "scripts/qa/out/propolis-design"
OUT.mkdir(parents=True, exist_ok=True)

for source, name in [
    (CAPTURES / "centered-built/1440-opening.png", "desktop.webp"),
    (CAPTURES / "centered-built/390-opening.png", "phone.webp"),
    (CAPTURES / "before/1440-opening.png", "before.webp"),
]:
    with Image.open(source) as image:
        image.save(OUT / name, "WEBP", quality=94, method=6)

html = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>Green Bee Propolis — the bottle at the centre</title>
<style>*{box-sizing:border-box}body{margin:0;background:#f8f3ea;color:#171612;font:18px/1.6 system-ui,sans-serif}main{max-width:1280px;margin:auto;padding:40px 24px}h1{font:500 clamp(34px,6vw,62px)/1.1 Georgia,serif;letter-spacing:-.035em}h2{font:400 30px/1.2 Georgia,serif;margin:0 0 24px}p{max-width:44em}a{color:inherit;text-underline-offset:5px}section{padding:36px 0;border-top:1px solid #ccc6ba;margin-top:32px}img{display:block;width:100%;height:auto}.phone{max-width:390px}.choices{display:grid;grid-template-columns:1fr 1fr;gap:28px}.choices figure{margin:0}.choices figcaption{padding:14px 0}summary{cursor:pointer;padding:20px 0;font-size:22px}small{font-size:16px}@media(max-width:600px){main{padding:24px 18px}.choices{grid-template-columns:1fr}}</style></head>
<body><main><small>BiGH · Local design review · October 16, 2026</small><h1>The bottle at the centre.</h1><p>Green on the left. Bee and Propolis on the right. Lighter lettering, more room around the real bottle, and a simpler purchase area beneath.</p><p><strong>Design assessment: 9/10.</strong> The introductory paragraph is still a little dense on a phone.</p><section><h2>A — refined desktop design</h2><a href="desktop.webp"><img src="desktop.webp" alt="Green on the left, the approved bottle in the centre, Bee above Propolis on the right"></a><p><a href="desktop.webp">Open the desktop screenshot at full size</a></p></section><section><h2>The phone layout</h2><a href="phone.webp"><img class="phone" src="phone.webp" alt="The name arranged above the original bottle on a phone" loading="lazy"></a></section><details><summary>Compare the two starting concepts</summary><div class="choices"><figure><a href="concept-A-desktop.png"><img src="concept-A-desktop.png" alt="Concept A keeps Green left and Bee Propolis right" loading="lazy"></a><figcaption><strong>A — recommended and developed.</strong> Keeps the original name arrangement.</figcaption></figure><figure><a href="concept-B-desktop.png"><img src="concept-B-desktop.png" alt="Concept B puts Green Bee together on the left" loading="lazy"></a><figcaption><strong>B.</strong> Groups Green Bee on the left.</figcaption></figure></div></details><details><summary>The original public design</summary><img src="before.webp" alt="The original heavier product-name lettering surrounding the bottle" loading="lazy"></details><p>Real screenshots of the local production build. The public demo has not changed.</p></main></body></html>'''
(OUT / "index.html").write_text(html, encoding="utf-8", newline="\n")
print(OUT / "index.html")
