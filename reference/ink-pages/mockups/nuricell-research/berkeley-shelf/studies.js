// The standalone review keeps the studies and accessible labels from the built page.
const books = [...document.querySelectorAll('[data-book]')];
const rows = [...document.querySelectorAll('[data-study]')];
const fades = [...document.querySelectorAll('[data-fade]')];
let openRow = 0;
function paint(row) {
  books.forEach((book, i) => fades[i].toggleAttribute('data-dim', row !== null && book.getAttribute('aria-controls') !== 'research-answer-' + row));
}
function openStudy(index) {
  openRow = index;
  rows.forEach((row, i) => {
    const active = i === index;
    row.toggleAttribute('data-open', active);
    row.querySelector('button').setAttribute('aria-expanded', String(active));
    row.querySelector('[id^="research-answer"]').toggleAttribute('data-open', active);
  });
  books.forEach(book => book.setAttribute('aria-expanded', String(book.getAttribute('aria-controls') === 'research-answer-' + index)));
  paint(index);
}
function previewOnHover(button, index) {
  button.addEventListener('pointerenter', e => { if (e.pointerType === 'mouse') paint(index); });
  button.addEventListener('pointerleave', e => { if (e.pointerType === 'mouse') paint(openRow); });
  button.addEventListener('focus', () => paint(index));
  button.addEventListener('blur', () => paint(openRow));
}
rows.forEach((row, i) => {
  const button = row.querySelector('button');
  previewOnHover(button, i);
  button.addEventListener('click', () => openStudy(i === openRow ? null : i));
});
books.forEach(book => {
  const index = rows.findIndex(row => row.querySelector('button').getAttribute('aria-controls') === book.getAttribute('aria-controls'));
  previewOnHover(book, index);
  book.addEventListener('click', () => {
    openStudy(index);
    if (innerWidth < 960) rows[index].scrollIntoView({block: 'start',behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
  });
});
