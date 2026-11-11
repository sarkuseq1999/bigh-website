//@include m6.js
(() => {
  // B, "Blue and gold": no place. One broad brush stroke of the bottle's own blue across the paper
  // behind the name, and a torn strip of gold leaf the bottle stands on. California's state colours.
  const m = window.__m6;
  const cfg = window.__blue || {};
  const NAT = { w: 1536, h: 522 };
  const g = m.glass();
  const stroke = m.layer("/mock-art/stroke.png", 0);
  if (m.phone) {
    // One column: the stroke runs behind the name and the bottle's shoulders, the bottle's foot on
    // bare paper. Only the stroke's middle shows, its ragged edges above the name and under the label.
    const nr = m.first.getBoundingClientRect();
    const y0 = nr.top - (cfg.phoneUp ?? 0.05) * m.W;
    const y1 = g.top + (cfg.phoneDown ?? 0.6) * (g.foot - g.top);
    const h = y1 - y0;
    const w = (NAT.w / NAT.h) * h;
    m.place(stroke, (m.W - w) / 2 + (cfg.phoneDx ?? 0) * w, y0, w, h);
  } else {
    // Centred on the letters, running off both sides of the window.
    const w = m.W * (cfg.wide ?? 1.04);
    const h = (NAT.h / NAT.w) * w * (cfg.tall ?? 0.84);
    m.place(stroke, (m.W - w) / 2, (g.top + g.foot) / 2 - h / 2 + (cfg.dy ?? 0), w, h);
  }
  // The gold the bottle stands on: a torn strip of leaf, flat, no glow.
  if (cfg.gold !== false) {
    const gw = g.w * (cfg.goldWide ?? 1.75);
    const strip = m.layer("/mock-art/gold-strip.png", 0, "normal");
    const gh = (44 / 620) * gw;
    m.place(strip, g.cx - gw / 2 + (cfg.goldDx ?? 0), g.foot - gh * (cfg.goldUp ?? 0.5), gw, gh);
    strip.style.rotate = (cfg.goldTurn ?? -0.5) + "deg";
  }
  m.contact(cfg.shadow ?? 0.34, 1);
  document.documentElement.style.overflowX = "clip";
})();
