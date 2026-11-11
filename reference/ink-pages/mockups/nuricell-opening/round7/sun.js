// Mock: lay the sunlight layers into the opening's painting group (.sky), before the fog.
// window.__sun = { kind: "corner" | "disc", take: "suncorner-a" | "sundisc-b", sea: "sundisc-b" }
(() => {
  const cfg = window.__sun || { kind: "corner", take: "suncorner-a" };
  const sky = document.querySelector("[data-sky]");
  const fog = [...sky.children].find((e) => e.className.includes("skyFog"));
  const src = (take, part) => `/images/products/nuricell/ink/opening-sun-${take}-${part}.webp?v=${Date.now()}`;
  const add = (cls, take, part) => {
    const img = document.createElement("img");
    img.src = src(take, part);
    img.alt = "";
    img.className = cls;
    sky.insertBefore(img, fog);
    return img;
  };
  const css = document.createElement("style");
  // Shared: where the sun is (its middle 0.32 name-sizes in from the window's right edge), and
  // its glitter on the sea under it. Glitter's sun: 308/582 across its layer.
  let text = `
    [data-sky] { --sun-x: calc(50% + 50vw - 0.32 * var(--name)); --sun-row: calc(360 / 800 * 100%);
      --disc-w: 23.6%; --disc-h: 44%; --sea-w: 17.8%; --sea-h: 6%; }
    [data-sky] img.mockSunSea { position: absolute; display: block; max-width: none;
      width: var(--sea-w) !important; height: var(--sea-h) !important;
      left: calc(var(--sun-x) - 0.529 * var(--sea-w)); top: calc(610 / 800 * 100%); }
    @media (max-width: 959px) {
      [data-sky] { --sun-x: calc(50% + 50vw - 46px); --sun-row: 55.7%;
        --disc-w: 26.9%; --disc-h: 32.7%; --sea-w: 20.4%; --sea-h: 4.4%; }
    }`;
  if (cfg.kind === "corner") {
    add("mockSunCorner", cfg.take, "sky");
    text += `
      [data-sky] img.mockSunCorner { position: absolute; display: block; max-width: none; height: auto;
        top: var(--sun-top, -1.6%); width: var(--sun-w, 42%) !important; left: calc(50% + 50vw - var(--sun-w, 42%)); }
      @media (max-width: 959px) {
        [data-sky] img.mockSunCorner { --sun-top: -3.75%; --sun-w: 44%; }
      }`;
    // Under the corner's light, the glitter sits a little further out (the sun is beyond the corner).
    if (cfg.sea) {
      add("mockSunSea", cfg.sea, "sea");
      text += `
        [data-sky] { --sun-x: calc(50% + 50vw - 0.22 * var(--name)); }
        @media (max-width: 959px) { [data-sky] { --sun-x: calc(50% + 50vw - 34px); } }`;
    }
  } else {
    add("mockSunDisc", cfg.take, "sky");
    add("mockSunSea", cfg.sea || cfg.take, "sea");
    // Sun's middle in its layer: 494/768 across, 183/747 down.
    text += `
      [data-sky] img.mockSunDisc { position: absolute; display: block; max-width: none;
        width: var(--disc-w) !important; height: auto !important;
        left: calc(var(--sun-x) - 0.643 * var(--disc-w)); top: calc(var(--sun-row) - 0.245 * var(--disc-h)); }`;
  }
  css.textContent = text;
  document.head.append(css);
})();
