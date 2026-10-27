// A "Signed by Dr. Liu": the one-line headline and the purpose (mock_line.js), and at the foot who
// made it: Dr. Liu's real photo, in colour, and "Formulated by Dr. Jiankang Liu" (the product's
// credit), his field under it (his chapter's own words).
window.__idea = "a";
window.__row =
  '<span data-m="face" role="img" aria-label="Dr. Jiankang Liu"></span>' +
  '<p data-m="who">Formulated by <span style="white-space:nowrap">Dr. Jiankang Liu</span></p>' +
  '<p data-m="field">Scientist in mitochondrial biology and aging</p>';
window.__rowCss = `
[data-mock=a] [data-m=row] { display: grid; grid-template-columns: auto 1fr; column-gap: 16px; align-items: center; }
[data-mock=a] [data-m=face] {
  grid-row: 1 / 3; width: 64px; height: 64px; border-radius: 50%;
  background: url(/images/jiankang-liu.jpg) 49% 16% / 175% auto no-repeat;
}
[data-mock=a] [data-m=who] { margin: 0; align-self: end; font-size: 19px; font-weight: 500; line-height: 1.3; }
[data-mock=a] [data-m=field] { margin: 2px 0 0; align-self: start; color: var(--muted); font-size: 15px; line-height: 1.4; }
@media (max-width: 959px) {
  [data-mock=a] [data-m=row] { margin-bottom: 8px; }
  [data-mock=a] [data-m=face] { width: 60px; height: 60px; }
  [data-mock=a] [data-m=who] { font-size: 18px; }
}
`;
//@include mock_line.js
