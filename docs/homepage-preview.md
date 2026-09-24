# BiGH homepage — first design preview

September 17, 2026. Draft on `codex/blank-start`, deployed to a Vercel preview with Mo's approval. Not promoted to production.

Remote preview: https://bigh-website-haq92wjpw-sarkuseq1999s-projects.vercel.app

The hosted build completed successfully. The homepage opened in the signed-in browser and was visually checked at 390 px width. An unauthenticated request redirects to Vercel login. A login-free share link was not created: automatic approval review requires explicit approval for that access change. Deployment ID: `dpl_2x8wFrHAXeExDsGwLvNjrp46ZoQn`.

## Direction

Read the September 16 Obsidian build handoff, current brand cheat sheet, and live BiGH-tagged Design Vault notes before building. The vault has no named projects yet. Selected references: #046–047 for an immersive, restrained opening; #004 for clear navigation; #005 for a simple scientist introduction; #007 for science explained one idea at a time; #013 for a spacious footer. #045's warning about tiny navigation informed the larger header.

Original palette: pale mineral green, warm ivory, deep green, and copper. Manrope with Instrument Serif. The artwork is an artistic interpretation of cellular energy, not an anatomical diagram. The animation is a slow camera drift over the still image, not a generated video. Pause control and reduced-motion styling are included.

No archived website layouts, colors, copy, animations, or archived image files were used as design references.

## What is connected

- Home, Products, About, and Science anchors navigate within this homepage.
- Science dropdown and mobile navigation work through explicit controls.
- Scientist biography, product information, educational summaries, planned Ask BiGH Science, and Support open native dialogs.
- Three science topics switch the diagram and short explanation.
- Product purchasing, accounts, live support, and science question submission are not connected. The dialogs state this clearly.
- Existing locale routes are preserved. All content in this first preview is English, explicitly marked `lang="en"` within the page. Translations remain future work.
- Search indexing remains disabled.

## Assets and publication checks

The bottle photographs are copied from Mo's separate Dropbox product-materials collection, not `old-storage/`. They are existing packaging references, not newly approved labels. Current formulations, claims on packaging, serving information, price, and availability need confirmation before launch.

- NuriCell: `materials/Products/1_NuriCell/product-images/NuriCell_render-1.png`
- Turmerific: `materials/Products/2_Turmerific/product-images/Turmerific_render-1.png`
- Advanced OPC: `materials/Products/3_Advanced-OPC/product-images/AdvancedOPC_render-1.png`
- Green Bee Propolis: `materials/Products/4_Green-Bee-Propolis/product-images/GreenBeePropolis_render-1.png`
- Nature Calm: `materials/Products/5_Nature-Calm/product-images/NatureCalm_render-1.png`

Dr. Liu's draft portrait is sourced from his [university biography](https://www.uhrs.edu.cn/info/1050/1805.htm), image `https://www.uhrs.edu.cn/__local/D/39/EE/DDC03657E805CD20F2272DC1341_566F7A96_6B27.jpg`. Confirm publication permission before launch. His credentials in the dialog were checked against this source. Iris is text-only; no photograph, invented quote, exact unconfirmed formula credit, or formal advisor title is included.

No invented customer reviews, ratings, result timelines, certifications, manufacturing claims, or checkout prices were added. The customer-experience section explicitly awaits permissioned stories. Quality copy describes commitments rather than claiming unverified certification. The Ask BiGH Science service is described as planned.

## Science sources

- [Mitochondria — National Human Genome Research Institute](https://www.genome.gov/genetics-glossary/Mitochondria)
- [Antioxidant supplements — National Center for Complementary and Integrative Health](https://www.nccih.nih.gov/health/antioxidant-supplements-what-you-need-to-know)
- [Hallmarks of Aging, 2023](https://pubmed.ncbi.nlm.nih.gov/36599349/)
- [Liu et al., 2002, animal research](https://pubmed.ncbi.nlm.nih.gov/11854529/). Identified as an animal ingredient study, not a NuriCell trial.

## Local preview note

Use `npm run dev -- --hostname localhost --port 3000`, then visit `http://localhost:3000`. Next.js 16.2.6 can redirect-loop on the default language rewrite when bound to `127.0.0.1`; do not work around this by changing public language routes. Use the localhost host consistently.

## Next review

Review the visual direction first: hero, colors, typography, and section pacing. Then replace pending content with approved assets and evidence, build full destination pages, and connect the separate backend.

## Verification completed

- `npm run build`: compiled successfully; 10 static pages generated. TypeScript completed successfully. Build needs network access to fetch the selected Google Fonts.
- `npm run lint`: exit 0, no warnings.
- `npm run format:check`: all matched files use Prettier code style.
- `git diff --check`: exit 0.
- All six locale entry routes returned HTTP 200 with homepage content. They currently show the English preview.
- Opened the homepage in the actual browser at desktop, 390 px, 320 px, and 768 px widths. The final narrow-screen fix removed science-diagram overflow; 320 px testing reported a 305 px content area and a matching 305 px scroll width.
- Clicked motion pause/resume, desktop Science menu, mobile menu and Products link, NuriCell details, scientist biography, science topic buttons, educational details, Ask BiGH Science, and Support FAQ.
- Native dialog Escape/close behavior worked. Focus returned to the originating product button and body scrolling was restored.
- Final browser check: no recorded console errors and no broken loaded images. Desktop viewport override reset; homepage left at the top with motion enabled and marked as the deliverable.
- Reduced-motion styling is implemented but was not tested with an emulated operating-system preference. No representative-user accessibility study or live checkout test was performed.

Original generated hero asset and exact prompt: [artwork notes](hero-artwork.md).
