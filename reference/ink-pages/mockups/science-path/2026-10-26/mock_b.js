// Mockup B for the Science page: Dr. Liu first, then his path one place per screen, going down,
// then research, health explained, the formulas and Ask. Injected into the live page (throwaway).
(() => {
  const main = document.querySelector("main");
  const journey = document.getElementById("scientists");
  const liu = document.getElementById("liu");
  if (!main || !journey || !liu || document.getElementById("mock-hero")) return;

  const css = `
  #scientists, #liu { display: none !important; }
  #mock-hero { padding-top: 112px; }
  @media (min-width: 960px) { #mock-hero { padding-top: clamp(116px, calc(5.3vw + 42px), 124px); } }
  #mock-hero .mh-grid { max-width: calc(1040px + 2 * var(--gutter)); margin-top: 56px; }
  #mock-hero .mh-grid dl { display: none; }
  #mock-path { padding-top: clamp(48px, 4.5vw, 72px); }
  #mock-path .mp-head { text-align: center; }
  #mock-path .mp-head h2 { margin: 10px 0 0; font-size: clamp(38px, 3.6vw, 54px); font-weight: 500; line-height: 1.04; letter-spacing: -0.012em; }
  #mock-path .mp-head .lead { margin: 14px auto 0; max-width: 44ch; color: var(--muted); font-size: 19px; line-height: 1.6; }
  .place { display: grid; align-items: center; margin-top: clamp(64px, 8vw, 128px); }
  .place:first-of-type { margin-top: 0; }
  .place figure { position: relative; margin: 0; }
  .place img { display: block; width: 100%; height: auto; mix-blend-mode: multiply; }
  .place figcaption { position: absolute; bottom: 2px; right: var(--gutter); margin: 0; color: var(--muted); font-size: 14px; }
  .place .words { padding: 0 var(--gutter); }
  .place .when { margin: 0; color: var(--ink); font-size: 18px; font-weight: 500; }
  #mock-path .place h3 { margin: 12px 0 0; font-size: clamp(46px, 4.6vw, 70px); font-weight: 500; line-height: 1; letter-spacing: -0.015em; }
  .place .what { margin: 18px 0 0; color: var(--ink); font-size: 21px; line-height: 1.35; }
  .place .text { margin: 10px 0 0; color: var(--muted); font-size: 19px; line-height: 1.6; }
  .place .links { display: flex; flex-wrap: wrap; gap: 10px 26px; margin-top: 20px; }
  .place .links a { color: var(--ink); font-size: 17px; text-decoration: underline; text-decoration-color: var(--hair); text-underline-offset: 6px; }
  .place .links a::after { content: " \\2197"; font-size: 14px; }
  @media (min-width: 960px) {
    .place { grid-template-columns: minmax(0, 60fr) minmax(0, 40fr); column-gap: 40px; }
    .place.right { grid-template-columns: minmax(0, 40fr) minmax(0, 60fr); }
    .place.right figure { order: 2; }
    .place.left .words { padding-left: 0; }
    .place.right .words { padding-right: 0; justify-self: end; }
    .place .words { max-width: calc(470px + var(--gutter)); }
    .place.left figcaption { right: auto; left: var(--gutter); }
    .place.right figcaption { right: var(--gutter); }
    .place.wide { grid-template-columns: minmax(0, 1fr); width: min(1120px, 86vw); margin-left: auto; margin-right: auto; }
    .place.wide figure, .place.wide .words { grid-area: 1 / 1; }
    .place.wide figure { width: 100%; }
    .place.wide figcaption { right: 0; }
    .place.wide .words { align-self: start; justify-self: start; max-width: 420px; margin-top: 1%; padding: 0; position: relative; }
  }
  @media (max-width: 959px) {
    #mock-hero .mh-grid { margin-top: 36px; }
    .place figure { width: 100%; }
    .place .words { margin-top: 18px; }
    #mock-path .place h3 { font-size: 46px; }
    .place .what { font-size: 20px; }
    .place .text { font-size: 18px; }
  }`;
  const style = document.createElement("style");
  style.id = "mock-b-style";
  style.textContent = css;
  document.head.append(style);

  // 1. The opening: the title, then Dr. Liu (clones; the originals are hidden).
  const hero = document.createElement("section");
  hero.id = "mock-hero";
  const words = journey.querySelector("[data-pin] > header").cloneNode(true);
  words.classList.add("mh-words");
  const grid = liu.firstElementChild.cloneNode(true);
  grid.classList.add("mh-grid");
  hero.append(words, grid);

  // 2. His path, one place per screen.
  const pic = (name, alt) => `
    <figure>
      <picture>
        <source media="(max-width: 959px)" srcset="/__mock/${name}-phone.webp">
        <img src="/__mock/${name}.webp" alt="${alt}">
      </picture>
      <figcaption>Illustration</figcaption>
    </figure>`;
  const place = (side, name, alt, when, where, what, text, links) => `
    <article class="place ${side}">
      ${pic(name, alt)}
      <div class="words">
        ${when ? `<p class="when">${when}</p>` : ""}
        <h3>${where}</h3>
        ${what ? `<p class="what">${what}</p>` : ""}
        <p class="text">${text}</p>
        ${links.length ? `<p class="links">${links.map(([t, u]) => `<a href="${u}">${t}</a>`).join("")}</p>` : ""}
      </div>
    </article>`;
  const path = document.createElement("section");
  path.id = "mock-path";
  path.innerHTML = `
    ${place(
      "left",
      "okayama",
      "Okayama castle on its hill above the sea",
      "Japan",
      "Okayama",
      "A doctorate in neuroscience",
      "His scientific training began at Okayama University in Japan.",
      [["Faculty profile (Chinese)", "#"]],
    )}
    ${place(
      "right",
      "berkeley",
      "Berkeley's bell tower among eucalyptus above the bay",
      "1994 – 2002 &middot; California",
      "Berkeley",
      "Research in Bruce Ames’s laboratory",
      "At the University of California, Berkeley. In 2002 their study of two nutrients and the aging cell appeared in PNAS, as an animal study.",
      [
        ["Faculty profile (Chinese)", "#"],
        ["Read the 2002 study", "#"],
      ],
    )}
    ${place(
      "left",
      "salzburg",
      "Salzburg's fortress above the old town and the river",
      "2025 &middot; Austria",
      "Salzburg",
      "An academy honor",
      "Elected to the European Academy of Sciences and Arts, based in Salzburg, with more than 280 papers.",
      [["University announcement", "#"]],
    )}
    ${place(
      "wide",
      "california",
      "California oaks on golden hills under a gold sun",
      "",
      "Today",
      "",
      "His research now guides the science behind our formulas.",
      [],
    )}`;

  main.insertBefore(hero, journey);
  main.insertBefore(path, journey);

  // 3. The rest in story order: research, health explained, the formulas, Ask.
  const formulas = document.getElementById("formulas");
  const ask = document.getElementById("ask");
  if (formulas && ask) ask.parentNode.insertBefore(formulas, ask);
  window.scrollTo(0, 0);
})();
