"use client";

import { useEffect, useRef } from "react";
import * as THREE from "three";

const MAX_DROPS = 14;
const DROP_LIFE = 3.6;

const FRAG = /* glsl */ `
  precision highp float;

  #define MAX_DROPS ${MAX_DROPS}
  #define DROP_LIFE ${DROP_LIFE.toFixed(1)}

  uniform float uTime;
  uniform vec2 uRes;
  uniform vec2 uPointer;
  uniform vec3 uDrops[MAX_DROPS]; // xy = uv position, z = birth time
  uniform vec3 uBase;
  uniform vec3 uMid;
  uniform vec3 uHigh;
  uniform vec3 uEdge;

  float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);
  }

  float noise(in vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    float a = hash(i);
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(a, b, u.x) + (c - a) * u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
  }

  float fbm(vec2 p) {
    float v = 0.0;
    float amp = 0.5;
    for (int i = 0; i < 5; i++) {
      v += amp * noise(p);
      p *= 2.03;
      amp *= 0.55;
    }
    return v;
  }

  void main() {
    vec2 uv = gl_FragCoord.xy / uRes.xy;
    float aspect = uRes.x / uRes.y;
    vec2 p = uv;
    p.x *= aspect;

    // pebble ripples: expanding rings along the cursor's path that
    // bend the silk field and leave a glacial glow
    vec2 rippleBend = vec2(0.0);
    float rippleGlow = 0.0;
    for (int i = 0; i < MAX_DROPS; i++) {
      float age = uTime - uDrops[i].z;
      if (age < 0.0 || age > DROP_LIFE) continue;
      vec2 dpos = vec2(uDrops[i].x * aspect, uDrops[i].y);
      float dd = distance(p, dpos);
      float radius = 0.03 + age * 0.13;
      float band = 1.0 - smoothstep(0.0, 0.045, abs(dd - radius));
      float energy = band * pow(1.0 - age / DROP_LIFE, 1.6) * exp(-dd * 3.5);
      vec2 dir = dd > 0.0001 ? (p - dpos) / dd : vec2(0.0);
      rippleBend += dir * energy * 0.04;
      rippleGlow += energy;
    }
    p += rippleBend;

    float t = uTime * 0.045;

    vec2 q = vec2(fbm(p * 1.4 + t), fbm(p * 1.4 - t * 0.7));
    vec2 r = vec2(
      fbm(p * 1.2 + 2.2 * q + vec2(1.7, 9.2) + 0.35 * t),
      fbm(p * 1.1 + 2.0 * q + vec2(8.3, 2.8) - 0.26 * t)
    );
    float f = fbm(p * 1.3 + 2.4 * r + uPointer * 0.22);

    vec3 base   = uBase;
    vec3 indigo = uMid;
    vec3 azure  = uHigh;
    vec3 ice    = uEdge;

    // silk gathers toward the lower right; darkness dominates elsewhere
    float zone = smoothstep(0.3, 1.08, uv.x * 0.72 + (1.0 - uv.y) * 0.5);

    vec3 col = mix(base, indigo, smoothstep(0.28, 0.68, f) * zone);
    col = mix(col, azure, smoothstep(0.46, 0.86, length(q) * f * 1.55) * zone);
    col = mix(col, ice, smoothstep(0.70, 1.0, f * f * 1.9) * 0.45 * zone);

    // calm zone: one tall dark pocket on the left where all the copy sits
    float d = length(vec2(uv.x - 0.24, (uv.y - 0.55) * 0.75));
    col = mix(col, base, smoothstep(0.64, 0.0, d) * 0.93);

    // edge vignette deepens the frame
    float edge = distance(uv, vec2(0.5, 0.5));
    col = mix(col, base * 0.6, smoothstep(0.62, 1.15, edge) * 0.6);

    // ember energy: thin orange rings that smolder and slowly fade
    vec3 emberGlow = vec3(1.0, 0.42, 0.10);
    vec3 emberCore = vec3(1.0, 0.78, 0.45);
    col += emberGlow * rippleGlow * 0.12
         + emberCore * rippleGlow * rippleGlow * 0.05;

    // film grain
    col += (hash(gl_FragCoord.xy + mod(uTime, 97.0)) * 2.0 - 1.0) * 0.02;

    gl_FragColor = vec4(col, 1.0);
  }
`;

const VERT = /* glsl */ `
  void main() {
    gl_Position = vec4(position, 1.0);
  }
`;

// Two silk moods, one shader. "navy" = the /a design-lab abyssal blue;
// "gold" = molten gold on espresso black, the literal Golden Hour read.
const PALETTES = {
  navy: {
    base: [0.016, 0.031, 0.059], // abyssal navy
    mid: [0.071, 0.149, 0.322], // deep indigo
    high: [0.165, 0.42, 0.851], // electric azure
    edge: [0.475, 0.812, 0.957], // glacial cyan edges
  },
  gold: {
    base: [0.051, 0.031, 0.014], // espresso black
    mid: [0.322, 0.165, 0.055], // deep bronze
    high: [0.851, 0.53, 0.155], // molten gold
    edge: [0.957, 0.812, 0.475], // champagne edges
  },
} as const;

export type SilkPalette = keyof typeof PALETTES;

export default function Silk({ palette = "navy" }: { palette?: SilkPalette }) {
  const mountRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) return;
    const colors = PALETTES[palette];

    const reduced = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;

    const renderer = new THREE.WebGLRenderer({ antialias: false });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(mount.clientWidth, mount.clientHeight);
    mount.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);

    const uniforms = {
      uTime: { value: 0 },
      uRes: {
        value: new THREE.Vector2(
          mount.clientWidth * renderer.getPixelRatio(),
          mount.clientHeight * renderer.getPixelRatio(),
        ),
      },
      uPointer: { value: new THREE.Vector2(0, 0) },
      uDrops: {
        value: Array.from(
          { length: MAX_DROPS },
          () => new THREE.Vector3(0, 0, -100),
        ),
      },
      uBase: { value: new THREE.Vector3(...colors.base) },
      uMid: { value: new THREE.Vector3(...colors.mid) },
      uHigh: { value: new THREE.Vector3(...colors.high) },
      uEdge: { value: new THREE.Vector3(...colors.edge) },
    };

    const quad = new THREE.Mesh(
      new THREE.PlaneGeometry(2, 2),
      new THREE.ShaderMaterial({
        fragmentShader: FRAG,
        vertexShader: VERT,
        uniforms,
      }),
    );
    scene.add(quad);

    const pointerTarget = new THREE.Vector2(0, 0);
    const lastDrop = new THREE.Vector2(-10, -10);
    let dropIdx = 0;
    const onPointer = (e: PointerEvent) => {
      pointerTarget.set(
        (e.clientX / window.innerWidth) * 2 - 1,
        (e.clientY / window.innerHeight) * 2 - 1,
      );
      if (reduced) return;
      // spawn a pebble drop every ~18px of cursor travel
      const ux = e.clientX / window.innerWidth;
      const uy = 1 - e.clientY / window.innerHeight;
      if (lastDrop.distanceTo(new THREE.Vector2(ux, uy)) > 0.016) {
        lastDrop.set(ux, uy);
        uniforms.uDrops.value[dropIdx].set(ux, uy, clock.getElapsedTime());
        dropIdx = (dropIdx + 1) % MAX_DROPS;
      }
    };
    window.addEventListener("pointermove", onPointer);

    const onResize = () => {
      renderer.setSize(mount.clientWidth, mount.clientHeight);
      uniforms.uRes.value.set(
        mount.clientWidth * renderer.getPixelRatio(),
        mount.clientHeight * renderer.getPixelRatio(),
      );
      if (reduced) renderer.render(scene, camera);
    };
    window.addEventListener("resize", onResize);

    const clock = new THREE.Clock();
    let raf = 0;
    const tick = () => {
      uniforms.uTime.value = clock.getElapsedTime();
      uniforms.uPointer.value.lerp(pointerTarget, 0.04);
      renderer.render(scene, camera);
      raf = requestAnimationFrame(tick);
    };

    if (reduced) {
      uniforms.uTime.value = 8;
      renderer.render(scene, camera);
    } else {
      raf = requestAnimationFrame(tick);
    }

    const onVisibility = () => {
      if (reduced) return;
      if (document.hidden) {
        cancelAnimationFrame(raf);
      } else {
        clock.start();
        raf = requestAnimationFrame(tick);
      }
    };
    document.addEventListener("visibilitychange", onVisibility);

    return () => {
      cancelAnimationFrame(raf);
      document.removeEventListener("visibilitychange", onVisibility);
      window.removeEventListener("resize", onResize);
      window.removeEventListener("pointermove", onPointer);
      quad.geometry.dispose();
      (quad.material as THREE.Material).dispose();
      renderer.dispose();
      mount.removeChild(renderer.domElement);
    };
  }, [palette]);

  return (
    <div
      ref={mountRef}
      aria-hidden
      className="absolute inset-0 h-full w-full"
    />
  );
}
