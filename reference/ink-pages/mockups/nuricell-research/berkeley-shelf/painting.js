// Review-only overlay for the existing seven book buttons on the built page.
function placePainting(source) {
  const section = document.querySelector('[data-chapter="research"]');
  const figure = section.querySelector('figure');
  const painting = figure.querySelector('img');
  const polygons = [
    [[106,501],[166,473],[317,467],[284,505],[283,961],[267,973],[117,974]],
    [[280,508],[323,482],[459,483],[449,514],[453,963],[431,973],[290,972]],
    [[450,509],[475,474],[611,477],[620,500],[621,956],[606,971],[464,971]],
    [[617,473],[626,439],[774,442],[790,471],[790,954],[777,969],[631,970]],
    [[789,469],[786,446],[919,444],[948,471],[948,951],[937,965],[799,964]],
    [[947,486],[938,461],[1061,455],[1102,482],[1110,948],[1097,965],[956,960]],
    [[1103,499],[1178,457],[1245,471],[1336,935],[1305,955],[1205,966],[1115,917]],
  ];
  figure.style.setProperty('--aspect', 1402 / 1122);
  painting.removeAttribute('srcset');
  painting.removeAttribute('sizes');
  painting.loading = 'eager';
  painting.src = source;
  painting.width = 1402;
  painting.height = 1122;
  painting.alt = 'Seven clothbound books on a sunlit sill, with a live oak and the Berkeley hills beyond.';
  for (const [i, points] of polygons.entries()) {
    const clip = 'polygon(' + points.map(([x, y]) => (100*x/1402).toFixed(2) + '% ' + (100*y/1122).toFixed(2) + '%').join(', ') + ')';
    const fade = figure.querySelector('[data-fade="' + (i+1) + '"]');
    const button = figure.querySelector('[data-book="' + (i+1) + '"]');
    fade.style.mask = 'none';
    fade.style.clipPath = clip;
    button.style.clipPath = clip;
  }
}
