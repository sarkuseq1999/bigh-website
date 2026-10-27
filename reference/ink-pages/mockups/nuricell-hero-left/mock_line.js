// Shared by B and C: "Stay sharp. Live fully." on one line under "Nuri" and the bottle, the purpose
// shorter and in ink with no side line, and a row at the foot (window.__row, built by the idea)
// under a hairline that runs the block's width, like the one under the highlights. From 960px the
// row's foot sits on Add to cart's, so the two sides end together.
window.__copy =
  "Four nutrients for your mitochondria, the tiny power plants that supply energy for your brain and body.";
window.__css =
  `
[data-mock] [data-m=hl] {
  font-size: clamp(36px, 4.1vw, 64px) !important;
  font-weight: 540 !important;
  line-height: 1.04 !important;
  letter-spacing: -0.028em !important;
  margin: 0 0 18px !important;
  white-space: nowrap;
}
[data-mock] [data-m=hl] span { display: inline !important; }
[data-mock] [data-m=hl] span + span { margin-left: 0.26em; }
@media (max-width: 959px) {
  [data-mock] [data-m=hl] { white-space: normal; }
  [data-mock] [data-m=hl] span { display: block !important; }
  [data-mock] [data-m=hl] span + span { margin-left: 0; }
}
[data-mock] [data-m=tx] {
  color: var(--ink) !important; padding-left: 0 !important;
  max-width: 34em !important; font-size: clamp(18px, 1.35vw, 20px) !important; line-height: 1.55 !important;
}
[data-mock] [data-m=tx]::before { display: none !important; }
[data-mock] [data-m=row] { margin-top: 28px; padding-top: 16px; border-top: 1px solid var(--line); }
@media (min-width: 960px) {
  [data-mock] [data-m=left] { align-self: stretch; display: flex; flex-direction: column; }
  [data-mock] [data-m=row] { margin-top: auto; }
  [data-mock] [data-m=tx] { margin-bottom: 22px !important; }
}
` + (window.__rowCss || "");
//@include mock_common.js
(() => {
  const row = document.createElement("div");
  row.setAttribute("data-m", "row");
  row.innerHTML = window.__row;
  window.__parts.left.appendChild(row);
  if (innerWidth >= 960) {
    const btn = window.__parts.buy.querySelector("button");
    const rowBottom = window.__parts.buy.getBoundingClientRect().bottom;
    window.__parts.left.style.paddingBottom = rowBottom - btn.getBoundingClientRect().bottom + "px";
  }
})();
