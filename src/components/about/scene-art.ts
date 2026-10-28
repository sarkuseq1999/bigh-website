// The paintings of the two About openings Mo is comparing on the live site (October 27, 2026),
// made by reference/ink-pages/about-opening/build_about_opening.py from two Codex paintings. Each
// is two pictures with their paper made transparent: the painting with its gold taken down to a
// pale grey ghost, and the gold alone, which the page lets in over it (scene.module.css).

export const scenes = {
  superbloom: {
    src: "/images/about-opening/superbloom-v1.webp",
    gold: "/images/about-opening/superbloom-gold-v1.webp",
    width: 1536,
    height: 1024,
    alt: "Rolling California foothills in a spring superbloom, golden poppies covering the slopes, valley oaks on a far ridge, painted in ink",
  },
  walk: {
    src: "/images/about-opening/walk-v1.webp",
    gold: "/images/about-opening/walk-gold-v1.webp",
    width: 1536,
    height: 1024,
    alt: "A person with a walking stick and a small dog walking a dirt trail over misty California hills toward a ridge lit gold by the morning sun, painted in ink",
  },
} as const;

export type Scene = keyof typeof scenes;
