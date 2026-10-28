// The About opening's painting, the poppy meadow (Mo, October 27-28, 2026), made by
// reference/ink-pages/about-opening/build_about_opening.py from a Codex painting and Codex's
// continuation of its foot. Two pictures with their paper made transparent: the painting with its
// gold a pale grey ghost, and the gold alone over it, let in once its picture is in
// (meadow.module.css). The painting's first 1024 rows (`foot`) are the 3:2 meadow that fills the
// first screen; under them the meadow thins out into bare paper.

export const meadow = {
  src: "/images/about-opening/superbloom-v2.webp",
  gold: "/images/about-opening/superbloom-gold-v2.webp",
  width: 1536,
  height: 1439,
  foot: 1024,
} as const;
