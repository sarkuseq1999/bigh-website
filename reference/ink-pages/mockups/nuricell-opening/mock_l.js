(() => {
  // L, "The capsule in the line" (after Timeline's tagline with the pill set among its words): the
  // approved headline is the hero, huge and centred, one painted capsule lying among its words. Under
  // it three columns: the name and purpose, the real bottle, the buy box.
  const sec = document.querySelector('section[data-chapter="overview"]');
  const wrap = sec.firstElementChild;
  const h1 = sec.querySelector("h1");
  const [, first, stand, second] = h1.children;
  const words = h1.nextElementSibling;
  const [left, buy] = words.children;
  const headline = left.querySelector("p");
  const phone = innerWidth < 960;
  const nameFont = getComputedStyle(h1).fontFamily;

  // The hero line.
  const line = document.createElement("p");
  const cap = '<img src="/mock-art/capsule1.png" alt="" style="display:inline-block;height:0.78em;width:auto;vertical-align:-0.06em;margin:0 0.12em;mix-blend-mode:multiply">';
  line.innerHTML = phone
    ? `<span style="display:block;white-space:nowrap">Stay sharp.${cap}</span><span style="display:block">Live fully.</span>`
    : `<span style="display:block;white-space:nowrap">Stay sharp.${cap}Live fully.</span>`;
  Object.assign(line.style, {
    fontFamily: nameFont,
    fontWeight: "650",
    letterSpacing: "-0.045em",
    lineHeight: "0.95",
    fontSize: phone ? "13.6vw" : "min(7.3vw, 13.5vh)",
    margin: phone ? "6vw 0 8vw" : "0 0 5vh",
    textAlign: phone ? "left" : "center",
    color: "#151411",
  });

  // The name takes the headline's old place, as the purpose's title.
  const name = document.createElement("p");
  name.textContent = "NuriCell";
  Object.assign(name.style, { fontFamily: nameFont, fontWeight: "650", letterSpacing: "-0.04em", lineHeight: "1", fontSize: phone ? "44px" : "clamp(40px, 3.4vw, 60px)", margin: "0 0 0.35em" });
  headline.replaceWith(name);

  h1.style.display = "none";
  const bottle = new Image();
  bottle.src = "/mock-art/bottle.png";
  Object.assign(bottle.style, { display: "block", height: "auto", margin: "0 auto" });

  if (!phone) {
    wrap.insertBefore(line, h1);
    const row = document.createElement("div");
    Object.assign(row.style, { display: "grid", gridTemplateColumns: "1fr auto 1fr", gap: "56px", alignItems: "end" });
    bottle.style.width = "min(15vw, 26vh, 250px)";
    const mid = document.createElement("div");
    mid.append(bottle);
    row.append(left, mid, buy);
    Object.assign(buy.style, { width: "100%", maxWidth: "440px", justifySelf: "end", gridColumn: "auto", marginTop: "0" });
    Object.assign(left.style, { maxWidth: "440px" });
    for (const p of left.querySelectorAll("p")) p.style.maxWidth = "none";
    wrap.insertBefore(row, words);
    words.remove();
  } else {
    wrap.insertBefore(line, h1);
    bottle.style.width = "46vw";
    bottle.style.margin = "0 auto 8vw";
    wrap.insertBefore(bottle, words);
  }
  void first; void stand; void second;
})();
