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

## October 22, 2026: Aging cells becomes a brain cell (B, up close)

Mo found the engine growing old did not relate to the age slider and asked for painted cells
that age. Tried first (Codex, with `style-crane` as the style to copy): a cut-open school cell
(`cut-young-b2`; read as a cheese wheel, then a rock) and a patch of cells (`patch-young-a1`;
read as frog eggs). A brain cell worked. Mockup with working sliders:
`reference/ink-pages/mockups/home-science-cell/` (https://claude.ai/artifact/CZWSusKfxzSY8wbbe9FRTH).
Mo picked B, the cell up close, over A, the whole cell like an oak in winter (`neuron-young-a1`,
`neuron-middle-a1`, `neuron-old-b2`; its gold was too small on a phone).

| Age    | Original          | Site picture     |
| ------ | ----------------- | ---------------- |
| Young  | `close-young-a2`  | `cell-young-v2`  |
| Middle | `close-middle-a1` | `cell-middle-v2` |
| Old    | `close-old-a1`    | `cell-old-v2`    |

- `close-young-a2` was painted from `neuron-young-a1` (closer, broader strokes); the middle and
  old cells from `close-young-a2`. Codex moved and resized them a little, so `build_cell.py`
  scales each about its centre and shifts it back (values measured by the mockup's `align.py`)
  before dividing the paper out.
- Gold power plants: six (young), three (middle), one (old). No band of light over them.
- The first two topics kept the steam engine (`build_train.py`) until October 22, below.
- Unused takes: `C:/Users/mcbig/Documents/codes/bigh-archive/home-science-cell-2026-10-22/`.
- Reference pictures go to `codex exec` with `-i`, which takes several files: put `--` before the
  prompt, or `-i` swallows it.

## October 22, 2026: inside the powerhouse (Mitochondria and Free radicals)

Mo asked for a power plant instead of the steam train. Six painted ideas (mockup:
`reference/ink-pages/mockups/home-science-plants/`): A a brick powerhouse by a river
(`plant-brick-a1`), B a powerhouse at a Sierra waterfall (`plant-hydro-a2`), C a power station
lighting a town (`plant-town-a1`), D inside the powerhouse (`plant-inside-a2`), E a tiny powerhouse
on a palm (`plant-hand-a2`), F an old dynamo (`plant-dynamo-a1`). Mo picked D. Aging cells keeps
the brain cell (`build_cell.py`).

| Topic         | Painting                                                           | Original          | Site picture      |
| ------------- | ------------------------------------------------------------------ | ----------------- | ----------------- |
| Mitochondria  | The open powerhouse: log into the gold fire, steam turns the wheel | `plant-fuel-b1`   | `plant-fuel-v1`   |
| Free radicals | The chimney opened up: sparks rise into the screen, two escape     | `plant-sparks-a1` | `plant-sparks-v1` |

- `plant-fuel-b1` repainted `plant-inside-a2` in the crane's hand (`style-crane`), grey ink instead
  of pink brick and fewer parts; `plant-sparks-a1` was painted from `plant-fuel-b1`.
- `build_plant.py` makes the site pictures. Unused tries:
  `C:/Users/mcbig/Documents/codes/bigh-archive/home-science-plant-2026-10-22/`.


## October 23, 2026: Free radicals shows the harm

Mo found the chimney picture showed sparks caught but no harm, and free radicals harm us. Three
painted ideas (mockup: `reference/ink-pages/mockups/home-science-harm/`): A the few sparks that slip
past the screen burn holes in the roof (`harm-roof-a2`), B stray sparks burn the wheel and belt
(`harm-wheel-a1`), C two chimneys, with and without a screen (`harm-split-a1`). Mo picked A.
`harm-roof-b1` repainted it with the burns darker and only a dull fleck of gold in each, so the
black burns read first; `build_plant.py` ships it as `plant-sparks-v2`. Unused tries:
`C:/Users/mcbig/Documents/codes/bigh-archive/home-science-harm-2026-10-23/`.
