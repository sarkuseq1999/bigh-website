"""The ideas for the Science page's first screen, as CSS and script injected into the real page.

Selectors use the page's own hooks (data-zoom, data-zoom-layer, #science-title), never the hashed
CSS-module class names. Everything a mock adds carries data-mock, so shoot_hero.py can step its
animations. Pictures come from /__mock/<file> (plates/hero/, built by build_plates.py and
split_gold.py).
"""

# Shared helpers, put on window.__mock before an idea's own script runs.
HELPERS = """
window.__mock = {
  hills: () => document.querySelector('[data-zoom-layer="hills"]'),
  // The first screen's painting becomes /__mock/<src>.
  swap(src, position) {
    const img = this.hills();
    img.removeAttribute('srcset');
    img.removeAttribute('sizes');
    img.src = '/__mock/' + src;
    if (position) img.style.objectPosition = position;
    img.dataset.bloom = 'done';
    return new Promise((done) => (img.complete && img.naturalWidth ? done(img) : img.addEventListener('load', () => done(img), { once: true })));
  },
  // Where an object-fit: cover picture is drawn inside its own box.
  drawn(img) {
    const bw = img.offsetWidth, bh = img.offsetHeight;
    const k = Math.max(bw / img.naturalWidth, bh / img.naturalHeight);
    const w = img.naturalWidth * k, h = img.naturalHeight * k;
    const pos = getComputedStyle(img).objectPosition.split(' ').map((v) => parseFloat(v) / 100);
    return { left: img.offsetLeft + (bw - w) * pos[0], top: img.offsetTop + (bh - h) * pos[1], width: w, height: h };
  },
  // A painting's gold slivers (split_gold.py), each drifting a little on its own.
  async slivers(name, box, host, reach) {
    const data = await (await fetch('/__mock/' + name + '-gold.json')).json();
    const layer = document.createElement('div');
    layer.dataset.mock = '';
    layer.className = 'mock-gold';
    Object.assign(layer.style, { left: box.left + 'px', top: box.top + 'px', width: box.width + 'px', height: box.height + 'px' });
    let seed = 11;
    const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
    const loads = [];
    for (const s of data.slivers) {
      const el = document.createElement('img');
      el.alt = '';
      el.src = '/__mock/' + name + '-gold/' + s.file;
      loads.push(new Promise((done) => { el.onload = done; el.onerror = done; }));
      Object.assign(el.style, { left: s.x * 100 + '%', top: s.y * 100 + '%', width: s.w * 100 + '%', height: s.h * 100 + '%' });
      // Big slivers are near and travel further; small ones are far and barely move.
      const near = Math.min(1, Math.sqrt(s.area) / 60);
      const far = (0.35 + 0.65 * near) * reach;
      const angle = rnd() * Math.PI * 2;
      el.style.setProperty('--dx', (Math.cos(angle) * far).toFixed(1) + 'px');
      el.style.setProperty('--dy', (Math.sin(angle) * far * 0.6).toFixed(1) + 'px');
      el.style.setProperty('--rot', ((rnd() - 0.5) * 9).toFixed(1) + 'deg');
      el.style.animationDelay = (-rnd() * 12).toFixed(2) + 's, ' + (-rnd() * 6).toFixed(2) + 's';
      layer.append(el);
    }
    host.append(layer);
    await Promise.all(loads);
    return layer;
  },
};
"""

SHARED_CSS = """
.mock-gold { position: absolute; pointer-events: none; }
.mock-gold img {
  position: absolute;
  display: block;
  animation: mock-sway 6s ease-in-out infinite alternate, mock-turn 3s ease-in-out infinite alternate;
}
@keyframes mock-sway {
  from { translate: calc(var(--dx) * -1) calc(var(--dy) * -1); }
  to { translate: var(--dx) var(--dy); }
}
@keyframes mock-turn {
  from { rotate: calc(var(--rot) * -1); }
  to { rotate: var(--rot); }
}
"""

# A. Start inside the cell: the painting fills the window; its gold slivers drift.
INSIDE_JS = """
(async () => {
  const m = window.__mock;
  const img = await m.swap('inside-1-base.webp', innerWidth >= 960 ? '70% 60%' : '45% 60%');
  await m.slivers('inside-1', m.drawn(img), img.parentElement, innerWidth >= 960 ? 16 : 11);
})()
"""

# C. The gold dot: the words lead, very large; the full stop after "cell" is a dab of gold leaf,
# and one cell, the page's own painting, stands below it with its gold adrift.
DOT_CSS = """
[data-zoom-layer="hills"] { visibility: hidden; }
[data-zoom] header > p:last-child { display: none; }
#science-title {
  max-width: none !important;
  font-size: clamp(54px, 15.2vw, 64px) !important;
  line-height: 0.98 !important;
  letter-spacing: -0.02em !important;
}
#science-title .mock-dot {
  position: relative;
  display: inline-block;
  width: 0.27em;
  height: 0.27em;
  margin-left: 0.07em;
  overflow: hidden;
  border-radius: 47% 53% 51% 49% / 52% 48% 53% 47%;
  background-image:
    linear-gradient(rgba(110, 78, 20, 0.2), rgba(110, 78, 20, 0.2)),
    url("/images/home-v2/ink/gold-leaf-word.webp");
  background-position: center;
  background-size: 360% 360%;
  vertical-align: baseline;
}
#science-title .mock-dot::after {
  content: "";
  position: absolute;
  inset: -20%;
  background: linear-gradient(112deg, transparent 38%, rgba(255, 246, 214, 0.5) 50%, transparent 62%);
  animation: mock-sheen 12s ease-in-out infinite;
}
@keyframes mock-sheen {
  0%, 20% { transform: translateX(-90%); }
  42%, 100% { transform: translateX(90%); }
}
[data-zoom] header .mock-lead {
  position: relative;
  max-width: 21em;
  margin: 22px 0 0;
  color: #1c1a16;
  font-size: 21px;
  line-height: 1.42;
}
[data-zoom] header .mock-lead + .mock-lead { margin-top: 10px; font-size: 17px; }
[data-zoom] header > p:not(.mock-lead) { display: none; }
.mock-cell {
  position: absolute;
  left: -18vw;
  bottom: -9svh;
  width: 136vw;
  aspect-ratio: 1213 / 981;
  pointer-events: none;
}
.mock-cell > img { display: block; width: 100%; height: 100%; mix-blend-mode: multiply; }
.mock-cell .mock-gold { inset: 0; }
@media (min-width: 960px) {
  [data-zoom] header { padding-top: clamp(140px, 22svh, 240px) !important; }
  #science-title { font-size: clamp(88px, 9.6vw, 168px) !important; }
  [data-zoom] header .mock-lead { max-width: 19em; margin-top: 44px; font-size: clamp(24px, 1.9vw, 30px); }
  [data-zoom] header .mock-lead + .mock-lead { max-width: 24em; margin-top: 14px; font-size: clamp(19px, 1.4vw, 22px); }
  .mock-cell { left: auto; right: -5vw; bottom: -30svh; width: 56vw; }
}
"""

DOT_JS = """
(async () => {
  const h1 = document.getElementById('science-title');
  h1.innerHTML = 'Our science<br>starts in the cell<span class="mock-dot" data-mock></span>';
  const a = document.createElement('p');
  a.className = 'mock-lead';
  a.textContent = 'A cell is tiny. Thousands of yours would fit inside that gold dot.';
  const b = document.createElement('p');
  b.className = 'mock-lead';
  b.textContent = 'Dr. Jiankang Liu has spent decades studying how they make energy, and what changes as we age.';
  h1.after(a, b);
  const stage = window.__mock.hills().parentElement;
  const cell = document.createElement('div');
  cell.className = 'mock-cell';
  cell.dataset.mock = '';
  const art = document.createElement('img');
  art.alt = '';
  art.src = '/__mock/cell-base.webp';
  cell.append(art);
  stage.insertBefore(cell, h1.parentElement);
  await new Promise((done) => { art.onload = done; art.onerror = done; });
  const layer = await window.__mock.slivers('cell', { left: 0, top: 0, width: cell.offsetWidth, height: cell.offsetHeight }, cell, innerWidth >= 960 ? 12 : 9);
  Object.assign(layer.style, { left: 0, top: 0, width: '100%', height: '100%' });
})()
"""

# D. Keep today's scene, with the walker much larger and nearer the middle; a cloud's shadow drifts
# over the hills.
NEAR_CSS = """
.mock-cloud {
  position: absolute;
  left: 0;
  top: 46%;
  width: 62vw;
  height: 44%;
  background: radial-gradient(ellipse at center, rgba(96, 84, 60, 0.3), rgba(96, 84, 60, 0.14) 45%, transparent 70%);
  mix-blend-mode: color-burn;
  pointer-events: none;
  animation: mock-cloud 12s linear infinite;
}
@keyframes mock-cloud {
  from { transform: translateX(-70vw); }
  to { transform: translateX(110vw); }
}
@media (min-width: 960px) {
  [data-zoom] header { padding-top: clamp(118px, 16svh, 180px) !important; }
}
@media (max-width: 959px) {
  [data-zoom-layer="hills"] {
    top: 14% !important;
    height: 86% !important;
    -webkit-mask-image: linear-gradient(transparent, #000 16%);
    mask-image: linear-gradient(transparent, #000 16%);
  }
  .mock-cloud { top: 52%; width: 120vw; }
}
"""

NEAR_JS = """
(async () => {
  const m = window.__mock;
  const img = await m.swap('near-2.webp', innerWidth >= 960 ? '60% 0%' : '64% 100%');
  const cloud = document.createElement('div');
  cloud.className = 'mock-cloud';
  cloud.dataset.mock = '';
  img.after(cloud);
})()
"""

# B. The walker is painted in small dabs (a body is made of cells), some of them gold leaf
# (gild_dabs.py); a light passes over the gold now and then.
DABS_CSS = """
.mock-light {
  position: absolute;
  pointer-events: none;
  -webkit-mask-image: url("/__mock/dabs-mask.png");
  mask-image: url("/__mock/dabs-mask.png");
  -webkit-mask-size: 100% 100%;
  mask-size: 100% 100%;
  background-image: linear-gradient(100deg, transparent 42%, rgba(255, 248, 224, 0.8) 50%, transparent 58%);
  background-size: 400% 100%;
  background-repeat: no-repeat;
  animation: mock-pass 12s ease-in-out infinite;
}
@keyframes mock-pass {
  0%, 30% { background-position: 110% 0; }
  62%, 100% { background-position: -10% 0; }
}
@media (min-width: 960px) {
  [data-zoom] header { padding-top: clamp(118px, 16svh, 180px) !important; }
}
@media (max-width: 959px) {
  [data-zoom-layer="hills"] {
    top: 12% !important;
    height: 88% !important;
    -webkit-mask-image: linear-gradient(transparent, #000 16%);
    mask-image: linear-gradient(transparent, #000 16%);
  }
}
"""

DABS_JS = """
(async () => {
  const m = window.__mock;
  const lead = document.querySelector('[data-zoom] header > p');
  lead.textContent = 'You are made of about 37 trillion cells, and each one makes its own energy. Dr. Jiankang Liu has spent decades studying how.';
  const img = await m.swap('dabs-gold.webp', innerWidth >= 960 ? '60% 62%' : '62% 100%');
  const box = m.drawn(img);
  const light = document.createElement('div');
  light.className = 'mock-light';
  light.dataset.mock = '';
  Object.assign(light.style, { left: box.left + 'px', top: box.top + 'px', width: box.width + 'px', height: box.height + 'px' });
  img.after(light);
})()
"""

IDEAS = {
    # 0. Today's first screen, untouched, for comparison.
    "today": {"stops": (0.5, 1.0)},
    "inside": {"css": SHARED_CSS, "js": INSIDE_JS, "loop": 12},
    "dot": {"css": SHARED_CSS + DOT_CSS, "js": DOT_JS, "loop": 12},
    "near": {"css": NEAR_CSS, "js": NEAR_JS, "loop": 12},
    "dabs": {"css": DABS_CSS, "js": DABS_JS, "loop": 12},
}
