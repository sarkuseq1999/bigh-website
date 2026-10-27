// Replace NuriCell's Questions section with one of three ideas. Set window.__idea ("a", "b", "c")
// and, for A, window.__pick (the chosen question, 0-5) before this runs. Pictures come from
// /mock-art/ (this folder's art/, paper divided out); the bottle and its pool from the site.
(() => {
  const idea = window.__idea;
  const pick = window.__pick ?? 0;
  const QA = [
    {
      q: "How do I take NuriCell?",
      a: "Take 3 capsules once a day, with or after a meal.",
      big: "3 a day",
      art: "q1-take",
    },
    {
      q: "How long does one bottle last?",
      a: "Each bottle holds 90 vegetarian capsules: a 30-day supply at 3 capsules a day.",
      big: "30 days",
      art: "q2-month",
    },
    {
      q: "What is the capsule made of?",
      a: "The capsule is vegetarian: hypromellose, with titanium dioxide for its white colour. The other ingredients are rice flour, silicon dioxide and magnesium stearate.",
      big: "Vegetarian",
      art: "q3-capsule",
    },
    {
      q: "Has NuriCell itself been tested in a clinical trial?",
      a: "The research we share is about NuriCell’s ingredients, not the finished product. Each study says whether it was done in people or in animals.",
      big: "Ingredient studies",
      art: "q4-studied",
    },
    {
      q: "Can I take it with medicines or other supplements?",
      a: "Ask your doctor first, especially if you have a health condition or take medicines.",
      big: "Ask your doctor",
      art: "q5-doctor",
    },
    {
      q: "Can I take NuriCell during pregnancy?",
      a: "No. The label advises not to take it if you are pregnant or breastfeeding.",
      big: "No",
      art: "q6-pregnancy",
    },
  ];

  const section = document.querySelector("#questions");
  const wrap = section.querySelector(":scope > div");
  const heading = wrap.querySelector("h2");
  [...wrap.children].forEach((el) => el !== heading && el.remove());

  const css = document.createElement("style");
  const root = document.createElement("div");
  root.className = `mq mq-${idea}`;
  wrap.append(root);

  const phone = innerWidth < 960;
  const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");

  css.textContent = `
  .mq { --mq-ink: var(--ink, #0c0b0a); --mq-muted: var(--muted, #514e48); --mq-hair: var(--hair, rgba(28,27,25,.28)); }
  .mq img.art { display: block; width: 100%; height: auto; mix-blend-mode: multiply; }
  .mq p { margin: 0; }
  `;

  if (idea === "a") {
    // A. Pick a question: the questions on the left, the chosen one's painting and answer on the
    // right (one picture at a time). Phones: the chosen question opens in place with its picture.
    css.textContent += `
    .mq-a { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: clamp(40px, 6vw, 110px); align-items: start; margin-top: 8px; }
    .mq-a ol { list-style: none; margin: 0; padding: 0; }
    .mq-a li { border-top: 1px solid var(--mq-hair); }
    .mq-a li:last-child { border-bottom: 1px solid var(--mq-hair); }
    .mq-a button { all: unset; box-sizing: border-box; display: block; position: relative; width: 100%; padding: 19px 0 19px 0; font-size: 20px; line-height: 1.35; font-weight: 500; color: var(--mq-muted); cursor: pointer; }
    .mq-a li.on button { color: var(--mq-ink); }
    .mq-a li.on button::before { content: ""; position: absolute; inset: 8px -14px 8px -14px; background: url("/images/home-v2/nav/inscription/wash-v1.webp") 0 0 / 100% 100% no-repeat; opacity: .55; z-index: -1; }
    .mq-a button { isolation: isolate; }
    .mq-a .stage { position: relative; }
    .mq-a .stage .art { max-width: 640px; margin: -24px 0 -28px -20px; }
    .mq-a .stage p { max-width: 21em; font-size: clamp(22px, 1.9vw, 28px); line-height: 1.32; color: var(--mq-ink); text-wrap: pretty; }
    .mq-a .stage small { display: block; margin-top: 14px; color: var(--mq-muted); font-size: 15px; }
    @media (max-width: 959px) {
      .mq-a { display: block; }
      .mq-a button { font-size: 19px; padding: 18px 44px 18px 0; color: var(--mq-ink); }
      .mq-a li.on button { padding-left: 0; }
      .mq-a li.on button::before { display: none; }
      .mq-a button::after { content: "+"; position: absolute; right: 0; top: 50%; width: 36px; height: 36px; margin-top: -18px; border: 1px solid var(--mq-hair); border-radius: 50%; display: grid; place-items: center; font-size: 18px; font-weight: 400; }
      .mq-a li.on button::after { content: "–"; }
      .mq-a .open .art { margin: -6px 0 2px; }
      .mq-a .open p { font-size: 20px; line-height: 1.4; color: var(--mq-ink); padding-bottom: 22px; }
    }`;
    const items = QA.map(
      (x, i) =>
        `<li class="${i === pick ? "on" : ""}"><button type="button">${esc(x.q)}</button>${
          phone && i === pick
            ? `<div class="open"><img class="art" src="/mock-art/${x.art}.png" alt=""><p>${esc(x.a)}</p></div>`
            : ""
        }</li>`,
    ).join("");
    root.innerHTML = phone
      ? `<ol>${items}</ol>`
      : `<ol>${items}</ol><div class="stage"><img class="art" src="/mock-art/${QA[pick].art}.png" alt=""><p>${esc(
          QA[pick].a,
        )}</p></div>`;
  }

  if (idea === "b") {
    // B. Big answers: every answer showing, its short form large on the left, the question and
    // the label's whole sentence on the right. Nothing to open.
    css.textContent += `
    .mq-b { margin-top: 8px; }
    .mq-b ol { list-style: none; margin: 0; padding: 0; }
    .mq-b li { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: 40px; align-items: baseline; padding: 26px 0 28px; border-top: 1px solid var(--mq-hair); }
    .mq-b li:last-child { border-bottom: 1px solid var(--mq-hair); }
    .mq-b .big { justify-self: start; position: relative; z-index: 0; font-family: var(--display-font); font-weight: var(--display-weight, 500); font-size: clamp(40px, 3.6vw, 58px); line-height: 1; letter-spacing: -0.03em; color: var(--mq-ink); }
    .mq-b .big::before { content: ""; position: absolute; inset: 14% -18px -10% -16px; background: url("/images/home-v2/nav/inscription/wash-v1.webp") 0 0 / 100% 100% no-repeat; opacity: .6; z-index: -1; }
    .mq-b .q { font-size: 20px; line-height: 1.35; font-weight: 500; color: var(--mq-ink); }
    .mq-b .a { margin-top: 8px; max-width: 34em; font-size: 17px; line-height: 1.55; color: var(--mq-muted); }
    @media (max-width: 959px) {
      .mq-b li { display: block; padding: 22px 0 24px; }
      .mq-b .big { font-size: 40px; }
      .mq-b .q { margin-top: 12px; font-size: 18px; }
    }`;
    root.innerHTML = `<ol>${QA.map(
      (x) =>
        `<li><p class="big">${esc(x.big)}</p><div><p class="q">${esc(x.q)}</p><p class="a">${esc(x.a)}</p></div></li>`,
    ).join("")}</ol>`;
  }

  if (idea === "c") {
    // C. The breakfast table: one painting, numbered like a botanist's plate, the real bottle
    // standing in its empty spot; every answer showing under it, keyed by number.
    const marks = window.__marks || [];
    css.textContent += `
    .mq-c { margin-top: 0; }
    .mq-c .plate { position: relative; max-width: 980px; margin: -10px auto 0; }
    .mq-c .bottle { position: absolute; }
    .mq-c .bottle img { position: absolute; display: block; max-width: none; height: auto; }
    .mq-c .bottle .pool { mix-blend-mode: multiply; opacity: .75; }
    .mq-c .mark { position: absolute; width: 34px; height: 34px; margin: -17px 0 0 -17px; border-radius: 50%; background: #f8f3ea; border: 1.5px solid var(--mq-ink); color: var(--mq-ink); display: grid; place-items: center; font-size: 16px; font-weight: 600; }
    .mq-c ol { list-style: none; margin: 18px 0 0; padding: 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); column-gap: clamp(28px, 3.4vw, 56px); }
    .mq-c li { display: grid; grid-template-columns: 34px minmax(0, 1fr); column-gap: 14px; padding: 22px 0 26px; border-top: 1px solid var(--mq-hair); }
    .mq-c li .n { box-sizing: border-box; width: 34px; height: 34px; border-radius: 50%; border: 1.5px solid var(--mq-ink); color: var(--mq-ink); display: grid; place-items: center; font-size: 16px; font-weight: 600; }
    .mq-c .q { font-size: 19px; line-height: 1.35; font-weight: 500; color: var(--mq-ink); }
    .mq-c .a { margin-top: 8px; font-size: 16.5px; line-height: 1.55; color: var(--mq-muted); }
    @media (max-width: 959px) {
      .mq-c .bleed { overflow: hidden; margin: 0 calc(-1 * var(--gutter)); }
      .mq-c .plate { width: 100%; margin: 0; }
      .mq-c .mark { width: 24px; height: 24px; margin: -12px 0 0 -12px; font-size: 12.5px; border-width: 1px; }
      .mq-c ol { grid-template-columns: 1fr; }
      .mq-c li { padding: 18px 0 20px; }
      .mq-c .q { font-size: 18px; }
    }`;
    const b = window.__bottle || { x: 0.8, y: 0.62, h: 0.42 };
    root.innerHTML = `<div class="bleed"><div class="plate"><img class="art" src="/mock-art/table.png" alt="">
      <span class="bottle" style="left:${b.x * 100}%;top:${b.y * 100}%;"></span>
      ${marks.map((m, i) => `<span class="mark" style="left:${m[0] * 100}%;top:${m[1] * 100}%">${i + 1}</span>`).join("")}
      </div></div><ol>${QA.map(
        (x, i) =>
          `<li><span class="n">${i + 1}</span><div><p class="q">${esc(x.q)}</p><p class="a">${esc(x.a)}</p></div></li>`,
      ).join("")}</ol>`;
    // The bottle: its height a share of the painting's, its base on the table line at (x, y).
    const plate = root.querySelector(".plate");
    const place = () => {
      const W = plate.clientWidth;
      const H = plate.querySelector(".art").clientHeight;
      const span = root.querySelector(".bottle");
      span.innerHTML = "";
      const bh = H * b.h;
      const bw = (bh * 1230) / 1278;
      const pool = document.createElement("img");
      pool.className = "pool";
      pool.src = "/images/home-v2/ink/pool.webp";
      const pw = bw * 1.25;
      pool.style.cssText = `width:${pw}px;left:${-pw / 2}px;top:${-pw * 0.3}px;`;
      const img = document.createElement("img");
      img.src = "/images/products/nuricell.png";
      // The bottle's visible base is 0.972 of its picture's height down.
      img.style.cssText = `width:${bw}px;left:${-bw / 2}px;top:${-bh * 0.972}px;`;
      span.append(pool, img);
    };
    const art = plate.querySelector(".art");
    art.addEventListener("load", place);
    if (art.complete && art.naturalWidth) place();
    addEventListener("resize", place);
  }

  document.head.append(css);
})();
