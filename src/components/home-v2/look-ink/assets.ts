// The Ink & Gold look's pictures (round 4, October 2, 2026). Every painting was made for this look
// with GPT Image 2.5 from the approved comps' regions (prompts in reference/home-v2/ink/prompts,
// originals in reference/home-v2/ink/originals, built by reference/home-v2/ink/build_assets.py).
// Each ships as webp; its lossless plate (what the build gate scored against the comp) is
// reference/home-v2/ink/plates/<name>.png. Paintings marked `ink` have their paper divided out and
// are placed with mix-blend-mode: multiply, so the page's own rice paper shows through them.
// The bottles are the approved product PNGs and Dr. Liu's photo is his real one, never generated.
const I = "/images/home-v2/ink";

type Picture = { src: string; width: number; height: number };

export const paper = `${I}/paper.webp`; // plate: reference/home-v2/ink/plates/paper.png

/** An ink blot's soft edge: paintings bloom through it as they enter. */
export const bloomMask = `${I}/bloom-mask.png`;

export const crane: Record<"landscape" | "crane" | "sun", Picture> = {
  /** Misty mountains (ink). Plate: reference/home-v2/ink/plates/landscape.png */
  landscape: { src: `${I}/landscape.webp`, width: 2400, height: 1029 },
  /** The crane of long life, cut out (BiRefNet). October 9: painted again by hand in the same pose
   *  (Mo: "more like a painting than a picture"; sample A), its whites brought to the first
   *  crane's. Plate: reference/home-v2/ink/plates/crane-painted.png */
  crane: { src: `${I}/crane-painted.webp`, width: 1600, height: 1062 },
  /** The gold-leaf sun, its leaf edge kept. Plate: reference/home-v2/ink/plates/sun.png */
  sun: { src: `${I}/sun.webp`, width: 760, height: 743 },
};

/** The opening crane's wingbeat (round 5): the same painting brought to life by a Kling loop, cut
 *  out frame by frame like the still (build_crane_flight.py). An animated webp. `small` is for
 *  phones. v3 (October 5, round 8): a take in which the black flight feathers stay solid ink
 *  through the beat. v4 (October 5): no held pose, one wingbeat a breath (2.4 s), and the whole
 *  bird lifts as its wings press down and settles as they rise. v4-twice (Mo, October 5: "fly
 *  like 2 times, then stop"): two beats, then the picture stops for good on the still's pose
 *  (its loop count is 2 and its last frame is the first pose again). a2-twice (October 9): the
 *  same beat, played the same way, from a new take of the hand-painted crane (crane-paint-a). */
export const craneFlight = {
  src: `${I}/crane-flight-a2-twice.webp`,
  small: `${I}/crane-flight-a2-twice-600.webp`,
};

/** The crane at rest, standing on the page's last brush stroke (ink). v2: painted again in the
 *  flying crane's hand; its feet are 8% above the picture's bottom edge (look-ink.module.css). */
export const craneRest: Picture = { src: `${I}/crane-rest-v2.webp`, width: 560, height: 864 };

/** A brush at rest on its inkstone, beside "Good questions deserve clear answers." (ink). v2:
 *  smooth wet washes, no drawn sheet of paper. */
export const inkstone: Picture = { src: `${I}/inkstone-v2.webp`, width: 1200, height: 896 };

/** The ink mitochondrion with its two gold-leaf folds (ink): "Tiny power plants." only. */
export const mito: Record<"glow", Picture> = {
  glow: { src: `${I}/mito.webp`, width: 2000, height: 1493 },
};

/** "Make sense of the science." (Mo, October 21, 2026: idea A, "a hiker, and a peek inside"): the
 *  October 19 paintings set a mood but did not explain their words. Now one hiker walks a golden
 *  California trail, and a round window shows what is happening in one of their cells, so each
 *  picture shows what its words say. Painted by Codex (the hiker's face hidden by the hat); built
 *  by reference/ink-pages/home-science/build_hiker.py: the scene in the stage's box and the cell
 *  for the window (ink). `lead` is where the window's leader starts, the hiker's thigh, in the
 *  stage's 1600 x 1195. */
const S = `${I}/science`;
export type Peek = { scene: Picture; cell: Picture; lead: [number, number] };
const peek = (state: string, lead: [number, number]): Peek => ({
  scene: { src: `${S}/hiker-${state}-v1.webp`, width: 1600, height: 1195 },
  cell: { src: `${S}/cell-${state}-v1.webp`, width: 900, height: 900 },
  lead,
});
export const sciencePaintings = {
  /** The hiker eats an orange; in the cell, the orange turns to gold at the power plants. */
  energy: peek("energy", [411, 795]),
  /** The hiker climbs; closer in, a power plant at work throws off sparks (free radicals). */
  balance: peek("sparks", [471, 707]),
  /** The same hiker at three ages on the same spot (young, middle, old), with fewer and dimmer
   *  power plants in the cell. The age slider shows one of them at a time. */
  aging: [peek("young", [458, 836]), peek("middle", [463, 843]), peek("old", [458, 847])],
};

/** Where each painting is gold leaf, as an alpha mask (build_assets.py gold): the page lays a
 *  moving band of light over the painting through it, so only the leaf catches the light. */
export const gold = {
  mito: `${I}/mito-gold.webp`,
  energy: `${S}/hummingbird-v1-gold.webp`,
  purpose: `${I}/purpose-gold.webp`,
};

/** One breath of ink behind Dr. Liu's photograph (ink). */
export const halo: Picture = { src: `${I}/halo.webp`, width: 1100, height: 1100 };

/** The ink pool each bottle stands in, and its small dense contact shadow (ink). */
export const shadow: Picture = { src: `${I}/pool.webp`, width: 900, height: 482 };
export const contactShadow: Picture = { src: `${I}/pool-foot.webp`, width: 600, height: 170 };

/** Dr. Liu's only photograph (512 x 768), never shown larger than its own pixels allow. */
export const liu: Picture = { src: "/images/jiankang-liu.jpg", width: 512, height: 768 };

/** Ink still lifes for the sample stories: objects only, never people (ink). v2 (round 5): built
 *  at the originals' full width (1744px; they were 1200px), sharp at their large size on 2x
 *  screens. */
export const storyPaintings: Record<string, Picture> = {
  lisa: { src: `${I}/story-morning-v2.webp`, width: 1744, height: 2336 },
  michael: { src: `${I}/story-reading-v2.webp`, width: 1744, height: 2336 },
  susan: { src: `${I}/story-source-v2.webp`, width: 1744, height: 2336 },
};

/** The close: an old pine over a sea of mist, the gold sun low (ink). Its two cranes fly on their
 *  own layer (purposeCranes); the whole painting is the plate reference/home-v2/ink/plates/purpose.png. */
export const purposePainting: Picture = {
  src: `${I}/purpose-land.webp`,
  width: 2400,
  height: 1029,
};

/** The two cranes of the close, lifted out of the painting so they can fly (ink). `box` is where
 *  they sit in the painting, as fractions of its width and height (build_assets.py CRANES). */
export const purposeCranes = {
  src: `${I}/purpose-cranes.webp`,
  width: 326,
  height: 172,
  box: { left: 1500 / 2400, top: 468 / 1029, width: 326 / 2400 },
};
