(() => {
  // C, "The promise first": the giant words round the bottle become the promise, in the title face;
  // the name moves down to head the words under it (it is on the label already).
  const sec = document.querySelector('section[data-chapter="overview"]');
  const h1 = sec.querySelector("h1");
  const [, first, stand, second] = h1.children;
  const words = h1.nextElementSibling;
  const headline = words.children[0].querySelector("p");
  const phone = innerWidth < 960;

  const face = "var(--font-ysabeau), Georgia, serif";
  for (const [el, a, b] of [
    [first, "Stay", "sharp."],
    [second, "Live", "fully."],
  ]) {
    el.innerHTML = `<span class="mk-line">${a}</span><span class="mk-line">${b}</span>`;
    Object.assign(el.style, {
      fontFamily: face,
      fontWeight: "560",
      letterSpacing: "-0.025em",
      lineHeight: "0.9",
      whiteSpace: "nowrap",
    });
  }
  const css = document.createElement("style");
  css.textContent = `.mk-line{display:block}`;
  document.head.append(css);

  // The name heads the words under the bottle, in the page's own name style, smaller.
  const name = document.createElement("p");
  name.textContent = "NuriCell";
  Object.assign(name.style, {
    fontFamily: getComputedStyle(h1).fontFamily,
    fontWeight: "650",
    letterSpacing: "-0.045em",
    lineHeight: "1",
    fontSize: phone ? "56px" : "clamp(56px, 5vw, 84px)",
    margin: "0 0 0.3em",
    color: "inherit",
  });
  headline.replaceWith(name);

  if (!phone) {
    // Fit the wider line of each side to its column, the same size both sides.
    let size = 200;
    for (const el of [first, second]) {
      el.style.fontSize = "100px";
      const widest = Math.max(...[...el.children].map((s) => s.getBoundingClientRect().width));
      size = Math.min(size, (100 * el.getBoundingClientRect().width * 0.92) / widest);
    }
    for (const el of [first, second]) el.style.fontSize = size + "px";
    first.style.textAlign = "right";
    second.style.textAlign = "left";
  } else {
    Object.assign(h1.style, {
      gridTemplateColumns: "1fr",
      justifyItems: "center",
      textAlign: "center",
      rowGap: "0",
    });
    first.style.fontSize = second.style.fontSize = "19vw";
    first.style.gridRow = "1";
    stand.style.gridRow = "2";
    stand.style.gridColumn = "1";
    second.style.gridRow = "3";
    second.style.gridColumn = "1";
    for (const el of [first, second]) {
      el.innerHTML = el.textContent.replace(/^(Stay|Live)/, "$1 ");
      el.style.whiteSpace = "nowrap";
    }
    stand.style.margin = "4vw 0";
  }
})();
