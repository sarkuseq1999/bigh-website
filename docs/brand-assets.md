# BiGH brand assets

## Official BiGH logo files

Downloaded from the public BiGH website on September 18, 2026 at Mo's explicit request. These two logos are approved references for the new website; this does not authorize reusing the old website's design or other assets.

| Version                           | Local file                                      | Original source                                                  |
| --------------------------------- | ----------------------------------------------- | ---------------------------------------------------------------- |
| Black lettering with green leaves | `public/images/brand/bigh-logo-black-green.png` | https://bighnow.com/wp-content/uploads/2019/01/Black-Logo.png    |
| White lettering with green leaves | `public/images/brand/bigh-logo-white.png`       | https://bighnow.com/wp-content/uploads/2019/04/logo_white_97.png |

Both are unchanged original PNG files, 1448 × 811 pixels, with an RGBA transparency channel. Each contains 781,675 fully transparent pixels. Both include the tagline “Be in Good Health.” The white version retains the green leaves.

Checked the PNG format, image dimensions, transparency, and appearance. Use the black version on light backgrounds and the white version on dark backgrounds. Preserve the original proportions and colors.

Added to the homepage on September 18, 2026 at Mo's request:

- Black and green logo in the header and footer.
- White and green logo on the blue About panel.

The original PNG files remain intact. Display sizes adapt to the page while preserving the original proportions.

Mo subsequently requested removing the small “Be in Good Health” tagline beneath each logo. All three homepage placements now use a CSS crop showing the top 710 pixels of the original 1448 × 811 image. The logo ends at row 706; rows 707–740 are fully transparent; the tagline starts at row 741. This removes the tagline from the displayed logos without redrawing or changing the original lettering, leaves, colors, or PNG files. The accessible logo name is now “BiGH”. Separate page text is unchanged.

Built-in image edits were attempted but rejected because they altered edges and transparency. Those generated alternatives are not used by the website. The shipped implementation uses the original PNGs and a reversible display crop.

Checked the header, white About logo, and footer visually after cropping. Verified the crop at a 390-pixel phone width with no horizontal page overflow. Lint, TypeScript, and formatting checks passed.

Verified in the browser at 320, 390, and 1280 CSS pixel widths, with no horizontal page overflow. All three logo placements loaded successfully. The blue panel has enough height for the logo and text on phones. Lint, TypeScript, and formatting checks passed; no browser console errors were reported during the check.

Current preview (tagline removed from displayed logos): https://bigh-website-axwji8fcc-sarkuseq1999s-projects.vercel.app

Vercel build completed successfully (10 generated pages, deployment `dpl_B5zpxCzrq11G8KbJrXA94aeGyiKM`, READY). Opened the hosted preview and visually confirmed the header logo renders without the tagline. Existing Vercel sign-in protection remains in place.

## Approved product images — September 18, 2026

After reviewing the five side-by-side comparisons, Mo approved the enhanced versions for future product images: “So let's use those for future product images.” These are the preferred product assets for subsequent website and product-image work.

| Product | Approved transparent PNG |
| --- | --- |
| NuriCell | `public/images/products/nuricell.png` |
| Green Bee Propolis | `public/images/products/green-bee-propolis.png` |
| Advanced OPC Formula | `public/images/products/advanced-opc.png` |
| Turmerific | `public/images/products/turmerific.png` |
| Nature Calm | `public/images/products/nature-calm.png` |

These files are exact copies of the reviewed `public/experiments/*-enhanced-transparent.png` assets. All five copies were verified by matching SHA-256 hashes. Preserve their transparency and proportions. Keep the original `public/images/*.png` files and comparison assets for reference; do not overwrite them.

Review page: https://bigh-website-4j6jy61te-sarkuseq1999s-projects.vercel.app/experiments/products.html

The generation prompts and observed label-detail differences remain documented in `reference/experiments/product-enhancements/`. Approval establishes the preferred imagery; it does not establish character-by-character accuracy of generated label text. This approval step records the choice and saves canonical copies; it does not change current homepage image references or deploy a new preview.
