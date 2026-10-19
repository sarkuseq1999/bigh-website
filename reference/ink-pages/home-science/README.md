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
