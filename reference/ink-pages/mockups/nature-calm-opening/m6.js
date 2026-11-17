// Round 6's shared helper: the opening's parts, and layers under and over them.
window.__m6 = (() => {
  const sec = document.querySelector('section[data-chapter="overview"]');
  const wrap = sec.firstElementChild;
  const h1 = sec.querySelector("h1");
  const first = h1.querySelector('[class*="first"]');
  const stand = h1.querySelector('[class*="stand"]');
  const second = h1.querySelector('[class*="second"]');
  const img = stand.querySelector("img");
  const words = h1.nextElementSibling;
  const phone = innerWidth < 960;
  const W = document.documentElement.clientWidth;
  // The opening's own parts sit over a painting (z 0) and under a shade (z 2).
  sec.style.position = "relative";
  Object.assign(wrap.style, { position: "relative", zIndex: "1" });
  // The glass inside the bottle picture (its empty margins: 291..940 of 1230, 49..1242 of 1278).
  const glass = () => {
    const b = img.getBoundingClientRect();
    return {
      l: b.left + (291 / 1230) * b.width,
      r: b.left + (940 / 1230) * b.width,
      top: b.top + (49 / 1278) * b.height,
      foot: b.top + (1242 / 1278) * b.height,
      cx: b.left + (615.5 / 1230) * b.width,
      w: ((940 - 291) / 1230) * b.width,
      box: b,
    };
  };
  // A picture multiplied onto the page, placed in window pixels (the page is at its top).
  const layer = (src, z, blend = "multiply") => {
    const el = new Image();
    el.src = src;
    Object.assign(el.style, { position: "absolute", maxWidth: "none", height: "auto", mixBlendMode: blend, pointerEvents: "none", zIndex: String(z) });
    sec.append(el);
    return el;
  };
  const place = (el, x, y, w, h) => {
    const r = sec.getBoundingClientRect();
    Object.assign(el.style, { left: x - r.left + "px", top: y - r.top + "px", width: w + "px" });
    if (h) el.style.height = h + "px";
  };
  // A soft contact shadow where the bottle meets what it stands on.
  const contact = (strength = 0.3, widen = 1) => {
    const sh = document.createElement("span");
    Object.assign(sh.style, {
      position: "absolute",
      left: 50 - 29 * widen + "%",
      width: 58 * widen + "%",
      top: (1242 / 1278) * 100 - 2.6 + "%",
      height: "5.5%",
      borderRadius: "50%",
      background: `radial-gradient(closest-side, rgba(38,34,28,${strength}), rgba(38,34,28,${strength / 3}) 62%, transparent)`,
      mixBlendMode: "multiply",
      pointerEvents: "none",
    });
    stand.style.position = "relative";
    stand.prepend(sh);
    img.style.position = "relative";
    return sh;
  };
  return { sec, wrap, h1, first, stand, second, img, words, phone, W, glass, layer, place, contact };
})();
