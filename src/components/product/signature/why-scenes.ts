// The "why" chapter's scenes (October 2, 2026; Turmerific first): one photo per line of the story,
// handed over with a liquid wash in WebGL instead of a plain cross-fade (Mo: the same picture under
// every line "doesn't look that interesting"; Timeline's How it works, Design Vault #019-#029, changes
// its picture as you scroll). Everything happens to the photos' own pixels (Mo, September 2026: never
// paste flat shapes on a photo): the next photo spreads out from the subject along a soft, noisy
// front, the pixels near the front ripple like liquid, and the gold in them brightens as it passes.
// Between hand-overs the liquid scenes keep a faint living ripple.
//
// The canvas lies exactly over the chapter's photos (same frame, same mask). The photos are drawn
// as their raw sRGB values, untouched, so the canvas matches the <img> beneath it pixel for pixel.

import type * as T from "three";
import { createLoop } from "./rigs";

export type WhyScenes = {
  /** 0 = the first scene; 1.5 = halfway from the second to the third. */
  setProgress(progress: number): void;
  dispose(): void;
};

const vertex = /* glsl */ `
varying vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = vec4(position.xy, 0.0, 1.0);
}
`;

const fragment = /* glsl */ `
precision highp float;
varying vec2 vUv;
uniform sampler2D uFrom;
uniform sampler2D uTo;
uniform float uMix;      // 0..1 through one hand-over
uniform float uTime;     // seconds
uniform float uAspect;   // photo width / height
uniform vec2 uFocus;     // the subject, in uv
uniform float uRipple;   // living ripple of the scene on screen (0 for still scenes)

float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float noise(vec2 p) {
  vec2 i = floor(p), f = fract(p);
  vec2 u = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), u.x),
             mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x), u.y);
}
float fbm(vec2 p) {
  float v = 0.0, a = 0.5;
  for (int k = 0; k < 3; k++) { v += a * noise(p); p *= 2.03; a *= 0.5; }
  return v;
}

void main() {
  vec2 uv = vUv;
  float t = uTime;
  // A slow field of liquid motion, in the photo's own proportions.
  vec2 q = uv * vec2(uAspect, 1.0) * 3.2;
  vec2 flow = vec2(fbm(q + vec2(t * 0.06, 0.0)), fbm(q + vec2(5.2, 1.3) - vec2(0.0, t * 0.05))) - 0.5;

  // The front: a ring spreading from the subject, its edge broken up by the same liquid noise.
  vec2 d = (uv - uFocus) * vec2(uAspect, 1.0);
  float wobble = (fbm(q * 1.4 + vec2(t * 0.15, -t * 0.1)) - 0.5) * 0.42;
  float r = length(d) + wobble;
  float front = uMix * 1.85 - 0.12;
  float shown = 1.0 - smoothstep(front - 0.16, front + 0.02, r);
  float moving = step(0.0005, uMix) * step(uMix, 0.9995);
  float band = moving * (1.0 - smoothstep(0.0, 0.14, abs(r - front + 0.07)));

  // Pixels near the front ripple; the scene on screen keeps a faint ripple of its own.
  vec2 warp = flow * (0.028 * band + uRipple);
  vec3 a = texture2D(uFrom, uv + warp * (1.0 - shown)).rgb;
  vec3 b = texture2D(uTo, uv - warp * shown).rgb;
  vec3 colour = mix(a, b, shown);
  // The gold already in the photo brightens as the front passes: light, not a drawn line.
  float warm = clamp((colour.r - colour.b) * 2.2, 0.0, 1.0);
  colour += colour * band * warm * 0.55;
  gl_FragColor = vec4(colour, 1.0);
}
`;

/**
 * Build the scenes on `canvas`. `ripples` gives each photo's living ripple (0 for still ones).
 * Calls `onReady` once every photo is on the GPU and the first frame is drawn.
 */
export async function createWhyScenes(
  canvas: HTMLCanvasElement,
  sources: string[],
  ripples: number[],
  focus: [number, number],
  onReady: () => void,
): Promise<WhyScenes> {
  const three = await import("three");
  const renderer = new three.WebGLRenderer({
    canvas,
    antialias: false,
    alpha: false,
    powerPreference: "high-performance",
  });
  // Raw values in, raw values out: no colour conversion, no tone mapping.
  renderer.outputColorSpace = three.LinearSRGBColorSpace;
  renderer.toneMapping = three.NoToneMapping;

  // Each photo once (a scene may come back), and no bigger than the screen can show: four 2752px
  // photos with their mipmaps are about 90 MB of GPU memory, too much for a phone. A copy a little
  // wider than the canvas (the frame's slow push-in enlarges it 6%) looks the same.
  const needed = Math.ceil(
    (canvas.clientWidth || canvas.getBoundingClientRect().width || 1600) *
      Math.min(window.devicePixelRatio || 1, 1.5) *
      1.1,
  );
  const load = (source: string) =>
    new Promise<T.Texture>((resolve, reject) => {
      const image = new window.Image();
      image.decoding = "async";
      image.onload = () => {
        let texture: T.Texture;
        if (image.naturalWidth > needed) {
          const copy = document.createElement("canvas");
          copy.width = needed;
          copy.height = Math.round((image.naturalHeight * needed) / image.naturalWidth);
          const context = copy.getContext("2d");
          if (!context) return reject(new Error("no 2d context"));
          context.imageSmoothingQuality = "high";
          context.drawImage(image, 0, 0, copy.width, copy.height);
          texture = new three.CanvasTexture(copy);
        } else {
          texture = new three.Texture(image);
          texture.needsUpdate = true;
        }
        texture.colorSpace = three.NoColorSpace;
        texture.minFilter = three.LinearMipmapLinearFilter;
        texture.magFilter = three.LinearFilter;
        resolve(texture);
      };
      image.onerror = reject;
      image.src = source;
    });
  const unique = [...new Set(sources)];
  const loaded = await Promise.all(unique.map(load));
  const textures = sources.map((source) => loaded[unique.indexOf(source)]);
  const firstImage = textures[0].image as HTMLImageElement | HTMLCanvasElement;
  const first =
    firstImage instanceof HTMLImageElement
      ? { width: firstImage.naturalWidth, height: firstImage.naturalHeight }
      : { width: firstImage.width, height: firstImage.height };
  const uniforms = {
    uFrom: { value: textures[0] },
    uTo: { value: textures[Math.min(1, textures.length - 1)] },
    uMix: { value: 0 },
    uTime: { value: 0 },
    uAspect: { value: first.width / first.height },
    uFocus: { value: new three.Vector2(focus[0], 1 - focus[1]) },
    uRipple: { value: ripples[0] ?? 0 },
  };
  const material = new three.ShaderMaterial({
    vertexShader: vertex,
    fragmentShader: fragment,
    uniforms,
    depthTest: false,
    depthWrite: false,
    toneMapped: false,
  });
  const quad = new three.Mesh(new three.PlaneGeometry(2, 2), material);
  const scene = new three.Scene();
  scene.add(quad);
  const camera = new three.Camera();

  // The canvas follows its frame; a software renderer (no GPU) draws at 1x.
  const resize = () => {
    const box = canvas.getBoundingClientRect();
    const width = canvas.clientWidth || box.width;
    const height = canvas.clientHeight || box.height;
    if (!width || !height) return;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
    renderer.setSize(width, height, false);
    dirty = true;
  };
  let dirty = true;
  let progress = 0;
  const apply = () => {
    const last = textures.length - 1;
    const p = Math.min(last, Math.max(0, progress));
    const index = Math.min(last - 1, Math.floor(p));
    const local = p - index;
    uniforms.uFrom.value = textures[Math.max(0, index)];
    uniforms.uTo.value = textures[Math.min(last, index + 1)];
    uniforms.uMix.value = last === 0 ? 0 : local;
    // The ripple of whichever scene holds the screen.
    const holding = local < 0.5 ? index : index + 1;
    uniforms.uRipple.value = ripples[holding] ?? 0;
  };
  const sizer = new ResizeObserver(resize);
  sizer.observe(canvas);
  resize();
  apply();
  renderer.render(scene, camera);
  onReady();

  const started = performance.now();
  const loop = createLoop(canvas, (now) => {
    // Still scenes only redraw when the scroll moves them; liquid ones always ripple a little.
    if (!dirty && uniforms.uRipple.value === 0 && uniforms.uMix.value === 0) return;
    uniforms.uTime.value = (now - started) / 1000;
    renderer.render(scene, camera);
    dirty = false;
  });

  return {
    setProgress(value: number) {
      if (value === progress) return;
      progress = value;
      apply();
      dirty = true;
    },
    dispose() {
      loop.dispose();
      sizer.disconnect();
      loaded.forEach((texture) => texture.dispose());
      material.dispose();
      quad.geometry.dispose();
      renderer.dispose();
    },
  };
}
