// Shared by every idea: finds the opening's words and marks them so an idea's CSS can reach them.
// window.__idea is the idea's letter, window.__css its stylesheet, window.__copy the purpose's words
// (optional). Run in the page (mock.py).
(() => {
  const sec = document.querySelector("[data-chapter=overview]");
  const h1 = sec.querySelector("h1");
  const ow = h1.nextElementSibling;
  const left = ow.firstElementChild;
  const [headline, text] = left.children;
  const buy = ow.children[1];
  ow.setAttribute("data-mock", window.__idea);
  left.setAttribute("data-m", "left");
  headline.setAttribute("data-m", "hl");
  text.setAttribute("data-m", "tx");
  buy.setAttribute("data-m", "buy");
  // The settle animation already ran; changing the words must not replay it.
  ow.querySelectorAll("*").forEach((e) => (e.style.animation = "none"));
  if (window.__copy) text.textContent = window.__copy;
  const st = document.createElement("style");
  st.textContent = window.__css;
  document.head.appendChild(st);
  window.__parts = { sec, h1, ow, left, headline, text, buy };
})();
