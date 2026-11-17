//@include m6.js
(() => {
  // Nature Calm's opening (November 16, 2026; the OPC vineyard's mock, for this page): one loose painting fills the
  // first screen as NuriCell's clear day does. The real bottle stands on the bare ground between
  // the near vine rows (the painting is placed by the bottle's foot), a little of the painting's
  // own grass in front of its foot; the name is lifted, if it must be, so its foot rests on the
  // far hills with sky behind the letters. Under it the painting ends in bare paper, where the
  // words and the buy box stay as they are.
  const m = window.__m6;
  const cfg = window.__sky || {};
  const NAT = { w: 1536, h: 1024 };
  const ridgeRow = cfg.ridge ?? 0.59; // the far hills' tops under the name
  const standRow = cfg.stand ?? 0.76; // the middle's ground, where the bottle stands
  const endRow = cfg.end ?? 0.83; // the last of the foreground
  if (!m.phone) m.h1.style.marginTop = -(cfg.lift ?? 16) + "px";
  const g = m.glass();
  const scale = Math.max(m.W / NAT.w, (g.foot + 8) / (standRow * NAT.h)) * (cfg.zoom || 1);
  const w = NAT.w * scale;
  const h = NAT.h * scale;
  const left = g.cx - w / 2;
  const top = g.foot + (cfg.sink ?? 0.006) * h - standRow * h;
  const sky = m.layer(`/mock-art/${cfg.art}.png`, 0);
  m.place(sky, left, top, w);
  if (!m.phone) {
    // The name's foot on the hills: "Formula"'s baseline (a probe; the first half is a column with
    // its first half is the same size) at most a few pixels under the hills' tops.
    const probe = document.createElement("span");
    Object.assign(probe.style, { display: "inline-block", width: "0", height: "0", verticalAlign: "baseline" });
    m.second.append(probe);
    const baseline = probe.getBoundingClientRect().top;
    probe.remove();
    const up = baseline - (top + ridgeRow * h) - (cfg.under ?? 4);
    if (up > 0) for (const half of [m.first, m.second]) half.style.translate = `0 ${-up}px`;
  }
  // The painting's own grass over the bottle's foot.
  const f = cfg.front;
  if (f) {
    const grass = m.layer(`/mock-art/${cfg.art}-front.png`, 2);
    m.place(grass, left + f[0] * scale, top + f[1] * scale, (f[2] - f[0]) * scale);
  }
  m.contact(cfg.shadow ?? 0.4, 1.12);
  const end = top + endRow * h + (cfg.gap ?? 0);
  const wt = m.words.getBoundingClientRect().top;
  if (wt < end) m.words.style.marginTop = parseFloat(getComputedStyle(m.words).marginTop) + (end - wt) + "px";
  document.documentElement.style.overflowX = "clip";
})();
