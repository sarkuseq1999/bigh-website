# NuriCell enhancement experiment

Created September 18, 2026 using the built-in image generation tool in edit mode.

- Before: `public/images/nuricell.png` (1140 × 1183, transparent PNG).
- After: `reference/experiments/nuricell/nuricell-enhanced-v1.png`.
- This is a separate comparison experiment. The homepage product image remains unchanged.
- Visually inspected both versions. The after version has stronger dimensional lighting, cleaner plastic, deeper blues, and a pale studio background with a contact shadow.
- Observed limitation: fine circuit artwork and small label geometry differ from the source. This is a generated retouch concept, not an exact label-preserving production photograph. The after image has a background rather than the original transparent cutout.

## Exact edit prompt

### Transparent comparison follow-up

Requested by Mo after reviewing the first enhancement. Final file: `nuricell-enhanced-transparent.png` (1230 × 1278, RGBA PNG).

Two built-in background-removal attempts produced defective transparency that erased white product areas. Those files were not selected. The final PNG instead retains the enhanced photo's visible color pixels and uses the original product cutout's alpha channel, aligned to the enhanced canvas and slightly inset at the boundary. Reproducible processing is in `make-transparent.mjs`.

Verified 872,710 fully transparent pixels, 694,345 fully opaque pixels, an opaque white cap/shoulder/base, transparent corners, and zero changed visible RGB pixels compared with the enhanced photo. Inspected `transparency-check-dark.png` against a dark background. The original enhancement's label-art differences remain; background removal does not correct them.

### Original enhancement prompt

Use case: precise-object-edit.
Asset type: enhanced e-commerce product photograph, one NuriCell supplement bottle.
Input image 1: the existing product image, EDIT TARGET and exact packaging reference.
Primary request: professionally retouch and enhance this same bottle photo for a premium website. Preserve its identity and exact packaging; improve photographic quality, not the design.

Keep the same straight-on camera angle, cylindrical proportions, white ribbed screw cap, white plastic shoulder and base, and exact blue wraparound label layout. Preserve the BiGH leaf logo, its printed tagline, circuit-brain illustration, silver ellipse border, hexagonal blue artwork, all colors, all existing typography, and line placement. Do not remove any printing. The large product name is exactly "NuriCell" (N-u-r-i-C-e-l-l), not Neuracell. Retain visible label text: "BiGH", "Be in Good Health", "NuriCell", "Boosts Memory and Energy*", "Boosts Brain Function*", "DIETARY SUPPLEMENT", "90 VEGETARIAN CAPSULES". Copy the source printing faithfully. Do not invent or rewrite side-panel text.

Enhance only: reduce the grainy artificial-looking texture; make plastic and cap ridges clean, realistic and finely resolved; use elegant large softbox light from upper left with subtle right-side fill; improve highlight control and dimensional separation; retain detailed whites without blown-out areas; make the existing label crisp without sharpening halos or changed colors. Photorealistic premium catalog retouch, restrained and credible, not glossy CGI or a packaging redesign.

Composition: one complete upright bottle, centered, cap and base fully visible, same silhouette and orientation as source. Bottle height about 90 percent of the near-square portrait frame. Keep ample empty space on both sides so it can be compared at equal scale with the original. Soft seamless very pale warm gray studio background, approximately #f4f4f0, with a faint realistic contact shadow beneath the base. No props, pills, plants, extra bottles, scenery, promotional badges, new claims, text overlays, borders, watermarks, or before/after layout. Output only the enhanced single product photo at high resolution.
