# Questions: a painting for each answer

The questions part of every ink product page (`src/components/product/ink/questions.tsx`). Mo picked
A, "a picture for each question", on October 26, 2026, from the mockups in
`reference/ink-pages/mockups/nuricell-questions/` (artifact `MceTcmgqxFuQPtLHrJ8xfE`): from 960px the
questions on the left and the picked one's painting and answer on the right; on a phone each
question opens in place with its painting.

## Paintings

One per question, 28 in all, Codex (`codex exec`, its built-in image tool) on Mo's ChatGPT plan: no
paid credits. The style is the homepage crane's (`../home-science/originals/style-crane.png`, sent with
every order); the shared words are in `prompts/_style.txt`, each subject in `prompts/subjects.txt`, and
each whole order in `prompts/<name>.txt`.

- `paint_questions.py [name ...]`: paints the subjects, eight at a time, into `originals/`.
- `build_questions.py`: divides the paper out, fades the edges, writes
  `public/images/products/<slug>/ink/q-<key>-v1.webp` and `src/components/product/ink/questions-art.ts`.
  Every painting stays 4:3, so each answer sits at the same height under its painting.

NuriCell's take, month, capsule and doctor paintings are the mockups' own. Repainted before building:

- NuriCell studied: the mockup's tray held what looked like star anise, which NuriCell does not
  contain; now four plain powders.
- NuriCell pregnancy: the mockup's booties looked like lumpy slippers.
- OPC studied: the first take's noni slice looked like lotus root (reads as Asian); now a whole noni.
- OPC month and Propolis month: 60 days must be two pages of 30 (six across, five down); the first
  takes had 25 and 20 squares a page. Propolis's kept painting is an edit of OPC's (a bee added),
  after three takes still came out four rows deep.
- Turmerific take: the first take's capsules were soft gels; Turmerific's are two-piece capsules.

Propolis month's order is `prompts/propolis-month.txt` (the edit), not its line in `subjects.txt`
(the last of the takes that came out four rows deep).

The rejected takes, Codex's logs, and the mockups' raw screenshots and paintings (the mockup page
keeps its own JPEGs in `../mockups/nuricell-questions/page/`) are in
`codes/bigh-archive/questions-unused-2026-10-26/`, outside the public repository.

## Checks

`scripts/qa/qa_questions.py <base-url>`: all five pages, wide and phone, no script, four languages.
