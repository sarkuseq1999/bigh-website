// NuriCell's signature moment, second version (September 25, 2026; Mo found the first "very
// plain"). A cutaway on a dark stage, after Seed's sliced-open capsule (Design Vault #040): the
// capsule's front half lifts away, the powder inside is shown as one layer per ingredient, each
// as long as its share of the serving, and the layers then part so each can be met on its own.
// Labels are page elements that follow their layer (leader lines, #040), so they stay crisp and
// readable. Scroll time is in screens; the page writes `state.time`.
// September 28 (Mo: the closed capsule was "boring", and the page never said how the four work
// together): a gold scan band now sweeps the closed capsule and shows the layers through the
// shell, and after each ingredient is met the pieces form a ring and gold links light up between
// the pairs that work together.
// The capsule is hypromellose with titanium dioxide: opaque white, never glass. The layer colours
// only tell the ingredients apart (the powders are white or pale yellow); the page says so.

import type * as T from "three";
import {
  buildMolecule,
  clamp01,
  createLoop,
  createViewport,
  mix,
  smooth,
  type Three,
} from "./rigs";

export type CutawayState = { time: number };

export type CutawayIngredient = { key: string; amount: number; colour: string };

/** Two ingredients that work together, by their index in the ingredient list. */
export type CutawayLink = { from: number; to: number };

/** The script, in screens of scrolling. The page's words use the same marks. */
export function cutawayScript(count: number, links = 0) {
  const FOCUS = 0.72;
  const LINK = 0.9;
  const focusStart = 2.85;
  const afterFocus = focusStart + count * FOCUS;
  const linkStart = afterFocus + (links ? 0.6 : 0);
  const together = linkStart + links * LINK + 0.1;
  return {
    FOCUS,
    LINK,
    arrive: [0, 0.5] as const,
    scan: [0.4, 1.3] as const,
    open: [1.45, 2.0] as const,
    part: [2.1, 2.6] as const,
    focusStart,
    ring: [afterFocus + 0.05, afterFocus + 0.6] as const,
    linkStart,
    links,
    together,
    close: [together + 0.85, together + 1.35] as const,
    trio: [together + 1.4, together + 1.9] as const,
    length: together + 2.4,
  };
}

// A size 0 capsule: about 21.7 mm long and 7.6 mm wide (one unit = 10 mm).
const L = 2.17;
const R = 0.38;
const WALL = 0.03;
const GAP = 0.004;
const DOME = L / 2 - R; // where the round ends begin, along the axis

const band = (time: number, [from, to]: readonly [number, number]) =>
  smooth(clamp01((time - from) / (to - from)));

/** Radius of the capsule's inside at height y along its axis. */
function innerRadius(y: number) {
  const inner = R - WALL - GAP;
  const beyond = Math.abs(y) - DOME;
  return beyond <= 0 ? inner : Math.sqrt(Math.max(0, inner * inner - beyond * beyond));
}

function grainTexture(three: Three) {
  const size = 256;
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = size;
  const context = canvas.getContext("2d")!;
  const image = context.createImageData(size, size);
  for (let i = 0; i < size * size; i++) {
    const v = 110 + Math.random() * 40;
    image.data.set([v, v, v, 255], i * 4);
  }
  context.putImageData(image, 0, 0);
  const texture = new three.CanvasTexture(canvas);
  texture.wrapS = texture.wrapT = three.RepeatWrapping;
  texture.repeat.set(5, 5);
  return texture;
}

export function createCutawayScene(
  three: Three,
  canvas: HTMLCanvasElement,
  stage: HTMLElement,
  ingredients: CutawayIngredient[],
  labels: (HTMLElement | null)[],
  links: CutawayLink[] = [],
) {
  const state: CutawayState = { time: 0 };
  const script = cutawayScript(ingredients.length, links.length);
  let lastKey = "";
  const view = createViewport(three, canvas, stage, () => (lastKey = ""));
  const { renderer, camera } = view;
  renderer.toneMappingExposure = 1.05;
  renderer.localClippingEnabled = true;
  const scene = new three.Scene();
  const disposables: { dispose: () => void }[] = [];

  // Light: a warm key from the upper left, a gold rim behind, a cool fill, soft reflections.
  const pmrem = new three.PMREMGenerator(renderer);
  disposables.push(pmrem);
  import("three/addons/environments/RoomEnvironment.js").then(({ RoomEnvironment }) => {
    const room = new RoomEnvironment();
    const environment = pmrem.fromScene(room, 0.04).texture;
    disposables.push(environment);
    scene.environment = environment;
    scene.environmentIntensity = 0.42;
    room.dispose();
    lastKey = "";
  });
  const key = new three.DirectionalLight("#fff1dc", 2.1);
  key.position.set(-3, 4, 5);
  const rim = new three.DirectionalLight("#ffc46b", 2.6);
  rim.position.set(3.5, 2.5, -4);
  const fill = new three.DirectionalLight("#9fb8ff", 0.55);
  fill.position.set(4, -3, 3);
  const glow = new three.PointLight("#ffb347", 0, 3.2, 2);
  // Light carried by the scan band, so the layers it reveals glow from within.
  const scanLight = new three.PointLight("#ffd28a", 0, 2.4, 2);
  scene.add(scanLight);
  scene.add(key, rim, fill, glow, new three.AmbientLight("#b8c6ff", 0.12));

  // The capsule, built along the y axis, then laid down (or left standing on tall screens).
  const holder = new three.Group(); // screen placement and the slow turn
  const axis = new three.Group(); // capsule axis: y
  holder.add(axis);
  scene.add(holder);

  const shellMaterial = new three.MeshPhysicalMaterial({
    color: "#f7f4ee",
    roughness: 0.36,
    clearcoat: 0.55,
    clearcoatRoughness: 0.22,
    sheen: 0.45,
    sheenRoughness: 0.5,
    sheenColor: new three.Color("#ffffff"),
    side: three.DoubleSide,
    transparent: true,
  });
  // The halves fade on their own (the front lifts away, the back steps aside), so each has its
  // own copy; the three whole capsules at the end use the original.
  const frontMaterial = shellMaterial.clone();
  const backMaterial = shellMaterial.clone();
  disposables.push(shellMaterial, frontMaterial, backMaterial);

  // The scan: a band that slides along the closed capsule. Inside the band the shell turns to a
  // faint ghost so the layers show through; the rest stays opaque. Clipping planes, in world
  // space, set each frame: the opaque shell keeps what lies outside the band (either side), the
  // ghost keeps what lies inside it.
  const keepBelowA = new three.Plane();
  const keepAboveB = new three.Plane();
  const keepAboveA = new three.Plane();
  const keepBelowB = new three.Plane();
  [frontMaterial, backMaterial].forEach((material) => {
    material.clippingPlanes = [keepBelowA, keepAboveB];
    material.clipIntersection = true;
  });
  const ghostMaterial = new three.MeshPhysicalMaterial({
    color: "#eaf1ff",
    roughness: 0.2,
    transparent: true,
    opacity: 0.1,
    depthWrite: false,
    side: three.DoubleSide,
    clippingPlanes: [keepAboveA, keepBelowB],
  });
  const scanMaterial = new three.MeshBasicMaterial({ color: "#ffd78f", toneMapped: false });
  const scanHaloMaterial = new three.MeshBasicMaterial({
    color: "#ffc466",
    transparent: true,
    opacity: 0.28,
    depthWrite: false,
    toneMapped: false,
    blending: three.AdditiveBlending,
  });
  disposables.push(ghostMaterial, scanMaterial, scanHaloMaterial);

  // Shell profile: outer skin from tip to tip, then the inner skin back down.
  const shellPoints: T.Vector2[] = [];
  const steps = 24;
  for (let i = 0; i <= steps; i++) {
    const a = (i / steps) * (Math.PI / 2);
    shellPoints.push(new three.Vector2(Math.sin(a) * R, -DOME - Math.cos(a) * R));
  }
  for (let i = 0; i <= steps; i++) {
    const a = (i / steps) * (Math.PI / 2);
    shellPoints.push(new three.Vector2(Math.cos(a) * R, DOME + Math.sin(a) * R));
  }
  const inner = R - WALL;
  for (let i = 0; i <= steps; i++) {
    const a = (i / steps) * (Math.PI / 2);
    shellPoints.push(new three.Vector2(Math.sin(a) * inner, DOME + Math.cos(a) * inner));
  }
  for (let i = 0; i <= steps; i++) {
    const a = (i / steps) * (Math.PI / 2);
    shellPoints.push(new three.Vector2(Math.cos(a) * inner, -DOME - Math.sin(a) * inner));
  }
  // The flat face where the shell is cut: its outline with the inside cut out.
  const outline = (radius: number) => {
    const shape = new three.Shape();
    shape.absarc(0, DOME, radius, 0, Math.PI, false);
    shape.absarc(0, -DOME, radius, Math.PI, Math.PI * 2, false);
    shape.closePath();
    return shape;
  };
  const cutShape = outline(R);
  cutShape.holes.push(outline(inner) as unknown as T.Path);
  const cutGeometry = new three.ShapeGeometry(cutShape, 24);
  // Lathe: vertex = (sin φ · r, y, cos φ · r). The back half is φ ∈ [π, 2π] (x ≤ 0), its cut face
  // at x = 0 looking along +x; the axis group turns +x toward the camera.
  const backGeometry = new three.LatheGeometry(shellPoints, 64, Math.PI, Math.PI);
  const frontGeometry = new three.LatheGeometry(shellPoints, 64, 0, Math.PI);
  disposables.push(cutGeometry, backGeometry, frontGeometry);
  const back = new three.Group();
  const front = new three.Group();
  back.add(new three.Mesh(backGeometry, backMaterial));
  front.add(new three.Mesh(frontGeometry, frontMaterial));
  const backCut = new three.Mesh(cutGeometry, backMaterial);
  backCut.rotation.y = Math.PI / 2; // shape plane → the x = 0 plane, facing +x
  back.add(backCut);
  const frontCut = new three.Mesh(cutGeometry, frontMaterial);
  frontCut.rotation.y = -Math.PI / 2;
  front.add(frontCut);
  back.add(new three.Mesh(backGeometry, ghostMaterial));
  front.add(new three.Mesh(frontGeometry, ghostMaterial));
  axis.add(back, front);
  // The band's two edges: thin gold rings round the capsule, with a soft halo.
  const ringGeometry = new three.TorusGeometry(R * 1.03, 0.007, 8, 128);
  const haloGeometry = new three.TorusGeometry(R * 1.03, 0.03, 8, 128);
  disposables.push(ringGeometry, haloGeometry);
  const scanRings = [0, 1].map(() => {
    const ring = new three.Group();
    ring.add(
      new three.Mesh(ringGeometry, scanMaterial),
      new three.Mesh(haloGeometry, scanHaloMaterial),
    );
    ring.rotation.x = Math.PI / 2; // the torus's axis along the capsule's
    ring.visible = false;
    axis.add(ring);
    return ring;
  });

  // The fill: one half-solid per ingredient, each as long as its share of the serving.
  const grain = grainTexture(three);
  disposables.push(grain);
  const total = ingredients.reduce((sum, item) => sum + item.amount, 0) || 1;
  const top = L / 2 - WALL - GAP;
  const span = top * 2;
  let cursor = -top;
  const layers = ingredients.map((item) => {
    const y0 = cursor;
    const y1 = cursor + (span * item.amount) / total;
    cursor = y1;
    // Profile: axis → out along the lower face → up the side → in along the upper face.
    const points: T.Vector2[] = [new three.Vector2(0, y0)];
    const r0 = innerRadius(y0);
    points.push(new three.Vector2(r0, y0), new three.Vector2(r0, y0));
    const rows = 28;
    for (let i = 1; i < rows; i++) {
      const y = mix(y0, y1, i / rows);
      points.push(new three.Vector2(innerRadius(y), y));
    }
    const r1 = innerRadius(y1);
    points.push(new three.Vector2(r1, y1), new three.Vector2(r1, y1), new three.Vector2(0, y1));
    const material = new three.MeshStandardMaterial({
      color: item.colour,
      roughness: 0.98,
      bumpMap: grain,
      bumpScale: 2.2,
      transparent: true,
    });
    const body = new three.LatheGeometry(points, 48, Math.PI, Math.PI);
    // The cut face: the layer's outline in the x = 0 plane.
    const face = new three.Shape();
    face.moveTo(-r0, y0);
    for (let i = 0; i <= rows; i++) {
      const y = mix(y0, y1, i / rows);
      face.lineTo(-innerRadius(y), y);
    }
    for (let i = rows; i >= 0; i--) {
      const y = mix(y0, y1, i / rows);
      face.lineTo(innerRadius(y), y);
    }
    face.closePath();
    const faceGeometry = new three.ShapeGeometry(face);
    const group = new three.Group();
    group.add(new three.Mesh(body, material));
    const faceMesh = new three.Mesh(faceGeometry, material);
    faceMesh.rotation.y = Math.PI / 2;
    group.add(faceMesh);
    axis.add(group);
    disposables.push(material, body, faceGeometry);
    return {
      group,
      material,
      centre: (y0 + y1) / 2,
      length: y1 - y0,
      base: new three.Color(item.colour),
    };
  });

  // Each ingredient's molecule, shown while its layer is being met.
  const molecules = ingredients.map((item) => {
    const molecule = buildMolecule(three, item.key);
    if (molecule) {
      scene.add(molecule.outer);
      disposables.push(molecule);
    }
    return molecule;
  });

  // How they work together: gold links between the pieces once they stand in a ring. Each link
  // is a bright core and a soft halo, drawn out from one piece to the other, with a bead of light
  // that travels along it while its pair is being explained.
  const rodGeometry = new three.CylinderGeometry(1, 1, 1, 12, 1, true);
  const beadGeometry = new three.SphereGeometry(1, 16, 12);
  const linkCore = new three.MeshBasicMaterial({ color: "#ffe2a8", toneMapped: false });
  const linkHalo = new three.MeshBasicMaterial({
    color: "#ffb84d",
    transparent: true,
    opacity: 0.22,
    depthWrite: false,
    toneMapped: false,
    blending: three.AdditiveBlending,
  });
  disposables.push(rodGeometry, beadGeometry, linkCore, linkHalo);
  const linkMeshes = links.map(() => {
    const core = new three.Mesh(rodGeometry, linkCore);
    const halo = new three.Mesh(rodGeometry, linkHalo);
    const bead = new three.Mesh(beadGeometry, linkCore);
    [core, halo, bead].forEach((mesh) => {
      mesh.visible = false;
      scene.add(mesh);
    });
    return { core, halo, bead };
  });
  // The ring's order follows the links: the first pair, then whoever joins next, then the rest.
  const ringOrder: number[] = [];
  links.forEach(({ from, to }) => {
    [from, to].forEach((index) => {
      if (!ringOrder.includes(index)) ringOrder.push(index);
    });
  });
  ingredients.forEach((_, index) => {
    if (!ringOrder.includes(index)) ringOrder.push(index);
  });

  // Three whole capsules for the daily serving at the end.
  const trio = [0, 1].map(() => {
    const group = new three.Group();
    group.add(
      new three.Mesh(backGeometry, shellMaterial),
      new three.Mesh(frontGeometry, shellMaterial),
    );
    group.visible = false;
    scene.add(group);
    return group;
  });

  // ------------------------------------------------------------------------------------------

  let tall = false;
  let unit = 1; // world units per screen height at the capsule
  function layout() {
    tall = view.portrait;
    camera.fov = tall ? 30 : 26;
    camera.position.set(0, 0, 9);
    camera.lookAt(0, 0, 0);
    camera.updateProjectionMatrix();
    unit = 2 * 9 * Math.tan(((camera.fov / 2) * Math.PI) / 180);
  }

  const tmp = new three.Vector3();
  const other = new three.Vector3();
  const axisDir = new three.Vector3(); // the capsule's length, in world space
  let running = true;
  let laidOutFor = "";

  /** A layer's edge on screen: the end of its cut face that sits highest (or rightmost). */
  function anchor(index: number) {
    const layer = layers[index];
    const radius = innerRadius(layer.centre) * 0.96;
    tmp.set(0, layer.centre, radius).applyMatrix4(layer.group.matrixWorld);
    other.set(0, layer.centre, -radius).applyMatrix4(layer.group.matrixWorld);
    tmp.project(camera);
    other.project(camera);
    const pick = tall ? (tmp.x > other.x ? tmp : other) : tmp.y > other.y ? tmp : other;
    return {
      x: ((pick.x + 1) / 2) * view.width,
      y: ((1 - pick.y) / 2) * view.height,
      index,
    };
  }

  function render(now: number) {
    if (!running) return;
    const shape = `${view.width}x${view.height}`;
    if (shape !== laidOutFor) {
      layout();
      laidOutFor = shape;
    }
    const t = state.time;
    const clock = now / 1000;
    const arrive = band(t, script.arrive);
    const open = band(t, script.open) * (1 - band(t, script.close));
    const part =
      band(t, script.part) * (1 - band(t, [script.together + 0.35, script.together + 0.8]));
    const trioIn = band(t, script.trio);
    const ringIn = script.links
      ? band(t, script.ring) * (1 - band(t, [script.together + 0.3, script.together + 0.8]))
      : 0;
    // Each link: drawn out as its turn begins, and highlighted while it is being explained.
    const linkState = links.map((_, index) => {
      const start = script.linkStart + index * script.LINK;
      return {
        drawn: band(t, [start, start + 0.3]) * ringIn,
        lit:
          band(t, [start, start + 0.2]) *
          (1 - band(t, [start + script.LINK - 0.15, start + script.LINK])),
      };
    });
    const anyLit = Math.max(0, ...linkState.map((link) => link.lit));

    // Which layer is being met, and how much (0–1, rising and falling within its screen).
    const focus = ingredients.map((_, index) => {
      const start = script.focusStart + index * script.FOCUS;
      return (
        band(t, [start, start + 0.22]) *
        (1 - band(t, [start + script.FOCUS - 0.18, start + script.FOCUS + 0.04]))
      );
    });
    const anyFocus = Math.max(0, ...focus);

    // Size and place: lying down right of centre on wide screens (the words sit left), standing
    // in the upper part of tall ones (the words sit below). Parted, it shrinks a little to fit.
    const screenW = unit * camera.aspect;
    const length = tall ? unit * 0.4 : Math.min(screenW * 0.4, unit * 0.66);
    holder.scale.setScalar(
      (length / L) * mix(0.72, 1, arrive) * (1 - part * (tall ? 0.28 : 0.24)) * (1 - trioIn * 0.34),
    );
    holder.position.set(screenW * (tall ? -0.16 : 0.2), tall ? unit * 0.15 : -unit * 0.02, 0);
    // A three-quarter view: the capsule's length recedes a little and we look down onto the cut.
    const drift = Math.sin(clock * 0.35) * 0.035;
    if (tall) holder.rotation.set(0.22, 0, 0.1);
    else holder.rotation.set(0.1, mix(-0.9, -0.32, arrive) + drift, Math.PI / 2);
    axis.rotation.y = -Math.PI / 2 + mix(-2.2, 0, arrive) + mix(0.15, 0.62, open) + drift;

    // The scan band slides from one end of the closed capsule to the other.
    const scan = band(t, script.scan);
    const bandHalf = 0.38;
    const scanning = scan > 0.001 && scan < 0.999 && open < 0.01;
    // Left to right on wide screens, top to bottom on tall ones (the axis points left / up).
    const centre = mix(L / 2 + bandHalf, -L / 2 - bandHalf, scan);
    const a = scanning ? centre - bandHalf : 99;
    const b = scanning ? centre + bandHalf : 99;
    holder.updateMatrixWorld(true);
    const along = axisDir.set(0, 1, 0).transformDirection(axis.matrixWorld);
    const pointA = tmp.set(0, a, 0).applyMatrix4(axis.matrixWorld);
    keepBelowA.setFromNormalAndCoplanarPoint(along.clone().negate(), pointA);
    keepAboveA.setFromNormalAndCoplanarPoint(along, pointA);
    const pointB = tmp.set(0, b, 0).applyMatrix4(axis.matrixWorld);
    keepAboveB.setFromNormalAndCoplanarPoint(along, pointB);
    keepBelowB.setFromNormalAndCoplanarPoint(along.clone().negate(), pointB);
    scanLight.intensity = scanning ? 2.6 * Math.sin(Math.PI * scan) : 0;
    if (scanning) {
      scanLight.position.copy(tmp.set(0.5, centre, 0).applyMatrix4(axis.matrixWorld));
    }
    scanRings.forEach((ring, index) => {
      const y = index === 0 ? a : b;
      ring.visible = scanning && Math.abs(y) < L / 2 - 0.02;
      ring.position.set(0, y, 0);
      const radius = innerRadius(y) + WALL + GAP + 0.004;
      ring.scale.setScalar(Math.max(0.05, radius / (R * 1.03)));
    });

    // The front half lifts off toward the viewer and fades; the back half fades while the
    // layers stand free, and both return to close the capsule.
    front.position.set(open * 0.55, 0, 0);
    frontMaterial.opacity = 1 - smooth(clamp01((open - 0.1) / 0.45));
    front.visible = frontMaterial.opacity > 0.01;
    backMaterial.opacity = 1 - part;
    backMaterial.depthWrite = backMaterial.opacity > 0.98;
    back.visible = backMaterial.opacity > 0.01;

    // Layers part along the axis; the one being met comes forward and the rest step back.
    // Later they stand in a ring (corners of a soft rectangle, in the links' order) so the links
    // between them can be drawn.
    const gapSize = 0.36;
    let offset = -((layers.length - 1) * gapSize) / 2;
    holder.updateMatrixWorld(true);
    // The ring: right of centre beside the words on wide screens; centred in the upper half, a
    // little smaller, on tall ones (the words sit below).
    const ringScale = mix(1, tall ? 0.66 : 1, ringIn);
    const ringCentreX = tall ? 0 : holder.position.x;
    const ringCentreY = tall ? unit * 0.27 : holder.position.y;
    const ringX = tall ? screenW * 0.25 : unit * 0.22;
    const ringY = tall ? unit * 0.08 : unit * 0.18;
    const corners = [
      [-1, 1],
      [1, 1],
      [1, -1],
      [-1, -1],
    ];
    layers.forEach((layer, index) => {
      const f = focus[index];
      const scale = (1 + f * 0.1 + ringIn * 0.08) * ringScale;
      tmp.set(f * 0.75, offset * part, 0);
      if (ringIn > 0.001) {
        const slot = ringOrder.indexOf(index);
        const corner = corners[slot % corners.length];
        const spread = 1 + Math.floor(slot / corners.length) * 0.35;
        const world = other.set(
          ringCentreX + corner[0] * ringX * spread,
          ringCentreY + corner[1] * ringY * spread,
          holder.position.z,
        );
        const local = axis.worldToLocal(world);
        local.y -= layer.centre * scale;
        tmp.lerp(local, ringIn);
      }
      layer.group.position.copy(tmp);
      layer.group.scale.setScalar(scale);
      const linked = linkState.reduce(
        (sum, link, n) => sum + (links[n].from === index || links[n].to === index ? link.lit : 0),
        0,
      );
      layer.material.opacity =
        (1 - anyFocus * (1 - f) * 0.8) * (1 - anyLit * (1 - Math.min(1, linked)) * 0.45);
      layer.group.rotation.y = f * 0.35;
      layer.material.depthWrite = layer.material.opacity > 0.98;
      offset += gapSize;
    });

    // The links, from one piece's edge to the other's.
    if (links.length) scene.updateMatrixWorld(true);
    links.forEach((link, index) => {
      const { core, halo, bead } = linkMeshes[index];
      const { drawn, lit } = linkState[index];
      const show = drawn > 0.01;
      core.visible = halo.visible = show;
      bead.visible = show && lit > 0.05;
      if (!show) return;
      const start = new three.Vector3(0, layers[link.from].centre, 0).applyMatrix4(
        layers[link.from].group.matrixWorld,
      );
      const end = new three.Vector3(0, layers[link.to].centre, 0).applyMatrix4(
        layers[link.to].group.matrixWorld,
      );
      const direction = end.clone().sub(start);
      const full = direction.length();
      direction.normalize();
      // Keep clear of the pieces: stop short by about each piece's half size, which is wide
      // across and slim up and down.
      const lengthwise = Math.min(1, Math.abs(direction.dot(axisDir)));
      const inset =
        holder.scale.x *
        ringScale *
        (0.58 * lengthwise + 0.3 * Math.sqrt(1 - lengthwise * lengthwise));
      const from = start.clone().addScaledVector(direction, inset);
      const length = Math.max(0.001, full - inset * 2) * drawn;
      const middle = from.clone().addScaledVector(direction, length / 2);
      const quaternion = new three.Quaternion().setFromUnitVectors(
        new three.Vector3(0, 1, 0),
        direction,
      );
      const thin = holder.scale.x * ringScale * (0.012 + lit * 0.006);
      core.position.copy(middle);
      core.quaternion.copy(quaternion);
      core.scale.set(thin, length, thin);
      halo.position.copy(middle);
      halo.quaternion.copy(quaternion);
      halo.scale.set(thin * 3.2, length, thin * 3.2);
      (halo.material as T.MeshBasicMaterial).opacity = 0.16 + anyLit * 0.12;
      const travel = (clock * 0.55) % 1;
      bead.position.copy(from).addScaledVector(direction, length * travel);
      bead.scale.setScalar(holder.scale.x * ringScale * 0.035 * lit);
    });
    const focused = focus.indexOf(anyFocus);
    if (anyFocus > 0.01 && focused >= 0) {
      scene.updateMatrixWorld(true);
      tmp.set(0, layers[focused].centre, 0).applyMatrix4(layers[focused].group.matrixWorld);
      glow.position.set(tmp.x - 0.2, tmp.y + 0.6, tmp.z + 1.2);
    }
    glow.intensity = anyFocus * 3;

    // The layer being met shows its molecule above it, turning slowly: its real shape, from
    // PubChem (rigs.ts), in pearl and gold.
    molecules.forEach((molecule, index) => {
      if (!molecule) return;
      const f = focus[index];
      molecule.outer.visible = f > 0.01;
      if (!molecule.outer.visible) return;
      tmp.set(0, layers[index].centre, 0).applyMatrix4(layers[index].group.matrixWorld);
      const lift = holder.scale.x * (tall ? 0.9 : 0.95);
      molecule.outer.position.set(
        tmp.x + (tall ? holder.scale.x * 1.25 : 0),
        tmp.y + (tall ? 0 : lift) + (1 - f) * -0.15,
        tmp.z + 0.4,
      );
      molecule.outer.scale.setScalar(holder.scale.x * 0.5 * mix(0.7, 1, f));
      molecule.inner.rotation.set(0.35, clock * 0.45 + index, 0.1);
      molecule.inner.traverse((node) => {
        const mesh = node as T.Mesh;
        if (!mesh.isMesh) return;
        const material = mesh.material as T.MeshPhysicalMaterial;
        material.transparent = true;
        material.opacity = f;
      });
    });

    // The daily serving: the capsule closes and two more join it.
    // Three in a loose row, each at its own angle, like capsules set down on a table.
    trio.forEach((group, index) => {
      const side = index === 0 ? -1 : 1;
      group.visible = trioIn > 0.01;
      group.scale.setScalar(holder.scale.x);
      const spread = unit * (tall ? 0.15 : 0.19) * trioIn;
      group.position.set(
        holder.position.x + (tall ? side * spread * 0.9 : side * spread * 0.35),
        holder.position.y + (tall ? side * -0.02 : side * spread) - (1 - trioIn) * 0.3,
        -0.4 + side * 0.2,
      );
      group.rotation.set(
        holder.rotation.x + side * 0.08,
        holder.rotation.y + side * 0.28,
        holder.rotation.z + (tall ? side * 0.35 : side * 0.12),
      );
    });

    // Callouts: once the layers have parted, each gets a label in an even row above them (a
    // column beside them on tall screens) with a leader line down to its layer. In the ring,
    // each piece's name sits just outside it instead, with no leader.
    const showLabels =
      part * (1 - anyFocus) * (1 - band(t, [script.together + 0.3, script.together + 0.6]));
    if (scanning) {
      scene.updateMatrixWorld(true);
      const pixels = view.height / unit; // screen pixels per world unit at the capsule
      const radius = R * holder.scale.x * pixels;
      // One name at a time: the layer under the band's middle.
      const current = layers.findIndex(
        (layer) => Math.abs(centre - layer.centre) <= layer.length / 2,
      );
      layers.forEach((layer, index) => {
        const label = labels[index];
        if (!label) return;
        const half = layer.length / 2;
        const inside = index === current ? 1 : 0;
        if (inside <= 0.01) {
          label.style.opacity = "0";
          return;
        }
        const y = Math.min(layer.centre + half, Math.max(layer.centre - half, centre));
        tmp.set(0, y, 0).applyMatrix4(axis.matrixWorld).project(camera);
        const px = ((tmp.x + 1) / 2) * view.width;
        const py = ((1 - tmp.y) / 2) * view.height;
        const ax = tall ? px + radius : px;
        const ay = tall ? py : py - radius;
        const sx = tall ? ax + 44 : ax;
        const sy = tall ? ay : ay - 70;
        label.style.transform = `translate3d(${sx.toFixed(1)}px, ${sy.toFixed(1)}px, 0)`;
        label.style.setProperty("--len", `${Math.hypot(ax - sx, ay - sy).toFixed(1)}px`);
        label.style.setProperty("--angle", `${Math.atan2(ay - sy, ax - sx).toFixed(4)}rad`);
        label.style.opacity = inside.toFixed(3);
        label.dataset.side = tall ? "right" : "up";
      });
    } else if (ringIn > 0.85 && showLabels > 0.001) {
      scene.updateMatrixWorld(true);
      tmp.set(ringCentreX, ringCentreY, holder.position.z).project(camera);
      const cx = ((tmp.x + 1) / 2) * view.width;
      const cy = ((1 - tmp.y) / 2) * view.height;
      layers.forEach((layer, index) => {
        const label = labels[index];
        if (!label) return;
        tmp.set(0, layer.centre, 0).applyMatrix4(layer.group.matrixWorld).project(camera);
        const x = ((tmp.x + 1) / 2) * view.width;
        const y = ((1 - tmp.y) / 2) * view.height;
        const below = y > cy;
        const sy = y + (below ? 1 : -1) * (tall ? 34 : 78);
        const sx = x + (x > cx ? 1 : -1) * (tall ? 8 : 0);
        label.style.transform = `translate3d(${sx.toFixed(1)}px, ${sy.toFixed(1)}px, 0)`;
        label.style.setProperty("--len", "0px");
        label.style.opacity = (((ringIn - 0.85) / 0.15) * showLabels).toFixed(3);
        label.dataset.side = below ? "ring-below" : "ring-above";
        // Tall screens have little room: the name only.
        label.dataset.compact = tall ? "true" : "false";
      });
    } else if (showLabels > 0.001) {
      scene.updateMatrixWorld(true);
      const anchors = layers.map((_, index) => anchor(index));
      const order = [...anchors].sort((a, b) => (tall ? a.y - b.y : a.x - b.x));
      const slots = order.length;
      const first = tall ? order[0].y : order[0].x;
      const last = tall ? order[slots - 1].y : order[slots - 1].x;
      const spacing = Math.max(tall ? 70 : 170, slots > 1 ? (last - first) / (slots - 1) : 0);
      const middle = (first + last) / 2;
      const line = tall
        ? Math.max(...anchors.map((item) => item.x)) + 36
        : Math.min(...anchors.map((item) => item.y)) - 86;
      order.forEach((item, rank) => {
        const label = labels[item.index];
        if (!label) return;
        const along = middle + (rank - (slots - 1) / 2) * spacing;
        const sx = tall ? line : along;
        const sy = tall ? along : line;
        const dx = item.x - sx;
        const dy = item.y - sy;
        label.style.transform = `translate3d(${sx.toFixed(1)}px, ${sy.toFixed(1)}px, 0)`;
        label.style.setProperty("--len", `${Math.hypot(dx, dy).toFixed(1)}px`);
        label.style.setProperty("--angle", `${Math.atan2(dy, dx).toFixed(4)}rad`);
        label.style.opacity = (showLabels * (1 - ringIn * 2)).toFixed(3);
        label.dataset.side = tall ? "right" : "up";
      });
    } else {
      labels.forEach((label) => {
        if (label) label.style.opacity = "0";
      });
    }

    const keyNow = [t.toFixed(4), view.width, view.height, Math.round(clock * 30)].join();
    if (keyNow === lastKey && view.software) return;
    lastKey = keyNow;
    renderer.render(scene, camera);
    view.pace(now);
  }

  const loop = createLoop(stage, render);

  return {
    state,
    dispose() {
      running = false;
      loop.dispose();
      disposables.forEach((item) => item.dispose());
      view.dispose();
    },
  };
}

export type CutawayScene = ReturnType<typeof createCutawayScene>;
