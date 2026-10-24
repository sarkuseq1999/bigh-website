(() => {
  // I, "Morning surf": the words in one row across the top (name, headline and purpose left, the buy
  // box right); under them a wide beach painting runs the window's full width, an older surfer
  // walking out to sea, the real bottle standing on the sand in the foreground.
  const sec = document.querySelector('section[data-chapter="overview"]');
  const wrap = sec.firstElementChild;
  const h1 = sec.querySelector("h1");
  const [, first, stand, second] = h1.children;
  const words = h1.nextElementSibling;
  const [left, buy] = words.children;
  const phone = innerWidth < 960;
  const W = innerWidth, H = innerHeight;

  first.textContent = "NuriCell";
  stand.style.display = "none";
  second.style.display = "none";
  Object.assign(h1.style, { display: "block", fontSize: phone ? "21vw" : "clamp(72px, 6.2vw, 112px)", margin: "0", textAlign: "left" });

  const scene = document.createElement("div");
  const paint = new Image();
  paint.src = "/mock-art/surf1.png";
  Object.assign(paint.style, { display: "block", width: "100%", height: "auto", mixBlendMode: "multiply" });
  const bottle = new Image();
  bottle.src = "/mock-art/bottle.png";
  const shadow = document.createElement("div");
  Object.assign(shadow.style, {
    position: "absolute",
    borderRadius: "50%",
    height: "4%",
    background: "radial-gradient(closest-side, rgba(40,36,30,.36), rgba(40,36,30,.1) 60%, transparent)",
    mixBlendMode: "multiply",
  });
  Object.assign(bottle.style, { position: "absolute", height: "auto" });
  scene.append(paint, shadow, bottle);
  const place = (x, w, base) => {
    Object.assign(bottle.style, { left: x + "%", width: w + "%", bottom: 100 - base + "%" });
    Object.assign(shadow.style, { left: x - w * 0.14 + "%", width: w * 1.28 + "%", bottom: 100 - base - 1.6 + "%" });
  };
  const aspect = 1774 / 887;

  if (!phone) {
    Object.assign(sec.style, { position: "relative", overflow: "visible" });
    Object.assign(wrap.style, { position: "relative" });
    // One row of words: the name, headline and purpose on the left, the buy box on the right.
    const row = document.createElement("div");
    Object.assign(row.style, { position: "relative", zIndex: "1", display: "flex", justifyContent: "space-between", alignItems: "flex-end", gap: "48px" });
    const l = document.createElement("div");
    Object.assign(l.style, { width: "min(46%, 620px)" });
    l.append(h1, left);
    Object.assign(left.style, { marginTop: "10px" });
    for (const p of left.querySelectorAll("p")) p.style.maxWidth = "none";
    Object.assign(buy.style, { width: "min(36%, 460px)", maxWidth: "none", gridColumn: "auto", marginTop: "0" });
    row.append(l, buy);
    wrap.append(row);
    words.remove();
    wrap.prepend(scene);
    // The painting: the window's full width, its horizon just under the words, running off the foot.
    const w = wrap.getBoundingClientRect();
    const rowBottom = row.getBoundingClientRect().bottom;
    const sw = W + 120;
    const sh = sw / aspect;
    const horizon = 0.245; // the sea's far edge, from the painting's top
    const top = rowBottom + 84 - horizon * sh;
    Object.assign(scene.style, { position: "absolute", left: -60 - w.left + "px", top: top - w.top + "px", width: sw + "px", pointerEvents: "none" });
    // The bottle stands on the sand in the foreground, its foot a little above the window's foot.
    const bw = Math.min(W * 0.13, 210) * Math.min(1, H / 900);
    const bh = (bw * 1193) / 649;
    const footY = Math.max(rowBottom + 40 + bh, Math.min(H - 36, top + sh * 0.97));
    const bx = W * 0.25 - bw / 2;
    place(((bx + 60) / sw) * 100, (bw / sw) * 100, ((footY - top) / sh) * 100);
    // The section holds the whole painting (its own feathered foot ends inside it), so the next
    // chapter's words never lie on the sand. No mask or clip here: either would break the multiply.
    const secTop = sec.getBoundingClientRect().top;
    sec.style.minHeight = Math.max(H - secTop, top + sh - secTop) + "px";
  } else {
    Object.assign(scene.style, { position: "relative", width: "150vw", marginLeft: "-40vw", marginTop: "4vw" });
    place(30, 19, 92);
    h1.after(scene);
  }
})();
