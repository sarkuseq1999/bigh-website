"use client";

import Image from "next/image";
import gsap from "gsap";
import { MoveHorizontal } from "lucide-react";
import { useEffect, useRef, useState, type RefObject } from "react";
import { useCopy } from "@/i18n/use-copy";
import { stories } from "./stories-data";
import styles from "./stories-showroom.module.css";
import { useReducedMotion } from "./use-reduced-motion";

// Showroom: the three everyday objects stand on a real 3D turntable (three.js). Choosing a person
// turns their object to the front; dragging spins the stand and snaps to the nearest story.
type Api = { goTo: (index: number) => void };
type Three = typeof import("three");

type Options = {
  initial: number;
  getSelected: () => number;
  onSnap: (index: number) => void;
  onReady: () => void;
  api: RefObject<Api | null>;
  canvasClass: string;
  grabbingClass: string;
};

const TAU = Math.PI * 2;
const STEP = TAU / stories.length;
const RADIUS = 2.15;
const HEIGHT = 2.45;

function buildShowroom(THREE: Three, element: HTMLElement, options: Options) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.domElement.className = options.canvasClass;
  element.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x1b3470, 1.5));
  const key = new THREE.DirectionalLight(0xffffff, 1.6);
  key.position.set(4, 8, 6);
  scene.add(key);

  const disposables: { dispose: () => void }[] = [];
  function track<T extends { dispose: () => void }>(resource: T) {
    disposables.push(resource);
    return resource;
  }

  // The stand: a pale stone plinth with a thin lime rim.
  const pedestal = new THREE.Mesh(
    track(new THREE.CylinderGeometry(3.45, 3.62, 0.6, 128)),
    track(new THREE.MeshStandardMaterial({ color: 0xf1f3f8, roughness: 0.55, metalness: 0.04 })),
  );
  pedestal.position.y = -0.3;
  scene.add(pedestal);
  const rim = new THREE.Mesh(
    track(new THREE.TorusGeometry(3.46, 0.035, 12, 180)),
    track(new THREE.MeshBasicMaterial({ color: 0xe2ed94 })),
  );
  rim.rotation.x = Math.PI / 2;
  rim.position.y = 0.004;
  scene.add(rim);

  // Soft contact shadow, drawn once on a canvas.
  const paint = document.createElement("canvas");
  paint.width = paint.height = 128;
  const brush = paint.getContext("2d");
  if (brush) {
    const glow = brush.createRadialGradient(64, 64, 0, 64, 64, 64);
    glow.addColorStop(0, "rgba(12, 26, 64, 0.5)");
    glow.addColorStop(1, "rgba(12, 26, 64, 0)");
    brush.fillStyle = glow;
    brush.fillRect(0, 0, 128, 128);
  }
  const shadowTexture = track(new THREE.CanvasTexture(paint));

  const table = new THREE.Group();
  scene.add(table);
  const loader = new THREE.TextureLoader();
  let loaded = 0;
  const items = stories.map((story, index) => {
    const slot = new THREE.Group();
    slot.position.set(Math.sin(index * STEP) * RADIUS, 0, Math.cos(index * STEP) * RADIUS);
    table.add(slot);
    const material = track(new THREE.SpriteMaterial({ transparent: true, depthWrite: false }));
    const sprite = new THREE.Sprite(material);
    const width = (HEIGHT * story.objectSize.width) / story.objectSize.height;
    sprite.center.set(0.5, 0);
    sprite.scale.set(width, HEIGHT, 1);
    slot.add(sprite);
    loader.load(story.object, (texture) => {
      texture.colorSpace = THREE.SRGBColorSpace;
      material.map = track(texture);
      material.needsUpdate = true;
      loaded += 1;
      if (loaded === stories.length) options.onReady();
    });
    const shadow = new THREE.Mesh(
      track(new THREE.PlaneGeometry(HEIGHT * 1.35, HEIGHT * 0.5)),
      track(
        new THREE.MeshBasicMaterial({ map: shadowTexture, transparent: true, depthWrite: false }),
      ),
    );
    shadow.rotation.x = -Math.PI / 2;
    shadow.position.y = 0.01;
    slot.add(shadow);
    return { sprite, material, index, width };
  });

  // Frame the stand so it always fits, whatever the box's shape.
  function fit() {
    const width = element.clientWidth;
    const height = element.clientHeight;
    if (!width || !height) return;
    renderer.setSize(width, height);
    camera.aspect = width / height;
    const halfV = Math.tan((camera.fov * Math.PI) / 360);
    const distance = Math.max(3.85 / (halfV * camera.aspect), 2.75 / halfV);
    camera.position.set(0, distance * 0.27, distance);
    camera.lookAt(0, 1.05, 0);
    camera.updateProjectionMatrix();
  }
  fit();

  const turn = { value: -options.initial * STEP };
  table.rotation.y = turn.value;
  let tween: gsap.core.Tween | null = null;
  function goTo(index: number) {
    let delta = (-index * STEP - turn.value) % TAU;
    if (delta > Math.PI) delta -= TAU;
    if (delta < -Math.PI) delta += TAU;
    tween?.kill();
    tween = gsap.to(turn, {
      value: turn.value + delta,
      duration: 1.25,
      ease: "power3.inOut",
      onUpdate: () => {
        table.rotation.y = turn.value;
      },
    });
  }
  options.api.current = { goTo };

  // Drag to spin; window listeners keep the drag alive when the pointer leaves the canvas.
  const canvas = renderer.domElement;
  let startX = 0;
  let startTurn = 0;
  let dragging = false;
  function move(event: PointerEvent) {
    if (!dragging) return;
    turn.value = startTurn + (event.clientX - startX) * 0.009;
    table.rotation.y = turn.value;
  }
  function end() {
    if (!dragging) return;
    dragging = false;
    canvas.classList.remove(options.grabbingClass);
    window.removeEventListener("pointermove", move);
    window.removeEventListener("pointerup", end);
    window.removeEventListener("pointercancel", end);
    const nearest = Math.round(-turn.value / STEP) % stories.length;
    const index = (nearest + stories.length) % stories.length;
    if (index === options.getSelected()) goTo(index);
    else options.onSnap(index);
  }
  function start(event: PointerEvent) {
    dragging = true;
    startX = event.clientX;
    startTurn = turn.value;
    tween?.kill();
    canvas.classList.add(options.grabbingClass);
    window.addEventListener("pointermove", move);
    window.addEventListener("pointerup", end);
    window.addEventListener("pointercancel", end);
  }
  canvas.addEventListener("pointerdown", start);

  // Render only while on screen. The front object is brightest and bobs gently.
  let frame = 0;
  function draw() {
    frame = requestAnimationFrame(draw);
    const seconds = performance.now() / 1000;
    for (const item of items) {
      const front = (Math.cos(item.index * STEP + turn.value) + 1) / 2;
      const grow = 0.82 + 0.3 * front;
      item.sprite.scale.set(item.width * grow, HEIGHT * grow, 1);
      item.material.color.setScalar(0.4 + 0.6 * front);
      item.material.opacity = 0.6 + 0.4 * front;
      item.sprite.position.y = Math.sin(seconds * 1.3 + item.index * 2.1) * 0.05 * front;
    }
    renderer.render(scene, camera);
  }
  const visibility = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting && !frame) draw();
    if (!entry.isIntersecting && frame) {
      cancelAnimationFrame(frame);
      frame = 0;
    }
  });
  visibility.observe(element);
  const resize = new ResizeObserver(fit);
  resize.observe(element);

  return () => {
    cancelAnimationFrame(frame);
    visibility.disconnect();
    resize.disconnect();
    tween?.kill();
    canvas.removeEventListener("pointerdown", start);
    window.removeEventListener("pointermove", move);
    window.removeEventListener("pointerup", end);
    window.removeEventListener("pointercancel", end);
    for (const resource of disposables) resource.dispose();
    renderer.dispose();
    canvas.remove();
  };
}

export function ShowroomStage({
  selected,
  onSelect,
}: {
  selected: number;
  onSelect: (index: number) => void;
}) {
  const copy = useCopy();
  const reducedMotion = useReducedMotion();
  const holder = useRef<HTMLDivElement>(null);
  const api = useRef<Api | null>(null);
  const selectedRef = useRef(selected);
  const onSelectRef = useRef(onSelect);
  const [status, setStatus] = useState<"loading" | "ready" | "failed">("loading");

  useEffect(() => {
    selectedRef.current = selected;
    onSelectRef.current = onSelect;
  });

  useEffect(() => {
    api.current?.goTo(selected);
  }, [selected]);

  // three.js loads only when this design is on the page; without WebGL the still version shows.
  useEffect(() => {
    const element = holder.current;
    if (!element || reducedMotion) return;
    let disposed = false;
    let teardown = () => {};
    import("three")
      .then((THREE) => {
        if (disposed) return;
        try {
          teardown = buildShowroom(THREE, element, {
            initial: selectedRef.current,
            getSelected: () => selectedRef.current,
            onSnap: (index) => onSelectRef.current(index),
            onReady: () => setStatus("ready"),
            api,
            canvasClass: styles.canvas,
            grabbingClass: styles.grabbing,
          });
        } catch {
          setStatus("failed");
        }
      })
      .catch(() => setStatus("failed"));
    return () => {
      disposed = true;
      teardown();
      api.current = null;
    };
  }, [reducedMotion]);

  const still = reducedMotion || status === "failed";
  const story = stories[selected];

  return (
    <div className={styles.showroom} data-status={still ? "still" : status} aria-hidden="true">
      <span className={styles.spot} />
      <div ref={holder} className={styles.holder} />
      {still ? (
        <div className={styles.still}>
          <span className={styles.plinth} />
          <Image
            src={story.object}
            width={story.objectSize.width}
            height={story.objectSize.height}
            sizes="(max-width: 899px) 70vw, 30vw"
            alt=""
          />
        </div>
      ) : (
        <p className={styles.hint}>
          <MoveHorizontal size={16} aria-hidden="true" />
          {copy("Drag to turn")}
        </p>
      )}
    </div>
  );
}
