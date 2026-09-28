// Shared 3D pieces for the product pages: a soft studio, a white capsule that opens, NuriCell's
// ingredient molecules, soft contact shadows, and a renderer that adapts to the device.
// The capsule is hypromellose with titanium dioxide: opaque white, never glass.

import type * as T from "three";
import { molecules, type Element } from "./molecules";

export type Three = typeof import("three");

export const smooth = (t: number) => t * t * (3 - 2 * t);
export const clamp01 = (t: number) => Math.min(1, Math.max(0, t));
export const mix = (a: number, b: number, t: number) => a + (b - a) * t;

// ---------------------------------------------------------------------------------------------
// Renderer and viewport: 1x and draw-on-demand on software renderers, step down on slow GPUs.

export type Viewport = {
  renderer: T.WebGLRenderer;
  camera: T.PerspectiveCamera;
  software: boolean;
  width: number;
  height: number;
  halfW: number;
  halfH: number;
  portrait: boolean;
  /** Call when the stage size changes. */
  resize: () => void;
  /** Feed each frame's timestamp; lowers the pixel ratio if frames keep running slow. */
  pace: (now: number) => void;
  dispose: () => void;
};

export function createViewport(
  three: Three,
  canvas: HTMLCanvasElement,
  stage: HTMLElement,
  onResize?: () => void,
): Viewport {
  const renderer = new three.WebGLRenderer({
    canvas,
    alpha: true,
    antialias: true,
    powerPreference: "high-performance",
  });
  renderer.setClearColor(0x000000, 0);
  renderer.toneMapping = three.NeutralToneMapping;
  renderer.toneMappingExposure = 1.02;

  const camera = new three.PerspectiveCamera(30, 1, 0.1, 100);
  camera.position.set(0, 0, 14);

  const gl = renderer.getContext();
  const debugInfo = gl.getExtension("WEBGL_debug_renderer_info");
  const gpu = debugInfo ? String(gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL)) : "";
  const software = /swiftshader|llvmpipe|software|basic render/i.test(gpu);
  let ratioCap = software ? 1 : 2;
  let lastFrame = 0;
  let slowFrames = 0;

  const view: Viewport = {
    renderer,
    camera,
    software,
    width: 1,
    height: 1,
    halfW: 1,
    halfH: 1,
    portrait: false,
    resize() {
      const rect = stage.getBoundingClientRect();
      view.width = Math.max(1, rect.width);
      view.height = Math.max(1, rect.height);
      view.portrait = view.width / view.height < 0.9;
      const cap = view.portrait ? Math.min(1.6, ratioCap) : ratioCap;
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, cap));
      renderer.setSize(view.width, view.height, false);
      camera.aspect = view.width / view.height;
      camera.updateProjectionMatrix();
      view.halfH = camera.position.z * Math.tan(((camera.fov / 2) * Math.PI) / 180);
      view.halfW = view.halfH * camera.aspect;
      onResize?.();
    },
    pace(now: number) {
      if (lastFrame && now - lastFrame > 34 && ratioCap > 1) {
        slowFrames += 1;
        if (slowFrames > 45) {
          ratioCap = Math.max(1, ratioCap - 0.5);
          slowFrames = 0;
          view.resize();
        }
      } else {
        slowFrames = Math.max(0, slowFrames - 1);
      }
      lastFrame = now;
    },
    dispose() {
      resizer.disconnect();
      renderer.dispose();
    },
  };
  const resizer = new ResizeObserver(() => view.resize());
  resizer.observe(stage);
  view.resize();
  return view;
}

/** A render loop that runs only while `target` is on screen and the tab is visible. */
export function createLoop(target: HTMLElement, frame: (now: number) => void) {
  let handle = 0;
  let running = false;
  const tick = (now: number) => {
    if (!running) return;
    frame(now);
    handle = requestAnimationFrame(tick);
  };
  const start = () => {
    if (running) return;
    running = true;
    handle = requestAnimationFrame(tick);
  };
  const stop = () => {
    running = false;
    cancelAnimationFrame(handle);
  };
  let onScreen = false;
  const sync = () => (onScreen && !document.hidden ? start() : stop());
  const observer = new IntersectionObserver(([entry]) => {
    onScreen = entry.isIntersecting;
    sync();
  });
  observer.observe(target);
  document.addEventListener("visibilitychange", sync);
  return {
    dispose() {
      stop();
      observer.disconnect();
      document.removeEventListener("visibilitychange", sync);
    },
  };
}

// ---------------------------------------------------------------------------------------------
// Studio light: a neutral room for reflections, a warm key and a cool fill.

export function addStudio(
  three: Three,
  renderer: T.WebGLRenderer,
  scene: T.Scene,
  onReady?: () => void,
) {
  const pmrem = new three.PMREMGenerator(renderer);
  let environment: T.Texture | null = null;
  let disposed = false;
  import("three/addons/environments/RoomEnvironment.js").then(({ RoomEnvironment }) => {
    if (disposed) return;
    const room = new RoomEnvironment();
    environment = pmrem.fromScene(room, 0.04).texture;
    scene.environment = environment;
    scene.environmentIntensity = 0.9;
    room.dispose();
    onReady?.();
  });
  const key = new three.DirectionalLight("#fff0da", 1.6);
  key.position.set(-4, 6, 8);
  const fill = new three.DirectionalLight("#dfe9ff", 0.5);
  fill.position.set(6, -2, 4);
  const ambient = new three.AmbientLight("#ffffff", 0.25);
  scene.add(key, fill, ambient);
  return {
    dispose() {
      disposed = true;
      environment?.dispose();
      pmrem.dispose();
    },
  };
}

// ---------------------------------------------------------------------------------------------
// The capsule: a longer body and a slightly wider cap that slides over it (a size 0 capsule is
// about 21.7 mm long; one model unit is 10 mm).

export const CAPSULE_LENGTH = 2.17;
const BODY = { radius: 0.367, length: 1.86 };
const CAP = { radius: 0.382, length: 1.07 };
const WALL = 0.03;
const SLIDE = { cap: 0.7, body: 0.4 };
const closedBodyX = CAPSULE_LENGTH / 2 - BODY.radius;
const closedCapX = -CAPSULE_LENGTH / 2 + CAP.radius;
const bodyRim = closedBodyX - (BODY.length - BODY.radius);
const capRim = closedCapX + (CAP.length - CAP.radius);

function shellProfile(three: Three, radius: number, length: number) {
  // Outer dome → wall → rim → inner wall → inner dome, so an open half shows a real thin shell.
  const points: T.Vector2[] = [];
  const steps = 28;
  for (let i = 0; i <= steps; i++) {
    const a = (i / steps) * (Math.PI / 2);
    points.push(new three.Vector2(Math.sin(a) * radius, -Math.cos(a) * radius));
  }
  points.push(new three.Vector2(radius, length - radius));
  points.push(new three.Vector2(radius - WALL * 0.5, length - radius + WALL * 0.3));
  points.push(new three.Vector2(radius - WALL, length - radius));
  const inner = radius - WALL;
  for (let i = steps; i >= 0; i--) {
    const a = (i / steps) * (Math.PI / 2);
    points.push(new three.Vector2(Math.sin(a) * inner, -Math.cos(a) * inner));
  }
  return points;
}

export type Capsule = {
  group: T.Group;
  tilt: T.Group;
  body: T.Group;
  cap: T.Group;
};

export function createCapsuleKit(three: Three) {
  const shell = new three.MeshPhysicalMaterial({
    color: "#f7f4ee",
    roughness: 0.4,
    clearcoat: 0.45,
    clearcoatRoughness: 0.28,
    sheen: 0.5,
    sheenRoughness: 0.55,
    sheenColor: new three.Color("#ffffff"),
  });
  const powder = new three.MeshStandardMaterial({ color: "#efe7d6", roughness: 1 });
  const bodyGeometry = new three.LatheGeometry(shellProfile(three, BODY.radius, BODY.length), 72);
  const capGeometry = new three.LatheGeometry(shellProfile(three, CAP.radius, CAP.length), 72);
  const plugGeometry = new three.CylinderGeometry(1, 1, 1, 40);

  function make(): Capsule {
    const group = new three.Group();
    const tilt = new three.Group();
    group.add(tilt);
    const body = new three.Group();
    const bodyMesh = new three.Mesh(bodyGeometry, shell);
    bodyMesh.rotation.z = Math.PI / 2; // rim faces −x, dome at +x
    const fillLength = BODY.length - BODY.radius - 0.12;
    const bodyPowder = new three.Mesh(plugGeometry, powder);
    bodyPowder.rotation.z = Math.PI / 2;
    bodyPowder.scale.set(BODY.radius - WALL - 0.004, fillLength, BODY.radius - WALL - 0.004);
    bodyPowder.position.x = -fillLength / 2 + 0.02;
    body.add(bodyMesh, bodyPowder);
    const cap = new three.Group();
    const capMesh = new three.Mesh(capGeometry, shell);
    capMesh.rotation.z = -Math.PI / 2; // rim faces +x, dome at −x
    cap.add(capMesh);
    tilt.add(body, cap);
    body.position.x = closedBodyX;
    cap.position.x = closedCapX;
    return { group, tilt, body, cap };
  }

  /** Slide the two halves apart (0 closed, 1 open); the pair stays centred on the group. */
  function open(capsule: Capsule, amount: number) {
    const o = smooth(clamp01(amount));
    const shift = ((SLIDE.cap - SLIDE.body) / 2) * o;
    capsule.cap.position.x = closedCapX - o * SLIDE.cap + shift;
    capsule.body.position.x = closedBodyX + o * SLIDE.body + shift;
    capsule.cap.rotation.z = o * 0.14;
    capsule.body.rotation.z = -o * 0.08;
    capsule.cap.position.y = o * 0.08;
    capsule.body.position.y = -o * 0.04;
    return o;
  }

  /** World position of the opening's middle, where molecules come out. */
  function gap(capsule: Capsule, amount: number, out: T.Vector3) {
    const o = smooth(clamp01(amount));
    const shift = ((SLIDE.cap - SLIDE.body) / 2) * o;
    capsule.group.updateMatrixWorld(true);
    out.set((capRim - o * SLIDE.cap + bodyRim + o * SLIDE.body) / 2 + shift, 0, 0);
    return capsule.tilt.localToWorld(out);
  }

  return {
    make,
    open,
    gap,
    dispose() {
      [bodyGeometry, capGeometry, plugGeometry].forEach((geometry) => geometry.dispose());
      [shell, powder].forEach((material) => material.dispose());
    },
  };
}

// ---------------------------------------------------------------------------------------------
// Molecules: real 3D shapes from PubChem, as pearl ball-and-stick models. Oxygen is warm gold,
// nitrogen sky blue, sulfur lime; the whole model is scaled to a radius of 1.

const ATOMS: Record<Element, { r: number; color: string }> = {
  C: { r: 0.34, color: "#efe8da" },
  H: { r: 0.2, color: "#ffffff" },
  O: { r: 0.33, color: "#eaa43a" },
  N: { r: 0.34, color: "#8fbde6" },
  S: { r: 0.45, color: "#d8e070" },
};

export type Molecule = { outer: T.Group; inner: T.Group; dispose: () => void };

export function buildMolecule(three: Three, key: string): Molecule | null {
  const data = molecules.find((molecule) => molecule.key === key);
  if (!data) return null;
  const outer = new three.Group();
  const inner = new three.Group();
  outer.add(inner);

  const atomMaterial = new three.MeshPhysicalMaterial({
    color: "#ffffff",
    roughness: 0.2,
    clearcoat: 1,
    clearcoatRoughness: 0.08,
    sheen: 0.25,
    sheenColor: new three.Color("#fff3dc"),
  });
  const bondMaterial = new three.MeshPhysicalMaterial({
    color: "#e6ddcb",
    roughness: 0.3,
    clearcoat: 0.8,
    clearcoatRoughness: 0.12,
  });

  const sphere = new three.SphereGeometry(1, 24, 16);
  const atoms = new three.InstancedMesh(sphere, atomMaterial, data.atoms.length);
  const matrix = new three.Matrix4();
  const color = new three.Color();
  let bound = 0;
  data.atoms.forEach(([element, x, y, z], i) => {
    const { r, color: hex } = ATOMS[element];
    matrix.makeScale(r, r, r).setPosition(x, y, z);
    atoms.setMatrixAt(i, matrix);
    atoms.setColorAt(i, color.set(hex));
    bound = Math.max(bound, Math.hypot(x, y, z) + r);
  });
  inner.add(atoms);

  const rods: { from: T.Vector3; to: T.Vector3; radius: number }[] = [];
  const up = new three.Vector3(0, 1, 0);
  data.bonds.forEach(([a, b, order]) => {
    const [, ax, ay, az] = data.atoms[a];
    const [, bx, by, bz] = data.atoms[b];
    const from = new three.Vector3(ax, ay, az);
    const to = new three.Vector3(bx, by, bz);
    if (order === 1) {
      rods.push({ from, to, radius: 0.085 });
      return;
    }
    // Double bonds are two thinner rods, side by side.
    const direction = to.clone().sub(from).normalize();
    const side = direction
      .clone()
      .cross(Math.abs(direction.z) < 0.9 ? new three.Vector3(0, 0, 1) : up);
    side.normalize().multiplyScalar(0.11);
    rods.push({ from: from.clone().add(side), to: to.clone().add(side), radius: 0.06 });
    rods.push({ from: from.clone().sub(side), to: to.clone().sub(side), radius: 0.06 });
  });
  const rod = new three.CylinderGeometry(1, 1, 1, 14, 1, true);
  const bonds = new three.InstancedMesh(rod, bondMaterial, rods.length);
  const quaternion = new three.Quaternion();
  const scale = new three.Vector3();
  const middle = new three.Vector3();
  rods.forEach(({ from, to, radius }, i) => {
    const direction = to.clone().sub(from);
    const length = direction.length();
    quaternion.setFromUnitVectors(up, direction.normalize());
    middle.copy(from).add(to).multiplyScalar(0.5);
    scale.set(radius, length, radius);
    matrix.compose(middle, quaternion, scale);
    bonds.setMatrixAt(i, matrix);
  });
  inner.add(bonds);
  inner.scale.setScalar(1 / bound);
  outer.visible = false;

  return {
    outer,
    inner,
    dispose() {
      [sphere, rod].forEach((geometry) => geometry.dispose());
      [atomMaterial, bondMaterial].forEach((material) => material.dispose());
      [atoms, bonds].forEach((mesh) => mesh.dispose());
    },
  };
}

// ---------------------------------------------------------------------------------------------
// Soft contact shadows, drawn in the same scene.

export function createShadows(three: Three, count: number) {
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = 128;
  const context = canvas.getContext("2d")!;
  const gradient = context.createRadialGradient(64, 64, 0, 64, 64, 64);
  gradient.addColorStop(0, "rgba(64,48,28,0.55)");
  gradient.addColorStop(0.55, "rgba(64,48,28,0.16)");
  gradient.addColorStop(1, "rgba(64,48,28,0)");
  context.fillStyle = gradient;
  context.fillRect(0, 0, 128, 128);
  const texture = new three.CanvasTexture(canvas);
  texture.colorSpace = three.SRGBColorSpace;
  const geometry = new three.PlaneGeometry(1, 1);
  const meshes = Array.from({ length: count }, () => {
    const material = new three.MeshBasicMaterial({
      map: texture,
      transparent: true,
      depthWrite: false,
      toneMapped: false,
    });
    const mesh = new three.Mesh(geometry, material);
    mesh.visible = false; // shown once placed
    return mesh;
  });
  return {
    meshes,
    /** Place a shadow under an object of width `len` sitting at (x, y). */
    place(mesh: T.Mesh, x: number, y: number, len: number, strength: number, z = -0.6) {
      mesh.visible = strength > 0.01;
      mesh.position.set(x, y - len * 0.3, z);
      mesh.scale.set(len * 1.15, len * 0.16, 1);
      (mesh.material as T.MeshBasicMaterial).opacity = 0.3 * strength;
    },
    dispose() {
      meshes.forEach((mesh) => (mesh.material as T.Material).dispose());
      geometry.dispose();
      texture.dispose();
    },
  };
}
