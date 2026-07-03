"use client";

import { useLayoutEffect, useRef } from "react";
import * as THREE from "three";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

// Screen 2 · THE LIGHT BREAK — after the dusk-silk hero, the honest truth
// is told in daylight. The data IS the picture: 100 motes of light are the
// body's energy budget; on scroll, 20 ignite ember and gather — the brain's
// fifth. The stats are the legend of that picture, not a metric grid.

const DATA_MOTES = 100; // the honest number — 100 units of energy
const BRAIN_MOTES = 20; // the brain's share ignites
const DUST = 240; // atmosphere only, never ignites

const VERT = /* glsl */ `
  attribute float aBrain;
  attribute float aDust;
  attribute float aSeed;
  attribute vec3 aCluster;
  uniform float uTime;
  uniform float uProgress;
  uniform float uPx;
  varying float vBrain;
  varying float vDust;
  varying float vSeed;
  varying float vIgnite;

  void main() {
    // each brain mote ignites on its own beat as progress sweeps 0 → 1
    float ignite = smoothstep(aSeed * 0.45, aSeed * 0.45 + 0.55, uProgress) * aBrain;
    vec3 pos = mix(position, aCluster, ignite);

    float t = uTime * (0.22 + aSeed * 0.3) + aSeed * 43.0;
    float drift = mix(0.17, 0.06, ignite) * (1.0 - aDust * 0.4);
    pos += vec3(sin(t * 0.9), cos(t * 0.72), sin(t * 1.31)) * drift;

    vec4 mv = modelViewMatrix * vec4(pos, 1.0);
    float size = mix(11.0, 17.0, aSeed) * (1.0 - aDust * 0.74);
    size *= 1.0 + ignite * 1.6; // room for the warm halo
    gl_PointSize = size * uPx * (10.0 / -mv.z);
    gl_Position = projectionMatrix * mv;

    vBrain = aBrain;
    vDust = aDust;
    vSeed = aSeed;
    vIgnite = ignite;
  }
`;

const FRAG = /* glsl */ `
  precision highp float;
  uniform vec3 uInk;
  uniform vec3 uEmberA;
  uniform vec3 uEmberB;
  varying float vBrain;
  varying float vDust;
  varying float vSeed;
  varying float vIgnite;

  void main() {
    vec2 c = gl_PointCoord - 0.5;
    float d = length(c);
    if (d > 0.5) discard;
    // soft pollen-in-light discs; ignited motes get a bright core + warm halo
    float soft = smoothstep(0.5, 0.12, d);
    float core = smoothstep(0.2, 0.02, d);
    vec3 ember = mix(uEmberA, uEmberB, vSeed);
    vec3 col = mix(uInk, ember, vIgnite);
    float restAlpha = soft * mix(0.3, 0.15, vDust);
    float igniteAlpha = core * 0.95 + soft * 0.38;
    float alpha = mix(restAlpha, igniteAlpha, vIgnite);
    gl_FragColor = vec4(col, alpha);
  }
`;

function buildGeometry() {
  const total = DATA_MOTES + DUST;
  const position = new Float32Array(total * 3);
  const cluster = new Float32Array(total * 3);
  const brain = new Float32Array(total);
  const dust = new Float32Array(total);
  const seed = new Float32Array(total);

  // loose ellipsoid the full width of the stage, weighted right of center
  const field = (i: number, arr: Float32Array, rx: number, ry: number, rz: number) => {
    arr[i * 3] = 0.7 + (Math.random() * 2 - 1) * rx;
    arr[i * 3 + 1] = (Math.random() * 2 - 1) * ry;
    arr[i * 3 + 2] = (Math.random() * 2 - 1) * rz;
  };

  for (let i = 0; i < total; i++) {
    const isData = i < DATA_MOTES;
    const isBrain = i < BRAIN_MOTES;
    field(i, position, isData ? 4.6 : 5.4, isData ? 2.3 : 2.9, 1.6);
    if (isBrain) {
      // the constellation the brain-fifth gathers into — upper right
      cluster[i * 3] = 2.6 + (Math.random() * 2 - 1) * 0.72;
      cluster[i * 3 + 1] = 0.55 + (Math.random() * 2 - 1) * 0.55;
      cluster[i * 3 + 2] = (Math.random() * 2 - 1) * 0.4;
    } else {
      cluster[i * 3] = position[i * 3];
      cluster[i * 3 + 1] = position[i * 3 + 1];
      cluster[i * 3 + 2] = position[i * 3 + 2];
    }
    brain[i] = isBrain ? 1 : 0;
    dust[i] = isData ? 0 : 1;
    seed[i] = Math.random();
  }

  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.BufferAttribute(position, 3));
  geo.setAttribute("aCluster", new THREE.BufferAttribute(cluster, 3));
  geo.setAttribute("aBrain", new THREE.BufferAttribute(brain, 1));
  geo.setAttribute("aDust", new THREE.BufferAttribute(dust, 1));
  geo.setAttribute("aSeed", new THREE.BufferAttribute(seed, 1));
  return geo;
}

export function Truth({
  kicker,
  body,
  stat1,
  stat2,
}: {
  kicker: string;
  body: string;
  stat1: string;
  stat2: string;
}) {
  const section = useRef<HTMLElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  const n1 = useRef<HTMLSpanElement>(null);
  const n2 = useRef<HTMLSpanElement>(null);

  useLayoutEffect(() => {
    const el = section.current;
    const cv = canvas.current;
    if (!el || !cv) return;

    const reduced = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;

    // ── three.js stage ──
    const renderer = new THREE.WebGLRenderer({
      canvas: cv,
      alpha: true,
      antialias: true,
    });
    renderer.setClearColor(0x000000, 0);
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 40);
    camera.position.set(0, 0, 9);

    const geo = buildGeometry();
    const mat = new THREE.ShaderMaterial({
      vertexShader: VERT,
      fragmentShader: FRAG,
      transparent: true,
      depthWrite: false,
      uniforms: {
        uTime: { value: 0 },
        uProgress: { value: reduced ? 1 : 0 },
        uPx: { value: Math.min(window.devicePixelRatio, 2) },
        uInk: { value: new THREE.Color("#2b4a66") },
        uEmberA: { value: new THREE.Color("#d97742") },
        uEmberB: { value: new THREE.Color("#a84e1e") },
      },
    });
    const points = new THREE.Points(geo, mat);
    const group = new THREE.Group();
    group.add(points);

    // warmth pooling behind the gathered fifth — one soft ember wash
    const glowCanvas = document.createElement("canvas");
    glowCanvas.width = glowCanvas.height = 256;
    const gctx = glowCanvas.getContext("2d")!;
    const grad = gctx.createRadialGradient(128, 128, 0, 128, 128, 128);
    grad.addColorStop(0, "rgba(217, 119, 66, 0.55)");
    grad.addColorStop(0.5, "rgba(217, 119, 66, 0.16)");
    grad.addColorStop(1, "rgba(217, 119, 66, 0)");
    gctx.fillStyle = grad;
    gctx.fillRect(0, 0, 256, 256);
    const glowMat = new THREE.SpriteMaterial({
      map: new THREE.CanvasTexture(glowCanvas),
      transparent: true,
      opacity: 0,
      depthWrite: false,
    });
    const glow = new THREE.Sprite(glowMat);
    glow.position.set(2.6, 0.55, -0.6);
    glow.scale.setScalar(3.9);
    group.add(glow);
    scene.add(group);

    const resize = () => {
      const w = el.clientWidth;
      const h = el.clientHeight;
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.setSize(w, h, false);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      // narrow screens: sink the field into the lower half, under the copy
      const narrow = w < 768;
      group.position.set(narrow ? -0.7 : 0, narrow ? -1.15 : -0.1, 0);
      group.scale.setScalar(narrow ? 0.72 : 1);
    };
    resize();
    const ro = new ResizeObserver(resize);
    ro.observe(el);

    // gentle pointer parallax (desktop only, cheap)
    const pointer = { x: 0, y: 0 };
    const onPointer = (e: PointerEvent) => {
      pointer.x = (e.clientX / window.innerWidth - 0.5) * 0.5;
      pointer.y = (e.clientY / window.innerHeight - 0.5) * 0.3;
    };
    if (!reduced) window.addEventListener("pointermove", onPointer);

    const clock = new THREE.Clock();
    let raf = 0;
    const renderFrame = () => {
      mat.uniforms.uTime.value = clock.getElapsedTime();
      camera.position.x += (pointer.x - camera.position.x) * 0.04;
      camera.position.y += (-pointer.y - camera.position.y) * 0.04;
      camera.lookAt(0.6, 0, 0);
      renderer.render(scene, camera);
      raf = requestAnimationFrame(renderFrame);
    };

    if (reduced) {
      // static final state: one honest frame, no loop
      renderer.render(scene, camera);
    } else {
      raf = requestAnimationFrame(renderFrame);
    }

    // ── choreography ──
    const state = { p: 0 };
    const applyProgress = (p: number) => {
      mat.uniforms.uProgress.value = p;
      glowMat.opacity = p * p * 0.7;
      // 2% is a static fact — resolve it early; 20% tracks the ignition
      if (n1.current)
        n1.current.textContent = `${Math.round(Math.min(p * 4, 1) * 2)}%`;
      if (n2.current) n2.current.textContent = `${Math.round(p * 20)}%`;
    };

    const mm = gsap.matchMedia();

    mm.add(
      "(min-width: 768px) and (prefers-reduced-motion: no-preference)",
      () => {
        applyProgress(0);
        const tl = gsap.timeline({
          scrollTrigger: {
            trigger: el,
            start: "top top",
            end: "+=130%",
            pin: true,
            scrub: 0.6,
          },
        });
        tl.to(state, {
          p: 1,
          ease: "none",
          onUpdate: () => applyProgress(state.p),
        });
      },
    );

    mm.add(
      "(max-width: 767px) and (prefers-reduced-motion: no-preference)",
      () => {
        applyProgress(0);
        gsap.to(state, {
          p: 1,
          duration: 2.2,
          ease: "power2.inOut",
          onUpdate: () => applyProgress(state.p),
          scrollTrigger: { trigger: el, start: "top 55%", once: true },
        });
      },
    );

    mm.add("(prefers-reduced-motion: no-preference)", () => {
      gsap.from(el.querySelectorAll("[data-rise]"), {
        y: 36,
        autoAlpha: 0,
        duration: 1.15,
        ease: "power4.out",
        stagger: 0.12,
        scrollTrigger: { trigger: el, start: "top 72%", once: true },
      });
    });

    return () => {
      mm.revert();
      ro.disconnect();
      window.removeEventListener("pointermove", onPointer);
      cancelAnimationFrame(raf);
      geo.dispose();
      mat.dispose();
      glowMat.map?.dispose();
      glowMat.dispose();
      renderer.dispose();
    };
  }, []);

  return (
    <section
      ref={section}
      id="truth"
      className="ghl relative min-h-svh overflow-hidden"
    >
      <canvas
        ref={canvas}
        aria-hidden
        className="absolute inset-0 h-full w-full"
      />

      <div className="relative z-10 flex min-h-svh flex-col justify-between px-6 pb-12 pt-24 sm:px-12 sm:pb-16 sm:pt-32">
        <div className="max-w-3xl">
          <p
            data-rise
            className="font-mono text-[12px] uppercase tracking-[0.24em] text-[color:var(--ghl-ember)]"
          >
            {kicker}
          </p>
          <p
            data-rise
            className="gh-serif mt-7 text-[clamp(1.7rem,3.3vw,2.7rem)] leading-[1.32] [text-wrap:pretty]"
          >
            {body}
          </p>
        </div>

        {/* the legend of the picture: each label names what the motes show */}
        <div className="flex flex-col gap-9 sm:flex-row sm:items-end sm:justify-between">
          <div data-rise className="max-w-[21rem]">
            <p className="gh-serif text-[clamp(2.6rem,5vw,4rem)] leading-none [font-variant-numeric:tabular-nums]">
              <span ref={n1}>2%</span>
            </p>
            <p className="mt-3 text-[15px] leading-relaxed text-[color:var(--ghl-muted)]">
              {stat1}
            </p>
          </div>
          <div data-rise className="max-w-[21rem] sm:text-right">
            <p className="gh-serif flex items-baseline gap-3 text-[clamp(2.6rem,5vw,4rem)] leading-none text-[color:var(--ghl-ember)] [font-variant-numeric:tabular-nums] sm:justify-end">
              <span
                aria-hidden
                className="inline-block h-2.5 w-2.5 shrink-0 self-center rounded-full bg-[#d97742]"
              />
              <span ref={n2}>20%</span>
            </p>
            <p className="mt-3 text-[15px] leading-relaxed text-[color:var(--ghl-muted)]">
              {stat2}
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
