// Look B ("Scroll film"): the film at the top of the Science page, made in code from four stills.
// The scroll bar is the playhead. One WebGL quad composites the shots, so the camera can push,
// dissolve through light and pull back like a single take (Mo's opening, September 28: "nature
// under the lens"):
//   1. A leaf in morning backlight with a glass lens over it. The camera pushes toward the lens.
//   2. The lens fills the frame and the view through it dissolves into the leaf's cells under the
//      microscope: the round field of the microscope lines up with the lens's own circle, so it
//      reads as looking through the glass. The camera keeps pushing toward the one bright cell.
//   3. That cell blooms into light, briefly, and the glowing mitochondrion comes out of it: the
//      light clears from the edges inward, so its glass rim is the first thing to resolve. It
//      floats with a little depth (its depth map shifts nearer glass more than the ground).
//   4. The camera pulls back and the cell dissolves into a field of cells; the frame settles.
// Every value is a pure function of the playhead (frameAt), so the DOM fallback without WebGL
// uses the same choreography. A software renderer (SwiftShader, llvmpipe) draws at 1x, without
// grain or drift, and only when the playhead moves.
type Three = typeof import("three");

export type Shot = { src: string; width: number; height: number };
export type OpeningShot = Shot & {
  // Alt text (DRAFT); the second shot is a bridge between two shots and has none.
  alt: string;
  // The round window the two shots share (0-1 across the picture's width; the center is 0-1 of
  // width and height, y down): the lens's clear opening in the first, the microscope's round field
  // in the second. The film scales the second so the two circles coincide on screen.
  circle: { center: [number, number]; radius: number };
  // The bright point the camera dives into (the second shot's glowing cell).
  point: [number, number];
  // Crops for the other places the first picture appears (CSS object-position).
  phone?: string;
  today?: string;
};

// ---- THE OPENING: the film's first two shots. Swap them here, and nowhere else. ------------
// Mo chose "Nature under the lens" (idea 2) on September 28, 2026. Any pair works that shares a
// round window and has one bright point to dive into.
export const OPENING: { still: OpeningShot; macro: OpeningShot } = {
  still: {
    src: "/images/science-page/film/lens-leaf.webp",
    width: 2400,
    height: 1340,
    alt: "Illustration: a green leaf in warm morning light, with a round glass lens over it that shows its fine veins.",
    circle: { center: [0.7208, 0.4925], radius: 0.215 },
    point: [0.7208, 0.4925],
    phone: "60% 50%",
    today: "90% 50%",
  },
  macro: {
    src: "/images/science-page/film/lens-cells.webp",
    width: 2400,
    height: 1340,
    alt: "",
    circle: { center: [0.5, 0.5], radius: 0.4325 },
    point: [0.4952, 0.4812],
  },
};

export const SHOTS = {
  opening: OPENING.still,
  macro: OPENING.macro,
  cell: { src: "/images/science-page/dark-cell.webp", width: 1920, height: 1086 },
  field: { src: "/images/closing/space-cells.webp", width: 1600, height: 900 },
} satisfies Record<string, Shot>;
// The glass cell's depth map (made for the same render on white; the dark render matches it).
const DEPTH = "/images/science/glass-cell-depth.png";
const ORDER = [SHOTS.opening, SHOTS.macro, SHOTS.cell, SHOTS.field];

// ---------------------------------------------------------------------------------------------
// The choreography. p is the playhead (0-1); aspect is the screen's width / height; t is seconds
// of idle time for the slow drift (0 on a software renderer).

export type Layer = {
  // The camera: the image point at the middle of the screen (0-1, y down), and the zoom (1 = cover).
  cx: number;
  cy: number;
  zoom: number;
  alpha: number;
  // Where the subject lands on the screen (0-1, y down), for the zoom blur and the light.
  fx: number;
  fy: number;
  // The visible part of the image at zoom 1 ("cover").
  sx: number;
  sy: number;
};
export type Frame = {
  layers: Layer[];
  flash: number;
  blur: number;
  bloom: number;
  light: number;
  dim: number;
  focus: [number, number];
  // The lens on screen (center x, y as 0-1 of the screen, radius as a share of its height) and how
  // far the view through it has opened to the whole frame (0: only inside the lens, 1: everywhere).
  lens: [number, number, number];
  lensOpen: number;
};

const clamp = (value: number, min = 0, max = 1) => Math.min(max, Math.max(min, value));
const seg = (p: number, a: number, b: number) => clamp((p - a) / (b - a));
const smooth = (t: number) => t * t * (3 - 2 * t);
const outCubic = (t: number) => 1 - Math.pow(1 - t, 3);
const inOut = (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const mix = (a: number, b: number, t: number) => a + (b - a) * t;

function cover(shot: Shot, aspect: number) {
  const image = shot.width / shot.height;
  return aspect > image ? { sx: 1, sy: image / aspect } : { sx: aspect / image, sy: 1 };
}

// Puts the image point (ix, iy) at (px, py) on the screen at this zoom. With edges kept, the
// camera never looks past the picture (the subject then lands as near as it can).
function place(
  shot: Shot,
  aspect: number,
  ix: number,
  iy: number,
  px: number,
  py: number,
  zoom: number,
  alpha: number,
  keepEdges: boolean,
): Layer {
  const { sx, sy } = cover(shot, aspect);
  let cx = ix - ((px - 0.5) * sx) / zoom;
  let cy = iy - ((py - 0.5) * sy) / zoom;
  if (keepEdges) {
    const hx = (0.5 * sx) / zoom;
    const hy = (0.5 * sy) / zoom;
    cx = hx >= 0.5 ? 0.5 : clamp(cx, hx, 1 - hx);
    cy = hy >= 0.5 ? 0.5 : clamp(cy, hy, 1 - hy);
  }
  return {
    cx,
    cy,
    zoom,
    alpha,
    fx: 0.5 + ((ix - cx) * zoom) / sx,
    fy: 0.5 + ((iy - cy) * zoom) / sy,
    sx,
    sy,
  };
}

// Scene timings on the playhead. The captions in look-film.tsx follow the same marks.
export const MARKS = {
  titleOut: [0.025, 0.11],
  cellCaption: [0.47, 0.53, 0.63, 0.68],
  fieldCaption: [0.8, 0.87],
} as const;

export function frameAt(p: number, aspect: number, t = 0): Frame {
  // A camera that is never quite still: a very slow breath and sway.
  const breath = 1 + 0.008 * Math.sin(t * 0.21);
  const swayX = 0.004 * Math.sin(t * 0.13);
  const swayY = 0.003 * Math.cos(t * 0.11);

  // 1. The leaf and its lens: a slow push toward the lens that gathers pace. The picture starts
  // with its dark left side fully in frame (the headline sits there).
  const { still, macro: bridge } = OPENING;
  const [lx, ly] = still.circle.center;
  const early = seg(p, 0, 0.27);
  const late = seg(p, 0.27, 0.37);
  const camera =
    (early < 1
      ? 1 + 1.05 * (0.25 * early + 0.75 * Math.pow(early, 2.2))
      : 2.05 + 4.2 * late * late) * breath;
  const approach = smooth(early);
  const leafStart = cover(SHOTS.opening, aspect);
  // Where the lens sits in the opening frame (the picture centered, as the file composes it).
  const lensHomeX = 0.5 + (lx - 0.5) / leafStart.sx;
  const opening = place(
    SHOTS.opening,
    aspect,
    lx,
    ly,
    mix(lensHomeX, 0.56, approach) + swayX,
    mix(ly, 0.5, approach) + swayY,
    camera,
    p < 0.285 ? 1 : 0,
    true,
  );

  // 2. Through the lens: the microscope's round field matches the lens's opening on screen, then
  // the camera keeps pushing toward the bright cell until it fills the frame.
  const leafCover = cover(SHOTS.opening, aspect);
  const cellsCover = cover(SHOTS.macro, aspect);
  const match =
    (camera * still.circle.radius * cellsCover.sx) / (leafCover.sx * bridge.circle.radius);
  const toward = smooth(seg(p, 0.26, 0.37));
  const [bx, by] = bridge.circle.center;
  const [tx, ty] = bridge.point;
  const macro = place(
    SHOTS.macro,
    aspect,
    mix(bx, tx, toward),
    mix(by, ty, toward),
    mix(opening.fx, 0.5, toward),
    mix(opening.fy, 0.5, toward),
    match,
    smooth(seg(p, 0.19, 0.27)) * (1 - seg(p, 0.385, 0.41)),
    false,
  );

  // 3. Out of the light, the glass cell. It arrives large, its glass rim near the edges of the
  // frame, so the rim is the first thing the clearing light shows; then it settles, holds, and
  // the camera draws away until the cell is small.
  const settle = outCubic(seg(p, 0.35, 0.54));
  const hold = seg(p, 0.54, 0.665);
  const away = inOut(seg(p, 0.665, 0.81));
  const cellZoom = mix(mix(1.75, 0.9, settle), 0.84, hold) * (1 - away) + 0.26 * away;
  const cell = place(
    SHOTS.cell,
    aspect,
    0.5,
    0.49,
    mix(0.645, 0.64, away) + swayX,
    mix(0.4, 0.54, away) + swayY,
    cellZoom * breath,
    smooth(seg(p, 0.35, 0.372)) * (1 - smooth(seg(p, 0.75, 0.83))),
    false,
  );

  // 4. The field of cells: it arrives over the small cell (a double exposure) and settles.
  const f1 = outCubic(seg(p, 0.665, 0.92));
  const f2 = seg(p, 0.92, 1);
  const field = place(
    SHOTS.field,
    aspect,
    0.465,
    0.6,
    0.64 + swayX,
    0.555 + swayY,
    mix(mix(3.4, 1.07, f1), 1.0, f2) * breath,
    smooth(seg(p, 0.68, 0.8)),
    false,
  );

  // The bright cell blooms into light only briefly (0.325-0.41), at its fullest at 0.362.
  const rise = seg(p, 0.33, 0.362);
  const fall = seg(p, 0.362, 0.388);
  const flash = p < 0.362 ? Math.pow(rise, 1.7) : 1 - smooth(fall);
  const blur =
    0.13 * smooth(seg(p, 0.28, 0.355)) * (1 - smooth(seg(p, 0.355, 0.38))) +
    0.05 * smooth(seg(p, 0.67, 0.74)) * (1 - smooth(seg(p, 0.74, 0.82)));
  const focus: [number, number] =
    p < 0.22
      ? [opening.fx, opening.fy]
      : p < 0.362
        ? [macro.fx, macro.fy]
        : p < 0.7
          ? [cell.fx, cell.fy]
          : [field.fx, field.fy];

  return {
    layers: [opening, macro, cell, field],
    flash,
    blur,
    bloom: 0.25 + 0.5 * seg(p, 0.18, 0.34) - 0.5 * seg(p, 0.37, 0.47),
    light: 1 + 0.1 * smooth(seg(p, 0.2, 0.34)) - 0.1 * smooth(seg(p, 0.36, 0.46)),
    dim: 1 - 0.42 * smooth(seg(p, 0.9, 1)),
    focus,
    // The lens's clear opening, measured on the leaf (its radius is a share of the picture's width).
    lens: [opening.fx, opening.fy, (still.circle.radius * camera * aspect) / leafCover.sx],
    lensOpen: smooth(seg(p, 0.25, 0.3)),
  };
}

// ---------------------------------------------------------------------------------------------
// The WebGL film.

const vertexShader = /* glsl */ `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = vec4(position.xy, 0.0, 1.0);
  }
`;

const fragmentShader = /* glsl */ `
  precision highp float;
  uniform sampler2D uTex0;
  uniform sampler2D uTex1;
  uniform sampler2D uTex2;
  uniform sampler2D uTex3;
  uniform sampler2D uDepth;
  uniform vec4 uCam[4];   // camera x, y (image, y down), zoom, alpha
  uniform vec2 uCover[4]; // the visible part of each image at zoom 1
  uniform vec2 uFocus;    // screen, y down
  uniform vec3 uLens;     // the lens on screen: center (y down) and radius (share of the height)
  uniform float uLensOpen;
  uniform vec2 uRes;
  uniform vec2 uTilt;
  uniform float uBlur;
  uniform float uFlash;
  uniform float uBloom;
  uniform float uLight;
  uniform float uDim;
  uniform float uTime;
  uniform float uGrain;
  varying vec2 vUv;

  float hash(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
  }

  vec2 imageUv(vec2 s, vec4 cam, vec2 cover) {
    vec2 p = cam.xy + (s - 0.5) * cover / cam.z;
    return vec2(p.x, 1.0 - p.y);
  }

  // The cell: nearer glass shifts with the tilt, the dark ground barely moves.
  vec2 cellUv(vec2 s) {
    vec2 uv = imageUv(s, uCam[2], uCover[2]);
    float depth = texture2D(uDepth, uv).r;
    return uv + uTilt * (depth - 0.25) * 0.022;
  }

  // The leaf shots are graded a touch warmer and softer in their greens, toward the page's gold.
  vec3 warm(vec3 c) {
    float l = dot(c, vec3(0.299, 0.587, 0.114));
    c = mix(vec3(l), c, 0.88);
    return c * vec3(1.035, 0.995, 0.93);
  }

  // All shots at one screen point. bias > 0 reads a softer mip level (for the glow).
  vec3 shots(vec2 s, float bias) {
    vec3 c = vec3(0.0);
    if (uCam[0].w > 0.001) c = mix(c, warm(texture2D(uTex0, imageUv(s, uCam[0], uCover[0]), bias).rgb), uCam[0].w);
    // The cells appear inside the lens first, as if seen through it, then fill the frame.
    if (uCam[1].w > 0.001) {
      float r = length((s - uLens.xy) * vec2(uRes.x / uRes.y, 1.0));
      float inside = 1.0 - smoothstep(uLens.z * 0.9, uLens.z * 1.01, r);
      float a = uCam[1].w * mix(inside, 1.0, uLensOpen);
      c = mix(c, warm(texture2D(uTex1, imageUv(s, uCam[1], uCover[1]), bias).rgb), a);
    }
    if (uCam[2].w > 0.001) c = mix(c, texture2D(uTex2, cellUv(s), bias).rgb, uCam[2].w);
    // The field arrives as a double exposure (light adds to light, the dark stays dark), then
    // takes over the frame.
    if (uCam[3].w > 0.001) {
      float a = uCam[3].w;
      vec3 f = texture2D(uTex3, imageUv(s, uCam[3], uCover[3]), bias).rgb;
      vec3 exposed = 1.0 - (1.0 - c) * (1.0 - f * a);
      c = mix(exposed, mix(c, f, a), smoothstep(0.6, 1.0, a));
    }
    return c;
  }

  void main() {
    vec2 s = vec2(vUv.x, 1.0 - vUv.y);
    float aspect = uRes.x / uRes.y;
    vec3 color;

    // A zoom blur toward the light while the camera rushes in.
    if (uBlur > 0.001) {
      vec3 sum = vec3(0.0);
      float jitter = hash(gl_FragCoord.xy + uTime) / 12.0;
      for (int k = 0; k < 12; k++) {
        float f = float(k) / 12.0 + jitter;
        sum += shots(uFocus + (s - uFocus) * (1.0 - uBlur * f), 0.0);
      }
      color = sum / 12.0;
    } else {
      color = shots(s, 0.0);
    }

    // Bloom: only the brightest light spills, softly and warm (a blurred, thresholded copy).
    vec2 o = vec2(0.012 / aspect, 0.012);
    vec3 soft = shots(s, 5.0) * 0.4 + shots(s + o, 4.0) * 0.15 + shots(s - o, 4.0) * 0.15
      + shots(s + vec2(o.x, -o.y) * 2.0, 5.5) * 0.15 + shots(s + vec2(-o.x, o.y) * 2.0, 5.5) * 0.15;
    float softLum = dot(soft, vec3(0.299, 0.587, 0.114));
    vec3 glow = soft * smoothstep(0.55, 0.95, softLum) * uBloom * vec3(1.0, 0.78, 0.52);

    // Exposure rises as the camera pushes toward the beaker. The added light rolls off into the
    // headroom above each pixel, so a still at rest looks exactly like its file and highlights
    // never clip to a flat colour.
    vec3 lifted = color * uLight + glow - color;
    vec3 room = max(1.0 - color, 0.0);
    color += room * (1.0 - exp(-max(lifted, 0.0) / max(room, 0.001)));

    // Lens: a quiet vignette and the end-of-film dim.
    float v = smoothstep(1.3, 0.3, length((s - 0.5) * vec2(aspect * 0.78, 1.0)));
    color *= mix(0.66, 1.0, v) * uDim;

    // The light fills the lens: the middle of the glow and the brightest parts go first. The light
    // is warm white at its heart and amber toward the edges.
    float d = length((s - uFocus) * vec2(aspect, 1.0));
    float lum = dot(color, vec3(0.299, 0.587, 0.114));
    float reach = smoothstep(0.0, 1.0, clamp(uFlash * 2.2 - d * 0.75 + lum * 0.5 - 0.3, 0.0, 1.0));
    vec3 light = mix(vec3(1.0, 0.95, 0.84), vec3(0.96, 0.64, 0.28), smoothstep(0.05, 1.1, d));
    color = mix(color, light, reach * min(0.5, uFlash * 0.95));

    color += (hash(gl_FragCoord.xy * 0.73 + fract(uTime * 7.13) * 91.0) - 0.5) * uGrain;
    gl_FragColor = vec4(clamp(color, 0.0, 1.0), 1.0);
  }
`;

export type FilmMode = "webgl" | "slow";
export type FilmScene = { dispose: () => void };
type Options = {
  // The smoothed playhead, 0-1.
  progress: () => number;
  onReady: (mode: FilmMode) => void;
  onFail: () => void;
};

export function createFilm(
  THREE: Three,
  holder: HTMLElement,
  stage: HTMLElement,
  options: Options,
): FilmScene {
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
  const slow = /swiftshader|llvmpipe|software/i.test(name);
  // The stills are about 2,000 px wide: more than 1.5x adds no detail, only work.
  renderer.setPixelRatio(slow ? 1 : Math.min(window.devicePixelRatio || 1, 1.5));
  renderer.setClearColor(0x05070d, 1);
  const canvas = renderer.domElement;
  canvas.setAttribute("aria-hidden", "true");
  canvas.dataset.renderer = name;
  holder.appendChild(canvas);

  const uniforms = {
    uTex0: { value: null as import("three").Texture | null },
    uTex1: { value: null as import("three").Texture | null },
    uTex2: { value: null as import("three").Texture | null },
    uTex3: { value: null as import("three").Texture | null },
    uDepth: { value: null as import("three").Texture | null },
    uCam: { value: ORDER.map(() => new THREE.Vector4(0.5, 0.5, 1, 0)) },
    uCover: { value: ORDER.map(() => new THREE.Vector2(1, 1)) },
    uFocus: { value: new THREE.Vector2(0.5, 0.5) },
    uLens: { value: new THREE.Vector3(0.5, 0.5, 0.3) },
    uLensOpen: { value: 0 },
    uRes: { value: new THREE.Vector2(1, 1) },
    uTilt: { value: new THREE.Vector2() },
    uBlur: { value: 0 },
    uFlash: { value: 0 },
    uBloom: { value: 0 },
    uLight: { value: 1 },
    uDim: { value: 1 },
    uTime: { value: 0 },
    uGrain: { value: slow ? 0 : 0.028 },
  };
  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const geometry = new THREE.PlaneGeometry(2, 2);
  const material = new THREE.ShaderMaterial({
    uniforms,
    vertexShader,
    fragmentShader,
    depthTest: false,
    depthWrite: false,
  });
  scene.add(new THREE.Mesh(geometry, material));

  // Textures are read as plain sRGB bytes (no decode), so the output matches the files. Mipmaps
  // stay on: the glow reads the softer levels.
  const loader = new THREE.TextureLoader();
  const textures: import("three").Texture[] = [];
  let loaded = false;
  let disposed = false;
  Promise.all([...ORDER.map((shot) => shot.src), DEPTH].map((src) => loader.loadAsync(src)))
    .then((list) => {
      if (disposed) {
        list.forEach((texture) => texture.dispose());
        return;
      }
      list.forEach((texture) => {
        texture.wrapS = THREE.ClampToEdgeWrapping;
        texture.wrapT = THREE.ClampToEdgeWrapping;
        texture.anisotropy = Math.min(4, renderer.capabilities.getMaxAnisotropy());
        textures.push(texture);
      });
      [uniforms.uTex0, uniforms.uTex1, uniforms.uTex2, uniforms.uTex3, uniforms.uDepth].forEach(
        (slot, index) => {
          slot.value = list[index];
        },
      );
      loaded = true;
      schedule();
    })
    .catch(() => {
      if (!disposed) options.onFail();
    });

  let width = 1;
  let height = 1;
  function fit() {
    width = holder.clientWidth || 1;
    height = holder.clientHeight || 1;
    renderer.setSize(width, height, false);
    uniforms.uRes.value.set(width, height);
  }
  fit();

  // The pointer leans the cell a little; without a pointer it sways on its own.
  const pointer = { x: 0, y: 0, tx: 0, ty: 0, last: -1e9 };
  function lean(event: PointerEvent) {
    if (event.pointerType !== "mouse") return;
    pointer.tx = (event.clientX / window.innerWidth - 0.5) * 2;
    pointer.ty = (event.clientY / window.innerHeight - 0.5) * 2;
    pointer.last = performance.now();
    schedule();
  }
  window.addEventListener("pointermove", lean, { passive: true });

  let frame = 0;
  let visible = true;
  let drawn = false;
  let lastP = -1;
  const start = performance.now();
  let last = start;

  function draw(now: number) {
    frame = 0;
    if (!loaded) return;
    const seconds = Math.min((now - last) / 1000, 0.1);
    last = now;
    const t = slow ? 0 : (now - start) / 1000;
    const p = clamp(options.progress());
    const f = frameAt(p, width / height, t);

    f.layers.forEach((layer, index) => {
      uniforms.uCam.value[index].set(layer.cx, layer.cy, layer.zoom, layer.alpha);
      uniforms.uCover.value[index].set(layer.sx, layer.sy);
    });
    uniforms.uFocus.value.set(f.focus[0], f.focus[1]);
    uniforms.uLens.value.set(f.lens[0], f.lens[1], f.lens[2]);
    uniforms.uLensOpen.value = f.lensOpen;
    uniforms.uBlur.value = f.blur;
    uniforms.uFlash.value = f.flash;
    uniforms.uBloom.value = f.bloom;
    uniforms.uLight.value = f.light;
    uniforms.uDim.value = f.dim;
    uniforms.uTime.value = t;

    let moving = Math.abs(p - lastP) > 0.00005;
    lastP = p;
    if (!slow) {
      if (now - pointer.last > 2500) {
        pointer.tx = Math.sin(t * 0.37) * 0.6;
        pointer.ty = Math.cos(t * 0.29) * 0.4;
      }
      const ease = 1 - Math.exp(-seconds * 2.4);
      pointer.x += (pointer.tx - pointer.x) * ease;
      pointer.y += (pointer.ty - pointer.y) * ease;
    } else {
      pointer.x = pointer.tx;
      pointer.y = pointer.ty;
    }
    uniforms.uTilt.value.set(-pointer.x, pointer.y);

    renderer.render(scene, camera);
    stage.dataset.filmP = p.toFixed(3);
    if (!drawn) {
      drawn = true;
      moving = true;
      options.onReady(slow ? "slow" : "webgl");
    }
    // Alive: every frame. A software renderer draws again only while something moves.
    if (!slow || moving) schedule();
  }

  function schedule() {
    if (!frame && visible && !document.hidden && !disposed) frame = requestAnimationFrame(draw);
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
  watch.observe(stage);

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
  // A software renderer rests between scrolls; the scroll wakes it.
  const nudge = () => schedule();
  window.addEventListener("scroll", nudge, { passive: true });

  return {
    dispose() {
      disposed = true;
      if (frame) cancelAnimationFrame(frame);
      frame = 0;
      resize.disconnect();
      watch.disconnect();
      document.removeEventListener("visibilitychange", onVisibility);
      window.removeEventListener("pointermove", lean);
      window.removeEventListener("scroll", nudge);
      textures.forEach((texture) => texture.dispose());
      geometry.dispose();
      material.dispose();
      renderer.dispose();
      canvas.remove();
    },
  };
}
