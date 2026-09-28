// The product page's 3D bottle (September 25, 2026): the product's real bottle (its approved
// photo's own label, rebuilt by scripts/product-3d/build_bottle.py) alone in a soft studio. The
// opening sets the product's name in the page behind it; the buy chapter shows it on its own.
// Model units: the bottle is 1 tall and stands on y = 0.

import { buildBottle, type BottleData } from "../template-object-bottle";
import { clamp01, createLoop, createViewport, mix, smooth, type Three } from "./rigs";

export type HeroState = {
  /** Arrival when the page opens, 0 → 1. */
  enter: number;
  /** How far the hero has scrolled away, 0 at the top → 1 when it has left the screen. */
  scroll: number;
};

export type HeroScene = {
  state: HeroState;
  /** Resolves once the label and the reflections are in and the first frame is drawn. */
  ready: Promise<void>;
  dispose: () => void;
};

type Compose = {
  fov: number;
  /** Bottle height as a share of the frame height. */
  size: number;
  /** Bottle centre on screen, 0–1 from the left and from the top. */
  at: [number, number];
  /** Camera height above the bottle's middle, in bottle heights (a slight look down). */
  lift: number;
};

// Where the bottle sits, on wide stages and upright ones (rigs.ts: width / height < 0.9). The
// opening's CSS relies on these numbers (template-chapters-hero.module.css).
const COMPOSE: { wide: Compose; tall: Compose } = {
  wide: { fov: 22, size: 0.52, at: [0.5, 0.53], lift: 0.12 },
  tall: { fov: 26, size: 0.44, at: [0.5, 0.66], lift: 0.12 },
};

export function createHeroScene(
  three: Three,
  canvas: HTMLCanvasElement,
  stage: HTMLElement,
  data: BottleData,
  options: { still?: boolean; size?: number },
): HeroScene {
  const state: HeroState = { enter: 0, scroll: 0 };
  let reframe = true;
  const view = createViewport(three, canvas, stage, () => (reframe = true));
  const { renderer, camera } = view;
  renderer.toneMappingExposure = 1.0;

  const scene = new three.Scene();
  const bottle = buildBottle(three, renderer, data);
  const turn = new three.Group(); // the pointer and scroll turn the bottle here
  turn.add(bottle.group);
  scene.add(turn);

  const disposables: { dispose: () => void }[] = [bottle];
  const loads: Promise<unknown>[] = [bottle.ready];

  // The room's soft reflections, so white plastic reads as plastic.
  const pmrem = new three.PMREMGenerator(renderer);
  disposables.push(pmrem);
  loads.push(
    import("three/addons/environments/RoomEnvironment.js").then(({ RoomEnvironment }) => {
      const room = new RoomEnvironment();
      const environment = pmrem.fromScene(room, 0.04).texture;
      disposables.push(environment);
      scene.environment = environment;
      scene.environmentIntensity = 0.6;
      room.dispose();
    }),
  );

  // A soft contact shadow where the bottle meets the floor.
  const contactCanvas = document.createElement("canvas");
  contactCanvas.width = contactCanvas.height = 128;
  const contactContext = contactCanvas.getContext("2d")!;
  const gradient = contactContext.createRadialGradient(64, 64, 0, 64, 64, 64);
  gradient.addColorStop(0, "rgba(40,32,20,0.62)");
  gradient.addColorStop(0.5, "rgba(40,32,20,0.2)");
  gradient.addColorStop(1, "rgba(40,32,20,0)");
  contactContext.fillStyle = gradient;
  contactContext.fillRect(0, 0, 128, 128);
  const contactTexture = new three.CanvasTexture(contactCanvas);
  contactTexture.colorSpace = three.SRGBColorSpace;
  const contactMaterial = new three.MeshBasicMaterial({
    map: contactTexture,
    transparent: true,
    depthWrite: false,
    toneMapped: false,
  });
  const contact = new three.Mesh(new three.PlaneGeometry(1, 1), contactMaterial);
  contact.rotation.x = -Math.PI / 2;
  contact.renderOrder = 1;
  scene.add(contact);
  disposables.push(contactTexture, contactMaterial, contact.geometry);

  // A soft studio: a white key from the upper left, a cool fill, and a warm rim behind.
  const key = new three.DirectionalLight("#ffffff", 2.1);
  key.position.set(-6, 5, 4);
  const fill = new three.DirectionalLight("#dfe9ff", 0.55);
  fill.position.set(6, -1, 4);
  const rim = new three.DirectionalLight("#ffd79a", 1.4);
  rim.position.set(3, 4, -6);
  scene.add(key, fill, rim, new three.AmbientLight("#ffffff", 0.08));

  // ------------------------------------------------------------------------------------------
  // Framing: put the bottle where the composition wants it on this screen's shape.

  const target = new three.Vector3();
  let compose = COMPOSE.wide;
  function frame() {
    const preset = view.portrait ? COMPOSE.tall : COMPOSE.wide;
    compose = options.size ? { ...preset, size: options.size, at: [0.5, 0.5] } : preset;
    camera.fov = compose.fov;
    camera.updateProjectionMatrix();
    const frameHeight = 1 / compose.size;
    const distance = frameHeight / 2 / Math.tan(((compose.fov / 2) * Math.PI) / 180);
    const frameWidth = frameHeight * camera.aspect;
    const base = bottle.group.position;
    // The bottle's middle sits at `at` on screen: move the camera's aim the other way.
    target.set(
      base.x - (compose.at[0] - 0.5) * frameWidth,
      base.y + 0.5 + (compose.at[1] - 0.5) * frameHeight,
      base.z,
    );
    camera.position.set(target.x, target.y + compose.lift, base.z + distance);
    camera.lookAt(target);
    reframe = false;
  }

  // ------------------------------------------------------------------------------------------
  // Motion: the arrival, the pointer and the scroll.

  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
  const onPointer = (event: PointerEvent) => {
    pointer.tx = (event.clientX / window.innerWidth) * 2 - 1;
    pointer.ty = (event.clientY / window.innerHeight) * 2 - 1;
  };
  const finePointer = !view.software && window.matchMedia("(pointer: fine)").matches;
  if (finePointer) window.addEventListener("pointermove", onPointer, { passive: true });

  let lastKey = "";
  let first = true;
  let markReady: () => void = () => undefined;
  const ready = new Promise<void>((resolve) => (markReady = resolve));
  let loaded = false;
  Promise.all(loads).then(() => {
    loaded = true;
    lastKey = "";
  });

  // With reduced motion the bottle holds still, drawn on demand.
  const still = Boolean(options.still);
  function render(now: number) {
    if (reframe) frame();
    const t = still ? 12 : now / 1000;
    pointer.x += (pointer.tx - pointer.x) * 0.05;
    pointer.y += (pointer.ty - pointer.y) * 0.05;
    const enter = smooth(clamp01(state.enter));
    const scroll = clamp01(state.scroll);

    // Arrives with one slow turn, rising into place; scrolling lifts it and turns it a little.
    turn.rotation.y = (1 - enter) * -Math.PI * 1.6 + pointer.x * 0.42 + scroll * 0.55;
    turn.position.y = mix(-0.35, 0, enter) + scroll * 0.35 + Math.sin(t * 0.8) * 0.012;
    turn.scale.setScalar(mix(0.9, 1, enter) * (1 + scroll * 0.18));
    turn.rotation.x = pointer.y * 0.06;
    // The shadow stays on the floor and softens as the bottle lifts.
    const lift = Math.max(0, turn.position.y);
    contact.position.set(0, 0.002, 0);
    contact.scale.set(0.95 + lift, 0.5 + lift * 0.6, 1);
    contactMaterial.opacity = enter * (1 - scroll) * Math.max(0.25, 1 - lift * 1.6);

    // The camera drifts with the pointer; scrolling away rises a little, like stepping back.
    if (!reframe) {
      camera.position.x = target.x + pointer.x * 0.08;
      camera.position.y = target.y + compose.lift + pointer.y * -0.05 + scroll * 0.25;
      camera.lookAt(target.x, target.y + scroll * 0.12, target.z);
    }

    const frameKey = [
      enter.toFixed(3),
      scroll.toFixed(3),
      pointer.x.toFixed(3),
      pointer.y.toFixed(3),
      view.width,
      view.height,
      loaded,
    ].join();
    // Draw only when something changed.
    if (frameKey === lastKey) return;
    lastKey = frameKey;
    renderer.render(scene, camera);
    view.pace(now);
    if (loaded && first) {
      first = false;
      markReady();
    }
  }

  const loop = createLoop(stage, render);

  return {
    state,
    ready,
    dispose() {
      loop.dispose();
      window.removeEventListener("pointermove", onPointer);
      disposables.forEach((item) => item.dispose());
      view.dispose();
    },
  };
}
