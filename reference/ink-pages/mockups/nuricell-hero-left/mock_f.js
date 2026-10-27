// F "Bigger words": nothing added; the purpose becomes a large lead in ink that runs under the
// bottle (the column the block already spans), so the words alone fill the space and weigh as
// much as the buy block. The block ends where Add to cart ends (mock_base.js).
window.__idea = window.__idea || "f";
window.__push = window.__push || "tx";
window.__ideaCss = `
[data-mock] [data-m=hl] { margin-bottom: 20px !important; }
` + (window.__fCss || "") + `
[data-mock] [data-m=tx] {
  max-width: 30em !important; font-size: clamp(20px, 1.6vw, 26px) !important;
  line-height: 1.4 !important; letter-spacing: -0.012em !important; font-weight: 420 !important;
}
`;
//@include mock_base.js
