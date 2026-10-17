"""Photograph two opening compositions in the local browser, using the real bottle and copy."""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parents[1] / "mockups/propolis-centered"
OUT.mkdir(parents=True, exist_ok=True)
CSS = """
[data-chapter=overview] {padding:128px 0 0!important}
.prototype .stage{display:grid;grid-template-columns:minmax(0,1fr) min(32vw,50svh,470px) minmax(0,1fr);align-items:center;margin:0;font-family:var(--display-font);font-size:clamp(80px,10.4vw,160px);font-weight:500;line-height:.93;letter-spacing:-.045em}
.prototype .left{justify-self:end;white-space:nowrap;margin-top:.52em}
.prototype .right{display:flex;flex-direction:column;align-items:center;justify-self:start;white-space:nowrap;font-size:.73em;line-height:.96}
.prototype .stand img{display:block;width:100%;height:auto}
.prototype .details{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,.85fr);gap:clamp(64px,9vw,140px);margin-top:38px;align-items:start}
.prototype .lead{font:500 clamp(28px,2.7vw,42px)/1.15 var(--display-font);letter-spacing:-.02em;margin:0 0 24px;text-wrap:balance}
.prototype .lead span{display:block}
.prototype .purpose{font:400 18px/1.65 var(--sans);max-width:32em;margin:0;color:var(--muted)}
.prototype .highlights{display:flex;justify-content:space-between;gap:20px;border-bottom:1px solid var(--line);padding-bottom:18px;margin:0 0 24px;font:400 17px/1.4 var(--sans)}
.prototype .highlights span+span{padding-left:20px;border-left:1px solid var(--hair)}
.prototype .supply{font:400 17px/1.5 var(--sans);margin:0 0 14px}
.prototype .cart{display:block;width:100%;height:56px;background:var(--ink);color:var(--paper);border:0;border-radius:99px;font:450 20px var(--sans)}
.prototype .promise{font:400 15px/1.5 var(--sans);color:var(--muted);margin:12px 0 0}
.prototype .rule{margin-top:56px;border-top:1px solid var(--line)}
.prototype.variantB .left{display:flex;flex-direction:column;align-items:center;margin-top:0;font-size:.8em;line-height:.9}
.prototype.variantB .right{font-size:.73em;line-height:1}
@media(max-width:959px){[data-chapter=overview]{padding-top:124px!important}.prototype .stage{grid-template-columns:auto auto;justify-content:center;column-gap:16px;font-size:clamp(52px,12vw,110px)}.prototype .left{grid-column:1;grid-row:1;margin-top:.52em}.prototype .right{grid-column:2;grid-row:1}.prototype .stand{grid-column:1/-1;grid-row:2;width:min(76vw,340px);justify-self:center;margin-top:24px}.prototype .details{grid-template-columns:1fr;gap:32px;margin-top:32px}.prototype .lead{font-size:30px}.prototype .highlights{font-size:16px}.prototype .rule{margin-top:40px}}
"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    for variant in ["A", "B"]:
        for width, height in [(1440, 1000), (390, 844)]:
            page = browser.new_page(viewport={"width":width,"height":height}, reduced_motion="reduce")
            page.goto("http://localhost:3007/products/green-bee-propolis", wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            page.evaluate("""variant => {
              const root = document.querySelector('[data-chapter=overview]');
              const img = root.querySelector('img').outerHTML;
              const lead = root.querySelector('[class*=lead]').innerHTML;
              const purpose = root.querySelector('[class*=purpose]').innerHTML;
              const supply = root.querySelector('[class*=supply]').innerHTML;
              const promise = root.querySelector('[class*=promise]').innerHTML;
              const wrap = root.firstElementChild;
              wrap.classList.add('prototype', 'variant'+variant);
              wrap.innerHTML = `<h1 class="stage" lang="en"><span class="left">${variant==='A'?'Green':'<span>Green</span><span>Bee</span>'}</span><span class="stand">${img}</span><span class="right">${variant==='A'?'<span>Bee</span><span>Propolis</span>':'Propolis'}</span></h1><div class="details"><div><p class="lead">${lead}</p><p class="purpose">${purpose}</p></div><div><p class="highlights"><span>Minas Gerais, Brazil</span><span>Artepillin C</span></p><p class="supply">${supply}</p><button class="cart">Add to cart</button><p class="promise">${promise}</p></div></div><div class="rule"></div>`;
            }""", variant)
            page.add_style_tag(content=CSS)
            page.wait_for_timeout(700)
            page.screenshot(path=str(OUT / f"concept-{variant}-{'desktop' if width>900 else 'phone'}.png"))
            print(variant, width, flush=True)
            page.close()
    browser.close()
