"use client";

import { useEffect, useRef } from "react";

// Signature element: a slowly breathing "jade cell" — celadon glass shell with
// a warm inner particle glow. Breathes at a resting pace (~12/min). Falls back
// to a static gradient when WebGL is unavailable; freezes after one frame when
// the visitor prefers reduced motion.
export function CellOrb({ className = "" }: { className?: string }) {
  const mountRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const mount = mountRef.current;
    if (!mount) return;

    let disposed = false;
    let raf = 0;
    let cleanup: (() => void) | null = null;

    import("three").then((THREE) => {
      if (disposed || !mount) return;

      const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

      let renderer: InstanceType<typeof THREE.WebGLRenderer>;
      try {
        renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
      } catch {
        return; // static CSS fallback stays visible
      }
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.setClearColor(0x000000, 0);
      mount.appendChild(renderer.domElement);
      renderer.domElement.style.position = "absolute";
      renderer.domElement.style.inset = "0";

      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 50);
      camera.position.set(0, 0, 6);

      const group = new THREE.Group();
      scene.add(group);

      // glass shell — fresnel rim in celadon
      const shellGeo = new THREE.SphereGeometry(1.72, 96, 96);
      const shellMat = new THREE.ShaderMaterial({
        transparent: true,
        depthWrite: false,
        uniforms: {
          uRim: { value: new THREE.Color("#4a7a63") },
          uCore: { value: new THREE.Color("#cfe0d5") },
        },
        vertexShader: /* glsl */ `
          varying vec3 vNormal;
          varying vec3 vView;
          void main() {
            vNormal = normalize(normalMatrix * normal);
            vec4 mv = modelViewMatrix * vec4(position, 1.0);
            vView = normalize(-mv.xyz);
            gl_Position = projectionMatrix * mv;
          }
        `,
        fragmentShader: /* glsl */ `
          uniform vec3 uRim;
          uniform vec3 uCore;
          varying vec3 vNormal;
          varying vec3 vView;
          void main() {
            float fresnel = pow(1.0 - abs(dot(vNormal, vView)), 2.0);
            vec3 color = mix(uCore, uRim, fresnel);
            float alpha = 0.16 + fresnel * 0.9;
            gl_FragColor = vec4(color, alpha);
          }
        `,
      });
      group.add(new THREE.Mesh(shellGeo, shellMat));

      // inner life — warm amber-and-celadon particles drifting in the volume
      const COUNT = 750;
      const positions = new Float32Array(COUNT * 3);
      const colors = new Float32Array(COUNT * 3);
      const amber = new THREE.Color("#b97f2e");
      const celadon = new THREE.Color("#48715d");
      for (let i = 0; i < COUNT; i++) {
        // uniform-ish points inside a sphere
        const r = 1.45 * Math.cbrt((i + 0.5) / COUNT);
        const theta = i * 2.399963; // golden angle
        const y = 1 - (2 * (i + 0.5)) / COUNT;
        const rr = Math.sqrt(1 - y * y);
        positions[i * 3] = r * rr * Math.cos(theta);
        positions[i * 3 + 1] = r * y;
        positions[i * 3 + 2] = r * rr * Math.sin(theta);
        const c = i % 3 === 0 ? amber : celadon;
        colors[i * 3] = c.r;
        colors[i * 3 + 1] = c.g;
        colors[i * 3 + 2] = c.b;
      }
      const dotsGeo = new THREE.BufferGeometry();
      dotsGeo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
      dotsGeo.setAttribute("color", new THREE.BufferAttribute(colors, 3));
      const dotsMat = new THREE.PointsMaterial({
        size: 0.04,
        vertexColors: true,
        transparent: true,
        opacity: 0.85,
        depthWrite: false,
      });
      const dots = new THREE.Points(dotsGeo, dotsMat);
      group.add(dots);

      const resize = () => {
        const w = mount.clientWidth;
        const h = mount.clientHeight;
        renderer.setSize(w, h, false);
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
      };
      resize();
      const ro = new ResizeObserver(resize);
      ro.observe(mount);

      // gentle pointer parallax
      let targetX = 0;
      let targetY = 0;
      const onPointer = (e: PointerEvent) => {
        const rect = mount.getBoundingClientRect();
        targetX = ((e.clientX - rect.left) / rect.width - 0.5) * 0.35;
        targetY = ((e.clientY - rect.top) / rect.height - 0.5) * 0.25;
      };
      window.addEventListener("pointermove", onPointer, { passive: true });

      // pause when offscreen
      let visible = true;
      const io = new IntersectionObserver(([entry]) => {
        visible = entry.isIntersecting;
      });
      io.observe(mount);

      const t0 = performance.now();
      const frame = () => {
        const t = (performance.now() - t0) / 1000;
        const breath = 1 + 0.022 * Math.sin((t * Math.PI * 2) / 5); // ~12 breaths/min
        group.scale.setScalar(breath);
        dots.rotation.y = t * 0.06;
        dots.rotation.x = Math.sin(t * 0.05) * 0.15;
        group.rotation.y += (targetX - group.rotation.y) * 0.04;
        group.rotation.x += (targetY - group.rotation.x) * 0.04;
        renderer.render(scene, camera);
      };

      if (reduceMotion) {
        frame(); // a single dignified still
      } else {
        const loop = () => {
          if (visible) frame();
          raf = requestAnimationFrame(loop);
        };
        raf = requestAnimationFrame(loop);
      }

      cleanup = () => {
        cancelAnimationFrame(raf);
        window.removeEventListener("pointermove", onPointer);
        ro.disconnect();
        io.disconnect();
        shellGeo.dispose();
        shellMat.dispose();
        dotsGeo.dispose();
        dotsMat.dispose();
        renderer.dispose();
        renderer.domElement.remove();
      };
    });

    return () => {
      disposed = true;
      cleanup?.();
    };
  }, []);

  return (
    <div
      ref={mountRef}
      aria-hidden
      className={className}
      style={{
        // soft celadon field behind the orb — also the no-WebGL fallback
        background:
          "radial-gradient(closest-side, rgba(95,138,117,0.20), rgba(157,191,174,0.14) 55%, transparent 74%)",
      }}
    />
  );
}
