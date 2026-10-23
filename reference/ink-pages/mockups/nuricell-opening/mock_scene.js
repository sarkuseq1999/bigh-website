(() => {
  // One painting beside the words, with the real bottle in it or beside it. Set by window.__scene:
  //   art, aspect (width / height), words ("left" | "right"),
  //   bottle: { x, w, base } in % of the painting (in the scene) or { free: true, w } (beside it),
  //   front: an optional painting cut laid over the bottle (same box as the painting),
  //   ground: false to drop the soft contact shadow, phoneScale: painting width on a phone (vw).
  const cfg = window.__scene;
  const sec = document.querySelector('section[data-chapter="overview"]');
  const wrap = sec.firstElementChild;
  const h1 = sec.querySelector("h1");
  const [, first, stand, second] = h1.children;
  const words = h1.nextElementSibling;
  const [left, buy] = words.children;
  const phone = innerWidth < 960;

  first.textContent = "NuriCell";
  stand.style.display = "none";
  second.style.display = "none";
  Object.assign(h1.style, {
    display: "block",
    fontSize: phone ? "21vw" : "clamp(76px, 7vw, 124px)",
    margin: "0",
    textAlign: "left",
  });

  const scene = document.createElement("div");
  const paint = new Image();
  paint.src = `/mock-art/${cfg.art}.png`;
  Object.assign(paint.style, { display: "block", width: "100%", height: "auto", mixBlendMode: "multiply" });
  scene.append(paint);
  const bottle = new Image();
  bottle.src = "/mock-art/bottle.png";
  Object.assign(bottle.style, { height: "auto", display: "block" });
  const shadow = document.createElement("div");
  Object.assign(shadow.style, {
    position: "absolute",
    borderRadius: "50%",
    background: "radial-gradient(closest-side, rgba(40,36,30,.36), rgba(40,36,30,.1) 60%, transparent)",
    mixBlendMode: "multiply",
    height: "5%",
  });
  const inScene = !cfg.bottle.free;
  if (inScene) {
    if (cfg.ground !== false) scene.append(shadow);
    scene.append(bottle);
    const { x, w, base } = cfg.bottle;
    Object.assign(bottle.style, { position: "absolute", left: x + "%", width: w + "%", bottom: 100 - base + "%" });
    Object.assign(shadow.style, { left: x - w * 0.12 + "%", width: w * 1.24 + "%", bottom: 100 - base - 2.2 + "%" });
    if (cfg.front) {
      const f = new Image();
      f.src = `/mock-art/${cfg.front}.png`;
      Object.assign(f.style, { position: "absolute", inset: "0", width: "100%", height: "auto" });
      scene.append(f);
    }
  }

  if (!phone) {
    Object.assign(sec.style, { position: "relative", overflow: "visible" });
    Object.assign(wrap.style, { position: "relative" });
    wrap.prepend(scene);
    const col = document.createElement("div");
    Object.assign(col.style, {
      position: "relative",
      zIndex: "1",
      width: "min(36%, 460px)",
      display: "flex",
      flexDirection: "column",
      marginLeft: cfg.words === "right" ? "auto" : "0",
    });
    wrap.append(col);
    col.append(h1, left, buy);
    words.remove();
    Object.assign(left.style, { marginTop: "12px" });
    Object.assign(buy.style, { marginTop: "28px", width: "100%", maxWidth: "none", gridColumn: "auto" });
    for (const p of left.querySelectorAll("p")) p.style.maxWidth = "none";

    const W = innerWidth, H = innerHeight;
    const w = wrap.getBoundingClientRect();
    const c = col.getBoundingClientRect();
    const colBottom = c.bottom;
    const footY = Math.min(H - 30, Math.max(colBottom + 40, H * 0.9));
    const shift = Math.max(0, (footY - 40 - colBottom) / 2);
    col.style.marginTop = shift + "px";
    const room = H - 230;
    let sw, x0;
    if (cfg.words !== "right" && cfg.bottle.free) {
      // Words, then the bottle on bare paper, then the painting.
      const bw = cfg.bottle.wPx * Math.min(W / 1440, H / 900);
      const bh = (bw * 1193) / 649;
      const bx = c.right + 50;
      x0 = bx + bw + (cfg.gap ?? 20);
      sw = Math.min(W - x0 + (cfg.bleed ?? 40), cfg.aspect * (H - 140));
      Object.assign(bottle.style, { position: "absolute", width: bw + "px", left: bx - w.left + "px", top: footY - bh - w.top + "px" });
      Object.assign(shadow.style, {
        left: bx - w.left - bw * 0.12 + "px",
        width: bw * 1.24 + "px",
        top: footY - w.top - 11 + "px",
        height: "22px",
      });
      wrap.prepend(bottle);
      if (cfg.ground !== false) wrap.prepend(shadow);
    } else if (cfg.words !== "right") {
      x0 = c.right + 10;
      sw = cfg.bleed != null ? W - x0 + cfg.bleed : Math.min(W - x0 + 80, cfg.aspect * room);
      // Pull a painting with empty paper on its left in under the words' edge.
      x0 -= (cfg.pull ?? 0) * sw;
    } else {
      // The painting runs in from the window's left edge; the bottle stands between it and the words.
      const bw = cfg.bottle.w;
      sw = Math.min(cfg.aspect * room, c.left - bw - 60 + 60);
      x0 = c.left - bw - 60 - sw;
      x0 = Math.max(x0, -60);
      Object.assign(bottle.style, { position: "absolute", width: bw + "px" });
      wrap.prepend(bottle);
      if (cfg.ground !== false) wrap.prepend(shadow);
    }
    const sh = sw / cfg.aspect;
    // A scene can be pinned by its top (cfg.top, px under the window's top) and run off the foot.
    const top = cfg.top != null ? cfg.top * (H / 900) : footY - sh;
    Object.assign(scene.style, {
      position: "absolute",
      left: x0 - w.left + "px",
      top: top - w.top + "px",
      width: sw + "px",
      pointerEvents: "none",
    });
    if (cfg.words === "right") {
      const bx = c.left - cfg.bottle.w - 40;
      const bh = (cfg.bottle.w * 1193) / 649;
      Object.assign(bottle.style, { left: bx - w.left + "px", top: footY - 20 - bh - w.top + "px" });
      Object.assign(shadow.style, {
        left: bx - w.left - cfg.bottle.w * 0.12 + "px",
        width: cfg.bottle.w * 1.24 + "px",
        top: footY - 20 - w.top - 10 + "px",
        height: "22px",
      });
    }
  } else {
    // Phone: the name, then the painting (with the bottle), then the words.
    Object.assign(scene.style, {
      position: "relative",
      width: (cfg.phoneScale || 128) + "vw",
      marginLeft: cfg.phoneShift ?? "-6vw",
      marginTop: "2vw",
    });
    h1.after(scene);
    if (!inScene) {
      // The bottle stands in front of the painting's left part.
      Object.assign(bottle.style, { position: "absolute", width: "34%", left: "4%", bottom: "2%" });
      scene.append(bottle);
    }
    // Phone-only placement of the bottle, in % of the painting (cfg.phoneBottle: { x, w, base }).
    const pb = cfg.phoneBottle;
    if (pb) {
      Object.assign(bottle.style, { left: pb.x + "%", width: pb.w + "%", bottom: 100 - pb.base + "%" });
      Object.assign(shadow.style, { left: pb.x - pb.w * 0.12 + "%", width: pb.w * 1.24 + "%", bottom: 100 - pb.base - 2.2 + "%" });
      if (!inScene && cfg.ground !== false) scene.append(shadow);
    }
    if (cfg.phoneMarginBottom) scene.style.marginBottom = cfg.phoneMarginBottom;
  }
})();
