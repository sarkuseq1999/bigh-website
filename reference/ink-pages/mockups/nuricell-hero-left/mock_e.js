// E "The story ahead": under the purpose, the page's own chapters as a row of links down the page,
// one ink line between them like the highlights', a hairline over them. Built from the chapters
// the page has, so a page without a "people" chapter (Turmerific, Propolis) simply has one link
// fewer. Short names, the same on every product.
window.__idea = "e";
window.__push = "hl";
window.__foot = () => {
  const NAMES = {
    why: "Why it matters",
    inside: "What’s inside",
    research: "The research",
    people: "Who made it",
    daily: "How to take it",
  };
  return [...document.querySelectorAll("section[data-chapter]")]
    .map((s) => s.dataset.chapter)
    .filter((id) => NAMES[id])
    .map((id) => `<a data-m="ch" href="#chapter-${id}">${NAMES[id]}</a>`)
    .join("");
};
window.__ideaCss = `
[data-mock=e] [data-m=foot] {
  display: flex; flex-wrap: wrap; row-gap: 10px; margin-top: 24px; padding-top: 14px;
  border-top: 1px solid var(--line);
}
[data-mock=e] [data-m=ch] {
  position: relative; padding-inline: 14px; color: var(--ink); text-decoration: none;
  font-size: clamp(15px, 1.15vw, 17px); font-weight: 450; line-height: 1.3; white-space: nowrap;
}
[data-mock=e] [data-m=ch]:first-child { padding-left: 0; }
[data-mock=e] [data-m=ch] + [data-m=ch]::before {
  content: ""; position: absolute; left: 0; top: 50%; width: 1.5px; height: 1.2em;
  translate: 0 -50%; background: var(--ink); border-radius: 1px;
}
`;
//@include mock_base.js
