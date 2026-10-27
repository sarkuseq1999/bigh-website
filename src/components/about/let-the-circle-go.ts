// The circle waits for its picture (circle.module.css): with script on, its stroke holds until the
// stroke's picture is in. This lets it go before React hydrates, where the parser reaches it (after
// the page's HTML): once the picture is in, however late, it adopts a sheet that sets it running.
// No timer and no release on a failed picture: either would start the sweep over bare paper. It
// changes no node or attribute React rendered, so hydration cannot mismatch. Without constructed
// sheets it does nothing; once hydrated, the Opening lets it go too (about-ink.tsx). The About
// pages render it through BeforeHydration, in the server's HTML only, so a client-side navigation
// to /about neither builds a dead script nor logs React's script warning.
export const LET_THE_CIRCLE_GO = `(() => {
  const stroke = document.querySelector("[data-enso] img");
  if (!stroke || !document.adoptedStyleSheets) return;
  let sheet;
  try {
    sheet = new CSSStyleSheet();
    sheet.replaceSync("[data-enso] * { animation-play-state: running !important; }");
  } catch (e) {
    return;
  }
  const go = () => {
    document.adoptedStyleSheets = [...document.adoptedStyleSheets, sheet];
  };
  if (stroke.complete) {
    if (stroke.naturalWidth) go();
    return;
  }
  stroke.addEventListener("load", go, { once: true });
})();`;
