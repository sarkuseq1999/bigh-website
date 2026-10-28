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

/** The opening's pictures. October 28, 2026 (Mo): the misty peaks and the red-crowned crane read
 *  as Chinese to his colleagues; California took their place (Codex paintings, built by
 *  reference/ink-pages/home-california/build_home_opening.py, plates in its plates/site/). */
export const opening: Record<"landscape" | "bird" | "sun", Picture> = {
  /** Giant sequoias in the morning (ink and watercolour), painted as the whole first screen: one
   *  giant trunk on the right, a clearing of morning light beside it where the sun stands. */
  landscape: { src: `${I}/opening-sequoias-v1.webp`, width: 2400, height: 1600 },
  /** Anna's hummingbird, painted over the old crane's original in its place and pose (its tail
   *  where the crane's feet were, so the page's line still leaves from the bird), its wings
   *  repainted long, narrow and blurred. */
  bird: { src: `${I}/hummingbird-v1.webp`, width: 1600, height: 1062 },
  /** The gold-leaf sun, its leaf edge kept. Plate: reference/home-v2/ink/plates/sun.png */
  sun: { src: `${I}/sun.webp`, width: 760, height: 743 },
};

/** The crane at rest in the footer, in the grass beside the FDA park sign, bending toward the
 *  sign's poppy (ink; Mo picked C, October 26, 2026). Painted by Codex in the flying crane's hand
 *  (reference/ink-pages/footer-crane, built by build_footer_crane.py); placed by its feet
 *  (ink.module.css, `.look .rest`). It replaced crane-rest-v2, which stood beside the promise. */
export const cranePoppy: Picture = { src: `${I}/crane-poppy-v1.webp`, width: 800, height: 463 };

/** A brush at rest on its inkstone, beside "Good questions deserve clear answers." (ink). v2:
 *  smooth wet washes, no drawn sheet of paper. */
export const inkstone: Picture = { src: `${I}/inkstone-v2.webp`, width: 1200, height: 896 };

/** The ink mitochondrion with its two gold-leaf folds (ink): "Tiny power plants." only. */
export const mito: Record<"glow", Picture> = {
  glow: { src: `${I}/mito.webp`, width: 2000, height: 1493 },
};

/** "Make sense of the science.": every picture shows what its words say. Mitochondria and Free
 *  radicals (Mo, October 22, 2026, pick D, after the October 21 steam engine): one old powerhouse
 *  with its front left open like a storybook, as the words call mitochondria "tiny power plants":
 *  fuel feeds the fire, the fire turns the wheel, power runs out along the wire, and the chimney's
 *  screen catches the sparks. Painted by Codex in the homepage crane's hand (the fire and the
 *  sparks are the gold); built by reference/ink-pages/home-science/build_plant.py into the
 *  stage's box (ink). Aging cells (Mo, October 22): one brain cell up close, built by
 *  build_cell.py. */
const S = `${I}/science`;
export const sciencePaintings = {
  /** Inside the powerhouse: a worker feeds a log to the gold fire, its steam turns the big wheel,
   *  and power runs out along the wire (a thread of gold): fuel in, power out. */
  energy: { src: `${S}/plant-fuel-v1.webp`, width: 1600, height: 1195 },
  /** Closer, the chimney opened up: the screen on top holds most of the sparks, but the few that
   *  slip past fall on the roof and burn black holes in it (Mo, October 23, 2026, pick A: free
   *  radicals do harm, and the body's defences catch most, not all). A comparison; the stage
   *  says "Illustrations". */
  balance: { src: `${S}/plant-sparks-v2.webp`, width: 1600, height: 1195 },
  /** One brain cell up close at three ages, lined up on one framing: young (strong branches, six
   *  gold power plants), middle-aged (thinner branches, three still gold) and old (thin, pale
   *  branches, one still gold, still at work). The age slider shows one at a time. */
  aging: [
    { src: `${S}/cell-young-v2.webp`, width: 1600, height: 1195 },
    { src: `${S}/cell-middle-v2.webp`, width: 1600, height: 1195 },
    { src: `${S}/cell-old-v2.webp`, width: 1600, height: 1195 },
  ],
} satisfies Record<string, Picture | Picture[]>;

/** Where each painting is gold leaf, as an alpha mask (build_assets.py gold): the page lays a
 *  moving band of light over the painting through it, so only the leaf catches the light. */
export const gold = {
  mito: `${I}/mito-gold.webp`,
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
