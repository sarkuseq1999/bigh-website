"use client";

import Image from "next/image";
import gsap from "gsap";
import { MotionPathPlugin } from "gsap/MotionPathPlugin";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { ArrowDown, ArrowUpRight } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { useCopy } from "@/i18n/use-copy";
import { articles, facts, images, intro, type ScienceDesignProps } from "./science-data";
import styles from "./science-glass.module.css";
import { useReducedMotion } from "./use-reduced-motion";

// Glass cell (Mo's pick, after Timeline's "cellular batteries" page): one mitochondrion rendered as
// warm-gold glass stays centered while three topics scroll past. Tabs at the top always show the
// topic, and each topic has its own picture:
//   1 Mitochondria — energy flows out of the glass, like power from a power plant.
//   2 Free radicals — a short scene drawn inside the glass by the shader, so it shares the render's
//     light: making energy throws off a few embers; one reaches the wall and leaves a burn; lime
//     antioxidant droplets (a second render) meet the others before they can do the same.
//   3 Aging cells — an age slider (drag it, or sweep the mouse over it) runs from 20 to 80 and
//     turns the young render into an aged render of the same cell, patch by patch, while the
//     energy flowing out slows and dims.
// Without WebGL, or with reduced motion, the still render and all text remain.
type Three = typeof import("three");
type Point = { x: number; y: number };
type Ember = Point & { size: number; heat: number };
type Drop = Point & { size: number; alpha: number };
type Pulse = Point & { radius: number; alpha: number };
type Stain = Point & { radius: number; strength: number };
type Scene = { embers: Ember[]; drops: Drop[]; pulses: Pulse[]; stain: Stain };
type Cell = {
  scene: Scene;
  setGlow: (value: number) => void;
  setAge: (value: number) => void;
  dispose: () => void;
};

const EMBERS = 6;
const DROPS = 3;

const vertexShader = /* glsl */ `
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = vec4(position, 1.0);
  }
`;

// Everything is drawn in the render's own coordinates (uv, y up). Distances are measured in
// height units, so ASPECT keeps circles round on the 1000 x 566 picture.
const fragmentShader = /* glsl */ `
  precision highp float;
  uniform sampler2D uImage;
  uniform sampler2D uOld;
  uniform sampler2D uDepth;
  uniform sampler2D uDrop;
  uniform vec2 uTilt;
  uniform float uTime;
  uniform float uGlow;
  uniform float uAge;
  uniform vec4 uEmbers[${EMBERS}];
  uniform vec4 uDrops[${DROPS}];
  uniform vec4 uPulses[${DROPS}];
  uniform vec4 uStain;
  varying vec2 vUv;
  const vec2 ASPECT = vec2(1.767, 1.0);

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
    float depth = texture2D(uDepth, vUv).r;
    // Nearer parts of the glass shift with the tilt; the white ground barely moves.
    vec2 uv = vUv + uTilt * (depth - 0.2) * 0.03;
    // Each ember warms the glass around it, so the picture wavers a little there.
    for (int i = 0; i < ${EMBERS}; i++) {
      vec4 e = uEmbers[i];
      if (e.w <= 0.0) continue;
      vec2 d = (uv - e.xy) * ASPECT;
      float halo = exp(-dot(d, d) / (e.z * e.z * 5.0));
      uv += normalize(d + 1e-5) * halo * e.w * 0.003 * sin(uTime * 7.0 + float(i));
    }
    vec4 young = texture2D(uImage, uv);
    vec4 old = texture2D(uOld, uv);
    // Age runs in a straight line from the young render to the old one, each patch of the glass
    // a little ahead or behind, so every year changes something and nothing is old before 80.
    float lag = (fbm(uv * vec2(4.0, 2.2)) - 0.5) * 0.24;
    float turn = clamp(uAge * 1.24 - 0.12 + lag, 0.0, 1.0);
    vec4 color = mix(young, old, turn);

    // The golden folds breathe: warm, saturated pixels glow a little brighter on a slow cycle.
    float warm = smoothstep(0.08, 0.36, color.r - color.b);
    float breath = 0.5 + 0.5 * sin(uTime * 1.25);
    float life = 1.0 - 0.9 * uAge;
    color.rgb = mix(color.rgb, color.rgb * vec3(1.04, 0.98, 0.86), warm * (0.1 + 0.16 * breath) * uGlow * life);
    color.rgb += warm * (0.015 + 0.045 * breath) * uGlow * life * vec3(1.0, 0.78, 0.4);
    // With age the last of the gold softens toward a quiet grey (an illustration, not a measurement).
    float grey = dot(color.rgb, vec3(0.299, 0.587, 0.114));
    color.rgb = mix(color.rgb, vec3(grey) * vec3(0.97, 0.99, 1.03) + 0.05, warm * uAge * 0.3);
    // The last stretch, 60 to 80: the whole cell dims and cools a little further.
    float inside = 1.0 - smoothstep(0.86, 0.97, min(color.r, min(color.g, color.b)));
    float decline = smoothstep(0.6, 1.0, uAge);
    color.rgb = mix(color.rgb, color.rgb * vec3(0.84, 0.84, 0.86), decline * inside * 0.4);

    // A burn inside the glass: dark, smoky, with a ragged edge.
    if (uStain.w > 0.0) {
      vec2 d = (uv - uStain.xy) * ASPECT;
      float edge = uStain.z * (0.7 + 0.6 * fbm(uv * 60.0));
      float mark = uStain.w * (1.0 - smoothstep(edge * 0.3, edge, length(d)));
      vec3 burnt = mix(vec3(grey), color.rgb, 0.4) * vec3(0.62, 0.42, 0.27);
      color.rgb = mix(color.rgb, burnt, mark);
    }
    // Embers: a hot pale core inside a warm amber bloom, flickering.
    for (int i = 0; i < ${EMBERS}; i++) {
      vec4 e = uEmbers[i];
      if (e.w <= 0.0) continue;
      vec2 d = (uv - e.xy) * ASPECT;
      float r2 = dot(d, d);
      float r = sqrt(r2);
      float flicker = e.w * (0.86 + 0.14 * sin(uTime * 11.0 + float(i) * 1.7));
      float halo = exp(-r2 / (e.z * e.z * 4.0)) * flicker;
      float rim = exp(-pow((r - e.z * 0.9) / (e.z * 0.45), 2.0)) * flicker;
      float core = exp(-r2 / (e.z * e.z * 0.3)) * flicker;
      color.rgb = mix(color.rgb, color.rgb * vec3(1.0, 0.7, 0.3), min(halo * 0.7, 1.0));
      color.rgb = mix(color.rgb, vec3(1.0, 0.5, 0.1), min(rim * 0.85, 1.0));
      color.rgb = mix(color.rgb, vec3(1.0, 0.99, 0.93), min(core, 1.0));
    }
    // A soft lime ring where an ember was caught.
    for (int i = 0; i < ${DROPS}; i++) {
      vec4 q = uPulses[i];
      if (q.w <= 0.0) continue;
      float r = length((uv - q.xy) * ASPECT);
      float band = (r - q.z) / (q.z * 0.35 + 0.004);
      color.rgb = mix(color.rgb, vec3(0.78, 0.86, 0.35), exp(-band * band) * q.w * 0.7);
    }
    // Antioxidant droplets: a second render of lime glass, laid into the picture.
    for (int i = 0; i < ${DROPS}; i++) {
      vec4 p = uDrops[i];
      if (p.w <= 0.0) continue;
      vec2 local = ((uv - p.xy) * ASPECT) / p.z + 0.5;
      if (local.x < 0.0 || local.x > 1.0 || local.y < 0.0 || local.y > 1.0) continue;
      vec4 s = texture2D(uDrop, local);
      color.rgb = mix(color.rgb, s.rgb, s.a * p.w);
    }
    // The white ground stays pure white, so it multiplies away into the page.
    float light = min(color.r, min(color.g, color.b));
    color.rgb = mix(color.rgb, vec3(1.0), smoothstep(0.93, 0.98, light));
    gl_FragColor = vec4(clamp(color.rgb, 0.0, 1.0), 1.0);
  }
`;

// Picture coordinates (1000 x 566, y down) to the shader's uv (y up).
const uv = (x: number, y: number): Point => ({ x: x / 1000, y: 1 - y / 566 });

function makeScene(): Scene {
  return {
    embers: Array.from({ length: EMBERS }, () => ({ x: 0, y: 0, size: 0.019, heat: 0 })),
    drops: Array.from({ length: DROPS }, () => ({ x: 0, y: 0, size: 0.094, alpha: 0 })),
    pulses: Array.from({ length: DROPS }, () => ({ x: 0, y: 0, radius: 0, alpha: 0 })),
    stain: { ...uv(505, 392), radius: 0.05, strength: 0 },
  };
}

function buildCell(
  THREE: Three,
  holder: HTMLElement,
  visual: HTMLElement,
  options: { canvasClass: string; onReady: () => void; progress: () => number },
): Cell {
  const renderer = new THREE.WebGLRenderer({ alpha: false, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(0xffffff, 1);
  const canvas = renderer.domElement;
  canvas.className = options.canvasClass;
  holder.appendChild(canvas);

  const scene = makeScene();
  const stage = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const uniforms = {
    uImage: { value: null as import("three").Texture | null },
    uOld: { value: null as import("three").Texture | null },
    uDepth: { value: null as import("three").Texture | null },
    uDrop: { value: null as import("three").Texture | null },
    uTilt: { value: new THREE.Vector2() },
    uTime: { value: 0 },
    uGlow: { value: 1 },
    uAge: { value: 0 },
    uEmbers: { value: scene.embers.map(() => new THREE.Vector4()) },
    uDrops: { value: scene.drops.map(() => new THREE.Vector4()) },
    uPulses: { value: scene.pulses.map(() => new THREE.Vector4()) },
    uStain: { value: new THREE.Vector4() },
  };
  const geometry = new THREE.PlaneGeometry(2, 2);
  const material = new THREE.ShaderMaterial({ uniforms, vertexShader, fragmentShader });
  stage.add(new THREE.Mesh(geometry, material));

  // Textures are sampled as plain sRGB bytes (no decode), so the output matches the files.
  const loader = new THREE.TextureLoader();
  const sources = {
    uImage: images.glass.src,
    uOld: images.glassAged,
    uDepth: images.glassDepth,
    uDrop: images.drop,
  };
  let loaded = 0;
  const textures: import("three").Texture[] = [];
  (Object.keys(sources) as (keyof typeof sources)[]).forEach((key) =>
    loader.load(sources[key], (texture) => {
      // The small droplet keeps its mipmaps; the big renders are shown near their own size.
      if (key !== "uDrop") texture.minFilter = THREE.LinearFilter;
      textures.push(texture);
      uniforms[key].value = texture;
      loaded += 1;
      if (loaded === 4) options.onReady();
    }),
  );

  let boxWidth = 0;
  let boxHeight = 0;
  function fit() {
    boxWidth = holder.clientWidth;
    boxHeight = holder.clientHeight;
    if (boxWidth && boxHeight) renderer.setSize(boxWidth, boxHeight, false);
  }
  fit();
  const resize = new ResizeObserver(fit);
  resize.observe(holder);

  // The pointer steers the tilt; without one, the cell sways on its own and turns with the scroll.
  const target = new THREE.Vector2();
  let lastMove = -1e9;
  function point(event: PointerEvent) {
    const box = visual.getBoundingClientRect();
    target.set(
      ((event.clientX - box.left) / box.width - 0.5) * 2,
      -((event.clientY - box.top) / box.height - 0.5) * 2,
    );
    lastMove = performance.now();
  }
  window.addEventListener("pointermove", point, { passive: true });

  let ageTarget = 0;
  let frame = 0;
  let last = performance.now();
  function draw(now: number) {
    frame = requestAnimationFrame(draw);
    const seconds = now / 1000;
    uniforms.uTime.value += Math.min((now - last) / 1000, 0.05);
    last = now;
    if (now - lastMove > 2200) {
      target.set(
        Math.sin(seconds * 0.45) * 0.45 + (options.progress() - 0.5) * 0.8,
        Math.cos(seconds * 0.38) * 0.25,
      );
    }
    uniforms.uTilt.value.lerp(target, 0.06);
    uniforms.uAge.value += (ageTarget - uniforms.uAge.value) * 0.1;
    scene.embers.forEach((e, i) => uniforms.uEmbers.value[i].set(e.x, e.y, e.size, e.heat));
    scene.drops.forEach((d, i) => uniforms.uDrops.value[i].set(d.x, d.y, d.size, d.alpha));
    scene.pulses.forEach((p, i) => uniforms.uPulses.value[i].set(p.x, p.y, p.radius, p.alpha));
    const { stain } = scene;
    uniforms.uStain.value.set(stain.x, stain.y, stain.radius, stain.strength);
    // The shader samples 0.03 x (depth - 0.2) ahead; at the cell's depth that is about 1.8%.
    const shift = 0.018;
    visual.style.setProperty(
      "--shift-x",
      `${(-uniforms.uTilt.value.x * shift * boxWidth).toFixed(1)}px`,
    );
    visual.style.setProperty(
      "--shift-y",
      `${(uniforms.uTilt.value.y * shift * boxHeight).toFixed(1)}px`,
    );
    renderer.render(stage, camera);
  }
  const visibility = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting && !frame) {
      last = performance.now();
      frame = requestAnimationFrame(draw);
    }
    if (!entry.isIntersecting && frame) {
      cancelAnimationFrame(frame);
      frame = 0;
    }
  });
  visibility.observe(holder);

  let glowTween: gsap.core.Tween | null = null;
  return {
    scene,
    setGlow(value) {
      glowTween?.kill();
      glowTween = gsap.to(uniforms.uGlow, { value, duration: 1.2, ease: "power2.out" });
    },
    setAge(value) {
      ageTarget = value;
    },
    dispose() {
      cancelAnimationFrame(frame);
      visibility.disconnect();
      resize.disconnect();
      glowTween?.kill();
      window.removeEventListener("pointermove", point);
      textures.forEach((texture) => texture.dispose());
      geometry.dispose();
      material.dispose();
      renderer.dispose();
      canvas.remove();
    },
  };
}

// Drawn in the render's own coordinates (viewBox 1000 x 566; the cell spans about x 194-808,
// y 128-411). Energy leaves the glass along gentle curves, away from the facts on the right.
const streams = [
  "M252 206 Q 170 150 92 128",
  "M398 140 Q 372 80 330 30",
  "M604 132 Q 632 70 672 24",
  "M746 382 Q 800 430 858 474",
  "M562 410 Q 572 470 600 532",
];
// The free-radical scene. Embers are born at the golden folds (where energy is made) and drift a
// little; one reaches the lower wall. Droplets rest in the clear glass at the ends of the cell.
const births = [
  { at: uv(330, 240), to: uv(318, 214) },
  { at: uv(420, 278), to: uv(404, 256) },
  { at: uv(520, 258), to: uv(524, 296) },
  { at: uv(606, 300), to: uv(626, 280) },
  { at: uv(690, 246), to: uv(704, 222) },
  { at: uv(560, 250), to: uv(540, 366) },
];
const wall = uv(505, 392);
const rests = [uv(232, 262), uv(772, 282), uv(650, 388)];
// The three steps, told as a caption under the cell while the scene plays.
const radicalSteps = [
  "Making energy also makes a few free radicals",
  "Too many can damage the cell, starting with the mitochondria",
  "Antioxidants keep them in balance",
];
const glowFor = [1.35, 1, 1];
const ageMarks = [20, 40, 60, 80];

export function ScienceGlass({ onOpenArticle }: ScienceDesignProps) {
  const copy = useCopy();
  const reducedMotion = useReducedMotion();
  const root = useRef<HTMLDivElement>(null);
  const holder = useRef<HTMLDivElement>(null);
  const visual = useRef<HTMLDivElement>(null);
  const track = useRef<HTMLDivElement>(null);
  const cell = useRef<Cell | null>(null);
  const flows = useRef<gsap.core.Timeline[]>([]);
  const progress = useRef(0);
  const touched = useRef(false);
  const shown = useRef(false);
  const [chapter, setChapter] = useState(0);
  const [ready, setReady] = useState(false);
  const [age, setAge] = useState(20);
  const aged = chapter === 2 ? (age - 20) / 60 : 0;

  // WebGL loads only for this section; on failure the still render stays.
  useEffect(() => {
    const element = holder.current;
    const frame = visual.current;
    if (!element || !frame || reducedMotion) return;
    let disposed = false;
    import("three")
      .then((THREE) => {
        if (disposed) return;
        try {
          cell.current = buildCell(THREE, element, frame, {
            canvasClass: styles.canvas,
            onReady: () => setReady(true),
            progress: () => progress.current,
          });
        } catch {
          cell.current = null;
        }
      })
      .catch(() => undefined);
    return () => {
      disposed = true;
      cell.current?.dispose();
      cell.current = null;
    };
  }, [reducedMotion]);

  // The track's scroll picks the topic and fills the tabs' meter.
  useEffect(() => {
    const element = track.current;
    if (!element || reducedMotion) return;
    gsap.registerPlugin(ScrollTrigger);
    const trigger = ScrollTrigger.create({
      trigger: element,
      start: "top top",
      end: "bottom bottom",
      onUpdate: (self) => {
        progress.current = self.progress;
        root.current?.style.setProperty("--progress", self.progress.toFixed(4));
        setChapter(Math.min(articles.length - 1, Math.floor(self.progress * articles.length)));
      },
    });
    return () => trigger.kill();
  }, [reducedMotion]);

  // Age acts only in topic 3: it turns the render old and slows the energy flowing out.
  useEffect(() => {
    cell.current?.setAge(aged);
    root.current?.style.setProperty("--age", aged.toFixed(3));
    flows.current.forEach((flow) => flow.timeScale(1 - 0.75 * aged));
  }, [aged, ready, chapter]);

  // Each topic sets the glow and plays its own picture.
  useEffect(() => {
    cell.current?.setGlow(glowFor[chapter]);
    const element = visual.current;
    if (!element || reducedMotion) return;
    gsap.registerPlugin(MotionPathPlugin);
    let demo: gsap.core.Tween | null = null;
    const scene = cell.current?.scene;
    const context = gsap.context(() => {
      if (chapter === 0 || chapter === 2) {
        // Energy packets travel out of the glass along each stream.
        const packets = gsap.utils.toArray<SVGCircleElement>("[data-packet]");
        flows.current = packets.map((packet, index) => {
          const path = element.querySelector<SVGPathElement>(`[data-stream="${index}"]`);
          return gsap
            .timeline({ repeat: -1, delay: index * 0.42 })
            .set(packet, { opacity: 0 })
            .to(packet, {
              motionPath: { path: path ?? "", align: path ?? "", alignOrigin: [0.5, 0.5] },
              duration: 2.2,
              ease: "power1.in",
            })
            .to(packet, { opacity: 1, duration: 0.3 }, 0)
            .to(packet, { opacity: 0, duration: 0.4 }, 1.8);
        });
      }
      if (chapter === 0) {
        gsap.fromTo(
          "[data-pin]",
          { scale: 1, transformOrigin: "50% 50%" },
          { scale: 1.35, duration: 1.1, ease: "sine.inOut", yoyo: true, repeat: -1 },
        );
      }
      if (chapter === 1 && scene) {
        playRadicals(scene, root.current);
      }
      if (chapter === 2) {
        // The first visit shows what the slider does, once, unless the visitor got there first.
        if (!shown.current && !touched.current) {
          shown.current = true;
          const sweep = { value: 20 };
          demo = gsap.to(sweep, {
            value: 45,
            duration: 1.8,
            delay: 0.5,
            ease: "power2.inOut",
            onUpdate: () => {
              if (!touched.current) setAge(Math.round(sweep.value));
            },
          });
        }
      }
    }, element);
    return () => {
      demo?.kill();
      flows.current = [];
      context.revert();
      if (scene) clearScene(scene);
    };
  }, [chapter, reducedMotion, ready]);

  function goTo(index: number) {
    const element = track.current;
    if (!element) return;
    const top = element.getBoundingClientRect().top + window.scrollY;
    const travel = element.offsetHeight - window.innerHeight;
    window.scrollTo({
      top: top + travel * ((index + 0.5) / articles.length),
      behavior: reducedMotion ? "auto" : "smooth",
    });
  }

  // The slider follows a dragging finger or mouse; on a desktop it also follows a hovering mouse.
  function hover(event: React.PointerEvent<HTMLInputElement>) {
    if (event.pointerType !== "mouse" || event.buttons !== 0) return;
    const box = event.currentTarget.getBoundingClientRect();
    const share = Math.min(1, Math.max(0, (event.clientX - box.left) / box.width));
    touched.current = true;
    setAge(Math.round(20 + 60 * share));
  }

  return (
    <div
      ref={root}
      className={styles.glass}
      data-chapter={chapter}
      data-ready={ready}
      data-reduced={reducedMotion}
    >
      <header className={styles.head}>
        <h2 id="science-title" className={styles.heading}>
          {copy(intro.title)}
        </h2>
        <p>{copy(intro.text)}</p>
      </header>

      <div ref={track} className={styles.track}>
        <div className={styles.stage}>
          <nav className={styles.topics} aria-label={copy("Topics")}>
            {articles.map((article, index) => (
              <button
                type="button"
                key={article.id}
                aria-current={index === chapter ? "step" : undefined}
                onClick={() => goTo(index)}
              >
                <span className={styles.number}>{index + 1}</span>
                <span className={styles.topicName}>{copy(article.topic)}</span>
              </button>
            ))}
            <span className={styles.meter} aria-hidden="true">
              <span />
            </span>
          </nav>

          <div className={styles.figure}>
            <div className={styles.plate}>
              <div ref={visual} className={styles.visual} aria-hidden="true">
                <span className={styles.halo} />
                <div ref={holder} className={styles.cell}>
                  <Image
                    {...images.glass}
                    alt=""
                    sizes="(max-width: 899px) 100vw, 62vw"
                    className={styles.still}
                  />
                </div>
                <svg className={styles.overlay} viewBox="0 0 1000 566" role="presentation">
                  <defs>
                    <filter id="science-glow" x="-50%" y="-50%" width="200%" height="200%">
                      <feGaussianBlur stdDeviation="4" result="blur" />
                      <feMerge>
                        <feMergeNode in="blur" />
                        <feMergeNode in="SourceGraphic" />
                      </feMerge>
                    </filter>
                  </defs>
                  <g className={styles.flow} data-flow>
                    {streams.map((d, index) => (
                      <path key={d} d={d} className={styles.stream} data-stream={index} />
                    ))}
                    {streams.map((d, index) => (
                      <circle
                        key={d}
                        r="6"
                        className={styles.packet}
                        filter="url(#science-glow)"
                        data-packet={index}
                      />
                    ))}
                  </g>
                  <g data-part="0">
                    <circle cx="455" cy="262" r="8" className={styles.pin} data-pin />
                    <polyline points="455,262 300,470 205,470" className={styles.leader} />
                  </g>
                  <g data-part="1">
                    <polyline
                      points="420,278 400,80 334,80"
                      className={`${styles.leader} ${styles.radicalLeader}`}
                    />
                  </g>
                </svg>

                <p className={`${styles.label} ${styles.labelEnergy}`} data-part="0">
                  {copy("Inner folds: where energy is made")}
                </p>
                <p className={`${styles.label} ${styles.labelRadicals}`} data-part="1">
                  {copy("Free radicals")}
                </p>
                <p className={`${styles.label} ${styles.labelDefenses}`} data-part="1">
                  {copy("Antioxidants")}
                </p>
                <p className={styles.age} data-part="2">
                  <span>{copy("Age")}</span>
                  <strong>{age}</strong>
                </p>
              </div>

              <ol className={styles.caption} data-part="1">
                {radicalSteps.map((line, index) => (
                  <li key={line} data-step={index}>
                    <span className={styles.stepNumber}>{index + 1}</span>
                    {copy(line)}
                  </li>
                ))}
              </ol>

              <div className={styles.ageControl} data-part="2" inert={chapter !== 2}>
                <input
                  type="range"
                  min={20}
                  max={80}
                  step={1}
                  value={age}
                  aria-label={copy("Age")}
                  aria-valuetext={String(age)}
                  onChange={(event) => {
                    touched.current = true;
                    setAge(Number(event.target.value));
                  }}
                  onPointerMove={hover}
                />
                <span className={styles.ticks} aria-hidden="true">
                  {ageMarks.map((mark) => (
                    <span key={mark} style={{ left: `${((mark - 20) / 60) * 100}%` }}>
                      {mark}
                    </span>
                  ))}
                </span>
                <span className={styles.hint}>
                  {copy("Drag to change the age")} · {copy("Illustration, not a measurement")}
                </span>
              </div>
            </div>

            <ul key={chapter} className={styles.facts} data-topic={chapter}>
              {facts[chapter].map((fact, index) => (
                <li key={fact} style={{ animationDelay: `${200 + index * 140}ms` }}>
                  {copy(fact)}
                </li>
              ))}
            </ul>
          </div>

          <div className={styles.copy}>
            {articles.map((article, index) => (
              <article
                key={article.id}
                className={styles.chapter}
                data-active={reducedMotion || index === chapter}
                inert={!reducedMotion && index !== chapter}
              >
                <h3 className={styles.title}>{copy(article.title)}</h3>
                <p className={styles.preview}>{copy(article.preview)}</p>
                <ul className={styles.inlineFacts}>
                  {facts[index].map((fact) => (
                    <li key={fact}>{copy(fact)}</li>
                  ))}
                </ul>
                <button type="button" className={styles.read} onClick={() => onOpenArticle(index)}>
                  {copy("Read a quick explainer")} <ArrowUpRight size={19} aria-hidden="true" />
                </button>
              </article>
            ))}
          </div>
        </div>
      </div>

      <div className={styles.foot}>
        <a href="#research" className={styles.explore}>
          {copy(intro.button)} <ArrowDown size={19} aria-hidden="true" />
        </a>
      </div>
    </div>
  );
}

function clearScene(scene: Scene) {
  scene.embers.forEach((ember) => Object.assign(ember, { heat: 0, size: 0.019 }));
  scene.drops.forEach((drop) => Object.assign(drop, { alpha: 0, size: 0.094 }));
  scene.pulses.forEach((pulse) => Object.assign(pulse, { alpha: 0 }));
  scene.stain.strength = 0;
}

// Topic 2 as a looping scene inside the glass, with a caption under it:
// 1 making energy throws off a few embers; 2 one reaches the wall and burns it;
// 3 antioxidant droplets catch the others, one of them just short of the wall.
function playRadicals(scene: Scene, root: HTMLElement | null) {
  const steps = root?.querySelectorAll<HTMLElement>("[data-step]") ?? [];
  const light = (step: number) =>
    steps.forEach((item, index) => {
      item.dataset.lit = String(index === step);
    });
  const { embers, drops, pulses, stain } = scene;
  const timeline = gsap.timeline({ repeat: -1, repeatDelay: 1.2 });

  // A droplet reaches an ember: the ember goes out, a lime ring spreads, the droplet bumps.
  const catchEmber = (drop: number, ember: number, at: number, leave: number) => {
    const point = births[ember].to;
    timeline
      .to(drops[drop], { ...point, duration: at - leave, ease: "power2.inOut" }, leave)
      .to(embers[ember], { heat: 0, size: 0.006, duration: 0.25, ease: "power2.in" }, at)
      .set(pulses[drop], { ...point, radius: 0.012, alpha: 1 }, at)
      .to(pulses[drop], { radius: 0.075, alpha: 0, duration: 0.7, ease: "power2.out" }, at)
      .to(drops[drop], { size: 0.112, duration: 0.16, yoyo: true, repeat: 1 }, at);
  };

  timeline
    // Reset for each round.
    .call(light, [0], 0)
    .set(stain, { strength: 0, radius: 0.02 }, 0)
    .set(embers, { heat: 0, size: 0.019 }, 0)
    .set(pulses, { alpha: 0 }, 0);
  births.forEach((birth, index) => timeline.set(embers[index], birth.at, 0));
  rests.forEach((rest, index) => timeline.set(drops[index], { ...rest, size: 0.094 }, 0));
  timeline
    .to(drops, { alpha: 1, duration: 0.6, stagger: 0.1 }, 0)
    // 1 · Making energy throws off a few embers at the folds; they glow and drift a little.
    .to(embers.slice(0, 5), { heat: 1, duration: 0.6, ease: "power2.out", stagger: 0.22 }, 0.3);
  births
    .slice(0, 5)
    .forEach((birth, index) =>
      timeline.to(
        embers[index],
        { ...birth.to, duration: 2.4, ease: "sine.inOut" },
        0.4 + index * 0.1,
      ),
    );
  timeline
    // 2 · One reaches the wall: a flash, then a burn in the glass.
    .call(light, [1], 2.4)
    .to(embers[2], { ...wall, duration: 1.1, ease: "power2.in" }, 2.4)
    .to(embers[2], { heat: 1.6, size: 0.03, duration: 0.14, yoyo: true, repeat: 1 }, 3.5)
    .to(embers[2], { heat: 0, duration: 0.3 }, 3.8)
    .to(stain, { strength: 0.85, radius: 0.058, duration: 0.7, ease: "power2.out" }, 3.55)
    // 3 · Another heads for the wall; the droplets catch it and the rest.
    .call(light, [2], 4.6)
    .set(embers[5], births[5].at, 4.5)
    .to(embers[5], { heat: 1, duration: 0.4 }, 4.6)
    .to(embers[5], { ...births[5].to, duration: 1.5, ease: "power1.in" }, 4.8);
  catchEmber(0, 0, 5.5, 4.7);
  catchEmber(1, 4, 5.7, 4.9);
  catchEmber(0, 1, 6.4, 5.7);
  catchEmber(1, 3, 6.6, 5.9);
  catchEmber(2, 5, 6.3, 5.5);
  timeline
    // The cell repairs the burn, and the droplets drift back to their places.
    .to(stain, { strength: 0, duration: 1.8, ease: "power1.inOut" }, 6.8)
    .to(drops[0], { ...rests[0], duration: 1.3, ease: "power2.inOut" }, 7)
    .to(drops[1], { ...rests[1], duration: 1.3, ease: "power2.inOut" }, 7.1)
    .to(drops[2], { ...rests[2], duration: 1.3, ease: "power2.inOut" }, 7.2);
}
