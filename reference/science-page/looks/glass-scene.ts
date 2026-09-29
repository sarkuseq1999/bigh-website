import * as THREE from "three";
import { mergeVertices } from "three/examples/jsm/utils/BufferGeometryUtils.js";

// Look F's live glass mitochondrion, after the homepage render (public/images/science/glass-cell.webp):
// a clear glass bean with a honey-gold inside and one folded inner membrane (the cristae) that runs
// back and forth along its length. Everything inside is opaque, so the glass shell refracts it through
// three.js's transmission pass. Loaded with a dynamic import from look-glass.tsx, so three.js stays out
// of the page's first bundle.

export type GlassStats = { frames: number; renderer: string; slow: boolean; pixelRatio: number };
export type GlassCell = {
  setScroll: (progress: number) => void;
  setPointer: (x: number, y: number) => void;
  dispose: () => void;
  stats: GlassStats;
};
type Options = {
  // The width the object should have on screen (CSS px), so it lines up with the still render.
  objectWidth: () => number;
  onReady: () => void;
};

// The shape, in world units. A long body with rounded ends, bent like a gentle smile, a little fuller
// at the left end and flattened front to back, like the render.
const HALF = 1.72;
const RADIUS = 0.66;
const FLAT = 0.8;
const BEND = 0.15;
const INNER = 0.7;
const HALF_IN = HALF - (1 - INNER) * RADIUS * 1.1;
const WORLD_WIDTH = 2 * HALF + 0.08;

const spine = (x: number) => -BEND * (1 - (x / HALF) ** 2);
// Fuller at the left end, with a soft waist a little right of the middle, like the render.
const fuller = (x: number) =>
  (1 - 0.08 * (x / HALF)) * (1 - 0.07 * Math.exp(-(((x / HALF - 0.12) / 0.32) ** 2)));
const profile = (s: number) => Math.sqrt(Math.max(0, 1 - Math.min(1, Math.abs(s)) ** 4));
const innerHeight = (x: number) => RADIUS * INNER * profile(x / HALF_IN) * fuller(x);
const smooth = (a: number, b: number, t: number) => {
  const k = Math.min(1, Math.max(0, (t - a) / (b - a)));
  return k * k * (3 - 2 * k);
};

function beanGeometry(half: number, radius: number) {
  const rows = 180;
  const cols = 112;
  const position = new Float32Array((rows + 1) * cols * 3);
  let k = 0;
  for (let i = 0; i <= rows; i++) {
    // Rows bunch up toward the tips, where the curve turns fastest.
    const s = Math.sin(-Math.PI / 2 + (Math.PI * i) / rows);
    const x = s * half;
    const r = radius * profile(s) * fuller(x);
    for (let j = 0; j < cols; j++) {
      const v = (j / cols) * Math.PI * 2;
      position[k++] = x;
      position[k++] = spine(x) + r * Math.cos(v);
      position[k++] = r * FLAT * Math.sin(v);
    }
  }
  const index: number[] = [];
  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      const a = i * cols + j;
      const b = i * cols + ((j + 1) % cols);
      index.push(a, b, a + cols, b, b + cols, a + cols);
    }
  }
  const raw = new THREE.BufferGeometry();
  raw.setAttribute("position", new THREE.BufferAttribute(position, 3));
  raw.setIndex(index);
  // Weld the tips (every vertex of the first and last row sits on one point), then smooth normals.
  const geometry = mergeVertices(raw, 1e-6);
  raw.dispose();
  geometry.computeVertexNormals();
  return geometry;
}

// The folded inner membrane: one continuous sheet that runs back and forth along the body. Seen from
// the front it is the render's serpentine tube; as the cell turns, its folds show as shelves.
function cristaeGeometry() {
  const half = HALF_IN * 0.9;
  const span = 2 * half;
  const periods = 6;
  const omega = periods * Math.PI * 2;
  // Slows the path at each run's middle so the runs stand upright and the turns round out into loops.
  const neck = (1.45 * span) / (2 * omega);
  const thick = 0.05;
  const samples = 1300;
  const centers: THREE.Vector3[] = [];
  const depths: number[] = [];
  const scales: number[] = [];
  for (let i = 0; i <= samples; i++) {
    const t = i / samples;
    // A slow warp of the phase makes the loops a little uneven, as in the render, not a coil spring.
    const phase = omega * t + Math.PI + 0.55 * Math.sin(omega * t * 0.37 + 0.6);
    const base = -half + span * t + neck * Math.sin(2 * phase);
    const h = innerHeight(base);
    const swing = Math.cos(phase);
    const edge = Math.max(smooth(0.04, 0, t), smooth(0.96, 1, t));
    // The ends run out to meet the inner wall (from inside it); elsewhere the loops vary a little.
    const amp =
      Math.max(0, h - thick * 1.1 - 0.035 * (1 - edge)) *
      (0.9 + 0.1 * (1 - edge) * Math.sin(phase * 0.41 + 1.1));
    const x = base + 0.055 * swing;
    centers.push(new THREE.Vector3(x, spine(x) + amp * swing, 0));
    const room = Math.sqrt(Math.max(0, 1 - ((amp * swing) / Math.max(h, 1e-3)) ** 2));
    depths.push(Math.max(thick + 0.006, h * FLAT * room * 0.32));
    // Round, closed ends: the section shrinks along a quarter circle over the last few samples.
    const cap = Math.min(t, 1 - t) / 0.008;
    scales.push(cap >= 1 ? 1 : Math.sqrt(Math.max(0, 1 - (1 - cap) ** 2)));
  }

  // A stadium cross-section: two half-round rims joined by flat faces.
  type RingPoint = { cap: 0 | 1 | -1; angle: number; side: number; along: number };
  const ring: RingPoint[] = [];
  for (let q = 0; q <= 8; q++) ring.push({ cap: 1, angle: (Math.PI * q) / 8, side: 0, along: 0 });
  ring.push(
    { cap: 0, angle: 0, side: -1, along: 1 / 3 },
    { cap: 0, angle: 0, side: -1, along: -1 / 3 },
  );
  for (let q = 0; q <= 8; q++)
    ring.push({ cap: -1, angle: Math.PI + (Math.PI * q) / 8, side: 0, along: 0 });
  ring.push(
    { cap: 0, angle: 0, side: 1, along: -1 / 3 },
    { cap: 0, angle: 0, side: 1, along: 1 / 3 },
  );
  const K = ring.length;

  const position = new Float32Array(centers.length * K * 3);
  const normal = new Float32Array(centers.length * K * 3);
  const tangent = new THREE.Vector3();
  const across = new THREE.Vector3();
  let k = 0;
  for (let i = 0; i < centers.length; i++) {
    const prev = centers[Math.max(0, i - 1)];
    const next = centers[Math.min(centers.length - 1, i + 1)];
    tangent.subVectors(next, prev).normalize();
    across.set(-tangent.y, tangent.x, 0).normalize();
    const r = thick * scales[i];
    const flat = Math.max(0, depths[i] - thick) * scales[i];
    const c = centers[i];
    for (const point of ring) {
      let a: number, b: number, na: number, nb: number;
      if (point.cap !== 0) {
        na = Math.cos(point.angle);
        nb = Math.sin(point.angle);
        a = r * na;
        b = point.cap * flat + r * nb;
      } else {
        na = point.side;
        nb = 0;
        a = r * point.side;
        b = flat * point.along;
      }
      position[k] = c.x + across.x * a;
      position[k + 1] = c.y + across.y * a;
      position[k + 2] = c.z + b;
      const nx = across.x * na;
      const ny = across.y * na;
      const length = Math.hypot(nx, ny, nb) || 1;
      normal[k] = nx / length;
      normal[k + 1] = ny / length;
      normal[k + 2] = nb / length;
      k += 3;
    }
  }
  const index: number[] = [];
  for (let i = 0; i < centers.length - 1; i++) {
    for (let q = 0; q < K; q++) {
      const a = i * K + q;
      const b = i * K + ((q + 1) % K);
      index.push(a, b, a + K, b, b + K, a + K);
    }
  }
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute("position", new THREE.BufferAttribute(position, 3));
  geometry.setAttribute("normal", new THREE.BufferAttribute(normal, 3));
  geometry.setIndex(index);
  return geometry;
}

// The honey-gold inside, seen on the far wall of the inner membrane: warm, lit from within, with slow
// light ripples like the render's. Values stay under 1 so nothing clips to flat yellow.
const matrixVertex = /* glsl */ `
  varying vec3 vLocal;
  varying vec3 vNormalView;
  varying vec3 vViewPosition;
  void main() {
    vLocal = position;
    vec4 view = modelViewMatrix * vec4(position, 1.0);
    vViewPosition = view.xyz;
    vNormalView = normalize(normalMatrix * normal);
    gl_Position = projectionMatrix * view;
  }
`;
const matrixFragment = /* glsl */ `
  uniform float uTime;
  varying vec3 vLocal;
  varying vec3 vNormalView;
  varying vec3 vViewPosition;
  float ripple(vec3 p, float t) {
    float a = sin(p.x * 5.1 + sin(p.y * 6.3 + t * 0.7) * 1.4 + t * 0.35);
    float b = sin(p.y * 7.3 + sin(p.z * 5.7 - t * 0.5) * 1.2 - t * 0.28);
    float c = sin(p.z * 6.1 + sin(p.x * 4.3 + t * 0.4) * 1.6 + t * 0.22);
    return pow(1.0 - abs((a + b + c) / 3.0), 4.5);
  }
  void main() {
    vec3 n = normalize(vNormalView);
    float facing = abs(dot(n, normalize(-vViewPosition)));
    // Linear colors: deep amber at the edges, honey where the wall faces us.
    vec3 amber = vec3(0.46, 0.16, 0.014);
    vec3 honey = vec3(0.86, 0.44, 0.05);
    vec3 color = mix(amber, honey, smoothstep(0.1, 0.95, facing));
    float light = ripple(vLocal * 1.15, uTime) + 0.55 * ripple(vLocal * 2.2 + 3.1, uTime * 1.25);
    color += vec3(1.0, 0.64, 0.2) * light * 0.3;
    color += vec3(1.0, 0.78, 0.4) * pow(1.0 - facing, 3.0) * 0.8;
    gl_FragColor = vec4(min(color, vec3(1.0)), 1.0);
    #include <colorspace_fragment>
  }
`;

// What the glass refracts at its clear edges: the pearl page with a little lavender and ice light. It is
// drawn only into the transmission pass (see onBeforeRender), so the canvas itself stays see-through
// and the page's own moving light shows around the cell.
const backdropFragment = /* glsl */ `
  varying vec2 vUv;
  void main() {
    vec3 pearl = vec3(0.855, 0.879, 0.922);
    vec3 lavender = vec3(0.584, 0.546, 0.887);
    vec3 ice = vec3(0.625, 0.815, 0.93);
    vec3 gold = vec3(0.88, 0.55, 0.15);
    vec3 color = pearl;
    color = mix(color, lavender, 0.42 * smoothstep(0.75, 0.0, distance(vUv, vec2(0.18, 0.82))));
    color = mix(color, ice, 0.5 * smoothstep(0.7, 0.0, distance(vUv, vec2(0.86, 0.62))));
    color = mix(color, gold, 0.12 * smoothstep(0.55, 0.0, distance(vUv, vec2(0.5, 0.12))));
    gl_FragColor = vec4(color, 1.0);
  }
`;
const backdropVertex = /* glsl */ `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

// A studio for reflections: soft walls (lavender to one side, ice to the other) and a few long
// softboxes, so the glass catches long white highlights like the render's.
function studioScene() {
  const scene = new THREE.Scene();
  const parts: { dispose: () => void }[] = [];
  const skyGeometry = new THREE.SphereGeometry(20, 48, 24);
  const skyMaterial = new THREE.ShaderMaterial({
    side: THREE.BackSide,
    vertexShader: /* glsl */ `
      varying vec3 vDirection;
      void main() {
        vDirection = normalize(position);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `,
    fragmentShader: /* glsl */ `
      varying vec3 vDirection;
      void main() {
        vec3 d = normalize(vDirection);
        // Darker walls than the page (like a photographer's dark cards), so the glass edges read.
        vec3 top = vec3(0.95, 0.97, 1.04);
        vec3 horizon = vec3(0.36, 0.39, 0.47);
        vec3 ground = vec3(0.24, 0.24, 0.27);
        vec3 color = d.y > 0.0 ? mix(horizon, top, pow(d.y, 0.7)) : mix(horizon, ground, pow(-d.y, 0.6));
        color *= mix(vec3(1.0), vec3(0.86, 0.82, 1.06), smoothstep(0.1, -0.9, d.x) * 0.6);
        color *= mix(vec3(1.0), vec3(0.88, 1.0, 1.08), smoothstep(-0.1, 0.9, d.x) * 0.6);
        gl_FragColor = vec4(color, 1.0);
      }
    `,
  });
  scene.add(new THREE.Mesh(skyGeometry, skyMaterial));
  parts.push(skyGeometry, skyMaterial);
  const panel = (width: number, height: number, power: number, x: number, y: number, z: number) => {
    const geometry = new THREE.PlaneGeometry(width, height);
    const material = new THREE.MeshBasicMaterial({
      color: new THREE.Color(power, power, power * 0.98),
      side: THREE.DoubleSide,
    });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(x, y, z);
    mesh.lookAt(0, 0, 0);
    scene.add(mesh);
    parts.push(geometry, material);
  };
  panel(16, 2.4, 7.5, 0, 8.5, 2.2); // a long strip overhead: the highlight along the top edge
  panel(1.8, 9, 9, -8, 1.5, 4); // a tall strip on the left
  panel(2.4, 2.4, 14, 7, 4.5, 6); // a key light top right
  panel(12, 1.2, 1.6, 0, -7.5, 2.5); // a soft bounce below: the rim along the bottom
  panel(0.7, 0.7, 30, -4, 3, 7); // small bright lamps: sparkles along the rim
  panel(0.6, 0.6, 30, 5, -1.5, 7);
  panel(0.5, 0.5, 26, -6.5, -2, 5);
  return { scene, dispose: () => parts.forEach((part) => part.dispose()) };
}

export async function mountGlassCell(
  canvas: HTMLCanvasElement,
  options: Options,
): Promise<GlassCell | null> {
  // Ask a throwaway canvas first, so a browser without WebGL keeps the still quietly (three.js would
  // log an error while failing).
  const probe = document.createElement("canvas").getContext("webgl2");
  if (!probe) return null;
  probe.getExtension("WEBGL_lose_context")?.loseContext();
  let renderer: THREE.WebGLRenderer;
  try {
    renderer = new THREE.WebGLRenderer({
      canvas,
      alpha: true,
      antialias: true,
      powerPreference: "high-performance",
    });
  } catch {
    return null;
  }
  const gl = renderer.getContext();
  const debug = gl.getExtension("WEBGL_debug_renderer_info");
  const rendererName = String(
    debug ? gl.getParameter(debug.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER),
  );
  // Software rendering (no GPU): one pixel per CSS pixel, and draw only when something changes.
  const slow = /swiftshader|llvmpipe|software/i.test(rendererName);
  let pixelRatio = slow ? 1 : Math.min(window.devicePixelRatio || 1, 2);
  renderer.setPixelRatio(pixelRatio);
  renderer.setClearColor(0x000000, 0);
  renderer.toneMapping = THREE.NoToneMapping;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  const studio = studioScene();
  const environment = pmrem.fromScene(studio.scene, 0.02).texture;
  studio.dispose();
  scene.environment = environment;

  const camera = new THREE.PerspectiveCamera(24, 1, 0.1, 60);
  const cell = new THREE.Group();
  scene.add(cell);

  const shellGeometry = beanGeometry(HALF, RADIUS);
  const shell = new THREE.MeshPhysicalMaterial({
    color: 0xffffff,
    metalness: 0,
    roughness: 0.04,
    transmission: 1,
    thickness: 0.28,
    ior: 1.4,
    dispersion: 0.4,
    iridescence: 0.35,
    iridescenceIOR: 1.3,
    iridescenceThicknessRange: [200, 480],
    clearcoat: 0.6,
    clearcoatRoughness: 0.03,
    specularIntensity: 1,
    envMapIntensity: 1,
    attenuationColor: new THREE.Color("#fff6ea"),
    attenuationDistance: 4,
  });
  // Thick glass reads by its edges: a little darker and cooler toward the outline, with a bright ring
  // of focused light just inside it.
  shell.onBeforeCompile = (shader) => {
    shader.fragmentShader = shader.fragmentShader.replace(
      "#include <transmission_fragment>",
      /* glsl */ `#include <transmission_fragment>
      float shellEdge = 1.0 - abs(dot(normal, normalize(vViewPosition)));
      totalDiffuse *= mix(vec3(1.0), vec3(0.58, 0.63, 0.76), smoothstep(0.55, 0.98, shellEdge));
      totalDiffuse += vec3(1.0, 0.99, 0.97) * smoothstep(0.3, 0.62, shellEdge) * (1.0 - smoothstep(0.66, 0.86, shellEdge)) * 0.16;`,
    );
  };
  cell.add(new THREE.Mesh(shellGeometry, shell));

  const matrixGeometry = beanGeometry(HALF_IN, RADIUS * INNER);
  const matrix = new THREE.ShaderMaterial({
    uniforms: { uTime: { value: 0 } },
    vertexShader: matrixVertex,
    fragmentShader: matrixFragment,
    side: THREE.BackSide,
  });
  cell.add(new THREE.Mesh(matrixGeometry, matrix));

  const foldGeometry = cristaeGeometry();
  const fold = new THREE.MeshPhysicalMaterial({
    color: new THREE.Color("#e6a232"),
    emissive: new THREE.Color("#c47716"),
    emissiveIntensity: 0.26,
    roughness: 0.12,
    metalness: 0,
    clearcoat: 1,
    clearcoatRoughness: 0.04,
    envMapIntensity: 0.4,
  });
  // Like a glass tube full of light: a deeper gold middle and bright, thin edges.
  fold.onBeforeCompile = (shader) => {
    shader.fragmentShader = shader.fragmentShader.replace(
      "#include <emissivemap_fragment>",
      /* glsl */ `#include <emissivemap_fragment>
      float foldRim = pow(1.0 - abs(dot(normal, normalize(vViewPosition))), 2.6);
      totalEmissiveRadiance += vec3(1.0, 0.86, 0.46) * foldRim * 1.05;`,
    );
  };
  cell.add(new THREE.Mesh(foldGeometry, fold));

  // Warm light from inside, so the folds glow like the render's.
  const glowLeft = new THREE.PointLight(0xffc36a, 0.35, 0, 2);
  glowLeft.position.set(-0.75, -0.05, 0.42);
  const glowRight = new THREE.PointLight(0xffc36a, 0.35, 0, 2);
  glowRight.position.set(0.75, -0.1, 0.42);
  cell.add(glowLeft, glowRight);

  const backdropGeometry = new THREE.PlaneGeometry(1, 1);
  const backdropMaterial = new THREE.ShaderMaterial({
    vertexShader: backdropVertex,
    fragmentShader: backdropFragment,
    depthWrite: false,
  });
  const backdrop = new THREE.Mesh(backdropGeometry, backdropMaterial);
  backdrop.frustumCulled = false;
  backdrop.onBeforeRender = (target) => {
    backdropMaterial.colorWrite = target.getRenderTarget() !== null;
  };
  scene.add(backdrop);

  // Frame the camera so the object is as wide on screen as the still render's object.
  const BACKDROP_DISTANCE = 6;
  let width = 0;
  let height = 0;
  const fit = () => {
    const box = canvas.getBoundingClientRect();
    width = Math.max(1, Math.round(canvas.clientWidth || box.width));
    height = Math.max(1, Math.round(canvas.clientHeight || box.height));
    renderer.setSize(width, height, false);
    camera.aspect = width / height;
    const target = Math.max(80, options.objectWidth());
    const tan = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
    const distance = (WORLD_WIDTH * height) / (2 * tan * target);
    camera.position.set(0, 0, distance);
    camera.near = Math.max(0.1, distance - 4);
    camera.far = distance + BACKDROP_DISTANCE + 2;
    camera.updateProjectionMatrix();
    const planeHeight = 2 * tan * (distance + BACKDROP_DISTANCE) * 1.05;
    backdrop.position.set(0, 0, -BACKDROP_DISTANCE);
    backdrop.scale.set(planeHeight * camera.aspect, planeHeight, 1);
  };
  fit();

  const stats: GlassStats = { frames: 0, renderer: rendererName, slow, pixelRatio };
  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
  let scroll = 0;
  let scrollShown = 0;
  let running = false;
  let visible = true;
  let frame = 0;
  let last = performance.now();
  const start = last;
  const slowFrames: number[] = [];

  const draw = (now: number) => {
    const dt = Math.min(0.1, (now - last) / 1000);
    last = now;
    const t = slow ? 0 : (now - start) / 1000;
    const ease = slow ? 1 : 1 - Math.exp(-dt * 3.2);
    pointer.x += (pointer.tx - pointer.x) * ease;
    pointer.y += (pointer.ty - pointer.y) * ease;
    scrollShown += (scroll - scrollShown) * (slow ? 1 : 1 - Math.exp(-dt * 6));
    cell.rotation.set(
      0.1 + Math.sin(t * 0.19) * 0.16 + pointer.y * 0.16 + scrollShown * 0.35,
      Math.sin(t * 0.23) * 0.3 + pointer.x * 0.28 + scrollShown * 1.05,
      -0.1 + Math.sin(t * 0.13) * 0.035,
      "YXZ",
    );
    cell.position.y = Math.sin(t * 0.55) * 0.035;
    matrix.uniforms.uTime.value = t;
    renderer.render(scene, camera);
    stats.frames++;
  };

  const loop = (now: number) => {
    frame = requestAnimationFrame(loop);
    const dt = now - last;
    draw(now);
    // If the first seconds run slowly at a high pixel ratio, step it down once.
    if (stats.frames > 20 && stats.frames < 140 && pixelRatio > 1.25) {
      slowFrames.push(dt);
      if (slowFrames.length === 90) {
        const sorted = [...slowFrames].sort((a, b) => a - b);
        if (sorted[45] > 24) {
          pixelRatio = Math.max(1.25, pixelRatio * 0.75);
          stats.pixelRatio = pixelRatio;
          renderer.setPixelRatio(pixelRatio);
          fit();
        }
      }
    }
  };
  const requestDraw = () => {
    if (running || !visible) return;
    cancelAnimationFrame(frame);
    frame = requestAnimationFrame((now) => draw(now));
  };
  const update = () => {
    const shouldRun = !slow && visible && document.visibilityState === "visible";
    if (shouldRun && !running) {
      running = true;
      last = performance.now();
      frame = requestAnimationFrame(loop);
    } else if (!shouldRun && running) {
      running = false;
      cancelAnimationFrame(frame);
    }
  };

  const observer = new IntersectionObserver(
    ([entry]) => {
      visible = entry.isIntersecting;
      update();
      if (visible && slow) requestDraw();
    },
    { rootMargin: "80px" },
  );
  observer.observe(canvas);
  const onVisibility = () => update();
  document.addEventListener("visibilitychange", onVisibility);
  const resize = new ResizeObserver(() => {
    fit();
    if (!running) requestDraw();
  });
  resize.observe(canvas);

  try {
    await renderer.compileAsync(scene, camera);
  } catch {
    // Compiling ahead is only an optimization; the first render compiles anyway.
  }
  draw(performance.now());
  options.onReady();
  update();

  let disposed = false;
  return {
    stats,
    setScroll(progress) {
      scroll = progress;
      if (slow) requestDraw();
    },
    setPointer(x, y) {
      pointer.tx = x;
      pointer.ty = y;
      if (slow) requestDraw();
    },
    dispose() {
      if (disposed) return;
      disposed = true;
      running = false;
      cancelAnimationFrame(frame);
      observer.disconnect();
      resize.disconnect();
      document.removeEventListener("visibilitychange", onVisibility);
      shellGeometry.dispose();
      matrixGeometry.dispose();
      foldGeometry.dispose();
      backdropGeometry.dispose();
      shell.dispose();
      matrix.dispose();
      fold.dispose();
      backdropMaterial.dispose();
      environment.dispose();
      pmrem.dispose();
      renderer.dispose();
      renderer.forceContextLoss();
    },
  };
}
