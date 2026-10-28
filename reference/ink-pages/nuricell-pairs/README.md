# NuriCell pairs: on the ranch

"Why these four work together" on NuriCell's ink page. Mo found the 1A scenes' white powder heaps
with gold on top "a little strange, like drugs" (October 27, 2026). Ideas page (A two hands, B an old
California ranch, C a gold trail map): `../mockups/nuricell-pairs/index.html`, artifact
`H9XUk1ya3vXH7Ei7WvghnL`. Mo picked **B**. Built page recorded: `../mockups/nuricell-pairs/built.html`,
artifact `S6d2aNgCzBhZMUHdoQQebb`.

## Pictures

All by Codex on Mo's ChatGPT plan (`codex exec`, the crane style reference), no paid credits.

| Original (`originals/`)      | Prompt                                                   | Used as                          |
| ---------------------------- | -------------------------------------------------------- | -------------------------------- |
| `ranch-stove.png`            | `prompts/subjects.txt` (`ranch-stove`) + `_style.txt`    | firewood and the stove (flipped) |
| `ranch-windmill-v2.png`      | `prompts/subjects.txt` (`ranch-windmill-v2`) + `_style.txt` | the windmill and its tank     |
| `ranch-windmill-nowheel.png` | `prompts/ranch-windmill-nowheel.txt` (an edit of v2)     | the still windmill under the wheel |
| `ranch-rider.png`            | `prompts/subjects.txt` (`ranch-rider`) + `_style.txt`    | the rider and his horse          |

`paint_pairs.py` sends the orders in `prompts/subjects.txt` (one line per picture); the wheel-less
repaint was sent by hand with the attached painting (`-i`). Run `codex exec` with stdin closed
(`< /dev/null`): left open, it waits forever.

`build_nuricell_pairs.py` turns them into the site's pictures (`public/images/products/nuricell/ink/
pair-*-v1.webp`) and writes `src/components/product/ink/nuricell-pairs.ts`.

The originals of ideas A and C, the first windmill (its gold read as straw) and the first keepsake
tin (it read as a stash tin) are in `C:\Users\mcbig\Documents\codes\bigh-archive\nuricell-pairs-2026-10-27\`.
