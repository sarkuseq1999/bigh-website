"use client";

import { useEffect, useRef } from "react";
import * as THREE from "three";
import gsap from "gsap";

/* ─────────────────────────────────────────────────────────────────────────
   HeroScene — the "Ignite + Protect" WebGL layer.
   Spec: docs/superpowers/specs/2026-06-10-hero-3d-redesign-design.md

   A dim neuron field wakes up as amber mitochondria cores ignite one by
   one; a pale protective sweep passes once and clears the dark debris
   ("toxic waste"); afterwards bright sparks travel the connection lines
   forever. Mouse parallax, breathing idle, all on a transparent canvas so
   the CSS gradient behind it doubles as the no-WebGL fallback.

   Loaded client-only via next/dynamic — never on the server.
───────────────────────────────────────────────────────────────────────── */

type Props = {
  /** Fired once when WebGL is up and the scene took over from the static
      fallback layer. Never fired when WebGL is unavailable. */
  onActive?: () => void;
};

/* Palette (matches globals.css custom properties) */
const AMBER = new THREE.Color("#C28A3A");
const AMBER_HI = new THREE.Color("#DDA94E");
const WARM_WHITE = new THREE.Color("#FFF3DE");
const SWEEP_TEAL = new THREE.Color("#9FE3C9");

function webglAvailable(): boolean {
  try {
    const c = document.createElement("canvas");
    return !!(
      window.WebGLRenderingContext &&
      (c.getContext("webgl2") || c.getContext("webgl"))
    );
  } catch {
    return false;
  }
}

/* ── canvas-generated textures (no asset downloads) ──────────────────── */

function makeGlowTexture(): THREE.CanvasTexture {
  const c = document.createElement("canvas");
  c.width = c.height = 256;
  const g = c.getContext("2d")!;
  const grad = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  grad.addColorStop(0, "rgba(255,246,228,1)");
  grad.addColorStop(0.18, "rgba(238,196,118,0.85)");
  grad.addColorStop(0.45, "rgba(194,138,58,0.28)");
  grad.addColorStop(1, "rgba(194,138,58,0)");
  g.fillStyle = grad;
  g.fillRect(0, 0, 256, 256);
  return new THREE.CanvasTexture(c);
}

function makeSparkTexture(): THREE.CanvasTexture {
  const c = document.createElement("canvas");
  c.width = c.height = 64;
  const g = c.getContext("2d")!;
  const grad = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  grad.addColorStop(0, "rgba(255,255,244,1)");
  grad.addColorStop(0.35, "rgba(214,255,236,0.6)");
  grad.addColorStop(1, "rgba(159,227,201,0)");
  g.fillStyle = grad;
  g.fillRect(0, 0, 64, 64);
  return new THREE.CanvasTexture(c);
}

function makeRingTexture(): THREE.CanvasTexture {
  const c = document.createElement("canvas");
  c.width = c.height = 256;
  const g = c.getContext("2d")!;
  g.strokeStyle = "rgba(159,227,201,0.9)";
  g.lineWidth = 6;
  g.shadowColor = "rgba(159,227,201,0.9)";
  g.shadowBlur = 18;
  g.beginPath();
  g.arc(128, 128, 104, 0, Math.PI * 2);
  g.stroke();
  return new THREE.CanvasTexture(c);
}

/* ── shaders ─────────────────────────────────────────────────────────── */

const NEURON_VERT = /* glsl */ `
  uniform float uTime;
  uniform float uPixelRatio;
  attribute float aPhase;
  attribute float aSize;
  varying float vPhase;
  void main() {
    vPhase = aPhase;
    vec3 p = position;
    /* gentle organic wobble so the field feels alive */
    p.x += sin(uTime * 0.25 + aPhase * 6.2831) * 0.35;
    p.y += cos(uTime * 0.21 + aPhase * 9.42) * 0.30;
    vec4 mv = modelViewMatrix * vec4(p, 1.0);
    gl_PointSize = aSize * uPixelRatio * (140.0 / -mv.z);
    gl_Position = projectionMatrix * mv;
  }
`;

const NEURON_FRAG = /* glsl */ `
  uniform float uTime;
  uniform float uBrightness;
  uniform vec3 uColor;
  varying float vPhase;
  void main() {
    float d = length(gl_PointCoord - vec2(0.5));
    float disc = smoothstep(0.5, 0.05, d);
    float twinkle = 0.7 + 0.3 * sin(uTime * 1.3 + vPhase * 6.2831);
    float a = disc * twinkle * uBrightness;
    gl_FragColor = vec4(uColor, a);
  }
`;

const DEBRIS_VERT = /* glsl */ `
  uniform float uTime;
  uniform float uSweep;      /* protective sweep radius, world units */
  uniform float uPixelRatio;
  attribute float aDist;     /* rest distance from sweep origin */
  attribute vec3 aDir;       /* outward direction from sweep origin */
  attribute float aPhase;
  attribute float aSize;
  varying float vAlpha;
  void main() {
    vec3 p = position;
    p.x += sin(uTime * 0.18 + aPhase * 6.2831) * 0.4;
    p.y += cos(uTime * 0.15 + aPhase * 4.2) * 0.35;
    /* once the sweep wave passes this particle, push it out + dissolve */
    float f = clamp((uSweep - aDist) / 3.0, 0.0, 1.0);
    p += aDir * f * 7.0;
    vAlpha = (1.0 - f);
    vec4 mv = modelViewMatrix * vec4(p, 1.0);
    gl_PointSize = aSize * uPixelRatio * (140.0 / -mv.z) * (1.0 - 0.5 * f);
    gl_Position = projectionMatrix * mv;
  }
`;

const DEBRIS_FRAG = /* glsl */ `
  varying float vAlpha;
  void main() {
    float d = length(gl_PointCoord - vec2(0.5));
    float disc = smoothstep(0.5, 0.12, d);
    gl_FragColor = vec4(vec3(0.055, 0.06, 0.045), disc * vAlpha * 0.85);
  }
`;

/* ── component ───────────────────────────────────────────────────────── */

export default function HeroScene({ onActive }: Props) {
  const hostRef = useRef<HTMLDivElement>(null);
  const onActiveRef = useRef(onActive);
  onActiveRef.current = onActive;

  useEffect(() => {
    const host = hostRef.current;
    if (!host || !webglAvailable()) return; // static fallback stays

    /* Read the preference directly (not the hydration-safe hook): this
       component only ever mounts on the client, after hydration. */
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const small =
      window.innerWidth < 768 ||
      (navigator.hardwareConcurrency ?? 8) <= 4;

    const NEURONS = small ? 1200 : 2400;
    const CORES = small ? 9 : 16;
    const DEBRIS = small ? 140 : 280;
    const MAX_LINES = small ? 450 : 900;
    const MAX_PULSES = small ? 4 : 7;

    /* renderer / camera / scene -------------------------------------- */
    const renderer = new THREE.WebGLRenderer({
      alpha: true,
      antialias: false,
      powerPreference: "high-performance",
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.75));
    renderer.setClearColor(0x000000, 0);
    host.appendChild(renderer.domElement);

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(50, 1, 0.1, 120);
    camera.position.set(0, 0, 26);

    /* everything lives in one group so we can bias it right on desktop */
    const group = new THREE.Group();
    scene.add(group);

    const disposables: { dispose: () => void }[] = [];

    /* neuron field ----------------------------------------------------- */
    const nPos = new Float32Array(NEURONS * 3);
    const nPhase = new Float32Array(NEURONS);
    const nSize = new Float32Array(NEURONS);
    const RX = 17, RY = 9.5, RZ = 5;
    for (let i = 0; i < NEURONS; i++) {
      /* random point in an ellipsoid, denser toward the middle */
      let x = 0, y = 0, z = 0;
      do {
        x = Math.random() * 2 - 1;
        y = Math.random() * 2 - 1;
        z = Math.random() * 2 - 1;
      } while (x * x + y * y + z * z > 1);
      const pull = 0.55 + 0.45 * Math.random(); // mild center bias
      nPos[i * 3] = x * RX * pull;
      nPos[i * 3 + 1] = y * RY * pull;
      nPos[i * 3 + 2] = z * RZ * pull;
      nPhase[i] = Math.random();
      nSize[i] = 0.9 + Math.random() * 1.5;
    }
    const neuronGeo = new THREE.BufferGeometry();
    neuronGeo.setAttribute("position", new THREE.BufferAttribute(nPos, 3));
    neuronGeo.setAttribute("aPhase", new THREE.BufferAttribute(nPhase, 1));
    neuronGeo.setAttribute("aSize", new THREE.BufferAttribute(nSize, 1));
    const neuronMat = new THREE.ShaderMaterial({
      vertexShader: NEURON_VERT,
      fragmentShader: NEURON_FRAG,
      transparent: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
      uniforms: {
        uTime: { value: 0 },
        uBrightness: { value: reduce ? 0.5 : 0.12 },
        uPixelRatio: { value: renderer.getPixelRatio() },
        uColor: { value: WARM_WHITE.clone() },
      },
    });
    const neurons = new THREE.Points(neuronGeo, neuronMat);
    neurons.renderOrder = 2;
    group.add(neurons);
    disposables.push(neuronGeo, neuronMat);

    /* connection lines between near neighbors -------------------------- */
    const segs: { a: THREE.Vector3; b: THREE.Vector3 }[] = [];
    {
      const candidates = Math.min(700, NEURONS);
      const stride = Math.floor(NEURONS / candidates);
      const radius2 = 3.2 * 3.2;
      outer: for (let i = 0; i < NEURONS; i += stride) {
        const ax = nPos[i * 3], ay = nPos[i * 3 + 1], az = nPos[i * 3 + 2];
        let linked = 0;
        for (let j = i + 1; j < NEURONS && linked < 2; j += 7) {
          const dx = nPos[j * 3] - ax;
          const dy = nPos[j * 3 + 1] - ay;
          const dz = nPos[j * 3 + 2] - az;
          if (dx * dx + dy * dy + dz * dz < radius2) {
            segs.push({
              a: new THREE.Vector3(ax, ay, az),
              b: new THREE.Vector3(nPos[j * 3], nPos[j * 3 + 1], nPos[j * 3 + 2]),
            });
            linked++;
            if (segs.length >= MAX_LINES) break outer;
          }
        }
      }
    }
    const linePos = new Float32Array(segs.length * 6);
    segs.forEach((s, i) => {
      linePos.set([s.a.x, s.a.y, s.a.z, s.b.x, s.b.y, s.b.z], i * 6);
    });
    const lineGeo = new THREE.BufferGeometry();
    lineGeo.setAttribute("position", new THREE.BufferAttribute(linePos, 3));
    const lineMat = new THREE.LineBasicMaterial({
      color: AMBER_HI.clone().lerp(WARM_WHITE, 0.5),
      transparent: true,
      opacity: reduce ? 0.09 : 0,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    });
    const lines = new THREE.LineSegments(lineGeo, lineMat);
    lines.renderOrder = 1;
    group.add(lines);
    disposables.push(lineGeo, lineMat);

    /* mitochondria cores ------------------------------------------------ */
    const glowTex = makeGlowTexture();
    disposables.push(glowTex);
    type Core = {
      sprite: THREE.Sprite;
      base: number;
      phase: number;
      state: { lit: number };
    };
    const cores: Core[] = [];
    const corePts: THREE.Vector3[] = [];
    for (let i = 0; i < CORES; i++) {
      /* rejection-sample so cores keep breathing room between them */
      let p = new THREE.Vector3();
      for (let tries = 0; tries < 24; tries++) {
        p = new THREE.Vector3(
          (Math.random() * 2 - 1) * 10,
          (Math.random() * 2 - 1) * 6,
          -1 + Math.random() * 5,
        );
        if (corePts.every((q) => q.distanceTo(p) > 3.4)) break;
      }
      corePts.push(p);
      const mat = new THREE.SpriteMaterial({
        map: glowTex,
        transparent: true,
        opacity: 0,
        depthWrite: false,
        blending: THREE.AdditiveBlending,
        color: i % 3 === 0 ? AMBER_HI : AMBER.clone().lerp(AMBER_HI, Math.random()),
      });
      const sprite = new THREE.Sprite(mat);
      sprite.position.copy(p);
      sprite.renderOrder = 4;
      group.add(sprite);
      disposables.push(mat);
      cores.push({
        sprite,
        base: 3.2 + Math.random() * 2.6,
        phase: Math.random() * Math.PI * 2,
        state: { lit: reduce ? 1 : 0 },
      });
    }
    if (reduce) {
      /* the render loop never runs under reduced motion, so the lit state
         must be baked in before the single static frame */
      for (const c of cores) {
        c.sprite.material.opacity = 0.85;
        c.sprite.scale.setScalar(c.base * 1.1);
      }
    }

    /* toxic debris ------------------------------------------------------ */
    const dPos = new Float32Array(DEBRIS * 3);
    const dDist = new Float32Array(DEBRIS);
    const dDir = new Float32Array(DEBRIS * 3);
    const dPhase = new Float32Array(DEBRIS);
    const dSize = new Float32Array(DEBRIS);
    const sweepOrigin = new THREE.Vector3(0, 0, 1.5);
    for (let i = 0; i < DEBRIS; i++) {
      const v = new THREE.Vector3(
        (Math.random() * 2 - 1) * 10,
        (Math.random() * 2 - 1) * 6,
        (Math.random() * 2 - 1) * 3 + 1,
      );
      dPos.set([v.x, v.y, v.z], i * 3);
      const out = v.clone().sub(sweepOrigin);
      dDist[i] = out.length();
      out.normalize();
      dDir.set([out.x, out.y, out.z], i * 3);
      dPhase[i] = Math.random();
      dSize[i] = 3.0 + Math.random() * 3.5;
    }
    const debrisGeo = new THREE.BufferGeometry();
    debrisGeo.setAttribute("position", new THREE.BufferAttribute(dPos, 3));
    debrisGeo.setAttribute("aDist", new THREE.BufferAttribute(dDist, 1));
    debrisGeo.setAttribute("aDir", new THREE.BufferAttribute(dDir, 3));
    debrisGeo.setAttribute("aPhase", new THREE.BufferAttribute(dPhase, 1));
    debrisGeo.setAttribute("aSize", new THREE.BufferAttribute(dSize, 1));
    const debrisMat = new THREE.ShaderMaterial({
      vertexShader: DEBRIS_VERT,
      fragmentShader: DEBRIS_FRAG,
      transparent: true,
      depthWrite: false,
      uniforms: {
        uTime: { value: 0 },
        uSweep: { value: reduce ? 30 : 0 }, // reduced motion: already clean
        uPixelRatio: { value: renderer.getPixelRatio() },
      },
    });
    const debris = new THREE.Points(debrisGeo, debrisMat);
    debris.renderOrder = 3;
    group.add(debris);
    disposables.push(debrisGeo, debrisMat);

    /* protective sweep ring --------------------------------------------- */
    const ringTex = makeRingTexture();
    const ringMat = new THREE.SpriteMaterial({
      map: ringTex,
      transparent: true,
      opacity: 0,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
      color: SWEEP_TEAL,
    });
    const ring = new THREE.Sprite(ringMat);
    ring.position.copy(sweepOrigin);
    ring.renderOrder = 5;
    group.add(ring);
    disposables.push(ringTex, ringMat);

    /* traveling energy pulses ------------------------------------------- */
    const sparkTex = makeSparkTexture();
    disposables.push(sparkTex);
    type Pulse = {
      sprite: THREE.Sprite;
      seg: number;
      t: number;
      speed: number;
      active: boolean;
    };
    const pulses: Pulse[] = [];
    for (let i = 0; i < MAX_PULSES; i++) {
      const mat = new THREE.SpriteMaterial({
        map: sparkTex,
        transparent: true,
        opacity: 0,
        depthWrite: false,
        blending: THREE.AdditiveBlending,
      });
      const sprite = new THREE.Sprite(mat);
      sprite.scale.setScalar(0.65);
      sprite.renderOrder = 6;
      sprite.visible = false;
      group.add(sprite);
      disposables.push(mat);
      pulses.push({ sprite, seg: 0, t: 0, speed: 1, active: false });
    }
    let nextPulseAt = Infinity; // armed once ignition completes

    /* intro timeline ----------------------------------------------------- */
    const S = { lines: reduce ? 0.09 : 0, sweep: reduce ? 30 : 0, neurons: reduce ? 0.5 : 0.12 };
    let ignited = reduce; // pulses allowed only after ignition
    let tl: gsap.core.Timeline | null = null;
    if (!reduce) {
      tl = gsap.timeline({ delay: 0.25 });
      tl.to(
        cores.map((c) => c.state),
        { lit: 1, duration: 0.9, ease: "power2.in", stagger: { each: 0.07, from: "random" } },
        0.35,
      );
      tl.to(S, { sweep: 22, duration: 1.3, ease: "power1.inOut" }, 0.85);
      tl.to(S, { neurons: 0.5, duration: 1.5, ease: "power2.out" }, 1.0);
      tl.to(S, { lines: 0.09, duration: 1.4, ease: "power1.out" }, 1.1);
      tl.call(
        () => {
          ignited = true;
          nextPulseAt = time + 0.4;
        },
        [],
        2.4,
      );
    }

    /* sizing -------------------------------------------------------------- */
    const resize = () => {
      const w = host.clientWidth || 1;
      const h = host.clientHeight || 1;
      renderer.setSize(w, h);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      /* bias the cloud right of the text column on wide screens */
      group.position.x = w / h > 1.05 ? 6 : 0;
      if (reduce) renderer.render(scene, camera);
    };
    resize();
    const ro = new ResizeObserver(resize);
    ro.observe(host);

    /* pointer parallax ----------------------------------------------------- */
    const pointer = { x: 0, y: 0 };
    const onPointer = (e: PointerEvent) => {
      pointer.x = (e.clientX / window.innerWidth) * 2 - 1;
      pointer.y = (e.clientY / window.innerHeight) * 2 - 1;
    };
    if (!reduce) window.addEventListener("pointermove", onPointer, { passive: true });

    /* render loop ----------------------------------------------------------- */
    let time = 0;
    let raf = 0;
    let running = false;
    let inView = true;
    let last = performance.now();

    const frame = (now: number) => {
      raf = requestAnimationFrame(frame);
      const dt = Math.min((now - last) / 1000, 0.05);
      last = now;
      time += dt;

      neuronMat.uniforms.uTime.value = time;
      neuronMat.uniforms.uBrightness.value = S.neurons;
      debrisMat.uniforms.uTime.value = time;
      debrisMat.uniforms.uSweep.value = S.sweep;
      lineMat.opacity = S.lines;

      /* sweep ring visual: grows with the sweep radius, fades at both ends */
      const sw = S.sweep / 22;
      ring.scale.setScalar(Math.max(S.sweep * 2.4, 0.01));
      ringMat.opacity = Math.sin(Math.min(sw, 1) * Math.PI) * 0.3;

      /* cores: flicker while catching, then breathe */
      for (const c of cores) {
        const lit = c.state.lit;
        const catching = lit > 0.04 && lit < 0.96 ? (Math.random() - 0.5) * 0.35 * (1 - lit) : 0;
        const breathe = 0.78 + 0.22 * Math.sin(time * 0.8 + c.phase);
        c.sprite.material.opacity = Math.max(0, Math.min(1, lit * breathe + catching));
        c.sprite.scale.setScalar(c.base * (0.55 + 0.55 * lit) * (1 + 0.045 * Math.sin(time * 0.9 + c.phase)));
      }

      /* pulses: sparks traveling the connection lines */
      if (ignited && segs.length > 0 && time >= nextPulseAt) {
        const free = pulses.find((p) => !p.active);
        if (free) {
          free.active = true;
          free.t = 0;
          free.seg = Math.floor(Math.random() * segs.length);
          free.speed = 1 / (0.45 + Math.random() * 0.5);
          free.sprite.visible = true;
        }
        nextPulseAt = time + 0.25 + Math.random() * 0.7;
      }
      for (const p of pulses) {
        if (!p.active) continue;
        p.t += dt * p.speed;
        if (p.t >= 1) {
          p.active = false;
          p.sprite.visible = false;
          continue;
        }
        const s = segs[p.seg];
        p.sprite.position.lerpVectors(s.a, s.b, p.t);
        p.sprite.material.opacity = Math.sin(p.t * Math.PI) * 0.9;
      }

      /* camera parallax */
      camera.position.x += (pointer.x * 1.6 - camera.position.x) * 0.04;
      camera.position.y += (-pointer.y * 1.0 - camera.position.y) * 0.04;
      camera.lookAt(0, 0, 0);

      renderer.render(scene, camera);
    };

    const start = () => {
      if (running || reduce) return;
      running = true;
      last = performance.now();
      raf = requestAnimationFrame(frame);
    };
    const stop = () => {
      if (!running) return;
      running = false;
      cancelAnimationFrame(raf);
    };

    /* pause when offscreen or tab hidden */
    const io = new IntersectionObserver(([entry]) => {
      inView = entry.isIntersecting;
      if (inView && !document.hidden) start();
      else stop();
    });
    io.observe(host);
    const onVis = () => {
      if (!document.hidden && inView) start();
      else stop();
    };
    document.addEventListener("visibilitychange", onVis);

    if (reduce) {
      renderer.render(scene, camera); // single static lit frame
    } else {
      start();
    }

    /* hand off from the static CSS fallback */
    gsap.fromTo(
      host,
      { autoAlpha: 0 },
      { autoAlpha: 1, duration: reduce ? 0 : 0.6, ease: "power1.out" },
    );
    onActiveRef.current?.();

    return () => {
      stop();
      tl?.kill();
      io.disconnect();
      ro.disconnect();
      document.removeEventListener("visibilitychange", onVis);
      window.removeEventListener("pointermove", onPointer);
      gsap.killTweensOf(host);
      disposables.forEach((d) => d.dispose());
      renderer.dispose();
      host.removeChild(renderer.domElement);
    };
  }, []);

  return <div ref={hostRef} aria-hidden className="absolute inset-0 opacity-0" />;
}
