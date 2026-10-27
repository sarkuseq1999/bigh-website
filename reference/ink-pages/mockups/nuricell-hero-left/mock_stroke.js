// B "One brushstroke": the headline larger and a little heavier, one painted dry-brush stroke laid
// under "sharp." as the page opens (like the menu bar's rule), the purpose shorter and in ink, no
// side line, its last line on the refund line's level so the two sides end together.
// Stand-in stroke: the Buy chapter's, its paper divided out (a new one would be painted for this).
window.__idea = "stroke";
window.__copy =
  "Four nutrients for your mitochondria, the tiny power plants that supply energy for your brain and body.";
window.__css = `
[data-mock=stroke] [data-m=hl] {
  font-size: clamp(40px, 4.7vw, 76px) !important;
  font-weight: 560 !important;
  line-height: 1.17 !important;
  letter-spacing: -0.03em !important;
  margin: -0.08em 0 30px !important;
}
[data-mock=stroke] [data-m=hl] [data-m=stroke] { position: relative !important; display: inline-block !important; }
[data-mock=stroke] [data-m=stroke]::after {
  content: ""; position: absolute; z-index: -1;
  left: -0.04em; right: -0.22em; bottom: -0.11em; height: 0.2em;
  background: url(/mock-art/stroke-standin.webp) 0 0 / 100% 100% no-repeat;
  clip-path: inset(0 100% 0 0);
  animation: mockLay 1.1s cubic-bezier(.6,.05,.25,1) .3s forwards;
}
@keyframes mockLay { to { clip-path: inset(0 0 0 0); } }
[data-mock=stroke] [data-m=tx] {
  color: var(--ink) !important; padding-left: 0 !important;
  max-width: 22em !important; font-size: clamp(18px, 1.35vw, 20px) !important; line-height: 1.55 !important;
}
[data-mock=stroke] [data-m=tx]::before { display: none !important; }
@media (min-width: 960px) {
  [data-mock=stroke] [data-m=left] { align-self: stretch; display: flex; flex-direction: column; justify-content: space-between; }
}
`;
//@include mock_common.js
(() => {
  const first = window.__parts.headline.children[0];
  first.innerHTML = 'Stay <span data-m="stroke">sharp.</span>';
  window.__parts.headline.style.isolation = "isolate";
})();
