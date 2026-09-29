// The night sky behind look E ("Night sky"). One WebGL canvas: a navy gradient with a faint Milky
// Way, soft round stars at many depths, one warm planet beside the hero words, and 280 "paper"
// stars that appear one by one as the timeline is followed (an illustration of his papers; the
// page only ever states the one reported number, 280+).
//
// The stars live on a tile a little larger than the screen. The camera slides over it (scrolling,
// the sideways timeline, the pointer, a slow drift); each star moves by its depth, nearer stars
// more, which is how a moving perspective camera sees stars at different distances. Stars wrap
// around the tile's edges off screen, so a modest count covers a page of any length.
type Three = typeof import("three");

export type SkyView = { x: number; y: number; papers: number };
export type SkyMode = "webgl" | "still" | "slow";
export type Sky = {
  setPlanet: (x: number, y: number) => void;
  refresh: () => void;
  dispose: () => void;
};
type Options = {
  // Where the camera should be: page scroll (y), the sideways timeline (x), and how far along
  // the timeline the paper stars have come (0-1).
  view: () => SkyView;
  // Phones and reduced motion: one still frame, all stars shown.
  still: () => boolean;
  // Called once the first frame is on screen.
  onReady: (mode: SkyMode) => void;
};

const FIELD = 1800;
const BAND = 700;
const PAPERS = 280;
// Counts are tuned for a 1440 x 900 screen; smaller screens draw fewer (same density), larger
// screens draw them all (about 2,800 points at most).
const REFERENCE_AREA = 1440 * 900;
// The tile is this much larger than the screen, so stars wrap well outside it.
const MARGIN = 1.3;
const BAND_DEPTH = 0.035;
const PLANET_DEPTH = 0.6;
const POINTER = 46;
const DRIFT = 5;

const vertexShader = /* glsl */ `
  attribute vec3 aColor;
  attribute vec4 aStar;   // x: core size (CSS px), y: brightness, z: twinkle phase, w: twinkle speed
  attribute float aBirth; // -1: always shown; otherwise the timeline progress at which it appears
  uniform vec2 uViewport;
  uniform vec2 uTile;
  uniform vec2 uCam;
  uniform float uTime;
  uniform float uDpr;
  uniform float uPapers;
  uniform float uTwinkle;
  uniform float uFade;
  varying vec3 vColor;
  varying float vAlpha;
  varying float vCore;
  varying float vSprite;

  void main() {
    // position.xy: the star's place on the tile (0-1); position.z: its depth factor (near = large).
    vec2 p = mod(position.xy * uTile - uCam * position.z, uTile) - (uTile - uViewport) * 0.5;
    gl_Position = vec4(p.x / uViewport.x * 2.0 - 1.0, 1.0 - p.y / uViewport.y * 2.0, 0.0, 1.0);

    float amount = uTwinkle * (0.05 + 0.3 * aStar.y);
    float twinkle = 1.0 - amount * (0.5 + 0.5 * sin(uTime * aStar.w + aStar.z));
    float shown = 1.0;
    float flare = 0.0;
    if (aBirth >= 0.0) {
      float age = uPapers - aBirth;
      shown = smoothstep(0.0, 0.018, age);
      // A new star arrives a little brighter, then settles.
      flare = shown * exp(-max(age, 0.0) * 40.0);
    }
    vAlpha = aStar.y * twinkle * shown * uFade * (1.0 + 1.3 * flare);
    vColor = aColor;
    vCore = max(aStar.x * uDpr * (1.0 + 0.5 * flare), 0.5);
    vSprite = max(3.0, ceil(vCore * 9.0));
    gl_PointSize = vSprite;
    if (vAlpha < 0.003) gl_Position = vec4(2.0, 2.0, 2.0, 1.0);
  }
`;

// A soft round star: a bright core and a faint wide halo, fading to nothing before the sprite's
// edge (never a disc, never a fuzzy blob).
const fragmentShader = /* glsl */ `
  precision highp float;
  varying vec3 vColor;
  varying float vAlpha;
  varying float vCore;
  varying float vSprite;

  void main() {
    vec2 c = (gl_PointCoord - 0.5) * vSprite;
    float r = length(c);
    float core = exp(-(r * r) / (2.0 * vCore * vCore));
    float halo = 0.09 * exp(-r / (vCore * 2.4));
    float edge = 1.0 - smoothstep(vSprite * 0.36, vSprite * 0.5, r);
    gl_FragColor = vec4(vColor, (core + halo) * edge * vAlpha);
  }
`;

const planetVertex = /* glsl */ `
  uniform vec2 uViewport;
  uniform vec2 uPlanet;
  uniform float uDpr;
  uniform float uFade;
  uniform float uTime;
  uniform float uBreath;
  varying float vAlpha;
  varying float vSprite;
  varying float vCore;

  void main() {
    gl_Position = vec4(uPlanet.x / uViewport.x * 2.0 - 1.0, 1.0 - uPlanet.y / uViewport.y * 2.0, 0.0, 1.0);
    vCore = 2.4 * uDpr;
    vSprite = ceil(vCore * 22.0);
    vAlpha = uFade * (1.0 - uBreath * 0.08 * (0.5 + 0.5 * sin(uTime * 0.7)));
    gl_PointSize = vSprite;
  }
`;

// The planet: a warm point with a tight glow, like an evening star.
const planetFragment = /* glsl */ `
  precision highp float;
  varying float vAlpha;
  varying float vSprite;
  varying float vCore;

  void main() {
    vec2 c = (gl_PointCoord - 0.5) * vSprite;
    float r = length(c);
    float core = exp(-(r * r) / (2.0 * vCore * vCore));
    float glow = 0.3 * exp(-r / (vCore * 2.2)) + 0.07 * exp(-r / (vCore * 6.0));
    float edge = 1.0 - smoothstep(vSprite * 0.3, vSprite * 0.5, r);
    vec3 color = mix(vec3(1.0, 0.8, 0.46), vec3(1.0, 0.97, 0.9), core);
    gl_FragColor = vec4(color, min(1.0, (core * 1.2 + glow) * edge) * vAlpha);
  }
`;

const skyVertex = /* glsl */ `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = vec4(position.xy, 0.0, 1.0);
  }
`;

// The sky itself: deep at the top, a little lighter toward the horizon, and the Milky Way as a
// soft band along the tile's diagonal (it wraps with the stars; far away, so it barely moves).
const skyFragment = /* glsl */ `
  precision highp float;
  uniform vec2 uViewport;
  uniform vec2 uTile;
  uniform vec2 uCam;
  uniform float uFade;
  varying vec2 vUv;

  float hash(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
  }

  void main() {
    vec3 zenith = vec3(0.010, 0.031, 0.071);
    vec3 middle = vec3(0.020, 0.051, 0.110);
    vec3 horizon = vec3(0.040, 0.090, 0.180);
    vec3 color = mix(horizon, middle, smoothstep(0.0, 0.5, vUv.y));
    color = mix(color, zenith, smoothstep(0.5, 1.0, vUv.y));

    vec2 px = vec2(vUv.x, 1.0 - vUv.y) * uViewport;
    vec2 t = (px + (uTile - uViewport) * 0.5 + uCam * ${BAND_DEPTH.toFixed(3)}) / uTile;
    float s = fract(t.x + t.y + 0.5) - 0.5;
    float band = exp(-pow(s / 0.14, 2.0));
    float spine = exp(-pow(s / 0.05, 2.0));
    float vary = 0.62 + 0.22 * sin(6.2832 * 2.0 * t.x + 1.3) + 0.16 * sin(6.2832 * (3.0 * t.x + 2.0 * t.y) + 0.4);
    float lane = 1.0 - 0.4 * exp(-pow((s - 0.014) / 0.014, 2.0));
    vec3 tint = mix(vec3(0.55, 0.68, 0.95), vec3(1.0, 0.86, 0.66), 0.35 + 0.3 * sin(6.2832 * t.x));
    color += tint * (band * 0.045 + spine * 0.038) * vary * lane * uFade;
    // A whisper of noise so the gradient never shows bands.
    color += (hash(gl_FragCoord.xy) - 0.5) / 255.0;
    gl_FragColor = vec4(color, 1.0);
  }
`;

// A small seeded random generator: the same sky on every visit.
function random(seed: number) {
  let state = seed;
  return () => {
    state = (state + 0x6d2b79f5) | 0;
    let t = Math.imul(state ^ (state >>> 15), 1 | state);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const WARM = [1.0, 0.95, 0.87];
const GOLD = [1.0, 0.84, 0.56];
const BLUE = [0.77, 0.87, 1.0];
const PAPER = [1.0, 0.9, 0.72];

type Stars = {
  position: number[];
  color: number[];
  star: number[];
  birth: number[];
};

function push(
  stars: Stars,
  u: number,
  v: number,
  depth: number,
  color: number[],
  size: number,
  brightness: number,
  rand: () => number,
  birth = -1,
) {
  stars.position.push(u, v, depth);
  stars.color.push(color[0], color[1], color[2]);
  stars.star.push(size, brightness, rand() * Math.PI * 2, 0.5 + rand() * 1.3);
  stars.birth.push(birth);
}

function empty(): Stars {
  return { position: [], color: [], star: [], birth: [] };
}

function tint(rand: () => number) {
  const pick = rand();
  return pick < 0.66 ? WARM : pick < 0.83 ? BLUE : GOLD;
}

// The field: a few dozen bright stars spaced apart (best of twelve candidates, so they never
// clump), then many faint ones.
function fieldStars(rand: () => number) {
  const stars = empty();
  const bright: [number, number][] = [];
  const gap = (a: [number, number], b: [number, number]) => {
    const dx = Math.min(Math.abs(a[0] - b[0]), 1 - Math.abs(a[0] - b[0]));
    const dy = Math.min(Math.abs(a[1] - b[1]), 1 - Math.abs(a[1] - b[1]));
    return dx * dx + dy * dy;
  };
  for (let i = 0; i < 90; i += 1) {
    let best: [number, number] = [rand(), rand()];
    let bestGap = -1;
    for (let k = 0; k < 12; k += 1) {
      const candidate: [number, number] = [rand(), rand()];
      const nearest = bright.reduce((min, other) => Math.min(min, gap(candidate, other)), 9);
      if (nearest > bestGap) {
        best = candidate;
        bestGap = nearest;
      }
    }
    bright.push(best);
    const r = rand();
    push(
      stars,
      best[0],
      best[1],
      0.16 + 0.3 * r,
      tint(rand),
      0.8 + 0.55 * r,
      0.62 + 0.38 * rand(),
      rand,
    );
  }
  for (let i = bright.length; i < FIELD; i += 1) {
    const r = rand();
    const depth = 0.03 + 0.3 * Math.pow(rand(), 1.6);
    const size = 0.36 + 0.42 * Math.pow(r, 2.2);
    const brightness = 0.14 + 0.62 * Math.pow(r, 2.6);
    push(stars, rand(), rand(), depth, tint(rand), size, brightness, rand);
  }
  return stars;
}

// The Milky Way: faint far stars gathered along the tile's diagonal (u + v = 1, wrapping).
function bandStars(rand: () => number) {
  const stars = empty();
  for (let i = 0; i < BAND; i += 1) {
    // A normal spread across the band (Box-Muller), even along it.
    const g = Math.sqrt(-2 * Math.log(1 - rand())) * Math.cos(Math.PI * 2 * rand());
    const u = rand();
    const v = (((g * 0.1 - u) % 1) + 1) % 1;
    const color = rand() < 0.55 ? WARM : BLUE;
    push(
      stars,
      u,
      v,
      BAND_DEPTH * (0.6 + 0.8 * rand()),
      color,
      0.34 + 0.2 * rand(),
      0.1 + 0.26 * Math.pow(rand(), 2),
      rand,
    );
  }
  return stars;
}

// His papers: one star in each cell of a 20 x 14 grid (spread evenly, never clumped), each
// appearing at its own point along the timeline, in random order across the sky.
function paperStars(rand: () => number) {
  const stars = empty();
  const order = Array.from({ length: PAPERS }, (_, i) => i);
  for (let i = order.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rand() * (i + 1));
    [order[i], order[j]] = [order[j], order[i]];
  }
  for (let i = 0; i < PAPERS; i += 1) {
    const column = i % 20;
    const row = Math.floor(i / 20);
    const u = (column + 0.15 + 0.7 * rand()) / 20;
    const v = (row + 0.15 + 0.7 * rand()) / 14;
    const birth = 0.01 + (order[i] / PAPERS) * 0.97;
    push(
      stars,
      u,
      v,
      0.08 + 0.18 * rand(),
      PAPER,
      0.6 + 0.35 * rand(),
      0.7 + 0.3 * rand(),
      rand,
      birth,
    );
  }
  // Draw order follows the shuffle, so drawing fewer on a small screen keeps an even spread.
  const sorted = empty();
  order
    .map((rank, index) => ({ rank, index }))
    .sort((a, b) => a.rank - b.rank)
    .forEach(({ index }) => {
      sorted.position.push(...stars.position.slice(index * 3, index * 3 + 3));
      sorted.color.push(...stars.color.slice(index * 3, index * 3 + 3));
      sorted.star.push(...stars.star.slice(index * 4, index * 4 + 4));
      sorted.birth.push(stars.birth[index]);
    });
  return sorted;
}

export function createSky(
  THREE: Three,
  holder: HTMLElement,
  section: HTMLElement,
  options: Options,
): Sky {
  const renderer = new THREE.WebGLRenderer({
    alpha: false,
    antialias: false,
    powerPreference: "high-performance",
  });
  const gl = renderer.getContext();
  const info = gl.getExtension("WEBGL_debug_renderer_info");
  const name = String(
    info ? gl.getParameter(info.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER),
  );
  // A software renderer: one pixel per pixel, no twinkle, and a frame only when something moves.
  const slow = /swiftshader|llvmpipe|software/i.test(name);
  const dpr = slow ? 1 : Math.min(window.devicePixelRatio || 1, 2);
  renderer.setPixelRatio(dpr);
  renderer.setClearColor(0x050d1c, 1);
  const canvas = renderer.domElement;
  canvas.setAttribute("aria-hidden", "true");
  canvas.dataset.renderer = name;
  holder.appendChild(canvas);

  const rand = random(20251994);
  const shared = {
    uViewport: { value: new THREE.Vector2(1, 1) },
    uTile: { value: new THREE.Vector2(1, 1) },
    uCam: { value: new THREE.Vector2() },
    uTime: { value: 0 },
    uDpr: { value: dpr },
    uPapers: { value: 0 },
    uTwinkle: { value: slow ? 0 : 1 },
    uFade: { value: 0 },
  };

  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const disposables: { dispose: () => void }[] = [];

  const skyGeometry = new THREE.PlaneGeometry(2, 2);
  const skyMaterial = new THREE.ShaderMaterial({
    uniforms: shared,
    vertexShader: skyVertex,
    fragmentShader: skyFragment,
    depthTest: false,
    depthWrite: false,
  });
  const sky = new THREE.Mesh(skyGeometry, skyMaterial);
  sky.frustumCulled = false;
  sky.renderOrder = 0;
  scene.add(sky);
  disposables.push(skyGeometry, skyMaterial);

  const starMaterial = new THREE.ShaderMaterial({
    uniforms: shared,
    vertexShader,
    fragmentShader,
    transparent: true,
    depthTest: false,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  });
  disposables.push(starMaterial);

  const layers = [fieldStars(rand), bandStars(rand), paperStars(rand)].map((stars, index) => {
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute("position", new THREE.Float32BufferAttribute(stars.position, 3));
    geometry.setAttribute("aColor", new THREE.Float32BufferAttribute(stars.color, 3));
    geometry.setAttribute("aStar", new THREE.Float32BufferAttribute(stars.star, 4));
    geometry.setAttribute("aBirth", new THREE.Float32BufferAttribute(stars.birth, 1));
    const points = new THREE.Points(geometry, starMaterial);
    points.frustumCulled = false;
    points.renderOrder = 1 + index;
    scene.add(points);
    disposables.push(geometry);
    return { geometry, count: stars.birth.length };
  });

  const planetUniforms = {
    uViewport: shared.uViewport,
    uDpr: shared.uDpr,
    uFade: shared.uFade,
    uTime: shared.uTime,
    uPlanet: { value: new THREE.Vector2(-999, -999) },
    uBreath: { value: slow ? 0 : 1 },
  };
  const planetGeometry = new THREE.BufferGeometry();
  planetGeometry.setAttribute("position", new THREE.Float32BufferAttribute([0, 0, 0], 3));
  const planetMaterial = new THREE.ShaderMaterial({
    uniforms: planetUniforms,
    vertexShader: planetVertex,
    fragmentShader: planetFragment,
    transparent: true,
    depthTest: false,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  });
  const planet = new THREE.Points(planetGeometry, planetMaterial);
  planet.frustumCulled = false;
  planet.renderOrder = 5;
  scene.add(planet);
  disposables.push(planetGeometry, planetMaterial);
  const anchor = { x: -999, y: -999 };

  let width = 0;
  let height = 0;
  function fit() {
    width = holder.clientWidth;
    height = holder.clientHeight;
    if (!width || !height) return;
    renderer.setSize(width, height, false);
    shared.uViewport.value.set(width, height);
    shared.uTile.value.set(width * MARGIN, height * MARGIN);
    const density = Math.min(1, Math.max(0.3, (width * height) / REFERENCE_AREA));
    layers.forEach((layer) => layer.geometry.setDrawRange(0, Math.round(layer.count * density)));
  }
  fit();

  // The pointer leans the camera a little; the view eases toward where the page is.
  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
  const cam = { x: 0, y: 0, ready: false };
  function lean(event: PointerEvent) {
    if (event.pointerType !== "mouse") return;
    pointer.tx = (event.clientX / window.innerWidth - 0.5) * 2;
    pointer.ty = (event.clientY / window.innerHeight - 0.5) * 2;
    schedule();
  }
  window.addEventListener("pointermove", lean, { passive: true });

  let frame = 0;
  let visible = true;
  let last = performance.now();
  let start = -1;
  let drawn = false;
  // A still sky keeps the planet only while the hero words are on screen; it would otherwise sit
  // beside every screen of text. (One more frame when that changes; still no animation.)
  let stillPlanet = true;
  const planetWanted = () => window.scrollY < anchor.y + 160;

  function draw(now: number) {
    frame = 0;
    const still = options.still();
    const seconds = Math.min((now - last) / 1000, 0.1);
    last = now;
    const view = options.view();
    let moving = false;

    if (still) {
      cam.x = 0;
      cam.y = 0;
      shared.uCam.value.set(0, 0);
      shared.uPapers.value = 1;
      shared.uFade.value = 1;
      shared.uTwinkle.value = 0;
      planetUniforms.uBreath.value = 0;
      stillPlanet = planetWanted();
      planetUniforms.uPlanet.value.set(
        stillPlanet ? anchor.x : -999,
        stillPlanet ? anchor.y : -999,
      );
    } else {
      if (start < 0) start = now;
      if (!cam.ready) {
        // The first frame starts a little below where the page is, then settles (the sky rises).
        cam.x = view.x;
        cam.y = view.y - 150;
        cam.ready = true;
      }
      const ease = 1 - Math.exp(-seconds * 5);
      pointer.x += (pointer.tx - pointer.x) * (1 - Math.exp(-seconds * 3));
      pointer.y += (pointer.ty - pointer.y) * (1 - Math.exp(-seconds * 3));
      const dx = view.x - cam.x;
      const dy = view.y - cam.y;
      cam.x += dx * ease;
      cam.y += dy * ease;
      moving =
        Math.abs(dx) > 0.2 ||
        Math.abs(dy) > 0.2 ||
        Math.abs(pointer.tx - pointer.x) > 0.002 ||
        Math.abs(pointer.ty - pointer.y) > 0.002;
      if (!slow) shared.uTime.value += seconds;
      const drift = slow ? 0 : shared.uTime.value * DRIFT;
      shared.uCam.value.set(cam.x + drift + pointer.x * POINTER, cam.y + pointer.y * POINTER);
      shared.uPapers.value += (view.papers - shared.uPapers.value) * (slow ? 1 : ease);
      if (Math.abs(view.papers - shared.uPapers.value) > 0.001) moving = true;
      shared.uTwinkle.value = slow ? 0 : 1;
      planetUniforms.uBreath.value = slow ? 0 : 1;
      const fade = slow ? 1 : Math.min(1, (now - start) / 2600);
      shared.uFade.value = 1 - Math.pow(1 - fade, 3);
      if (fade < 1) moving = true;
      planetUniforms.uPlanet.value.set(
        anchor.x - (cam.x + pointer.x * POINTER) * PLANET_DEPTH,
        anchor.y - (cam.y + pointer.y * POINTER) * PLANET_DEPTH,
      );
    }

    renderer.render(scene, camera);
    if (!drawn) {
      drawn = true;
      options.onReady(still ? "still" : slow ? "slow" : "webgl");
    }
    section.dataset.skyCam = `${Math.round(cam.x)},${Math.round(cam.y)}`;
    // Keep going while the sky is alive; a still sky, or a software renderer at rest, waits.
    if (!still && (!slow || moving)) schedule();
  }

  function schedule() {
    if (!frame && visible && !document.hidden) frame = requestAnimationFrame(draw);
  }

  const resize = new ResizeObserver(() => {
    fit();
    schedule();
  });
  resize.observe(holder);

  const watch = new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting;
    if (visible) {
      last = performance.now();
      schedule();
    } else if (frame) {
      cancelAnimationFrame(frame);
      frame = 0;
    }
  });
  watch.observe(section);

  function onVisibility() {
    if (document.hidden) {
      if (frame) cancelAnimationFrame(frame);
      frame = 0;
    } else {
      last = performance.now();
      schedule();
    }
  }
  document.addEventListener("visibilitychange", onVisibility);
  // A software renderer draws only when the page moves; a still sky only when the planet goes.
  const nudge = () => {
    if (!options.still() || planetWanted() !== stillPlanet) schedule();
  };
  window.addEventListener("scroll", nudge, { passive: true });

  schedule();

  return {
    setPlanet(x, y) {
      anchor.x = x;
      anchor.y = y;
      schedule();
    },
    refresh() {
      fit();
      schedule();
    },
    dispose() {
      if (frame) cancelAnimationFrame(frame);
      frame = 0;
      resize.disconnect();
      watch.disconnect();
      document.removeEventListener("visibilitychange", onVisibility);
      window.removeEventListener("pointermove", lean);
      window.removeEventListener("scroll", nudge);
      disposables.forEach((item) => item.dispose());
      renderer.dispose();
      canvas.remove();
    },
  };
}
