# Original products section — saved September 22, 2026

Mo likes this design and explicitly requested saving it before the NuriCell spotlight work. This snapshot is from the page with Deep Space first, Dr. Liu second and the original dark Inside the cell design third.

## Restore just the products section

In `src/components/home/homepage.tsx`, set the `ProductsSection` prop to `design="original"` (the current page uses `design="comparison"`). This renders the original collection introduction, blue NuriCell bottle panel, ingredient pills, research link and four product cards. The original styles in `homepage.module.css` remain unchanged. This avoids reverting later changes elsewhere on the page. The later white NuriCell spotlight is also preserved as `design="spotlight"`.

The original mode was mounted and opened locally before switching to the new design. It displayed the original heading, bottle presentation and all five product buttons. The desktop section retained its original 1425 × 1695 capture size. `restore-mode-desktop.png` records that check. Screenshots are visual references, not a pixel-identical restoration assertion; browser focus/hover overlays can differ.

## Snapshot files

- `homepage.tsx.txt`: complete source immediately before extraction/redesign.
- `homepage.module.css.txt`: complete original stylesheet.
- `products-section.tsx.txt`: only the original products section markup.
- `images/`: the five original product images used by this version.
- `desktop.png`, `phone.png`: screenshots taken before changes.
- `manifest.json`: original paths, saved paths and SHA-256 hashes. The two source snapshots and five images matched their originals when copied.

Use the full-source snapshot only as a reference when restoring this section; do not overwrite a newer homepage wholesale. The original CSS hash was rechecked after implementation and is still unchanged. The product data remains in `homepage.tsx`, with its original values also preserved in this snapshot.

Protected preview before this change: https://bigh-website-jl4df30oy-sarkuseq1999s-projects.vercel.app/#products

These files are excluded from deployment by `.vercelignore`. No original assets were overwritten or removed.

Later header/language work on September 22 changed header rules in the active `homepage.module.css`; the original snapshot and its hashes remain intact. Restoring the product mode keeps the newer header. The active stylesheet is therefore no longer byte-identical to this historical snapshot.
