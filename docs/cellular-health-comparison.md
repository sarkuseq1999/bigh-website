# Cellular-health designs and section order — September 22, 2026

Mo accepted the section order below and moved on to the [NuriCell spotlight](nuricell-spotlight.md), which records the latest site preview.

## Current trial — Dr. Liu second, original dark cell design third

Mo asked to try this homepage order:

1. Approved Deep Space hero.
2. Existing white/near-white scientific-roots section featuring Dr. Jiankang Liu. Its content, portrait, styling and actions are unchanged.
3. The original dark **Inside the cell** design, using `public/images/science/comparison/01-inside-cell.webp`: copy on the left, blue/amber mitochondrion on the right.

This restores the original colored composition, not a recolored version of the newer left-side artwork. The approved cellular-health copy and Explore action remain. The numbered comparison controls are hidden for this complete-page trial, and only the original image is mounted. `homepage.tsx` now places `CellularHealthComparison variant="original"` after `#scientists`. Its default comparison mode, all six revised designs, and their artwork are preserved for later comparison. No new artwork was generated.

Local checks: the first three sections are `home`, `scientists`, `cellular-health` at 320, 390, 768, 1024, 1101 and 1440px; no horizontal overflow; the original image loads; no comparison controls appear. Inspected desktop and phone layouts plus both section transitions. Both Dr. Liu buttons and Explore open their respective dialogs; Escape closes them and restores focus. The hero's scientist link scrolls to the relocated section. Lint, TypeScript, changed-code formatting and the production build passed; all 10 pages were generated. Local browser console: zero errors and warnings. Screenshots: `reference/cellular-health/comparison/qa-scientists-first/`. Responsive checks were in a desktop browser, not a physical phone or Safari.

The remaining comparison notes describe the earlier review versions.

Mo requested all six proposed designs in the website section with numbered controls, like the earlier hero comparison. All six now use responsive page layouts, real approved text, a working Explore button, and separate clean artwork. The approved Deep Space hero is unchanged. These section designs use still artwork; no new animation was requested or generated for this comparison.

## Earlier comparison

The bottom-right controls appear while the cellular-health section is in view. Buttons 1–6 change its artwork, palette, typography and layout. The active number and design name are displayed. Mo liked options 1–3 and requested white backgrounds with the main object on the left. These three are now redesigned accordingly, with copy on the right, more space around the artwork, and balanced headline wrapping. Revised design 1 is the starting view for this review; it is not a final selection. Options 4–6 remain unchanged.

| Number | Design | Served artwork |
| --- | --- | --- |
| 1 | Inside the cell — blue/amber sculpture on white | `public/images/science/comparison/01-inside-cell-white-left-v2.webp` |
| 2 | Living microscope — green cell and magnified mitochondrion on white | `public/images/science/comparison/02-living-microscope-white-left-v2.webp` |
| 3 | Sculpted energy — copper folds on white | `public/images/science/comparison/03-sculpted-energy-white-left-v2.webp` |
| 4 | Pearl sculpture | `public/images/science/comparison/04-pearl-sculpture.webp` |
| 5 | A closer look | `public/images/science/comparison/05-white-zoom.webp` |
| 6 | Ivory editorial | `public/images/science/comparison/06-ivory-editorial.webp` |

Keyboard: Tab/Enter or Space selects a number; left/right arrows cycle, Home/End jump to first/last. The controls disappear outside the section. The default is 1 on reload; selection is not persisted. The Explore button opens the existing “Energy starts small.” science dialog, with Escape dismissal and focus restoration.

The original component and asset remain preserved. New component: `src/components/home/cellular-health-comparison.tsx`; styles: `cellular-health-comparison.module.css`. `homepage.tsx` mounts this in place of the first section component. At 1100px and below, illustration and text stack so artwork does not reduce copy contrast.

## Artwork provenance

All six earlier still mockups were inspected, then edited with built-in `image_gen` to remove lettering, labels and button graphics while preserving their compositions. The original PNG edits are saved at `reference/cellular-health/comparison/01-inside-cell.png` through `06-ivory-editorial.png`, using the same base filenames as the table. Each is 1536 × 1024. Copies were byte-verified against tool outputs. Each output was inspected: no baked text remains; cell-to-mitochondrion connectors remain in options 2 and 5.

[Original prompts, input files, generated source paths and asset paths](../reference/cellular-health/comparison/artwork.json). The first implementation used the original six compositions and started on white design 5. Its colored options 1–3 remain preserved as historical assets.

For the white/left revision, the three original clean PNGs were inspected and edited using **built-in image_gen**. Each was relit against white and recomposed on the left while retaining its scientific subject and material character. No text or controls are baked into the assets. Each final PNG is 1536 × 1024; the new workspace copies were byte-verified against the tool output and visually inspected.

- `reference/cellular-health/comparison/01-inside-cell-white-left-v2.png`
- `reference/cellular-health/comparison/02-living-microscope-white-left-v2.png`
- `reference/cellular-health/comparison/03-sculpted-energy-white-left-v2.png`

[Exact final prompt set, inputs, generated source paths and final paths](../reference/cellular-health/comparison/artwork-white-left-v2.json). [Reproducible copy and encoding script](../reference/cellular-health/comparison/prepare-artwork.cjs): run with `artwork-white-left-v2.json` to prepare only the new assets. Sharp only encodes the generated PNGs to WebP (quality 88); it does not edit their content. The three new served images total 468,422 bytes. Design 1 loads initially; the other five mount when the section first enters view, keeping subsequent comparisons quick. On smaller screens CSS crops away the unused white copy area and places the illustration between the heading and body. Tablet artwork edges are softly blended into white.

## Verification — white/left revision

- Checked revised options 1–3 at 320, 390, 768, 1024, 1101, 1280 and 1440px, plus a desktop regression of options 4–6: 24 combinations passed. Each loaded its artwork, kept exactly one selected button, kept the controls within the viewport and caused no horizontal overflow. Revised sections computed to a white background.
- Inspected desktop, phone and tablet screenshots. Desktop copy is right of the illustration with clear spacing. Headline wrapping is balanced. The artwork stacks between heading and body at 1100px and below. The final tablet edge refinement was visually rechecked.
- All three revised Explore buttons opened “Energy starts small.” Escape dismissed the dialog and restored focus. Arrow-key wrap, Home/End, and hiding controls outside the section passed.
- Lint, TypeScript, changed-code formatting and the final local production build passed; the build generated all 10 pages.
- A fresh local reload started on option 1. Final local browser console: zero errors and zero warnings.
- Screenshots: `reference/cellular-health/comparison/qa-white-left-v2/`. Checks use a desktop browser at responsive sizes, not a physical phone or Safari.

## Verification — original six-design implementation

- Clicked all six choices at 320, 390, 768, 1024 and 1440px. Each changed the active design, left exactly one number selected, kept the controls within the viewport, loaded its image, and caused no horizontal overflow.
- Inspected desktop and phone screenshots for every design. Tablet inspection led to the stacked layout, then all six were rechecked at 768 and 1024px; artwork ends before the body copy begins.
- Fixed two issues found during checking: control visibility after section/viewport size changes, and a narrow-screen control panel extending past the left edge due to viewport-unit scrollbar width.
- All six Explore buttons open the science dialog. Escape closes it and restores focus. Arrow-key wrap, Home/End and Tab/Enter selection verified. Controls hide at the hero and products; reduced-motion mode has zero animations in this section.
- Final local browser console: zero errors and zero warnings. A preliminary lazy-image LCP warning was resolved by loading the starting image eagerly.
- Lint, TypeScript, changed-code formatting and the local production build passed. The build generated all 10 pages. Deployment results are recorded below after completion.
- Screenshots: `reference/cellular-health/comparison/qa/`. Checks use a desktop browser at responsive sizes, not a physical phone or Safari.

## Preview

Current protected preview: https://bigh-website-jl4df30oy-sarkuseq1999s-projects.vercel.app/

The reordered homepage deployment `dpl_6unCu9oocfx6bt3qniAuy3amfGhr` reported READY. Its hosted build compiled, completed TypeScript and generated all 10 pages. Existing Vercel login protection is unchanged; production was not promoted. Visual and interaction checks were local; the hosted page remains behind the login gate.

Previous white/left preview: https://bigh-website-2b0jy6l5x-sarkuseq1999s-projects.vercel.app/#cellular-health

The white/left revision deployment `dpl_2ENqC2kh88tThbp58GkbySkqd31Q` reported READY. Its hosted build compiled, completed TypeScript and generated all 10 pages. Existing Vercel login protection is unchanged; production was not promoted. Visual and interaction checks were local; the hosted UI was not visually rechecked behind the login gate.

Previous protected preview: https://bigh-website-n58s9597a-sarkuseq1999s-projects.vercel.app/#cellular-health

Deployment `dpl_FUAqQnPxuoxqFCPJUcbPvKXGeUxV` reported READY. The hosted build compiled, completed TypeScript and generated all 10 pages. Existing Vercel login protection is unchanged; production was not promoted. The visual and interaction checks above were local. The hosted UI was not visually rechecked behind the login gate.
