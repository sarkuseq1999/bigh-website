(() => {
  // B, "The next move": a painted chess game in mid-play, one knight in gold leaf, and the real bottle
  // standing at the board's side. Words and the buy box on the left.
  const art = window.__mockArt || "chess3";
  const sec = document.querySelector('section[data-chapter="overview"]');
  const wrap = sec.firstElementChild;
  const h1 = sec.querySelector("h1");
  const [, first, stand, second] = h1.children;
  const words = h1.nextElementSibling;
  const [left, buy] = words.children;
  const phone = innerWidth < 960;

  // The name: one word, the page's own name style, smaller than the giant halves.
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
  paint.src = `/mock-art/${art}.png`;
  const bottle = new Image();
  bottle.src = "/mock-art/bottle.png";
  const shadow = document.createElement("div");
  scene.append(paint, shadow, bottle);
  Object.assign(paint.style, { display: "block", width: "100%", height: "auto", mixBlendMode: "multiply" });
  Object.assign(shadow.style, {
    position: "absolute",
    borderRadius: "50%",
    background: "radial-gradient(closest-side, rgba(40,36,30,.38), rgba(40,36,30,.12) 60%, transparent)",
    mixBlendMode: "multiply",
  });
  Object.assign(bottle.style, { position: "absolute", height: "auto" });
  // The bottle stands in front of the board, on the table's wash (the painting is mirrored, so the
  // empty table is on its left).
  const place = (bx, bw, baseY) => {
    Object.assign(bottle.style, { left: bx + "%", width: bw + "%", bottom: 100 - baseY + "%" });
    Object.assign(shadow.style, {
      left: bx - bw * 0.12 + "%",
      width: bw * 1.24 + "%",
      bottom: 100 - baseY - 2.2 + "%",
      height: "5%",
    });
  };

  if (!phone) {
    Object.assign(sec.style, { position: "relative", overflow: "visible" });
    Object.assign(wrap.style, { position: "relative" });
    wrap.prepend(scene);
    // Words column on the left, above the painting's paper.
    const col = document.createElement("div");
    Object.assign(col.style, {
      position: "relative",
      zIndex: "1",
      width: "min(36%, 460px)",
      display: "flex",
      flexDirection: "column",
      gap: "0",
    });
    wrap.append(col);
    col.append(h1, left, buy);
    words.remove();
    Object.assign(left.style, { marginTop: "12px" });
    Object.assign(buy.style, { marginTop: "28px", width: "100%", maxWidth: "none", gridColumn: "auto" });
    for (const p of left.querySelectorAll("p")) p.style.maxWidth = "none";
    // The painting: from just right of the words to a little past the window's edge, its foot near
    // the window's foot; the bottle stands on the table at its left.
    const W = innerWidth, H = innerHeight;
    const w = wrap.getBoundingClientRect();
    const colRight = col.getBoundingClientRect().right;
    const x0 = colRight + 10;
    const sw = Math.min(W - x0 + 80, 1.5 * (H - 230));
    const sh = sw / 1.5;
    const colBottom = col.getBoundingClientRect().bottom;
    const footY = Math.min(H - 30, Math.max(colBottom + 40, H * 0.9));
    // Centre the words on the picture when the window is taller than they need.
    const shift = Math.max(0, (footY - 40 - colBottom) / 2);
    col.style.marginTop = shift + "px";
    Object.assign(scene.style, {
      position: "absolute",
      left: x0 - w.left + "px",
      top: footY - sh - w.top + "px",
      width: sw + "px",
      pointerEvents: "none",
    });
    place(7, 21, 93);
  } else {
    Object.assign(scene.style, { position: "relative", width: "128vw", marginLeft: "-6vw", marginTop: "2vw" });
    place(6, 25, 93);
    h1.after(scene);
  }
})();
