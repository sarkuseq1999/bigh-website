// Look B "Glass": the glass battery. One photoreal render of a glass mitochondrion (the cell's
// battery, gold inside) drawn by a fragment shader, in the manner of the homepage glass cell
// (src/components/home/science-glass.tsx). Nothing is drawn on top of the render: every effect
// changes the render's own pixels.
//
//   charge   A fill front runs along the cell from left to right. Behind it the gold is lit, warm
//            and bright; ahead of it the gold drains to pale, clear glass. At the front, a soft
//            band of warm light, its edge alive with slow noise.
//   shimmer  The lit gold's caustics drift and brighten a little. Time only moves while the
//            visitor scrolls or moves the pointer, so the glass comes to rest when they read.
//   tilt     The nearer glass shifts over the depth map (pointer and scroll).
//   light    As it charges, the battery throws a warm glow onto the paper around it.
//
// The render sits on white. The shader turns white into transparency ("color to alpha"), so the
// picture melts into whatever ground the page has, and its soft shadow (lifted to sit just under
// the glass) falls on the paper.
type Three = typeof import("three");

export type BatteryFrame = {
  charge: number;
  /** A brief brightening when a fact joins the list, 1 fading to 0. */
  pulse: number;
  time: number;
  tiltX: number;
  tiltY: number;
};

export type BatteryScene = {
  /** True on a software renderer (headless browsers): drawn at 1x. */
  software: boolean;
  render: (frame: BatteryFrame) => void;
  dispose: () => void;
};

const vertexShader = /* glsl */ `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = vec4(position, 1.0);
  }
`;

// uv runs over the 1920 x 1086 render, y up. The glass spans about x 0.19-0.81, y 0.28-0.77.
const fragmentShader = /* glsl */ `
  precision highp float;
  uniform sampler2D uImage;
  uniform sampler2D uDepth;
  uniform sampler2D uAura;
  uniform vec2 uTilt;
  uniform float uTime;
  uniform float uCharge;
  uniform float uPulse;
  varying vec2 vUv;

  float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
  }
  float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    return mix(
      mix(hash(i), hash(i + vec2(1.0, 0.0)), f.x),
      mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), f.x),
      f.y
    );
  }
  float fbm(vec2 p) {
    return 0.6 * noise(p) + 0.3 * noise(p * 2.1 + 3.7) + 0.1 * noise(p * 4.3 + 9.1);
  }

  void main() {
    // Nearer parts of the glass shift with the tilt; the ground barely moves.
    float near = texture2D(uDepth, vUv).r;
    vec2 uv = vUv + uTilt * (near - 0.2) * 0.026;
    vec3 color = texture2D(uImage, uv).rgb;
    // The render's own soft shadow floats 13% of its height under the glass; lift it to sit just
    // beneath (rows under the glass read from 8.5% lower; both edges of the seam are empty ground).
    float under = 1.0 - smoothstep(0.262, 0.272, uv.y);
    color = mix(color, texture2D(uImage, uv - vec2(0.0, 0.085)).rgb, under);
    float depth = texture2D(uDepth, uv).r;
    float body = smoothstep(0.04, 0.3, depth);
    float lum = dot(color, vec3(0.299, 0.587, 0.114));
    float warm = smoothstep(0.05, 0.3, color.r - color.b) * body;

    // Where the fill front is: along the cell, left to right, with a slow, living edge.
    float along = (uv.x - 0.19) / 0.62 - (uv.y - 0.52) * 0.16;
    float edge = (fbm(vec2(uv.y * 5.0 + 1.3, uTime * 0.22)) - 0.5) * 0.16
      + (fbm(uv * vec2(8.0, 4.0) + uTime * 0.06) - 0.5) * 0.07;
    float front = mix(-0.14, 1.16, uCharge);
    float lit = 1.0 - smoothstep(front - 0.075, front + 0.075, along + edge);
    float rim = exp(-pow((along + edge - front) / 0.05, 2.0))
      * smoothstep(0.0, 0.04, uCharge) * (1.0 - smoothstep(0.93, 1.0, uCharge));

    // Ahead of the front the gold drains to pale, clear glass (a whisper of warmth stays).
    vec3 clear = vec3(lum) * vec3(0.99, 0.985, 0.975) * 0.74 + 0.25;
    color = mix(color, clear, warm * (1.0 - lit) * 0.88);

    // Behind it the gold is lit: warmer, brighter, its caustics drifting.
    float shimmer = fbm(uv * vec2(11.0, 6.0) + vec2(uTime * 0.23, -uTime * 0.14));
    float glow = warm * lit;
    float hot = smoothstep(0.58, 0.95, lum) * glow;
    float strength = 0.45 + 0.55 * uCharge + 0.35 * uPulse;
    color *= mix(vec3(1.0), vec3(1.05, 1.0, 0.86), glow * strength);
    color += glow * (0.015 + 0.075 * shimmer) * strength * vec3(1.0, 0.76, 0.36);
    color = mix(color, vec3(1.0, 0.96, 0.84), hot * (0.08 + 0.34 * shimmer) * strength);
    // The front itself: a soft band of warm light running through the glass.
    color = mix(color, vec3(1.0, 0.86, 0.5), rim * body * (0.35 + 0.3 * warm));

    // The white ground turns pure white (it becomes transparency below)...
    float light = min(color.r, min(color.g, color.b));
    color = mix(color, vec3(1.0), smoothstep(0.9, 0.972, light) * (1.0 - body));
    // ...and, as the battery charges, warm light falls on the paper around it.
    // (uAura is a wide, soft copy of the cell's outline: where its light falls on the paper.)
    float halo = smoothstep(0.015, 0.55, texture2D(uAura, vUv).r) * (1.0 - body * 0.7);
    float breathe = 0.92 + 0.08 * sin(uTime * 0.9);
    float warmth = 0.03 + 0.44 * uCharge * uCharge + 0.16 * uPulse;
    color = mix(color, vec3(1.0, 0.82, 0.5), halo * warmth * breathe);

    // Color to alpha from white: over white this gives back the picture exactly; over the
    // page's paper it sits in the paper. Output is premultiplied.
    color = clamp(color, 0.0, 1.0);
    float alpha = 1.0 - min(color.r, min(color.g, color.b));
    gl_FragColor = vec4(color - (1.0 - alpha), alpha);
  }
`;

// The glow's shape: the depth map shrunk to 192 x 108 and blurred wide (three box passes, close to
// a Gaussian), once, so the shader reads it in one lookup.
function makeAura(THREE: Three, image: CanvasImageSource) {
  const width = 192;
  const height = 108;
  const radius = 9;
  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  const context = canvas.getContext("2d", { willReadFrequently: true });
  if (!context) return new THREE.CanvasTexture(canvas);
  context.drawImage(image, 0, 0, width, height);
  const pixels = context.getImageData(0, 0, width, height);
  let values = new Float32Array(width * height);
  for (let i = 0; i < values.length; i++) values[i] = pixels.data[i * 4] / 255;
  const pass = (source: Float32Array, horizontal: boolean) => {
    const out = new Float32Array(source.length);
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        let sum = 0;
        for (let k = -radius; k <= radius; k++) {
          const sx = horizontal ? Math.min(width - 1, Math.max(0, x + k)) : x;
          const sy = horizontal ? y : Math.min(height - 1, Math.max(0, y + k));
          sum += source[sy * width + sx];
        }
        out[y * width + x] = sum / (radius * 2 + 1);
      }
    }
    return out;
  };
  for (let i = 0; i < 3; i++) values = pass(pass(values, true), false);
  for (let i = 0; i < values.length; i++) {
    const value = Math.round(values[i] * 255);
    pixels.data.set([value, value, value, 255], i * 4);
  }
  context.putImageData(pixels, 0, 0);
  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.generateMipmaps = false;
  return texture;
}

export function createBatteryScene(
  THREE: Three,
  holder: HTMLElement,
  options: { canvasClass: string; image: string; depth: string; onReady: () => void },
): BatteryScene {
  const renderer = new THREE.WebGLRenderer({
    alpha: true,
    premultipliedAlpha: true,
    antialias: false,
    powerPreference: "high-performance",
  });
  // Headless browsers draw with SwiftShader on the CPU: keep them at 1x so QA stays quick. On a
  // real GPU, a quarter more pixels than the screen's (the battery opens about a quarter larger
  // than its docked size, look-glass.module.css --open-s), still capped at 2x.
  const gl = renderer.getContext();
  const info = gl.getExtension("WEBGL_debug_renderer_info");
  const gpu = info ? String(gl.getParameter(info.UNMASKED_RENDERER_WEBGL)) : "";
  const software = /swiftshader|llvmpipe|software|basic render/i.test(gpu);
  renderer.setPixelRatio(software ? 1 : Math.min((window.devicePixelRatio || 1) * 1.26, 2));
  renderer.setClearColor(0x000000, 0);
  const canvas = renderer.domElement;
  canvas.className = options.canvasClass;
  holder.appendChild(canvas);

  const stage = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const uniforms = {
    uImage: { value: null as import("three").Texture | null },
    uDepth: { value: null as import("three").Texture | null },
    uAura: { value: null as import("three").Texture | null },
    uTilt: { value: new THREE.Vector2() },
    uTime: { value: 0 },
    uCharge: { value: 0 },
    uPulse: { value: 0 },
  };
  const geometry = new THREE.PlaneGeometry(2, 2);
  const material = new THREE.ShaderMaterial({
    uniforms,
    vertexShader,
    fragmentShader,
    blending: THREE.NoBlending,
    depthTest: false,
    depthWrite: false,
  });
  stage.add(new THREE.Mesh(geometry, material));

  // Textures are sampled as plain sRGB bytes (no decode), so the output matches the files.
  const loader = new THREE.TextureLoader();
  const textures: import("three").Texture[] = [];
  let loaded = 0;
  let ready = false;
  let pending: BatteryFrame | null = null;
  (["uImage", "uDepth"] as const).forEach((key) =>
    loader.load(key === "uImage" ? options.image : options.depth, (texture) => {
      texture.minFilter = THREE.LinearFilter;
      texture.generateMipmaps = false;
      textures.push(texture);
      uniforms[key].value = texture;
      if (key === "uDepth") {
        uniforms.uAura.value = makeAura(THREE, texture.image as CanvasImageSource);
        textures.push(uniforms.uAura.value);
      }
      loaded += 1;
      if (loaded === 2) {
        ready = true;
        if (pending) draw(pending);
        options.onReady();
      }
    }),
  );

  function fit() {
    const width = holder.clientWidth;
    const height = holder.clientHeight;
    if (width && height) renderer.setSize(width, height, false);
  }
  fit();
  const resize = new ResizeObserver(() => {
    fit();
    if (pending) draw(pending);
  });
  resize.observe(holder);

  function draw(frame: BatteryFrame) {
    uniforms.uCharge.value = frame.charge;
    uniforms.uPulse.value = frame.pulse;
    uniforms.uTime.value = frame.time;
    uniforms.uTilt.value.set(frame.tiltX, frame.tiltY);
    renderer.render(stage, camera);
  }

  return {
    software,
    render(frame) {
      pending = frame;
      if (ready) draw(frame);
    },
    dispose() {
      resize.disconnect();
      textures.forEach((texture) => texture.dispose());
      geometry.dispose();
      material.dispose();
      renderer.dispose();
      canvas.remove();
    },
  };
}
