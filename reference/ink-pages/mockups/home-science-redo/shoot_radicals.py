"""Mock a new Free radicals painting on the real homepage (browser-only swap; no site changes).

Usage: python -X utf8 shoot_radicals.py <base-url> <key> <art.jpg> "<line>" [labels.json]
  labels.json: [{"text": "Free radicals", "at": [x, y], "label": [x, y], "align": "left"}, ...]
  with every x, y a fraction of the painting's frame; a 1px ink leader runs from label to point.
Writes shots/<key>-<width>-1.jpg for 1440x1000 and 390x844.
"""
import base64
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE / "shots"
OUT.mkdir(exist_ok=True)
BASE, KEY, ART, LINE = sys.argv[1], sys.argv[2], Path(sys.argv[3]), sys.argv[4]
LABELS = json.loads(Path(sys.argv[5]).read_text(encoding="utf-8")) if len(sys.argv) > 5 else []

SWAP = """([url, line, labels, phone]) => {
  document.querySelectorAll('#science img[src*="lantern-soot"], #science img[data-mock]').forEach((img) => {
    img.dataset.mock = '1';
    img.loading = 'eager';
    img.removeAttribute('srcset');
    img.src = url;
    const stage = img.parentElement;
    stage.querySelectorAll('[data-mock-labels]').forEach((e) => e.remove());
    if (!labels.length || img.dataset.on === 'false') return;
    const box = document.createElement('div');
    box.dataset.mockLabels = '';
    box.style.cssText = 'position:absolute;inset:0;pointer-events:none;z-index:3';
    const ns = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('viewBox', '0 0 1000 750');
    svg.setAttribute('preserveAspectRatio', 'none');
    svg.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;overflow:visible';
    labels.forEach((l) => {
      const line = document.createElementNS(ns, 'line');
      line.setAttribute('x1', l.label[0] * 1000); line.setAttribute('y1', l.label[1] * 750);
      line.setAttribute('x2', l.at[0] * 1000); line.setAttribute('y2', l.at[1] * 750);
      line.setAttribute('stroke', '#1c1a17'); line.setAttribute('stroke-width', '1');
      line.setAttribute('vector-effect', 'non-scaling-stroke');
      svg.appendChild(line);
      const dot = document.createElementNS(ns, 'circle');
      dot.setAttribute('cx', l.at[0] * 1000); dot.setAttribute('cy', l.at[1] * 750);
      dot.setAttribute('r', phone ? 5 : 3.2); dot.setAttribute('fill', '#1c1a17');
      svg.appendChild(dot);
      const t = document.createElement('span');
      t.textContent = l.text;
      const side = l.align === 'right' ? 'right:' + (100 - l.label[0] * 100) + '%' : 'left:' + l.label[0] * 100 + '%';
      // "below": the words sit centred under the end of an upright leader.
      const shift = l.align === 'below' ? 'translate(-50%, 2px)' : 'translateY(-50%)';
      t.style.cssText = `position:absolute;${side};top:${l.label[1] * 100}%;transform:${shift};` +
        `padding:0 ${phone ? 5 : 8}px;font:450 ${phone ? 14 : 17}px/1.2 Switzer, system-ui, sans-serif;color:#1c1a17;white-space:nowrap`;
      box.appendChild(t);
    });
    box.insertBefore(svg, box.firstChild);
    stage.appendChild(box);
  });
  document.querySelectorAll('#science p, #science figcaption, #science span').forEach((el) => {
    if (el.children.length === 0 && el.textContent.includes('Every flame leaves a little soot')) el.textContent = line;
  });
}"""


def data_url(path: Path) -> str:
    kind = {".png": "png", ".jpg": "jpeg", ".webp": "webp"}[path.suffix]
    return f"data:image/{kind};base64," + base64.b64encode(path.read_bytes()).decode()


with sync_playwright() as p:
    browser = p.chromium.launch(
        args=["--use-gl=angle", "--use-angle=d3d11", "--enable-gpu", "--ignore-gpu-blocklist"]
    )
    url = data_url(ART)
    for width, height in [(1440, 1000), (390, 844)]:
        phone = width < 900
        context = browser.new_context(
            viewport={"width": width, "height": height},
            is_mobile=phone,
            has_touch=phone,
            device_scale_factor=2 if phone else 1,
        )
        page = context.new_page()
        page.goto(BASE, wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.locator("#science-title").evaluate(
            "(e) => scrollTo(0, scrollY + e.getBoundingClientRect().top - 110)"
        )
        page.wait_for_timeout(2500)
        page.locator("#science button").filter(has_text="Free radicals").first.click()
        page.wait_for_timeout(3600)
        if phone:
            page.locator("#science [role=tablist]").evaluate(
                "(e) => scrollTo(0, scrollY + e.getBoundingClientRect().top - 100)"
            )
            page.wait_for_timeout(400)
        page.evaluate(SWAP, [url, LINE, LABELS, phone])
        page.wait_for_function(
            """() => [...document.querySelectorAll('#science img[data-mock]')]
                 .every((i) => i.complete && i.naturalWidth > 0)""",
            timeout=20000,
        )
        page.wait_for_timeout(500)
        over = page.evaluate("document.documentElement.scrollWidth > innerWidth")
        page.screenshot(path=str(OUT / f"{KEY}-{width}-1.jpg"), type="jpeg", quality=90)
        print(f"{KEY} {width}: captured; overflow={over}", flush=True)
        context.close()
    browser.close()
