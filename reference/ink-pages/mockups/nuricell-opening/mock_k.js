(() => {
  // K, "Inside the redwoods" (after Nature Ritual's full-screen hero, words in its corners, and
  // Apple's AirPods page, one line and a buy pill): one full-width ink painting of a redwood grove,
  // the real bottle standing on an old stump in the middle, the headline's four words in the
  // painting's corners. Under the painting one slim row: the name and a fact, the bottle card, Add to cart.
  const sec = document.querySelector('section[data-chapter="overview"]');
  const wrap = sec.firstElementChild;
  const h1 = sec.querySelector("h1");
  const words = h1.nextElementSibling;
  const [left, buy] = words.children;
  const phone = innerWidth < 960;
  const W = innerWidth, H = innerHeight;
  const nameFont = getComputedStyle(h1).fontFamily;
  const cfg = window.__k || {};
  const aspect = cfg.aspect || 1.75;

  const scene = document.createElement("div");
  const paint = new Image();
  paint.src = `/mock-art/${cfg.art || "redwoods1"}.png`;
  Object.assign(paint.style, { display: "block", width: "100%", height: "auto", mixBlendMode: "multiply" });
  const bottle = new Image();
  bottle.src = "/mock-art/bottle.png";
  Object.assign(bottle.style, { position: "absolute", height: "auto" });
  scene.append(paint, bottle);
  const b = phone ? cfg.phoneBottle || cfg.bottle : cfg.bottle;
  Object.assign(bottle.style, { left: b.x + "%", width: b.w + "%", bottom: 100 - b.base + "%" });

  const corner = (text, pos) => {
    const el = document.createElement("p");
    el.textContent = text;
    Object.assign(el.style, {
      position: "absolute",
      margin: "0",
      fontFamily: nameFont,
      fontWeight: "650",
      letterSpacing: "-0.045em",
      lineHeight: "0.9",
      fontSize: phone ? "15vw" : cfg.wordSize || "min(10vw, 17vh)",
      color: "#151411",
      ...pos,
    });
    scene.append(el);
  };
  const inset = phone ? "4vw" : cfg.inset || "3.2%";
  corner("Stay", { left: inset, top: inset });
  corner("sharp.", { right: inset, top: inset });
  corner("Live", { left: inset, bottom: inset });
  corner("fully.", { right: inset, bottom: inset });

  const fact = document.createElement("p");
  fact.textContent = "Coast redwoods can live 2,000 years, and sprout again from an old stump.";
  Object.assign(fact.style, { margin: "6px 0 0", font: "500 15px/1.45 var(--font-switzer, Switzer), system-ui, sans-serif", color: "#5b564d" });

  h1.style.display = "none";
  const headline = left.querySelector("p");
  const name = document.createElement("p");
  name.textContent = "NuriCell";
  Object.assign(name.style, { fontFamily: nameFont, fontWeight: "650", letterSpacing: "-0.04em", lineHeight: "1", fontSize: phone ? "44px" : "clamp(40px, 3.2vw, 56px)", margin: "0 0 0.3em" });
  headline.replaceWith(name);

  if (!phone) {
    Object.assign(sec.style, { position: "relative", paddingTop: "0" });
    Object.assign(wrap.style, { position: "relative" });
    // The painting runs the window's full width, from just under the menu bar's rule.
    // The menu bar over the opening is clamp(88px, 6.6vw, 104px) tall (DESIGN.md), its rule at its foot.
    const navBottom = Math.min(104, Math.max(88, 0.066 * W)) + 10;
    const w = wrap.getBoundingClientRect();
    // The whole painting, its own soft edges kept: as wide as the window allows under the menu bar,
    // with room for one row under it.
    const sh = Math.min(W / aspect, H - navBottom - 150);
    const sw = sh * aspect;
    const ph = sh;
    Object.assign(scene.style, { position: "absolute", left: (W - sw) / 2 - w.left + "px", top: navBottom + 4 - w.top + "px", width: sw + "px", height: sh + "px", pointerEvents: "none" });
    Object.assign(paint.style, { position: "absolute", left: "0", bottom: -(cfg.cropFoot || 0) + "px" });
    Object.assign(bottle.style, { bottom: ((100 - b.base) / 100) * ph - (cfg.cropFoot || 0) + "px", width: (b.w / 100) * sw + "px", left: (b.x / 100) * sw + "px" });
    wrap.prepend(scene);
    const spacer = document.createElement("div");
    spacer.style.height = navBottom + 4 + sh - w.top + "px";
    wrap.insertBefore(spacer, h1);
    const row = document.createElement("div");
    Object.assign(row.style, { display: "grid", gridTemplateColumns: "1fr minmax(560px, 1.25fr)", gap: "40px", alignItems: "center", marginTop: "22px" });
    const purpose = left.querySelector("p:not(:first-child)");
    if (purpose) purpose.remove();
    left.querySelector("ul")?.remove();
    left.append(fact);
    row.append(left, buy);
    Object.assign(buy.style, { width: "100%", maxWidth: "none", gridColumn: "auto", marginTop: "0", display: "grid", gridTemplateColumns: "1.35fr 1fr", gap: "12px 20px", alignItems: "center" });
    buy.querySelector("ul")?.remove();
    wrap.insertBefore(row, words);
    words.remove();
  } else {
    // Phone: a window onto the middle of the painting, the stump in the middle, the words in its corners.
    const pw = 165;
    Object.assign(scene.style, { position: "relative", width: "100vw", height: "112vw", marginLeft: "calc(50% - 50vw)", marginTop: "2vw", overflow: "hidden" });
    Object.assign(paint.style, { position: "absolute", maxWidth: "none", width: pw + "vw", left: -(pw * b.x / 100 + pw * b.w / 200 - 50) + "vw", bottom: "15vw" });
    Object.assign(bottle.style, { width: (pw * b.w) / 100 + "vw", left: 50 - (pw * b.w) / 200 + "vw", bottom: 15 + ((100 - b.base) / 100) * (pw / aspect) + "vw" });
    wrap.insertBefore(scene, h1);
    left.append(fact);
  }
})();
