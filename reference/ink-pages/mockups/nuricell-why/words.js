// The Why chapter's words, tidied: no eyebrow, one lead-in line in place of three paragraphs, every
// line on the heading's left edge, the 2% set small beside a big 20% (the brain is small, its
// energy use is not), the 20-watt line kept as the close.
(() => {
  const ch = document.querySelector("[data-chapter=why]");
  const words = ch.querySelector("[data-words]");
  words.querySelector("p[class*=label]")?.remove();
  const texts = [...words.querySelectorAll("p[class*=text]")];
  texts.slice(1).forEach((p) => p.remove());
  const lead = texts[0];
  lead.textContent = "Inside many of your cells, mitochondria turn food into the energy you live on.";
  Object.assign(lead.style, {
    paddingLeft: "0",
    maxWidth: "21em",
    color: "var(--ink)",
    fontSize: "clamp(19px, 1.5vw, 22px)",
  });
  const facts = words.querySelector("dl");
  const [small, big] = facts.querySelectorAll(":scope > div");
  small.querySelector("dd").textContent = "Your brain is about 2% of your weight.";
  big.querySelector("dd").textContent = "Yet it uses about 20% of your energy.";
  Object.assign(facts.style, {
    gridTemplateColumns: "minmax(0, 0.8fr) minmax(0, 1.2fr)",
    alignItems: "end",
  });
  const n = (div) => div.querySelector("dt");
  n(small).style.fontSize = "clamp(44px, 4.2vw, 64px)";
  n(small).style.color = "var(--muted)";
  n(big).style.fontSize = "clamp(88px, 9.6vw, 150px)";
  for (const div of [small, big]) div.querySelector("dd").style.maxWidth = "12em";
})();
