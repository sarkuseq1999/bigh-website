# Starter prompts: the other three product pages in Ink & Gold

October 16, 2026. Mo pastes one of these into a new Claude Code session (started in the main folder,
`C:\Users\mcbig\Documents\codes\bigh-website`, so the memory loads). Each is self-contained. They follow
how Green Bee Propolis went (October 13-16; `reference/ink-pages/propolis/README.md`).

Reserved so parallel sessions don't collide: worktree, branch, preview ports and a translation key
range for each product.

| Product              | Worktree                     | Branch            | Dev / built ports | Translation keys |
| -------------------- | ---------------------------- | ----------------- | ----------------- | ---------------- |
| Advanced OPC Formula | `codes/bigh-opc-ink`         | `opc-ink`         | 3052 / 3053       | m700–m739        |
| Turmerific           | `codes/bigh-turmerific-ink`  | `turmerific-ink`  | 3054 / 3055       | m740–m779        |
| Nature Calm          | `codes/bigh-nature-calm-ink` | `nature-calm-ink` | 3056 / 3057       | m780–m819        |

---

## Advanced OPC Formula

```text
Let's give Advanced OPC Formula the Ink & Gold product page, the way we did Green Bee Propolis: NuriCell's ink template, but Advanced OPC's own paintings in every chapter and its own signature moment in "Why it matters". Show me mockups of the paintings to pick from before building. Ask before any push or spending.

SETUP
- First read docs/handoff-2026-09-24.md, AGENTS.md, your memory (especially project_propolis_ink.md, project_nuricell_ink.md, feedback_never_redraw_product.md, feedback_shared_theme_own_design.md, feedback_even_rhythm_no_repeats.md, feedback_bigh_california_not_asian.md), reference/ink-pages/propolis/README.md and docs/superpowers/specs/2026-10-09-nuricell-ink-design.md.
- Work in a new worktree from the latest origin/main: git worktree add -b opc-ink ../bigh-opc-ink origin/main --no-track, then npm ci. Add two entries to the main folder's .claude/launch.json: "bigh-opc-ink" (dev, port 3052) and "bigh-opc-ink-prod" (next start, port 3053).
- Other product sessions may run at the same time. Keep any template change optional, so NuriCell and Green Bee Propolis render exactly as now. Fetch and merge origin/main before any push. Use only translation keys m700 to m739 (start your translations script there).

RULES I'VE SET (follow them)
- Never redraw, repaint or restyle the bottle. Use the real approved bottle picture in public/images/products/. Only backgrounds are painted.
- Watercolor and ink, like the rest of the site. No photo-real scenes.
- BiGH is a California brand: nothing Asian-coded (no Chinese characters, teacups, "kintsugi"). The product's real origin story is welcome.
- One painting per chapter, each its own idea, calm and not busy. Gold leaf only where it means something. No lab glassware, no germs.
- Both bottles (the top of the page and Buy) as big as NuriCell's.
- Facts only from the product's data file and label. Never invent amounts, studies or claims. Write "animal study", not "rats". New sentences are drafts for me.
- Give me 2 or 3 labeled options with your pick, never long lists. Talk to me simply. Show pictures in a claude.ai artifact, on the real page template.

HOW PROPOLIS WENT (copy what worked)
- Pictures: GPT Image 2.5 through the helper pattern in reference/ink-pages/propolis/hf_propolis.py (copy it with its own ledger folder and a job cap). Ask me for a budget first ($3 covered Propolis's 29 pictures).
- Mockups: paint each chapter, show them on the real page with temporary local wiring (never committed), desktop and phone screenshots.
- Build: a build script like reference/ink-pages/propolis/build_propolis.py, the "ink" block in the product's data file, a QA script like scripts/qa/qa_propolis_ink.py. Keep qa_nuricell_ink, qa_propolis_ink, qa_home_ink, qa_nav and qa_fda green, and check on the built site (next start), not only the dev server.
- Template pieces that exist: Why can cross-fade (NuriCell's lantern) or spread gold out from a point (Propolis's cracks), or you can add a new optional mode. Buy can be a brush stroke or a painted scene with the real bottle standing in it. The painted sum is optional. Long names are sized to fit automatically; nameLockup sets one word plus a stacked pair (it reaches main with Propolis's October 16 update; if it isn't there yet, ask me).
- Go live only on my yes: push main, Vercel builds production, point bigh-website-demo.vercel.app at it, check it signed out, update docs/public-demo.md.

ABOUT ADVANCED OPC FORMULA (src/components/product/products/advanced-opc.ts)
- Thirteen ingredients (grape seed, pine bark, red wine, bilberry, tea, citrus, noni, lutein, melilotus, vitamins C and E, gamma-tocopherol, selenium). "What's inside" has to show many plants without looking busy.
- Two capsules a day, 120 per bottle, 60 days.
- "Why" today: "Why antioxidants matter. A balance worth keeping." Its picture today is a grape photo, dark then lit.
- People chapter: Dr. Iris Wang, words only. The credit is hers alone: "Formulated under the guidance of Dr. Iris Wang."
- The name is three words and long: try the automatic fit, or a lockup like Propolis's.
```

---

## Turmerific

```text
Let's give Turmerific the Ink & Gold product page, the way we did Green Bee Propolis: NuriCell's ink template, but Turmerific's own paintings in every chapter and its own signature moment in "Why it matters". Show me mockups of the paintings to pick from before building. Ask before any push or spending.

SETUP
- First read docs/handoff-2026-09-24.md, AGENTS.md, your memory (especially project_propolis_ink.md, project_nuricell_ink.md, project_turmerific_page.md, feedback_never_redraw_product.md, feedback_shared_theme_own_design.md, feedback_even_rhythm_no_repeats.md, feedback_bigh_california_not_asian.md), reference/ink-pages/propolis/README.md and docs/superpowers/specs/2026-10-09-nuricell-ink-design.md.
- Work in a new worktree from the latest origin/main: git worktree add -b turmerific-ink ../bigh-turmerific-ink origin/main --no-track, then npm ci. Add two entries to the main folder's .claude/launch.json: "bigh-turmerific-ink" (dev, port 3054) and "bigh-turmerific-ink-prod" (next start, port 3055).
- Other product sessions may run at the same time. Keep any template change optional, so NuriCell and Green Bee Propolis render exactly as now. Fetch and merge origin/main before any push. Use only translation keys m740 to m779 (start your translations script there).

RULES I'VE SET (follow them)
- Never redraw, repaint or restyle the bottle. Use the real approved bottle picture in public/images/products/. Only backgrounds are painted.
- Watercolor and ink, like the rest of the site. No photo-real scenes.
- BiGH is a California brand: nothing Asian-coded (no Chinese characters, teacups, "kintsugi"). The product's real origin story is welcome.
- One painting per chapter, each its own idea, calm and not busy. Gold leaf only where it means something. No lab glassware, no germs.
- Both bottles (the top of the page and Buy) as big as NuriCell's.
- Facts only from the product's data file and label. Never invent amounts, studies or claims. Write "animal study", not "rats". New sentences are drafts for me.
- Give me 2 or 3 labeled options with your pick, never long lists. Talk to me simply. Show pictures in a claude.ai artifact, on the real page template.

HOW PROPOLIS WENT (copy what worked)
- Pictures: GPT Image 2.5 through the helper pattern in reference/ink-pages/propolis/hf_propolis.py (copy it with its own ledger folder and a job cap). Ask me for a budget first ($3 covered Propolis's 29 pictures).
- Mockups: paint each chapter, show them on the real page with temporary local wiring (never committed), desktop and phone screenshots.
- Build: a build script like reference/ink-pages/propolis/build_propolis.py, the "ink" block in the product's data file, a QA script like scripts/qa/qa_propolis_ink.py. Keep qa_nuricell_ink, qa_propolis_ink, qa_home_ink, qa_nav and qa_fda green, and check on the built site (next start), not only the dev server.
- Template pieces that exist: Why can cross-fade (NuriCell's lantern) or spread gold out from a point (Propolis's cracks), or you can add a new optional mode. Buy can be a brush stroke or a painted scene with the real bottle standing in it. The painted sum is optional. Long names are sized to fit automatically; nameLockup sets one word plus a stacked pair (it reaches main with Propolis's October 16 update; if it isn't there yet, ask me).
- Go live only on my yes: push main, Vercel builds production, point bigh-website-demo.vercel.app at it, check it signed out, update docs/public-demo.md.

ABOUT TURMERIFIC (src/components/product/products/turmerific.ts)
- One ingredient, an optimized curcumin (Longvida). Don't name the supplier company.
- Two capsules a day, 60 per bottle, 30 days (or 60 days at one a day).
- "Why" today: "Why the form matters. A golden compound. A hard one to absorb." Its pictures today are cut turmeric roots, dark then lit.
- No People chapter (no person in its data). The credit is Dr. Jiankang Liu and Dr. Iris Wang.
- The name is one long word, split "Turm | erific" around the bottle; it is sized to fit automatically.
- The liver question in the FAQ is on hold until I finish my research.
```

---

## Nature Calm

```text
Let's give Nature Calm the Ink & Gold product page, the way we did Green Bee Propolis: NuriCell's ink template, but Nature Calm's own paintings in every chapter and its own signature moment in "Why it matters". Show me mockups of the paintings to pick from before building. Ask before any push or spending.

SETUP
- First read docs/handoff-2026-09-24.md, AGENTS.md, your memory (especially project_propolis_ink.md, project_nuricell_ink.md, feedback_never_redraw_product.md, feedback_never_ref_real_face.md, feedback_shared_theme_own_design.md, feedback_even_rhythm_no_repeats.md, feedback_bigh_california_not_asian.md), reference/ink-pages/propolis/README.md and docs/superpowers/specs/2026-10-09-nuricell-ink-design.md.
- Work in a new worktree from the latest origin/main: git worktree add -b nature-calm-ink ../bigh-nature-calm-ink origin/main --no-track, then npm ci. Add two entries to the main folder's .claude/launch.json: "bigh-nature-calm-ink" (dev, port 3056) and "bigh-nature-calm-ink-prod" (next start, port 3057).
- Other product sessions may run at the same time. Keep any template change optional, so NuriCell and Green Bee Propolis render exactly as now. Fetch and merge origin/main before any push. Use only translation keys m780 to m819 (start your translations script there).

RULES I'VE SET (follow them)
- Never redraw, repaint or restyle the bottle. Use the real approved bottle picture in public/images/products/. Only backgrounds are painted.
- Watercolor and ink, like the rest of the site. No photo-real scenes.
- BiGH is a California brand: nothing Asian-coded (no Chinese characters, teacups, "kintsugi"). The product's real origin story is welcome.
- One painting per chapter, each its own idea, calm and not busy. Gold leaf only where it means something. No lab glassware, no germs.
- Both bottles (the top of the page and Buy) as big as NuriCell's.
- Facts only from the product's data file and label. Never invent amounts, studies or claims. Write "animal study", not "rats". New sentences are drafts for me.
- Give me 2 or 3 labeled options with your pick, never long lists. Talk to me simply. Show pictures in a claude.ai artifact, on the real page template.

HOW PROPOLIS WENT (copy what worked)
- Pictures: GPT Image 2.5 through the helper pattern in reference/ink-pages/propolis/hf_propolis.py (copy it with its own ledger folder and a job cap). Ask me for a budget first ($3 covered Propolis's 29 pictures).
- Mockups: paint each chapter, show them on the real page with temporary local wiring (never committed), desktop and phone screenshots.
- Build: a build script like reference/ink-pages/propolis/build_propolis.py, the "ink" block in the product's data file, a QA script like scripts/qa/qa_propolis_ink.py. Keep qa_nuricell_ink, qa_propolis_ink, qa_home_ink, qa_nav and qa_fda green, and check on the built site (next start), not only the dev server.
- Template pieces that exist: Why can cross-fade (NuriCell's lantern) or spread gold out from a point (Propolis's cracks), or you can add a new optional mode. Buy can be a brush stroke or a painted scene with the real bottle standing in it. The painted sum is optional. Long names are sized to fit automatically; nameLockup sets one word plus a stacked pair (it reaches main with Propolis's October 16 update; if it isn't there yet, ask me).
- Go live only on my yes: push main, Vercel builds production, point bigh-website-demo.vercel.app at it, check it signed out, update docs/public-demo.md.

ABOUT NATURE CALM (src/components/product/products/nature-calm.ts)
- Many ingredients (CoQ10, NAC, L-theanine, tyrosine, carnosine, phosphatidylserine, resveratrol and more). "What's inside" has to show many without looking busy.
- Three capsules a day, 90 per bottle, 30 days. That is the same "3 x 30 = 90" NuriCell paints, so "How to take it" needs its own idea, not a repeat.
- "Why" today: "Why stress matters to your cells. Stress, seen from inside the cell." Its picture today is a microscope, dark then lit; a microscope can read as a lab, so think twice.
- People chapter: Dr. Jiankang Liu, with his real photo. NuriCell shows a painted portrait of him. Ask me whether to reuse that painting, use his photo, or do something else; never generate his face from scratch.
- The credit: "Developed by Dr. Jiankang Liu and Dr. Iris Wang."
- The name is two words, "Nature | Calm" around the bottle.
```
