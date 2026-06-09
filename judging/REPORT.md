# BiGH Homepage — Judge-Panel Enhancement Report (2026-06-09)

**Goal:** every section scores ≥8/10 from Steve Jobs, David Ogilvy, and Jony Ive
on content, UI design, and imagery (81 cells total).

## Score trajectory (each cell = content/UI/imagery, one judge)

| Round | Worst cells | Cells at 8+ | Avg per-judge minimum |
|---|---|---|---|
| 1 (baseline + first images) | imagery 1–3 across 5 sections; stories content 4 | ~4/81 | ~4.4 |
| 2 (full rebuild) | imagery 3s gone; stories 4→6 | 8/81 | 6.0 |
| 3 (evidence-first rebuild) | nothing under 5 | 9/81 | 6.3 |
| 4 (micro-craft pass) | nothing under 5 | 10/81 | 6.2 |

## Final scores (round 4) — Jobs / Ogilvy / Ive, content/ui/imagery

```
hero       7/7/7   7/7/7   8/7/7
yourmind   8/7/6   7/7/5   8/7/6
science    7/7/7   7/8/7   8/7/6
scientist  7/6/6   7/7/6   8/7/6
nuricell   8/7/5   7/7/6   8/7/6
system     6/7/7   7/7/7   7/7/7
stories    7/7/6   7/7/6   8/7/7
signup     7/6/5   7/7/6   8/7/6
founder    7/7/6   7/7/6   7/7/7
```

## Why the panel plateaus at 7 with AI-only assets

1. **The remaining blockers need real assets.** Across rounds 3–4 the judges'
   top imagery fixes converged on: commissioned photography ("the photo any
   brand could rent"), Mo Chen's real scanned signature, a real or licensed
   PNAS facsimile, real product labels/pack shots for all six formulas, and
   location photography that "doesn't share one golden AI-glow preset."
2. **At the 7→8 boundary the judges contradict each other and themselves.**
   Round 3 (Jobs): "strip the chemistry from the hero" → done → Round 4
   (Ogilvy): "name the nutrients in the body copy." Rounds 2–3 (Ogilvy/Ive):
   "add display-scale ghosted numerals" → done → Round 4 (Jobs): "the ghosted
   numerals are template decoration."
3. **Several content ceilings are business decisions, not copy edits.** All
   three judges want product renames ("Turmerific is a pun wearing a lab
   coat", "Advanced OPC is an acronym", "Deer Horn Reishi reads as deer
   antler"); Ogilvy wants price/guarantee/dose specifics that don't exist
   pre-launch; Jobs/Ive want a true founder-family anecdote only Mo can tell.

## What only Mo can supply to clear the 8-bar

- Real photographs: Dr. Liu, Mo Chen (or her real signature scan at minimum)
- Final product labels / pack shots for all six formulas (a "family portrait")
- A licensed/owned facsimile of the Feb 19, 2002 PNAS issue page
- Decisions: product naming (Turmerific / Advanced OPC / Deer Horn Reishi),
  price/guarantee language, the one true family sentence for the founder letter
- Optionally: a real brand photo shoot (one photographer, one light) for the
  hero, vignettes, and ingredient still-lifes

## Costs (verified from workflow telemetry)

- Pilot: 3 judges, 174k subagent tokens
- Rounds 1–4 panels: 27 judges each; 1.47M / 1.54M / 1.57M / 1.56M tokens
  (plus one round killed by a session limit and resumed from cache)
- Total judge-panel spend: ≈ 7.5M subagent tokens across 138 judge calls
- 25+ generated images (Gemini), 4 site-wide build rounds, all committed

## State of the page

All four rounds of work are committed on `homepage-rebuild`
(`96074a5`, `1b35f0f`, `51437c4` + final). Every section was rebuilt at least
once; every judge agrees the page improved every round and nothing regressed
below 5. Full per-judge feedback lives in `judging/round{1..4}/judgments-full.json`.
