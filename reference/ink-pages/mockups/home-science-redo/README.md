# Homepage science: the paintings again (November 20, 2026)

Mo sent the live Mitochondria and Free radicals paintings (the California ranch workshop and its
sparks, November 14): "The artwork on this section doesn't really looked that good, can you help
redesign and give me some mock up ideas".

Claude's reading of why: they are storybook drawings, not watercolors (hard cut-out edges, heavy
brown, about ten parts in one picture), beside pages painted in a few wet washes (the mailbox,
the hummingbird).

## Mo picked A, the lantern (November 20, 2026)

Built the same day: `lantern-fuel-v1.webp` and `lantern-soot-v1.webp` from
`reference/ink-pages/home-science/build_lantern.py` (the mockup's own fit: paper to white, a
little more body, edges feathered), `sciencePaintings` in `assets.ts`, and the line under each in
`content.ts` (`science.peek`). The stove and wheel originals, not picked, are in
`bigh-archive\home-science-redo-unused-2026-11-20\` (their prompts stay in `prompts/`).

## Round 1: three ideas, one object each

All in the mailbox's hand (`home-ask/originals/mailbox-4.png` attached as the brush reference):
one object, a few wet washes, bare paper, gold leaf only where the energy is. Each idea is a pair;
the second picture was painted with the first attached, so it is the same object.

| Idea | Mitochondria | Free radicals | Claude's score |
| --- | --- | --- | --- |
| A, the lantern (Claude's pick) | `redo-lantern-1` | `redo-lantern-soot-1` (soot dims the glass) | 9 |
| B, the wood stove (Mo's story kept) | `redo-stove-1` | `redo-stove-sparks-1` (screen, three burns) | 8.5 |
| C, the water wheel | `redo-wheel-1` | `redo-wheel-rust-2` (rust on the hub) | 8 |

`redo-wheel-rust-1` (a close view of the hub) was hard to read and is not shown.

Originals: `reference/ink-pages/home-science/originals/redo-lantern-*.png` (the others in the
archive); prompts under the same names
in `prompts/` (`redo-_style.txt` is the shared part); `paint_redo.sh` sends them to Codex (plan
allowance, no API spend).

## How the mockups are made

- `prep.py <name> [scale] [deepen]` fits an original to the stage's 4:3 frame on white (`art/`).
- `shoot.py <base-url> <key> <fuel> <sparks> "<line 0>" "<line 1>"` swaps the two paintings and
  the line under each in the browser only, on the built site (localhost:3006), and captures
  1440x1000 and 390x844 for both topics (`shots/`). No site file changes.
- `build_review.py` builds `review.html` from `review.json`.

The mockups swap pictures in the browser only; `art/`, `shots/` and `review.html` are not
committed (re-make them with the three scripts).

Review page: https://claude.ai/artifact/FA5ZvK6u13BzusHLvwq3XB (private to Mo).
