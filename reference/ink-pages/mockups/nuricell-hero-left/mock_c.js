// C "Facts on the left": the two highlights every product has ("Mitochondrial health | Mental
// energy") move from over the buy card to the foot of the words, a little larger, one ink line
// between them and a hairline over them, so the left ends on its two facts where Add to cart ends
// and the right starts straight with the card.
window.__idea = "c";
window.__push = window.__push || "hl";
window.__foot = (P) => P.buy.querySelector("ul");
window.__ideaCss = `
[data-mock=c] [data-m=foot] { margin-top: 22px; }
[data-mock=c] [data-m=hl] { margin-bottom: 18px !important; }
[data-mock=c] [data-m=foot] ul {
  display: flex !important; flex-wrap: wrap; gap: 8px 0; margin: 0 !important;
  padding: 14px 0 0 !important; border-bottom: 0 !important; border-top: 1px solid var(--line);
  font-size: clamp(18px, 1.5vw, 22px) !important; font-weight: 500 !important;
}
[data-mock=c] [data-m=foot] li { text-align: left !important; padding-inline: 0 22px !important; }
[data-mock=c] [data-m=foot] li + li { padding-left: 22px !important; }
[data-mock=c] [data-m=foot] li + li::before { height: 1.2em !important; }
`;
//@include mock_base.js
