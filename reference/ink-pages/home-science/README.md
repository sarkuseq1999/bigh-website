# Homepage science section: one painting per topic (idea A)

October 19, 2026. Mo found the mitochondrion overused: it showed in "Tiny power plants." and three
more times in "Make sense of the science." She picked idea A (each tab its own everyday California
painting) from a mockup, then the Joshua tree over a second oak, since the About page's "Our
purpose" now has an oak.

| Tab           | Painting                                    | Original                                     | Site picture (`public/images/home-v2/ink/science/`) |
| ------------- | ------------------------------------------- | -------------------------------------------- | --------------------------------------------------- |
| Mitochondria  | Hummingbird at California hummingbird sage  | `hummingbird-a1`                             | `hummingbird-v1` (+ `-gold`, the wings' leaf)       |
| Free radicals | Cut apple, one half browned; Meyer lemon    | `apple-lemon-a5`                             | `apple-lemon-v1`                                    |
| Aging cells   | Joshua tree: young, middle, old (slider)    | `joshua-young-a1`, `-middle-a1`, `-old-a1`   | `joshua-young-v1`, `-middle-v1`, `-old-v1`          |

- Painted by Codex (`codex exec`, its built-in image tool) on Mo's ChatGPT plan, about a minute
  each, no API spend. Prompts in `prompts/` under the same names; `_style.txt` is the shared style.
- References: `apple-lemon-a5` used the homepage crane (on paper) as a style reference, and
  `joshua-old-a1` used `hummingbird-a1`. `joshua-young-a1` and `joshua-middle-a1` were painted from
  `joshua-old-a1`, so the ground, the stones and the trunk's foot line up.
- `build_home_science.py` divides the paper out, dissolves paint at the edges, crops (one crop for
  the three trees) and fits each into the stage's 1600 x 1195 box; it also cuts the hummingbird's
  gold mask from its wings only.
- The slider never blends two trees: young to 42, middle from 43, old from 68 (opens at 45).
- Unused takes (four apples, two oak pairs) are in
  `C:\Users\mcbig\Documents\codes\bigh-archive\home-science-unused-2026-10-19\`.
- Mockups shown to Mo: `reference/ink-pages/mockups/home-science/`
  (https://claude.ai/artifact/T6vjFHVwfJ4ENzNeHhbAfe).

## October 21, 2026: the steam train (idea A, test branch `home-science-train`)

Mo found the October 19 paintings decorative, then a hiker with a round window into a cell (branch
`home-science-hiker`) hard to relate to: the cell read as "a ball with worms in it". Of three
new ideas painted as quick samples (mockup: `reference/ink-pages/mockups/home-science-ideas/`), A
the train, B the campfire (`campfire-sparks-a1`) and C the clear mitochondrion (`mito-clear-a1`),
Mo chose A: one small
steam engine in the redwoods, as the cells' "tiny power plants" are, with a line under each picture
that ties it to the words.

| Topic         | Painting                                              | Original             |
| ------------- | ----------------------------------------------------- | -------------------- |
| Mitochondria  | The fireman feeds a log to the gold fire              | `train-fuel-a2`      |
| Free radicals | The smokestack's mesh screen holds the sparks         | `train-sparks-c1`    |
| Aging cells   | The same engine new, well worn, old (the age slider) | `train-new-a1`, `train-middle-a1`, `train-old-a1` |

- `train-sparks-a1` (the first sample) was too dark and drawn; `train-sparks-b1` painted it again
  lighter and looser and is the base the others were painted from, so they line up.
- `build_train.py` makes the site's `train-<state>-v1.webp` (the originals are 4:3, the stage's
  shape). The fire is the one gold leaf; there is no band of light over it.
- Codex once hung waiting for input: `codex exec` needs `< /dev/null` when run from a script.

### Round 2, polished (v2 pictures)

Mo asked for looser, lighter ink, bigger sparks, and new and well worn easier to tell apart. The
homepage crane (`reference/home-v2/ink/originals/gpt25-crane-paint-a.png`, copied here as
`style-crane`) was given to Codex as the style to copy; `train-loose-a2` is the new base, and the
others were painted from it.

| Topic         | Original           | Site picture          |
| ------------- | ------------------ | --------------------- |
| Mitochondria  | `train-fuel-b1`    | `train-fuel-v2`       |
| Free radicals | `train-sparks-e2`  | `train-sparks-v2`     |
| Aging: new    | `train-new-b1`     | `train-new-v2`        |
| Aging: worn   | `train-worn-b1`    | `train-middle-v2`     |
| Aging: old    | `train-old-b1`     | `train-old-v2`        |

- Sparks: `train-sparks-d1`/`-d2` had big sparks but most flew free; `-e1`/`-e2` keep about ten
  inside the screen and let two escape (`-e2` shows them leaving the screen).

