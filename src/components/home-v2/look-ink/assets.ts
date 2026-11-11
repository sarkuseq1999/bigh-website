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
  /** Allen's hummingbird without its wings (Mo picked C, October 29, 2026: Allen's, "more
   *  painting-like", the beak one dry brush stroke), a few wet washes in the old crane's hand,
   *  lined up in the crane's frame on the first hummingbird (its tail where the crane's feet were,
   *  so the page's line still leaves from the bird). Its wings are `openingWings`. */
  bird: { src: `${I}/hummingbird-v2.webp`, width: 1600, height: 1062 },
  /** The gold-leaf sun, its leaf edge kept. Plate: reference/home-v2/ink/plates/sun.png */
  sun: { src: `${I}/sun.webp`, width: 760, height: 743 },
};

/** The hummingbird's wings, beating as it arrives, then at rest (Mo, November 4, 2026; see
 *  opening.module.css): its own painted wings, lifted out and beaten about the shoulder (build_wings.py), each frame blurred
 *  over its slice of the beat. Since November 11 (Mo: "I just see the upper wings move") each
 *  fans above the body, from raised as painted out to about level with the shoulder, and never
 *  swings down past the belly (v3). Each picture is one wing's six frames side by side; both are laid
 *  in `box` (percent of the bird's frame), the far wing behind the body, the near one over it. */
export const openingWings = {
  near: `${I}/hummingbird-v3-near.webp`,
  far: `${I}/hummingbird-v3-far.webp`,
  frames: 6,
  box: { left: 11.638, top: 14.174, width: 54.031, height: 55.621 },
};

/** Two California quail in the footer, in the grass beside the FDA park sign, one keeping watch,
 *  one bending toward the sign's poppy (Mo picked A1, November 3, 2026). A few wet washes by
 *  Codex in the opening hummingbird's hand, in their own thin colour on every page
 *  (reference/ink-pages/footer-crane, built by build_footer_quail.py); placed by their feet
 *  (ink.module.css, `.look .rest`). They replaced crane-poppy-v1, the crane at rest, which read as
 *  Chinese. */
export const quailSign: Picture = { src: `${I}/quail-sign-v1.webp`, width: 800, height: 558 };

/** A country mailbox with its flag up in gold leaf, beside "Good questions deserve clear answers."
 *  (Mo picked A, October 30, 2026: the inkstone and brush read as Chinese). You send a question,
 *  an answer comes back. A few wet washes by Codex, its paper divided out (ink), its own thin colour
 *  in the painting, so no tinted twin (reference/ink-pages/home-ask, built by build_home_ask.py). */
export const mailbox: Picture = { src: `${I}/mailbox-v1.webp`, width: 1200, height: 896 };

/** The mitochondrion in "Tiny power plants." only, in softer ink (Mo picked B, November 4, 2026:
 *  he loves the cell's design, but the heavy black ink no longer fitted the page's California
 *  colours; he compared it live with a California colouring). The original ink painting
 *  (`mito.webp`, its source) a third lighter and warmed to sepia, every stroke kept; its own
 *  colour, so no tinted twin (reference/ink-pages/home-mito/build_mito_colour.py). Its two
 *  gold-leaf folds are the gold layer (`gold.mito`). */
export const mito: Picture = { src: `${I}/mito-soft-v1.webp`, width: 2000, height: 1493 };

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
  purpose: `${I}/purpose-ink-long-gold-v1.webp`,
};

/** One breath of ink behind Dr. Liu's photograph (ink). */
export const halo: Picture = { src: `${I}/halo.webp`, width: 1100, height: 1100 };

/** The ink pool each bottle stands in, and its small dense contact shadow (ink). */
export const shadow: Picture = { src: `${I}/pool.webp`, width: 900, height: 482 };
export const contactShadow: Picture = { src: `${I}/pool-foot.webp`, width: 600, height: 170 };

/** Dr. Liu's only photograph (512 x 768), never shown larger than its own pixels allow. */
export const liu: Picture = { src: "/images/jiankang-liu.jpg", width: 512, height: 768 };

/** The sample stories' still lifes: objects only, never people. Mo, November 6, 2026: the old
 *  ink still lifes (plum blossom in a vase, tea bowls, a low table) read as Asian; he picked A,
 *  one California back porch with golden hills and a valley oak beyond its rail, at three times
 *  of day: Lisa's breakfast in the morning, Michael's book at dusk, Susan's honeycomb and the
 *  Brazilian shrub in the afternoon. Codex paintings in ink and thin watercolour, their own colour
 *  (no green-spring twin), square, enlarged to 1744px (build_home_stories.py). */
export const storyPaintings: Record<string, Picture> = {
  lisa: { src: `${I}/story-porch-morning-v1.webp`, width: 1744, height: 1744 },
  michael: { src: `${I}/story-porch-dusk-v1.webp`, width: 1744, height: 1744 },
  susan: { src: `${I}/story-porch-afternoon-v1.webp`, width: 1744, height: 1744 },
};

/** The close: the long view down the Big Sur coast at evening, an older couple and their dog on
 *  the cliff-top trail, Bixby Bridge in the haze, the gold-leaf sun setting on the Pacific (ink and
 *  its own thin colour, so no tinted twin). Mo, November 2, 2026: the old pine, the misty peaks and
 *  the cranes read as Chinese; he picked a walk on the Big Sur coast, found it "a little bit
 *  simple" next to the old painting, tried two richer paintings live, found them "more picture
 *  like", and picked 1B: the same view painted in ink and wash, the old painting's way of painting.
 *  A Codex painting; the sun is the opening's own leaf, set on the horizon at the head of the
 *  glitter (reference/ink-pages/home-purpose, built by build_home_purpose.py). 2:1, not the old
 *  7:3: at 7:3 the land rose into the words. Its pelicans fly on their own layer (purposePelicans). */
export const purposePainting: Picture = {
  src: `${I}/purpose-ink-long-v1.webp`,
  width: 2400,
  height: 1200,
};

/** The close's five brown pelicans, on their own layer so they can fly home (ink). `box` is where
 *  they sit in the painting, as fractions of its width and height. */
export const purposePelicans = {
  src: `${I}/purpose-pelicans-v1.webp`,
  width: 800,
  height: 201,
  box: { left: 0.52, top: 0.43, width: 0.17 },
};
