// A product bottle rebuilt in 3D from its approved front photo (scripts/product-3d/build_bottle.py):
// the outline becomes a turned plastic body, the printed label is the photo's own artwork
// unwrapped onto a sleeve, and the ribbed cap is a separate part that can unscrew.
// Model units: the bottle is 1 tall, standing on y = 0.

import type * as T from "three";
import advancedOpc from "./bottles/advanced-opc.json";
import greenBeePropolis from "./bottles/green-bee-propolis.json";
import natureCalm from "./bottles/nature-calm.json";
import nuricell from "./bottles/nuricell.json";
import turmerific from "./bottles/turmerific.json";
import type { Three } from "./signature/rigs";

export type BottleData = typeof nuricell;

// One file per product under bottles/, written by build_bottle.py. A product whose file is still
// `null` has no 3D bottle yet, and its pages show the approved photo instead.
export const bottles: Record<string, BottleData> = Object.fromEntries(
  ([nuricell, greenBeePropolis, advancedOpc, turmerific, natureCalm] as (BottleData | null)[])
    .filter((bottle): bottle is BottleData => bottle !== null)
    .map((bottle) => [bottle.slug, bottle]),
);

export type Bottle = {
  group: T.Group;
  /** The cap's pivot: lift and turn it to open the bottle. */
  cap: T.Group;
  /** Height of the neck's rim, where a capsule comes out (model units). */
  rim: number;
  width: number;
  capHeight: number;
  ready: Promise<void>;
  dispose: () => void;
};

function resample(profile: number[][], from: number, to: number, steps: number) {
  // profile rows are [height, radius], top to bottom; return bottom-to-top evenly spaced points.
  const rows = [...profile].sort((a, b) => a[0] - b[0]);
  const radiusAt = (y: number) => {
    for (let i = 1; i < rows.length; i++) {
      if (rows[i][0] >= y) {
        const [y0, r0] = rows[i - 1];
        const [y1, r1] = rows[i];
        return r0 + ((r1 - r0) * (y - y0)) / Math.max(1e-6, y1 - y0);
      }
    }
    return rows[rows.length - 1][1];
  };
  return Array.from({ length: steps + 1 }, (_, i) => {
    const y = from + ((to - from) * i) / steps;
    return [y, radiusAt(y)];
  });
}

function ribTexture(three: Three) {
  // The cap's grip, as a bump map around its side, drawn after the approved photo (Mo, Sept 25):
  // flat ribs split by thin grooves, stopping short of a plain band at the bottom and a plain rim
  // at the top. The canvas's top row is the cap's top (textures are flipped on upload).
  const canvas = document.createElement("canvas");
  canvas.width = 2048;
  canvas.height = 128;
  const context = canvas.getContext("2d")!;
  context.fillStyle = "rgb(200,200,200)";
  context.fillRect(0, 0, canvas.width, canvas.height);
  const ribs = 72;
  const pitch = canvas.width / ribs;
  const top = Math.round(canvas.height * 0.05);
  const bottom = Math.round(canvas.height * 0.8);
  for (let x = 0; x < canvas.width; x++) {
    // Distance from the groove's centre, in rib widths: a groove about a fifth of a rib wide.
    const phase = (x % pitch) / pitch;
    const d = Math.min(phase, 1 - phase) / 0.11;
    const depth = d >= 1 ? 0 : 0.5 + 0.5 * Math.cos(d * Math.PI);
    const shade = Math.round(200 - 150 * depth);
    context.fillStyle = `rgb(${shade},${shade},${shade})`;
    context.fillRect(x, top, 1, bottom - top);
  }
  const bump = new three.CanvasTexture(canvas);
  bump.wrapS = three.RepeatWrapping;
  // The same grooves as a colour map: white, with the grooves a soft grey.
  const shadeCanvas = document.createElement("canvas");
  shadeCanvas.width = canvas.width;
  shadeCanvas.height = canvas.height;
  const shadeContext = shadeCanvas.getContext("2d")!;
  shadeContext.drawImage(canvas, 0, 0);
  const pixels = shadeContext.getImageData(0, 0, canvas.width, canvas.height);
  for (let i = 0; i < pixels.data.length; i += 4) {
    const depth = (200 - pixels.data[i]) / 150; // 0 flat, 1 deepest
    const value = Math.round(255 - 62 * Math.max(0, depth));
    pixels.data[i] = pixels.data[i + 1] = pixels.data[i + 2] = value;
  }
  shadeContext.putImageData(pixels, 0, 0);
  const shade = new three.CanvasTexture(shadeCanvas);
  shade.wrapS = three.RepeatWrapping;
  shade.colorSpace = three.SRGBColorSpace;
  return { bump, shade };
}

export function buildBottle(
  three: Three,
  renderer: T.WebGLRenderer,
  data: BottleData,
  options: {
    /** A little of the label's own colour that no light can tint. */
    labelGlow?: number;
    /**
     * A counter-tint, like a photographer's gel: under a golden sun a slightly cool plastic and
     * label read as true white and true blue again.
     */
    plasticColor?: string;
    labelTint?: string;
  } = {},
): Bottle {
  const group = new three.Group();
  // Tuned against the approved photo (Mo, September 25: the first 3D bottle read "washed out"):
  // a soft satin plastic whose sides fall into grey, and a label with only a thin gloss, so its
  // navy and cyan stay as deep as the print.
  const plastic = new three.MeshPhysicalMaterial({
    color: options.plasticColor ?? "#f2f3f4",
    roughness: 0.4,
    clearcoat: 0.18,
    clearcoatRoughness: 0.3,
    envMapIntensity: 0.7,
  });
  const ribs = ribTexture(three);
  // The cap is glossier than the body, so its ribs catch the light in stripes, as in the photo.
  const capSide = plastic.clone();
  capSide.roughness = 0.24;
  capSide.clearcoat = 0.45;
  capSide.clearcoatRoughness = 0.2;
  capSide.bumpMap = ribs.bump;
  capSide.bumpScale = 2.2;
  // The grooves also take a little less light, so they read on the sunlit side too.
  capSide.map = ribs.shade;
  const inside = new three.MeshStandardMaterial({
    color: "#d9d6cf",
    roughness: 0.9,
    side: three.BackSide,
  });
  const opening = new three.MeshBasicMaterial({ color: "#3a3833" });

  // Body: the photo's outline from the base up to the neck, then the threaded neck under the cap.
  const capBottom = data.cap.bottom;
  const capTop = data.cap.top;
  const neckR = data.neck.radius;
  const rim = capTop - 0.025;
  const outline = resample(data.profile, 0.004, data.neck.top, 120);
  const bodyPoints = [
    new three.Vector2(0, 0),
    ...outline.map(([y, r]) => new three.Vector2(r, y)),
    new three.Vector2(neckR, capBottom + 0.004),
    new three.Vector2(neckR * 0.985, rim - 0.006),
    new three.Vector2(neckR * 0.94, rim),
    new three.Vector2(neckR * 0.8, rim),
  ];
  const bodyGeometry = new three.LatheGeometry(bodyPoints, 128);
  // A soft shade on the neck under the cap's lip, as in the photo (light rarely reaches it).
  const neckShade = new Float32Array(bodyGeometry.attributes.position.count * 3);
  const positions = bodyGeometry.attributes.position;
  const shadeFrom = data.neck.top - 0.08;
  for (let i = 0; i < positions.count; i++) {
    const y = positions.getY(i);
    const t = Math.min(1, Math.max(0, (y - shadeFrom) / (data.neck.top - shadeFrom)));
    const value = 1 - 0.2 * t * t * (3 - 2 * t);
    neckShade.set([value, value, value], i * 3);
  }
  bodyGeometry.setAttribute("color", new three.BufferAttribute(neckShade, 3));
  const bodyPlastic = plastic.clone();
  bodyPlastic.vertexColors = true;
  const body = new three.Mesh(bodyGeometry, bodyPlastic);
  // The inner wall and the dark opening, seen only once the cap is off.
  const wellGeometry = new three.CylinderGeometry(neckR * 0.8, neckR * 0.8, 0.09, 64, 1, true);
  const well = new three.Mesh(wellGeometry, inside);
  well.position.y = rim - 0.045;
  const floorGeometry = new three.CircleGeometry(neckR * 0.8, 64);
  const floor = new three.Mesh(floorGeometry, opening);
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = rim - 0.085;
  // Two thread rings on the neck.
  const threadGeometry = new three.TorusGeometry(neckR * 1.01, 0.0045, 8, 96);
  const threads = [0.35, 0.7].map((t) => {
    const ring = new three.Mesh(threadGeometry, plastic);
    ring.rotation.x = Math.PI / 2;
    ring.position.y = capBottom + (rim - capBottom) * t;
    return ring;
  });

  // Label sleeve: the unwrapped photo artwork, a hair above the body so they never flicker.
  const band = resample(data.profile, data.labelBand.bottom, data.labelBand.top, 90);
  const labelGeometry = new three.LatheGeometry(
    band.map(([y, r]) => new three.Vector2(r * 1.0035, y)),
    160,
    Math.PI, // the front of the artwork (u = 0.5) faces the camera
    Math.PI * 2,
  );
  let markReady: () => void = () => undefined;
  const ready = new Promise<void>((resolve) => (markReady = resolve));
  const labelTexture = new three.TextureLoader().load(data.label, () => markReady());
  labelTexture.colorSpace = three.SRGBColorSpace;
  labelTexture.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy());
  const labelMaterial = new three.MeshPhysicalMaterial({
    map: labelTexture,
    color: options.labelTint ?? "#ffffff",
    roughness: 0.45,
    clearcoat: 0.2,
    clearcoatRoughness: 0.3,
    envMapIntensity: 0.5,
    side: three.DoubleSide,
  });
  if (options.labelGlow) {
    labelMaterial.emissive = new three.Color("#ffffff");
    labelMaterial.emissiveMap = labelTexture;
    labelMaterial.emissiveIntensity = options.labelGlow;
  }
  const label = new three.Mesh(labelGeometry, labelMaterial);

  // Cap: a ribbed side with a softly rounded top, pivoting at its own centre.
  const capR = data.cap.radius;
  const capHeight = capTop - capBottom;
  const bevel = Math.min(0.012, capHeight * 0.12);
  // Evenly spaced up the side, so the grip texture's rows land where they are drawn (a lathe
  // spreads its texture by point, not by distance).
  const sideRows = 16;
  const capSidePoints = [
    new three.Vector2(capR * 0.97, 0),
    ...Array.from({ length: sideRows }, (_, i) => {
      const y = 0.004 + ((capHeight - bevel - 0.004) * i) / (sideRows - 1);
      return new three.Vector2(capR, y);
    }),
  ];
  const capSideGeometry = new three.LatheGeometry(capSidePoints, 192);
  const capTopPoints: T.Vector2[] = [];
  for (let i = 0; i <= 8; i++) {
    const a = (i / 8) * (Math.PI / 2);
    capTopPoints.push(
      new three.Vector2(
        capR - bevel + Math.cos(a) * bevel,
        capHeight - bevel + Math.sin(a) * bevel,
      ),
    );
  }
  capTopPoints.push(new three.Vector2(0, capHeight));
  const capTopGeometry = new three.LatheGeometry(capTopPoints, 128);
  const capInnerGeometry = new three.CylinderGeometry(
    capR * 0.97,
    capR * 0.97,
    capHeight * 0.96,
    64,
    1,
    true,
  );
  const cap = new three.Group();
  const capPivot = new three.Group();
  capPivot.position.y = -capHeight / 2;
  const capInner = new three.Mesh(capInnerGeometry, inside);
  capInner.position.y = capHeight * 0.48;
  capPivot.add(
    new three.Mesh(capSideGeometry, capSide),
    new three.Mesh(capTopGeometry, plastic),
    capInner,
  );
  cap.add(capPivot);
  cap.position.y = capBottom + capHeight / 2;

  group.add(body, well, floor, ...threads, label, cap);

  return {
    group,
    cap,
    rim,
    width: Math.max(...data.profile.map(([, r]) => r)) * 2,
    capHeight,
    ready,
    dispose() {
      [
        bodyGeometry,
        wellGeometry,
        floorGeometry,
        threadGeometry,
        labelGeometry,
        capSideGeometry,
        capTopGeometry,
        capInnerGeometry,
      ].forEach((geometry) => geometry.dispose());
      [plastic, bodyPlastic, capSide, inside, opening, labelMaterial].forEach((material) =>
        material.dispose(),
      );
      [ribs.bump, ribs.shade, labelTexture].forEach((texture) => texture.dispose());
    },
  };
}
