// The liquid light behind look A ("Liquid light"): one fragment shader, domain-warped noise that
// flows slowly like ink in water, lit from within, with one thin thread of molten gold drifting
// through it. The hero, the years and river of his path, the three record numbers and Ask BiGH
// Science each draw it on their own canvas with their own preset (the hero's is the brightest and
// the only one the pointer stirs). The years and numbers are paper-colored text blocks blended with
// "lighten" over their canvas, so only the letters show the light.
//
// Plain WebGL 1, no library: a full-screen triangle and one shader. Each view pauses while it is
// off screen or the tab is hidden, caps its resolution, and on a software renderer (SwiftShader,
// llvmpipe) draws at half size and only when something changes. Reduced motion: one still frame.

export type LightPreset = "hero" | "fill" | "river" | "strip" | "ask";
export type LightMode = "webgl" | "slow" | "still";

type Params = {
  // CSS px per unit of the noise field (bigger = broader, calmer shapes).
  unit: number;
  // Field seconds per real second.
  speed: number;
  // How bright the light inside the ink gets (0-1.5).
  glow: number;
  // The gold thread's strength (0 = none).
  gold: number;
  grain: number;
  vignette: number;
  // Where the gold thread runs, as a fraction of the view's height (from the top).
  threadY: number;
  // Resolution: canvas pixels per CSS pixel at DPR 1 (the flow is soft; the grain stays fine).
  res: number;
  // Lift the darkest ink toward cobalt (the numbers need a mid-dark fill, not black).
  floor: number;
  stir: boolean;
  // Seconds the light takes to rise on first show (0 = at once).
  rise: number;
  // Where the light gathers, from the view's middle (x in heights, y down) and how strongly.
  pool: [number, number, number];
  // The thread fades in between these two points across the view (0-1 from the left), so it
  // stays clear of the hero's headline. [0, 0]: everywhere.
  threadFade: [number, number];
  // Brightest value any channel may reach (the text fills stay darker than the paper).
  ceil: number;
  // Lifts the whole light toward cobalt and ice (0 = as is).
  lift: number;
};

const PRESETS: Record<LightPreset, Params> = {
  hero: {
    unit: 820,
    speed: 1,
    glow: 1,
    gold: 1,
    grain: 0.05,
    vignette: 0.55,
    threadY: 0.27,
    res: 0.75,
    floor: 0,
    stir: true,
    rise: 2.6,
    pool: [0.42, -0.08, 0.85],
    threadFade: [0.34, 0.66],
    ceil: 1,
    lift: 0,
  },
  fill: {
    unit: 520,
    speed: 0.8,
    glow: 0.9,
    gold: 1,
    grain: 0.03,
    vignette: 0,
    threadY: 0.55,
    res: 1,
    floor: 0,
    stir: false,
    rise: 0,
    pool: [0, 0, 0],
    threadFade: [0, 0],
    ceil: 0.9,
    lift: 0.12,
  },
  river: {
    unit: 640,
    speed: 0.9,
    glow: 1.05,
    gold: 1,
    grain: 0.03,
    vignette: 0,
    threadY: 0.93,
    res: 1,
    floor: 0,
    stir: false,
    rise: 0,
    pool: [0, 0, 0],
    threadFade: [0, 0],
    ceil: 0.9,
    lift: 0.12,
  },
  // The thin upright band beside Dr. Liu's portrait: the hero's light, calm, no thread.
  strip: {
    unit: 560,
    speed: 0.7,
    glow: 1,
    gold: 0,
    grain: 0.03,
    vignette: 0,
    threadY: 0.5,
    res: 1,
    floor: 0,
    stir: false,
    rise: 0,
    pool: [0, 0, 0],
    threadFade: [0, 0],
    ceil: 0.95,
    lift: 0.1,
  },
  ask: {
    unit: 980,
    speed: 0.45,
    glow: 0.62,
    gold: 0.55,
    grain: 0.05,
    vignette: 0.7,
    threadY: 0.16,
    res: 0.6,
    floor: 0,
    stir: false,
    rise: 0,
    pool: [0.35, 0.1, 0.8],
    threadFade: [0.5, 0.8],
    ceil: 1,
    lift: 0,
  },
};

// Canvas pixels drawn per frame at most (the hero at 1440 x 900 and DPR 1 draws about 730,000).
const MAX_PIXELS = 1_300_000;

const VERTEX = /* glsl */ `
attribute vec2 aPosition;
void main() {
  gl_Position = vec4(aPosition, 0.0, 1.0);
}
`;

// LIGHT-FRAGMENT-START
const FRAGMENT = /* glsl */ `
#ifdef GL_OES_standard_derivatives
#extension GL_OES_standard_derivatives : enable
#endif
precision highp float;

uniform vec2 uRes;
uniform vec2 uSize;
uniform vec2 uOffset;
uniform float uUnit;
uniform float uTime;
uniform vec3 uStir;
uniform float uDepth;
uniform float uFade;
uniform float uGlow;
uniform float uGold;
uniform float uGrain;
uniform float uVignette;
uniform float uThreadY;
uniform float uFloor;
uniform float uSeed;
uniform vec3 uPool;
uniform vec2 uThreadFade;
uniform float uCeil;
uniform float uLift;

// 2D simplex noise (Ashima Arts, Ian McEwan; MIT).
vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec2 mod289(vec2 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec3 permute(vec3 x) { return mod289(((x * 34.0) + 1.0) * x); }
float snoise(vec2 v) {
  const vec4 C = vec4(0.211324865405187, 0.366025403784439, -0.577350269189626, 0.024390243902439);
  vec2 i = floor(v + dot(v, C.yy));
  vec2 x0 = v - i + dot(i, C.xx);
  vec2 i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
  vec4 x12 = x0.xyxy + C.xxzz;
  x12.xy -= i1;
  i = mod289(i);
  vec3 p = permute(permute(i.y + vec3(0.0, i1.y, 1.0)) + i.x + vec3(0.0, i1.x, 1.0));
  vec3 m = max(0.5 - vec3(dot(x0, x0), dot(x12.xy, x12.xy), dot(x12.zw, x12.zw)), 0.0);
  m = m * m;
  m = m * m;
  vec3 x = 2.0 * fract(p * C.www) - 1.0;
  vec3 h = abs(x) - 0.5;
  vec3 ox = floor(x + 0.5);
  vec3 a0 = x - ox;
  m *= 1.79284291400159 - 0.85373472095314 * (a0 * a0 + h * h);
  vec3 g;
  g.x = a0.x * x0.x + h.x * x0.y;
  g.yz = a0.yz * x12.xz + h.yz * x12.yw;
  return 130.0 * dot(m, g);
}

const mat2 TURN = mat2(0.8, 0.6, -0.6, 0.8);

// Four octaves: broad shapes with a little fine detail, never busy.
float fbm(vec2 p) {
  float sum = 0.0;
  float amp = 0.5;
  for (int i = 0; i < 4; i++) {
    sum += amp * snoise(p);
    p = TURN * p * 2.0 + vec2(17.1, 3.7);
    amp *= 0.42;
  }
  return sum;
}

float hash(vec2 p) {
  vec3 p3 = fract(vec3(p.xyx) * 0.1031);
  p3 += dot(p3, p3.yzx + 33.33);
  return fract((p3.x + p3.y) * p3.z);
}

// The warped field: two layers of warping (Inigo Quilez), drifting at different speeds.
float field(vec2 p, float t, out vec2 q, out vec2 r) {
  q = vec2(
    fbm(p + vec2(0.021, 0.013) * t),
    fbm(p + vec2(5.2, 1.3) - vec2(0.012, 0.019) * t)
  );
  r = vec2(
    fbm(p + 1.25 * q + vec2(1.7, 9.2) + vec2(0.026, -0.008) * t),
    fbm(p + 1.25 * q + vec2(8.3, 2.8) + vec2(-0.010, 0.021) * t)
  );
  return fbm(p + 1.35 * r);
}

void main() {
  // This pixel in CSS px (y down), then in the shared field.
  vec2 css = vec2(gl_FragCoord.x, uRes.y - gl_FragCoord.y) * (uSize / uRes);
  vec2 base = (css + uOffset) / uUnit + vec2(uSeed, uSeed * 0.37);
  vec2 p = base;
  float t = uTime;

  // The pointer stirs: a slow turn of the field around it that fades with distance.
  vec2 s = (uStir.xy + uOffset) / uUnit + vec2(uSeed, uSeed * 0.37);
  vec2 d = p - s;
  float turn = uStir.z * 0.8 * exp(-dot(d, d) * 4.0);
  float ct = cos(turn);
  float st = sin(turn);
  p = s + mat2(ct, st, -st, ct) * d;

  vec2 q;
  vec2 r;
  vec2 w = p * 0.42;
  float f = field(w, t, q, r);

  // Slope of the field: where it turns over, the light catches (like folds in silk).
  float e = 0.03;
  float fx = fbm(w + vec2(e, 0.0) + 1.35 * r);
  float fy = fbm(w + vec2(0.0, e) + 1.35 * r);
  vec3 normal = normalize(vec3((f - fx) / e, (f - fy) / e, 5.0));
  vec3 lightDir = normalize(vec3(-0.45, 0.55, 0.7));
  float diffuse = clamp(dot(normal, lightDir), 0.0, 1.0);
  float sheen = pow(clamp(dot(reflect(-lightDir, normal), vec3(0.0, 0.0, 1.0)), 0.0, 1.0), 18.0);

  vec3 night = vec3(0.012, 0.030, 0.125);
  vec3 deep = vec3(0.039, 0.086, 0.314);
  vec3 cobalt = vec3(0.129, 0.286, 0.639);
  vec3 ice = vec3(0.624, 0.816, 1.0);
  vec3 gold = vec3(0.953, 0.706, 0.298);

  // Where the light gathers: a broad pool that drifts slowly (the rest of the ink stays deep).
  vec2 view = css / uSize - 0.5;
  view.x *= uSize.x / uSize.y;
  vec2 center = uPool.xy + vec2(0.07 * sin(t * 0.043), 0.05 * cos(t * 0.037));
  vec2 away = view - center;
  float pool = mix(1.0, exp(-dot(away, away) * 2.2), uPool.z);

  // Body of the ink: night to ultramarine to cobalt, lit from within where it is thickest.
  float body = clamp(0.5 + 1.05 * f, 0.0, 1.0);
  body *= mix(0.62, 1.14, pool);
  float glow = smoothstep(0.35, 1.0, body) * (0.6 + 0.4 * clamp(length(q) * 1.6, 0.0, 1.0));
  vec3 color = mix(night, deep, smoothstep(0.0, 0.5, body));
  color = mix(color, cobalt, glow);
  color = mix(color, deep, uFloor * (1.0 - smoothstep(0.15, 0.55, body)));
  color *= 0.84 + 0.28 * diffuse;
  // Light from within: a soft glow through the thickest ink, and a faint sheen on the folds.
  color += ice * pow(glow, 2.4) * pool * 0.34 * uGlow;
  color += ice * sheen * (0.2 + 0.8 * glow) * 0.22 * uGlow * (0.35 + 0.65 * pool);
  color = mix(color, ice, pow(smoothstep(0.72, 1.0, body), 2.0) * 0.42 * uGlow);

  // The gold thread: one slow line, bent gently by the flow.
  float drift = 0.15 * snoise(vec2(base.x * 0.5 + t * 0.012, 7.3))
    + 0.05 * snoise(base * 1.1 + vec2(t * 0.02, 1.9)) + 0.04 * r.x;
  float line = (css.y / uSize.y - uThreadY) * uSize.y / uUnit + drift;
#ifdef GL_OES_standard_derivatives
  float width = max(fwidth(line), 1e-4);
#else
  float width = 1.2 / uUnit;
#endif
  float px = abs(line) / width;
  float strand = smoothstep(0.05, 0.75, 0.5 + 0.5 * snoise(vec2(base.x * 1.3 - t * 0.035, 3.1)));
  float core = exp(-px * px * 0.45);
  float halo = exp(-abs(line) * uUnit / 22.0);
  float across = uThreadFade.y > 0.0 ? smoothstep(uThreadFade.x, uThreadFade.y, css.x / uSize.x) : 1.0;
  float heat = strand * uGold * (0.55 + 0.45 * pool) * across;
  color = mix(color, gold, clamp(core * 0.95 + halo * 0.16, 0.0, 1.0) * heat);
  color += vec3(1.0, 0.9, 0.7) * core * core * heat * 0.25;

  color = mix(color, color * 0.7 + cobalt * 0.35 + ice * 0.08, uLift);

  // Deeper and darker as the view is left behind.
  color = mix(color, color * 0.42 + deep * 0.12, uDepth);

  // Soft vignette, the rise from dark, and fine grain.
  vec2 uv = css / uSize - 0.5;
  uv.x *= uSize.x / uSize.y * 0.75;
  float vignette = 1.0 - uVignette * smoothstep(0.35, 1.05, length(uv));
  color *= vignette;
  color = mix(night, color, uFade);
  float grain = hash(gl_FragCoord.xy + fract(t * 7.13) * 91.7) - 0.5;
  color += grain * uGrain;

  gl_FragColor = vec4(clamp(color, 0.0, uCeil), 1.0);
}
`;
// LIGHT-FRAGMENT-END

export type LightView = {
  canvas: HTMLCanvasElement;
  preset: LightPreset;
  // Where this view sits in the shared field, in CSS px (the river passes its track's offset, so
  // the light moves with the path; the numbers pass their place on the page, so the three read as
  // windows onto one flow).
  offset?: () => [number, number];
  // 0-1: how far the view has been left behind (the hero deepens and slows as it scrolls away).
  depth?: () => number;
  // Reduced motion: one still frame.
  still: () => boolean;
  seed?: number;
  onReady?: (mode: LightMode) => void;
};

export type Light = {
  // Draw again soon (a software renderer draws only on request).
  wake: () => void;
  refresh: () => void;
  dispose: () => void;
};

// Compiles the shader into a context and sets the preset's fixed values. Null if it fails.
function build(gl: WebGLRenderingContext, params: Params, seed: number) {
  const compile = (type: number, source: string) => {
    const shader = gl.createShader(type);
    if (!shader) return null;
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      console.warn(gl.getShaderInfoLog(shader));
      gl.deleteShader(shader);
      return null;
    }
    return shader;
  };
  const vertex = compile(gl.VERTEX_SHADER, VERTEX);
  const fragment = compile(gl.FRAGMENT_SHADER, FRAGMENT);
  const program = gl.createProgram();
  const lose = () => gl.getExtension("WEBGL_lose_context")?.loseContext();
  if (!vertex || !fragment || !program) return null;
  gl.attachShader(program, vertex);
  gl.attachShader(program, fragment);
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) return null;
  gl.useProgram(program);

  // One triangle that covers the whole canvas.
  const buffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const position = gl.getAttribLocation(program, "aPosition");
  gl.enableVertexAttribArray(position);
  gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 0, 0);

  const u = (key: string) => gl.getUniformLocation(program, key);
  const uniform = {
    res: u("uRes"),
    size: u("uSize"),
    offset: u("uOffset"),
    unit: u("uUnit"),
    time: u("uTime"),
    stir: u("uStir"),
    depth: u("uDepth"),
    fade: u("uFade"),
    glow: u("uGlow"),
    gold: u("uGold"),
    grain: u("uGrain"),
    vignette: u("uVignette"),
    threadY: u("uThreadY"),
    floor: u("uFloor"),
    seed: u("uSeed"),
    pool: u("uPool"),
    threadFade: u("uThreadFade"),
    ceil: u("uCeil"),
    lift: u("uLift"),
  };
  gl.uniform1f(uniform.unit, params.unit);
  gl.uniform1f(uniform.glow, params.glow);
  gl.uniform1f(uniform.gold, params.gold);
  gl.uniform1f(uniform.grain, params.grain);
  gl.uniform1f(uniform.vignette, params.vignette);
  gl.uniform1f(uniform.threadY, params.threadY);
  gl.uniform1f(uniform.floor, params.floor);
  gl.uniform1f(uniform.seed, seed);
  gl.uniform3f(uniform.pool, ...params.pool);
  gl.uniform2f(uniform.threadFade, ...params.threadFade);
  gl.uniform1f(uniform.ceil, params.ceil);
  gl.uniform1f(uniform.lift, params.lift);
  return { program, buffer, vertex, fragment, uniform, lose };
}

export function createLight(view: LightView): Light | null {
  const { canvas } = view;
  const params = PRESETS[view.preset];
  const context = canvas.getContext("webgl", {
    alpha: false,
    antialias: false,
    depth: false,
    stencil: false,
    premultipliedAlpha: false,
    preserveDrawingBuffer: false,
    powerPreference: "high-performance",
  });
  if (!context) return null;
  const gl: WebGLRenderingContext = context;
  gl.getExtension("OES_standard_derivatives");

  const info = gl.getExtension("WEBGL_debug_renderer_info");
  const name = String(
    info ? gl.getParameter(info.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER),
  );
  const slow = /swiftshader|llvmpipe|software/i.test(name);
  canvas.dataset.renderer = name;

  const built = build(gl, params, view.seed ?? 0);
  if (!built) {
    gl.getExtension("WEBGL_lose_context")?.loseContext();
    return null;
  }
  const { program, buffer, vertex, fragment, uniform, lose } = built;

  let width = 0;
  let height = 0;
  function fit() {
    width = canvas.clientWidth;
    height = canvas.clientHeight;
    if (!width || !height) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    let scale = slow ? 0.5 : dpr * params.res;
    const pixels = width * height * scale * scale;
    if (pixels > MAX_PIXELS) scale *= Math.sqrt(MAX_PIXELS / pixels);
    canvas.width = Math.max(1, Math.round(width * scale));
    canvas.height = Math.max(1, Math.round(height * scale));
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.uniform2f(uniform.res, canvas.width, canvas.height);
    gl.uniform2f(uniform.size, width, height);
  }
  fit();

  // The pointer: where it is over this canvas, and how much it is stirring (from its speed).
  const pointer = { x: -9999, y: -9999, stir: 0, target: 0, lastX: 0, lastY: 0, seen: false };
  function onPointer(event: PointerEvent) {
    if (event.pointerType !== "mouse") return;
    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    if (pointer.seen) {
      const moved = Math.hypot(x - pointer.lastX, y - pointer.lastY);
      pointer.target = Math.min(1, pointer.target + moved / 260);
    } else {
      pointer.x = x;
      pointer.y = y;
    }
    pointer.seen = true;
    pointer.lastX = x;
    pointer.lastY = y;
    wake();
  }
  if (params.stir) window.addEventListener("pointermove", onPointer, { passive: true });

  let frame = 0;
  let visible = false;
  let last = performance.now();
  let time = 11.0 + (view.seed ?? 0) * 3.1;
  let born = -1;
  let drawn = false;

  function draw(now: number) {
    frame = 0;
    if (!width || !height) fit();
    if (!width || !height) return;
    const still = view.still();
    const seconds = Math.min((now - last) / 1000, 0.1);
    last = now;
    const depth = view.depth ? view.depth() : 0;
    const [ox, oy] = view.offset ? view.offset() : [0, 0];
    let moving = false;

    if (!still && !slow) {
      time += seconds * params.speed * (1 - 0.72 * depth);
      moving = true;
    }
    if (born < 0) born = now;
    const rise =
      still || slow || !params.rise ? 1 : Math.min(1, (now - born) / (params.rise * 1000));
    const fade = 1 - Math.pow(1 - rise, 3);

    // The stir eases in and out; the stirring point trails the pointer.
    const ease = 1 - Math.exp(-seconds * 2.2);
    pointer.stir += (pointer.target - pointer.stir) * ease;
    pointer.target *= Math.exp(-seconds * 0.9);
    if (pointer.seen) {
      pointer.x += (pointer.lastX - pointer.x) * (1 - Math.exp(-seconds * 1.6));
      pointer.y += (pointer.lastY - pointer.y) * (1 - Math.exp(-seconds * 1.6));
    }
    if (slow && pointer.stir > 0.01) moving = true;

    gl.uniform1f(uniform.time, time);
    gl.uniform2f(uniform.offset, ox, oy);
    gl.uniform3f(uniform.stir, pointer.x, pointer.y, still ? 0 : pointer.stir);
    gl.uniform1f(uniform.depth, depth);
    gl.uniform1f(uniform.fade, fade);
    gl.drawArrays(gl.TRIANGLES, 0, 3);

    if (!drawn) {
      drawn = true;
      canvas.dataset.light = still ? "still" : slow ? "slow" : "webgl";
      view.onReady?.(still ? "still" : slow ? "slow" : "webgl");
    }
    canvas.dataset.frames = String(Number(canvas.dataset.frames ?? 0) + 1);
    if (!still && (moving || rise < 1)) schedule();
  }

  function schedule() {
    if (!frame && visible && !document.hidden) frame = requestAnimationFrame(draw);
  }
  function wake() {
    schedule();
  }

  const watch = new IntersectionObserver(
    ([entry]) => {
      visible = entry.isIntersecting;
      if (visible) {
        last = performance.now();
        schedule();
      } else if (frame) {
        cancelAnimationFrame(frame);
        frame = 0;
      }
    },
    { rootMargin: "120px 0px" },
  );
  watch.observe(canvas);

  const resize = new ResizeObserver(() => {
    fit();
    wake();
  });
  resize.observe(canvas);

  function onVisibility() {
    if (document.hidden) {
      if (frame) cancelAnimationFrame(frame);
      frame = 0;
    } else {
      last = performance.now();
      wake();
    }
  }
  document.addEventListener("visibilitychange", onVisibility);

  return {
    wake,
    refresh() {
      fit();
      wake();
    },
    dispose() {
      if (frame) cancelAnimationFrame(frame);
      frame = 0;
      watch.disconnect();
      resize.disconnect();
      document.removeEventListener("visibilitychange", onVisibility);
      if (params.stir) window.removeEventListener("pointermove", onPointer);
      gl.deleteBuffer(buffer);
      gl.deleteProgram(program);
      gl.deleteShader(vertex);
      gl.deleteShader(fragment);
      lose();
    },
  };
}

// One still frame of a preset as an image (phones and reduced motion use it to fill the years of
// his path with the light, without keeping a WebGL context open). Null without WebGL.
export function snapshot(preset: LightPreset, width: number, height: number, seed = 0) {
  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  const gl = canvas.getContext("webgl", { alpha: false, preserveDrawingBuffer: true });
  if (!gl) return null;
  gl.getExtension("OES_standard_derivatives");
  const built = build(gl, PRESETS[preset], seed);
  if (!built) {
    gl.getExtension("WEBGL_lose_context")?.loseContext();
    return null;
  }
  const { uniform, lose } = built;
  gl.viewport(0, 0, width, height);
  gl.uniform2f(uniform.res, width, height);
  gl.uniform2f(uniform.size, width, height);
  gl.uniform1f(uniform.time, 11 + seed * 3.1);
  gl.uniform2f(uniform.offset, 0, 0);
  gl.uniform3f(uniform.stir, -9999, -9999, 0);
  gl.uniform1f(uniform.depth, 0);
  gl.uniform1f(uniform.fade, 1);
  gl.drawArrays(gl.TRIANGLES, 0, 3);
  const url = canvas.toDataURL("image/png");
  lose();
  return url;
}
