// A "The bottle's label": the words follow the name's three columns. The headline, larger, under
// "Nuri"; the purpose, shorter and in ink, centred under the bottle like a museum label (a short
// painted-ink rule over it); the buy block under "Cell" as now. No side line.
window.__idea = "cols2";
window.__copy =
  "Four nutrients for your mitochondria, the tiny power plants that supply energy for your brain and body.";
window.__css = `
[data-mock=cols2] [data-m=tx] { color: var(--ink) !important; padding-left: 0 !important; }
[data-mock=cols2] [data-m=tx]::before { display: none !important; }
@media (min-width: 960px) {
  [data-mock=cols2] [data-m=left] { display: contents !important; }
  [data-mock=cols2] [data-m=hl] {
    grid-column: 1; grid-row: 1; align-self: end; margin-bottom: 38px !important;
    margin: 0 !important;
    font-size: clamp(40px, 5.6vw, 86px) !important;
    font-weight: 560 !important;
    line-height: 1.02 !important;
    letter-spacing: -0.03em !important;
  }
  [data-mock=cols2] [data-m=tx] {
    grid-column: 2; grid-row: 1; align-self: end; justify-self: center; margin-bottom: 38px !important;
    max-width: 17em !important;
    margin: 0 !important;
    padding-top: 52px !important;
    font-size: clamp(17px, 1.3vw, 20px) !important;
    line-height: 1.5 !important;
    text-align: center;
    position: relative;
  }
  [data-mock=cols2] [data-m=tx]::after {
    content: ""; position: absolute; top: 18px; left: 50%; width: 56px; height: 1.5px;
    translate: -50% 0; background: var(--ink); border-radius: 1px;
  }
  [data-mock=cols2] [data-m=buy] { grid-column: 3; grid-row: 1; }
}
@media (max-width: 959px) {
  [data-mock=cols2] [data-m=tx] { font-size: 19px !important; }
}
`;
//@include mock_common.js
