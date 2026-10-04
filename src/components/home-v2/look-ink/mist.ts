"use client";

import { useEffect, type RefObject } from "react";

// Living mist for the opening's mountains. The landscape is one ink painting; here it is drawn
// again on a canvas with slow banks of mist drifting through it. Mist in an ink painting is bare
// paper, so the mist only ever takes ink away: the far, pale ridges dissolve and return while the
// near, dark pines hold. The canvas takes the painting's place once it has bloomed (same pixels,
// same box, same multiply), then the mist rises over one breath. Without WebGL, on a software
// renderer, or with reduced motion, the still painting simply stays.

const VERTEX = `
attribute vec2 aPosition;
varying vec2 vUv;
void main() {
  vUv = aPosition * 0.5 + 0.5;
  gl_Position = vec4(aPosition, 0.0, 1.0);
}`;

const FRAGMENT = `
precision highp float;
uniform sampler2D uPainting;
uniform float uTime;
uniform float uMist;
uniform float uAspect;
varying vec2 vUv;

float hash(vec2 p) {
  p = fract(p * vec2(123.34, 456.21));
  p += dot(p, p + 45.32);
  return fract(p.x * p.y);
}

float noise(vec2 p) {
  vec2 i = floor(p);
  vec2 f = fract(p);
  vec2 u = f * f * (3.0 - 2.0 * f);
  return mix(
    mix(hash(i), hash(i + vec2(1.0, 0.0)), u.x),
    mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x),
    u.y
  );
}

float fbm(vec2 p) {
  float sum = 0.0;
  float amp = 0.5;
  for (int i = 0; i < 4; i++) {
    sum += amp * noise(p);
    p = p * 2.03 + 17.1;
    amp *= 0.5;
  }
  return sum;
}

void main() {
  vec3 painting = texture2D(uPainting, vUv).rgb;
  float ink = 1.0 - dot(painting, vec3(0.299, 0.587, 0.114));
  vec2 p = vec2(vUv.x * uAspect, vUv.y);
  // Two banks of low cloud, long and flat, crossing at their own slow pace.
  float low = fbm(vec2(p.x * 1.5 - uTime * 0.034, p.y * 4.2 + uTime * 0.005));
  float high = fbm(vec2(p.x * 3.1 + uTime * 0.019, p.y * 7.6 - uTime * 0.007) + 31.7);
  float mist = smoothstep(0.36, 0.66, low * 0.7 + high * 0.3);
  // Far ridges are pale washes and dissolve; near pines are dense ink and hold.
  float far = 1.0 - smoothstep(0.42, 0.9, ink);
  gl_FragColor = vec4(mix(painting, vec3(1.0), mist * far * uMist), 1.0);
}`;

function compile(gl: WebGLRenderingContext, type: number, source: string) {
  const shader = gl.createShader(type);
  if (!shader) return null;
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  return gl.getShaderParameter(shader, gl.COMPILE_STATUS) ? shader : null;
}

/**
 * Draws `painting` with drifting mist on `canvas` (which shares the painting's box and classes).
 * `host` gets data-mist="on" once the canvas has taken over, so CSS can hide the still.
 */
export function useMist(
  host: RefObject<HTMLElement | null>,
  painting: RefObject<HTMLImageElement | null>,
  canvas: RefObject<HTMLCanvasElement | null>,
  motion: boolean,
) {
  useEffect(() => {
    const root = host.current;
    const image = painting.current;
    const surface = canvas.current;
    if (!root || !image || !surface || !motion) return;

    const gl = surface.getContext("webgl", { alpha: false, antialias: false, depth: false });
    if (!gl) return;
    const info = gl.getExtension("WEBGL_debug_renderer_info");
    const renderer = info ? String(gl.getParameter(info.UNMASKED_RENDERER_WEBGL)) : "";
    if (/swiftshader|llvmpipe|software/i.test(renderer)) return;

    const vertex = compile(gl, gl.VERTEX_SHADER, VERTEX);
    const fragment = compile(gl, gl.FRAGMENT_SHADER, FRAGMENT);
    const program = gl.createProgram();
    if (!vertex || !fragment || !program) return;
    gl.attachShader(program, vertex);
    gl.attachShader(program, fragment);
    gl.linkProgram(program);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) return;
    gl.useProgram(program);

    const quad = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, quad);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    const position = gl.getAttribLocation(program, "aPosition");
    gl.enableVertexAttribArray(position);
    gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 0, 0);
    const uTime = gl.getUniformLocation(program, "uTime");
    const uMist = gl.getUniformLocation(program, "uMist");
    const uAspect = gl.getUniformLocation(program, "uAspect");

    let raf = 0;
    let live = false;
    let visible = true;
    let lost = false;
    let began = 0;
    const aspect = image.naturalWidth / Math.max(1, image.naturalHeight) || 2400 / 1029;

    /** The canvas holds the whole painting at the size it is shown (object-fit crops it). */
    const resize = () => {
      const box = image.getBoundingClientRect();
      const dpr = Math.min(1.5, window.devicePixelRatio || 1);
      const width = Math.min(2400, Math.ceil(Math.max(box.width, box.height * aspect) * dpr));
      const height = Math.round(width / aspect);
      if (surface.width === width && surface.height === height) return;
      surface.width = width;
      surface.height = height;
      gl.viewport(0, 0, width, height);
    };

    const start = () => {
      if (live || lost || !image.complete || !image.naturalWidth) return;
      const texture = gl.createTexture();
      gl.bindTexture(gl.TEXTURE_2D, texture);
      gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, 1);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      try {
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, image);
      } catch {
        return;
      }
      gl.uniform1f(uAspect, aspect);
      resize();
      live = true;
      began = performance.now();
      frame(began);
      // Same pixels as the still for the first frame, so the hand-over cannot be seen.
      root.setAttribute("data-mist", "on");
    };

    const frame = (now: number) => {
      raf = 0;
      if (!live || lost) return;
      const seconds = (now - began) / 1000;
      const rise = Math.min(1, seconds / 4.8);
      gl.uniform1f(uTime, seconds);
      gl.uniform1f(uMist, 0.94 * rise * rise * (3 - 2 * rise));
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      if (visible && !document.hidden) raf = requestAnimationFrame(frame);
    };
    const wake = () => {
      if (live && !raf && visible && !document.hidden) raf = requestAnimationFrame(frame);
    };

    // Wait for the painting's ink bloom to finish, then take its place.
    const bloomed = () => image.dataset.bloom === "done" || image.dataset.bloom === undefined;
    const watcher = new MutationObserver(() => bloomed() && start());
    watcher.observe(image, { attributes: true, attributeFilter: ["data-bloom"] });
    const onLoad = () => bloomed() && start();
    image.addEventListener("load", onLoad);
    if (bloomed()) start();

    const sight = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      wake();
    });
    sight.observe(surface);
    const sizes = new ResizeObserver(() => {
      if (!live) return;
      resize();
      if (!raf) frame(performance.now());
    });
    sizes.observe(image);
    const onLost = (event: Event) => {
      event.preventDefault();
      lost = true;
      root.removeAttribute("data-mist");
    };
    surface.addEventListener("webglcontextlost", onLost);
    document.addEventListener("visibilitychange", wake);

    return () => {
      cancelAnimationFrame(raf);
      watcher.disconnect();
      sight.disconnect();
      sizes.disconnect();
      image.removeEventListener("load", onLoad);
      surface.removeEventListener("webglcontextlost", onLost);
      document.removeEventListener("visibilitychange", wake);
      root.removeAttribute("data-mist");
    };
  }, [host, painting, canvas, motion]);
}
