//@include m6.js
(() => {
  // C, "Morning shade": no paint. The soft morning shadow of a valley oak branch falls across the
  // paper, the name and the bottle; the bottle throws its own shadow on the paper behind it.
  const m = window.__m6;
  const cfg = window.__shade || {};
  const NAT = { w: 1536, h: 1024 };
  const g = m.glass();
  const shade = m.layer(`/mock-art/${cfg.art || "shade"}.png`, 2);
  if (m.phone) {
    // One column: the branch reaches in over the name and the bottle; the words under them stay in
    // the sun. The picture's middle shows, not its dense corner.
    const h = (g.foot + 0.25 * m.W) * (cfg.phoneZoom ?? 1.25);
    const w = (NAT.w / NAT.h) * h;
    m.place(shade, m.W - w * (cfg.phoneShow ?? 0.78), cfg.phoneDy ?? -0.06 * h, w);
    shade.style.opacity = String(cfg.phoneOpacity ?? 0.62);
  } else {
    // The shade comes in from the window's top right corner and covers the opening.
    const scale = Math.max(m.W / NAT.w, innerHeight / NAT.h) * (cfg.zoom ?? 1.04);
    const w = NAT.w * scale;
    m.place(shade, m.W - w + (cfg.dx ?? 0.04) * w, (cfg.dy ?? -0.045) * w, w);
    shade.style.opacity = String(cfg.opacity ?? 0.72);
  }
  // The bottle's own shadow, thrown down and to the left on the paper behind it.
  const b = m.img.getBoundingClientRect();
  const cast = new Image();
  cast.src = m.img.currentSrc || m.img.src;
  m.stand.style.position = "relative";
  m.img.style.position = "relative";
  Object.assign(cast.style, {
    position: "absolute",
    left: "0",
    top: "0",
    width: "100%",
    height: "auto",
    maxWidth: "none",
    filter: `brightness(0) blur(${(cfg.blur ?? 0.045) * b.width}px)`,
    opacity: String(cfg.cast ?? 0.13),
    translate: `${(cfg.castX ?? -0.1) * b.width}px ${(cfg.castY ?? 0.04) * b.width}px`,
    pointerEvents: "none",
  });
  m.stand.prepend(cast);
  m.contact(cfg.shadow ?? 0.36, 1.02);
  document.documentElement.style.overflowX = "clip";
})();
