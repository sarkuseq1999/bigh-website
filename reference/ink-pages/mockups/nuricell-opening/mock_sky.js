//@include m6.js
(() => {
  // A, "A clear day": one loose watercolour fills the first screen, a clear California morning sky
  // over the Pacific, the name in the sky, the real bottle standing on the bluff. Under the bluff
  // the painting ends in bare paper, where the words and the buy box stay as they are.
  const m = window.__m6;
  const cfg = window.__sky || {};
  const NAT = { w: 1536, h: 1024 };
  const horizonRow = cfg.horizon ?? 0.5938; // the sea's horizon
  const standRow = cfg.stand ?? 0.6924; // the bluff's top in the middle, where the bottle stands
  const endRow = cfg.end ?? 0.762; // the last of the grass
  // On a wide screen the whole name band sits a little higher, so the first screen still ends on
  // the refund line.
  if (!m.phone) m.h1.style.marginTop = -(cfg.lift ?? 16) + "px";
  const g = m.glass();
  // As wide as the window, and tall enough that the sky reaches the window's top.
  const scale = Math.max(m.W / NAT.w, (g.foot + 8) / (standRow * NAT.h)) * (cfg.zoom || 1);
  const w = NAT.w * scale;
  const h = NAT.h * scale;
  let top;
  if (m.phone) {
    // The bottle stands a little into the grass.
    top = g.foot - (cfg.sink ?? 0.012) * h - standRow * h;
  } else {
    // The name sits on the horizon: the letters' baseline, found with a probe in the first half.
    const probe = document.createElement("span");
    Object.assign(probe.style, { display: "inline-block", width: "0", height: "0", verticalAlign: "baseline" });
    m.first.append(probe);
    const baseline = probe.getBoundingClientRect().top;
    probe.remove();
    top = baseline + (cfg.under ?? 3) - horizonRow * h;
  }
  const sky = m.layer(`/mock-art/${cfg.art || "sky"}.png`, 0);
  m.place(sky, g.cx - w / 2, top, w);
  m.contact(cfg.shadow ?? 0.5, 1.12);
  // The words start under the last of the grass.
  const end = top + endRow * h + (cfg.gap ?? 0);
  const wt = m.words.getBoundingClientRect().top;
  if (wt < end) m.words.style.marginTop = parseFloat(getComputedStyle(m.words).marginTop) + (end - wt) + "px";
  // The page must not scroll sideways for the painting's overhang.
  document.documentElement.style.overflowX = "clip";
})();
