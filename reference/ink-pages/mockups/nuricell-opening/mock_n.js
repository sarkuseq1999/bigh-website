(() => {
  // N, "Greetings from California" (after the 1940s "large letter" travel postcards): the name in
  // huge block letters across the page, each letter a little window onto California life. Under it
  // three columns: the headline and purpose, the real bottle, the buy box. Phones stack NURI over CELL.
  const sec = document.querySelector('section[data-chapter="overview"]');
  const wrap = sec.firstElementChild;
  const h1 = sec.querySelector("h1");
  const words = h1.nextElementSibling;
  const [left, buy] = words.children;
  const phone = innerWidth < 960;

  const letters = document.createElement("div");
  const img = (n) => {
    const i = new Image();
    i.src = `/mock-art/post-${n}.png`;
    Object.assign(i.style, { display: "block", height: "auto", maxWidth: "none", mixBlendMode: "multiply" });
    return i;
  };
  const nuri = img("nuri");
  const cell = img("cell");
  letters.append(nuri, cell);
  h1.style.display = "none";
  const bottle = new Image();
  bottle.src = "/mock-art/bottle.png";
  Object.assign(bottle.style, { display: "block", height: "auto", margin: "0 auto" });

  if (!phone) {
    // One line: NURI and CELL at one letter height, the pair as wide as the page's column.
    // The column the page's words use: from the purpose's left edge to the buy box's right edge.
    const colL = left.getBoundingClientRect().left;
    const colW = buy.getBoundingClientRect().right - colL;
    const gap = 0.014 * colW;
    // The pair as wide as the column, never taller than a third of the window.
    const h = Math.min((colW - gap) / (1791 / 585 + 1884 / 618), innerHeight * 0.3);
    nuri.style.height = h + "px";
    cell.style.height = h + "px";
    nuri.style.width = cell.style.width = "auto";
    Object.assign(letters.style, { display: "flex", justifyContent: "center", alignItems: "flex-end", gap: gap + "px", margin: "0 0 3.5vh" });
    wrap.insertBefore(letters, h1);
    const row = document.createElement("div");
    Object.assign(row.style, { display: "grid", gridTemplateColumns: "1fr auto 1fr", gap: "56px", alignItems: "end" });
    bottle.style.width = "min(13vw, 24vh, 230px)";
    const mid = document.createElement("div");
    mid.append(bottle);
    row.append(left, mid, buy);
    Object.assign(buy.style, { width: "100%", maxWidth: "440px", justifySelf: "end", gridColumn: "auto", marginTop: "0" });
    Object.assign(left.style, { maxWidth: "460px" });
    for (const p of left.querySelectorAll("p")) p.style.maxWidth = "none";
    wrap.insertBefore(row, words);
    words.remove();
  } else {
    nuri.style.width = cell.style.width = "100%";
    Object.assign(letters.style, { display: "grid", gap: "2.5vw", margin: "4vw 0 6vw" });
    wrap.insertBefore(letters, h1);
    bottle.style.width = "44vw";
    bottle.style.margin = "0 auto 8vw";
    wrap.insertBefore(bottle, words);
  }
})();
