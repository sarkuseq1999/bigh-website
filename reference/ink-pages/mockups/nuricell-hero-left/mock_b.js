// B "What's inside": the one-line headline and the purpose (mock_line.js), and at the foot the four
// nutrients and how much of each in a serving of 3 capsules (the label's amounts, nuricell.ts), one
// ink line between them like the highlights' under "Cell". Two by two on a phone, with no lines
// (stacked over the highlights' line they made a table).
window.__idea = "b";
window.__row = [
  ["400 mg", "Acetyl-L-carnitine"],
  ["400 mg", "Creatine"],
  ["200 mg", "Alpha-lipoic acid"],
  ["100 mg", "Choline"],
]
  .map(([amount, name]) => `<div data-m="n"><p data-m="amt">${amount}</p><p data-m="nm">${name}</p></div>`)
  .join("");
window.__rowCss = `
[data-mock=b] [data-m=row] { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); }
[data-mock=b] [data-m=n] { position: relative; padding-inline: 14px; }
[data-mock=b] [data-m=n]:first-child { padding-left: 0; }
[data-mock=b] [data-m=n] + [data-m=n]::before {
  content: ""; position: absolute; left: 0; top: 50%; width: 1.5px; height: 2.4em;
  translate: 0 -50%; background: var(--ink); border-radius: 1px;
}
[data-mock=b] [data-m=amt] { margin: 0; font-size: clamp(20px, 1.6vw, 24px); font-weight: 500; line-height: 1.2; letter-spacing: -0.01em; }
[data-mock=b] [data-m=nm] { margin: 3px 0 0; color: var(--muted); font-size: 15px; line-height: 1.3; }
@media (max-width: 599px) {
  [data-mock=b] [data-m=row] { grid-template-columns: repeat(2, minmax(0, 1fr)); row-gap: 16px; margin-bottom: 8px; }
  [data-mock=b] [data-m=n] { padding-left: 0; }
  [data-mock=b] [data-m=n]::before { display: none; }
}
`;
//@include mock_line.js
