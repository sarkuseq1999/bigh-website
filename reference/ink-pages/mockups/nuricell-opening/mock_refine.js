(() => {
  // Refinements of today's opening, switched on by window.__r:
  //   closer: the name grows until its letters nearly meet the bottle's glass (outer edges kept)
  //   shadow: a soft contact shadow under the bottle
  //   leaf:   the dot of the i in "Nuri" is a flake of real gold leaf
  //   ink:    the letters are filled with sumi ink (texture + slightly ragged edges)
  //   middle: the highlights move under the bottle, their ink line on its centre axis
  const r = window.__r || {};
  const sec = document.querySelector('section[data-chapter="overview"]');
  const h1 = sec.querySelector("h1");
  const first = h1.querySelector('[class*="first"]');
  const stand = h1.querySelector('[class*="stand"]');
  const second = h1.querySelector('[class*="second"]');
  const img = stand.querySelector("img");
  const phone = innerWidth < 960;
  const css = document.createElement("style");
  document.head.append(css);

  // The glass inside the bottle picture (its empty margins: 291..940 of 1230, 49..1242 of 1278).
  const glass = () => {
    const b = img.getBoundingClientRect();
    return { l: b.left + (291 / 1230) * b.width, r: b.left + (940 / 1230) * b.width, foot: b.top + (1242 / 1278) * b.height, w: b.width };
  };

  if (r.closer && !phone) {
    const g = glass();
    const f0 = parseFloat(getComputedStyle(h1).fontSize);
    const a = first.getBoundingClientRect();
    const gap = Math.max(14, 0.018 * innerWidth);
    // Grow the name so "Nuri" keeps its left edge and ends `gap` short of the glass.
    const k = (g.l - gap - a.left) / a.width;
    h1.style.fontSize = f0 * k + "px";
    const s = stand.getBoundingClientRect();
    first.style.marginRight = -(g.l - gap - s.left) + "px";
    second.style.marginLeft = -(s.right - (g.r + gap)) + "px";
    stand.style.zIndex = "1";
  }

  if (r.shadow) {
    const sh = document.createElement("span");
    Object.assign(sh.style, {
      position: "absolute",
      left: "21%",
      width: "58%",
      top: (1242 / 1278) * 100 - 2.6 + "%",
      height: "5.5%",
      borderRadius: "50%",
      background: "radial-gradient(closest-side, rgba(38,34,28,.30), rgba(38,34,28,.10) 62%, transparent)",
      mixBlendMode: "multiply",
      pointerEvents: "none",
    });
    stand.prepend(sh);
    img.style.position = "relative";
  }

  if (r.gold) {
    // "Cell" cut from gold leaf, as the homepage's gold word "cells." is (opening.module.css .gold).
    Object.assign(second.style, {
      backgroundImage: "linear-gradient(rgba(110, 78, 20, 0.2), rgba(110, 78, 20, 0.2)), url(/images/home-v2/ink/gold-leaf-word.webp)",
      backgroundPosition: "center",
      backgroundSize: "cover",
      webkitBackgroundClip: "text",
      backgroundClip: "text",
      color: "transparent",
      webkitTextFillColor: "transparent",
    });
  }

  if (r.ink) {
    // Ink in the letters: the painted ink sheet clipped to the type, and a faint ragged edge.
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("width", "0");
    svg.setAttribute("height", "0");
    svg.style.position = "absolute";
    svg.innerHTML = `<filter id="mk-rough" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="3" seed="7" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="${phone ? 3 : 5}" xChannelSelector="R" yChannelSelector="G"/>
    </filter>`;
    document.body.append(svg);
    css.textContent += `
      .mk-ink { background: url(/mock-art/inkfill.png) center / cover; -webkit-background-clip: text; background-clip: text; color: transparent; filter: url(#mk-rough); }
    `;
    first.classList.add("mk-ink");
    second.classList.add("mk-ink");
  }

  if (r.leaf) {
    // Swap the i for a dotless i and lay a gold leaf flake where its dot was (found by drawing the
    // two letters in the page's own face and comparing them).
    const cs = getComputedStyle(first);
    const size = parseFloat(cs.fontSize);
    const font = `${cs.fontWeight} ${size}px ${cs.fontFamily}`;
    const c = document.createElement("canvas");
    c.width = Math.ceil(size);
    c.height = Math.ceil(size * 1.4);
    const x = c.getContext("2d");
    const ink = (t) => {
      x.clearRect(0, 0, c.width, c.height);
      x.font = font;
      x.textBaseline = "alphabetic";
      x.fillText(t, size * 0.2, size * 1.1);
      return x.getImageData(0, 0, c.width, c.height).data;
    };
    const a = ink("i");
    const b = ink("ı");
    let x0 = 1e9, y0 = 1e9, x1 = -1, y1 = -1;
    for (let i = 3; i < a.length; i += 4) {
      if (a[i] > 128 && b[i] < 40) {
        const p = (i - 3) / 4, px = p % c.width, py = Math.floor(p / c.width);
        x0 = Math.min(x0, px); x1 = Math.max(x1, px); y0 = Math.min(y0, py); y1 = Math.max(y1, py);
      }
    }
    // Where the i's own box starts, in the canvas: its left side bearing is drawn from size * 0.2.
    const text = first.firstChild && first.firstChild.nodeType === 3 ? first.firstChild : [...first.childNodes].find((n) => n.nodeType === 3);
    const range = document.createRange();
    range.setStart(text, text.length - 1);
    range.setEnd(text, text.length);
    const ir = range.getBoundingClientRect();
    const base = first.getBoundingClientRect();
    // The i's baseline in the page: draw "i" at the canvas baseline (size * 1.1); in the page the
    // glyph's ink bottom sits on the baseline too, so match ink bottoms.
    let iy1 = -1;
    for (let i = 3; i < b.length; i += 4) if (b[i] > 128) iy1 = Math.max(iy1, Math.floor((i - 3) / 4 / c.width));
    text.textContent = text.textContent.slice(0, -1) + "ı";
    const dotW = x1 - x0, dotH = y1 - y0;
    const leaf = new Image();
    leaf.src = "/images/about-bc/enso-dot-v1.webp";
    const lw = dotW * (r.leafScale || 1.9);
    // The canvas drew the i starting at size*0.2; the range box starts at the glyph's advance origin.
    const cx = ir.left + (x0 + x1) / 2 - size * 0.2;
    // Ink bottom of the dotless i in the page = baseline; find it from the range box: the line box
    // bottom minus the descent. Use the canvas offset instead: baseline y in canvas = size * 1.1.
    const baseY = ir.top + (ir.height + size * 0.86 * 0) / 1;
    void baseY;
    first.style.position = "relative";
    Object.assign(leaf.style, { position: "absolute", width: lw + "px", height: "auto", maxWidth: "none", pointerEvents: "none", rotate: (r.leafTurn ?? -8) + "deg" });
    // Place by the dot's centre: measured against the dotless i's top in the page.
    const r2 = document.createRange();
    r2.setStart(text, text.length - 1);
    r2.setEnd(text, text.length);
    const glyphBox = r2.getBoundingClientRect();
    // Canvas: dot centre above the dotless i's top by (dotlessTop - dotCentreY).
    let dTop = 1e9;
    for (let i = 3; i < b.length; i += 4) if (b[i] > 128) dTop = Math.min(dTop, Math.floor((i - 3) / 4 / c.width));
    const dotCy = (y0 + y1) / 2;
    window.__leafMeasure = { dotW, dotH, dTop, dotCy, iy1, glyphTop: glyphBox.top, size };
    first.append(leaf);
    leaf.onload = () => {
      const probe = document.createElement("span");
      Object.assign(probe.style, { display: "inline-block", width: "0", height: "0", verticalAlign: "baseline" });
      first.insertBefore(probe, leaf);
      const baselineY = probe.getBoundingClientRect().top;
      probe.remove();
      const dotCentreY = baselineY - (size * 1.1 - dotCy) + size * (r.leafDy ?? 0.05);
      const lh = leaf.getBoundingClientRect().height;
      leaf.style.left = cx - first.getBoundingClientRect().left - lw / 2 + size * (r.leafDx ?? -0.012) + "px";
      leaf.style.top = dotCentreY - first.getBoundingClientRect().top - lh / 2 + "px";
    };
  }

  if (r.middle && !phone) {
    // The highlights under the bottle: one row centred on the bottle, its ink line on the bottle's axis.
    const words = h1.nextElementSibling;
    const ul = words.querySelector("ul");
    const s = stand.getBoundingClientRect();
    const g = glass();
    const holder = document.createElement("div");
    Object.assign(holder.style, { fontFamily: getComputedStyle(document.body).fontFamily, fontSize: "clamp(16px, 1.32vw, 19px)", fontWeight: "450", letterSpacing: "normal", lineHeight: "1.3", position: "absolute", left: s.left - h1.getBoundingClientRect().left + s.width / 2 + "px", top: g.foot - h1.getBoundingClientRect().top + 26 + "px", translate: "-50% 0", width: Math.max(s.width * 1.05, 420) + "px" });
    h1.style.position = "relative";
    Object.assign(ul.style, { margin: "0", borderBottom: "0", padding: "0" });
    holder.append(ul);
    h1.append(holder);
    words.style.marginTop = parseFloat(getComputedStyle(words).marginTop) + 34 + "px";
  }
})();
