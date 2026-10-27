// Second round (October 26): Mo turned down the photo credit because the pages without Dr. Liu
// would look lesser, so these ideas use only what all five product pages have. Shared by C, D and
// E: the headline as it is (two lines: the other products' headlines are too long for one), the
// purpose in ink at a reading size with no side line, and from 960px the block's foot on Add to
// cart's foot. An idea sets window.__foot (a row under the purpose, HTML, or a function that
// builds it from the page), window.__push (which part takes the free space above it: "hl" keeps
// the whole block together at the foot, "tx" keeps the headline up and drops the purpose) and
// window.__ideaCss.
window.__css =
  `
[data-mock] [data-m=tx] {
  color: var(--ink) !important; padding-left: 0 !important;
  max-width: var(--tx-measure, 27em) !important; font-size: clamp(18px, 1.4vw, 21px) !important; line-height: 1.55 !important;
}
[data-mock] [data-m=tx]::before { display: none !important; }
[data-mock] [data-m=foot] { margin-top: 28px; }
@media (min-width: 960px) {
  [data-mock] [data-m=left] { align-self: stretch; display: flex; flex-direction: column; }
  [data-mock]:not([data-buy-top]) [data-m=buy] { align-self: end; }
  [data-mock] [data-pushed] { margin-top: auto !important; }
}
` + (window.__ideaCss || "");
//@include mock_common.js
(() => {
  const P = window.__parts;
  // A dash stays with the word before it (the built page would do this in the data or keepTogether).
  P.text.textContent = P.text.textContent.replace(/(\S)—/g, "$1⁠—");
  if (window.__foot) {
    const foot = document.createElement("div");
    foot.setAttribute("data-m", "foot");
    const html = typeof window.__foot === "function" ? window.__foot(P) : window.__foot;
    if (typeof html === "string") foot.innerHTML = html;
    else foot.appendChild(html);
    P.left.appendChild(foot);
    P.foot = foot;
  }
  const push = { hl: P.headline, tx: P.text, foot: P.foot }[window.__push || "hl"];
  push.setAttribute("data-pushed", "");
  if (window.__buyTop) P.ow.setAttribute("data-buy-top", "");
  if (innerWidth >= 960 && !window.__buyTop) {
    const btn = P.buy.querySelector("button");
    P.left.style.paddingBottom = P.buy.getBoundingClientRect().bottom - btn.getBoundingClientRect().bottom + "px";
  }
})();
