(() => {
  // A, "Written by hand": the name round the bottle is brushed in ink instead of set in type.
  const set = window.__mockSet || "flat";
  const sec = document.querySelector('section[data-chapter="overview"]');
  const h1 = sec.querySelector("h1");
  const [, first, stand, second] = h1.children;
  const phone = innerWidth < 960;
  const nuriSize = window.__mockSizes?.[set]?.nuri || [800, 445];
  const cellSize = window.__mockSizes?.[set]?.cell || [686, 415];

  const img = (word) => {
    const i = new Image();
    i.src = `/mock-art/${set}-${word}.png`;
    Object.assign(i.style, { display: "block", mixBlendMode: "multiply", height: "auto" });
    return i;
  };
  const nuri = img("nuri");
  const cell = img("cell");
  const colW = first.getBoundingClientRect().width;
  first.textContent = "";
  second.textContent = "";
  first.append(nuri);
  second.append(cell);
  for (const el of [first, second]) {
    Object.assign(el.style, { lineHeight: "0", fontSize: "0", display: "flex", alignItems: "center" });
  }

  if (!phone) {
    // Both words at one scale; "Nuri" fills its column, as the typed name did.
    const scale = (colW * 1.0) / nuriSize[0];
    nuri.style.width = nuriSize[0] * scale + "px";
    cell.style.width = cellSize[0] * scale + "px";
    first.style.justifyContent = "flex-start";
    second.style.justifyContent = "flex-end";
  } else {
    // One word on a phone: the two halves side by side, about 86% of the screen wide.
    const total = innerWidth * 0.86;
    const scale = total / (nuriSize[0] + cellSize[0] + 20);
    nuri.style.width = nuriSize[0] * scale + "px";
    cell.style.width = cellSize[0] * scale + "px";
    cell.style.marginLeft = 20 * scale + "px";
    first.style.justifyContent = "flex-end";
    second.style.justifyContent = "flex-start";
  }
})();
