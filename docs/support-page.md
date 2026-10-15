# Support page: handoff ("Pull up a chair", October 14, 2026)

Worktree `C:\Users\mcbig\Documents\codes\bigh-support`, branch `support-page` (from `main` c31650f;
`origin/main` c62661b, the footer without a logo and the FDA trail sign, merged in locally on
October 14). Nothing is pushed: ask Mo before every push, merge or demo-alias change. Spec:
`docs/superpowers/specs/2026-10-14-support-page-design.md`; plan:
`docs/superpowers/plans/2026-10-14-support-page.md`.

## What the page is

Mockup A, the porch (Mo, October 14: "It's pretty cool"; approved screens in
`reference/ink-pages/mockups/support/`). The last page of the Ink & Gold restyle; it replaces the
Support pop-up, which is gone. Every Support link (the menu bar, the phone menu, the footer's
"Support & FAQs", the Science page's own header and footer) now leads to `/support`.

1. **Opening**: a California porch (two empty chairs, a cup whose steam is gold leaf), "How can we
   help?", "Pull up a chair. We're listening.", then Call us 800-919-2089 (`tel:`, set in
   Switzer), Email us support@bighnow.com (`mailto:`), Hours. The steam rises once the porch has
   bloomed and both its pictures are in (never alone on bare paper); with reduced motion it is
   hidden until both are in, then simply there. It and the mailbox load at low priority, so only
   the porch is preloaded. The porch shrinks with the window's height so that at 1440x900 the first
   screen also holds the three ways to reach us (never under 560px wide; 590px at 1440x900; on
   windows under about 835px tall, measured at 1440 wide (820px at 1280, 850px at 1536), the
   contact row runs past the fold).
2. **Write to us** (mailbox, left): the form, writing lines on the paper, never boxes.
3. **Returns** (parcel on the steps, right): 45 days, the return address, orders and shipping.
4. **Questions** (an open book on the rail, left): four questions, one open at a time, then "Ask
   BiGH Science" (the site's existing sheet).

From 960px each part is one painting beside its words, sides taking turns (About's `Spread`); under
960px one column, painting first. The three paintings read about the same size: each takes a share
of its column by its shape (book 100%, parcel 86%, mailbox 68%), so their areas stay close (13%
apart at most when measured; the QA allows 20%). The book stands level with the first question and
does not move when an answer opens. Questions keeps its bottom half-gap like every part (about
125px of paper above the footer, as on the homepage): the footer from main opens straight onto its
link columns, and without the gap the Ask BiGH Science pill read as the footer's.

## Where its parts live

- Route: `src/app/[locale]/support/page.tsx` (`/hken/support` redirects to `/cns/support`).
- Components, `src/components/support/`: `support-ink.tsx` (the page and its parts), `spread.tsx`
  (`Painting`, `Spread`, the steam gate `useSteamGate`), `support-form.tsx` (the form, its checks,
  the thank-you), `support-rules.ts` (field checks and the ticket number), `support-content.ts`
  (every word, the painting descriptions, `SENDING_LIVE`), `support-page.module.css` (every rule
  under `.supportPage`), `support-art.ts` (generated).
- Paintings: `reference/ink-pages/support/` (prompts, originals, plates, `build_support.py`, which
  writes `public/images/support/*.webp` and `support-art.ts`, and `check_support.py`). Spend:
  `reference/ink-pages/spend-support.md` (10 GPT Image 2.5 jobs, about 50¢ of Mo's $1).
- Servers: dev `bigh-support` on http://localhost:3060, built site `bigh-support-prod` on
  http://localhost:3061 (`next start`). The plan named 3050/3051; the Science session holds 3050.

## The preview switch and real sending

`SENDING_LIVE = false` in `support-content.ts`. The form checks everything, shows the cup, the
steam and a ticket number, and sends nothing. The page says so twice and promises nothing a
preview cannot keep (Ruling 16, Mo's honesty rule over the spec's wording):

- Write to us's lead is "We reply within 1–2 business days." (true of the phone and the email);
  the spec's "Your ticket number comes by email." is held back.
- Beside Send, the tag "Preview: messages aren't sent yet".
- On the thank-you, straight under "Thank you." and before the ticket number: "This is a preview,
  so nothing was sent. To reach us today, call 800-919-2089 or email support@bighnow.com.", the
  number and the address real `tel:` and `mailto:` links. The spec's "We'll reply by email within
  1–2 business days." is held back.

Setting the switch to `true` brings the spec's words back (the lead's ticket line, the thank-you's
reply line) and removes both preview lines; it does not make anything send. Before it may be
turned on, the client side needs:

- **An async send** to the server route, with a "sending" state on Send and a failure state that
  says so plainly and keeps every word the customer wrote (today Send swaps the form for the
  thank-you at once, which only a preview can do).
- **The ticket from the server**: the thank-you shows the number the service issued, never the
  browser's `ticketNumber()`.
- **The cancelled-picker fix**: cancelling the file dialog after a photo was chosen empties the
  input but leaves the old photo in state; the send must read one source of truth (clear the photo
  when the input empties).
- **A privacy notice** beside the form: what is kept and for how long, who reads it, for health
  reports ("I had a reaction") and photos in particular.

Real sending also needs, on the server:

- **Resend through Vercel** (the Marketplace integration), its API key as a server-only variable.
- **bighnow.com's DNS records at GoDaddy**: the sending-domain records Resend gives (SPF, DKIM and
  a DMARC policy), so mail from the site is not junked.
- **A server route** (a route handler or server action) that checks the fields again, mails
  support@bighnow.com with the customer's email as reply-to (and the topic, the order number and
  the photo as an attachment, pictures only, up to 4 MB), and puts "I had a reaction" first.
- **A ticket number the service issues** and stores. Today's number (`BH-` + month and day + four
  signs) is made in the browser by `ticketNumber()` and means nothing to the team.
- **Spam guards**: a hidden honeypot field, a rate limit per address, and a bot check (Vercel
  BotID or Turnstile) before the mail goes out.
- A copy to the customer, since the live lead says "Your ticket number comes by email."

Without script the page shows no form at all, only a line with the email and the phone as real
links (a form without script would send its fields in the address).

## Words and languages

English only. None of the page's new words has a copy key yet, so every other language shows them
in English (the menu, footer and sheets stay translated). On those languages the page's content is
marked `lang="en"` (so a screen reader reads it in English) while the document, the menu and the
footer keep the locale's; the three words that already had keys ("Your name", "45 days to
decide.", "Ask BiGH Science") show translated and carry the locale's tag (`useWordsLang` in
`spread.tsx`). When the translations land, drop the wrapper's `lang="en"`. They come through a
`reference/ink-pages/support/translations-support.cjs` written like
`reference/ink-pages/about-bc/translations-c.cjs`, from the next free key (m618 on October 15: Green
Bee Propolis took m612-m617). Read the highest key in `src/i18n/copy-keys.json` first.
Mo approved the spec, the four answers included, on October 14 ("yes"). The old pop-up's keys
(m072, m073 and its FAQ) are now used only by the unused `src/components/home/homepage.tsx`.

## Checks

Run each against the dev server and against the built site (the built site orders CSS differently):

- `python -X utf8 scripts/qa/qa_support.py <url>` (groups `opening`, `motion`, `rhythm`,
  `questions`, `form`, `links`, `languages`; `--only=` runs some). It covers the first screen and
  what is preloaded, the steam's gate (slow and failed pictures, with motion and with reduced
  motion, on the porch and on the thank-you's cup), the sides and the sizes, every painting
  multiplying with no stacking context up to the page root, the form's every check (and that a
  screen reader hears each error as focus lands), the preview's honest words and their order, the
  thank-you and its focus, a double send, no script, forced colors, every Support link (and the
  phone menu closing when Support is chosen on /support), and the four languages and their `lang`.
- `scripts/qa/qa_nav.py`, `qa_home_ink.py`, `qa_about.py` (they expect the page, not the pop-up),
  and `qa_fda.py` (the shared footer's FDA sign).
- `scripts/qa/home_snapshot.py nav <url> -`, then the homepage stays pixel-identical to
  `origin/main`'s: `home_snapshot.py compare <url> <new-tag> baseline-main` on dev, or the same with
  `baseline-main-prod` on the built site (both taken from `origin/main` c62661b on October 14; the
  older `baseline-support` sets predate the new footer).

## Traps

- Multiply: nothing between a painting and the page root (`[data-look]`) may make a stacking
  context (z-index on a positioned or grid item, isolation, opacity, transform, filter, mask,
  will-change). `qa_support.py` checks every painting and the cup.
- The steam's rise is keyed to `data-steam="ready"`, which script sets only once both pictures are
  in; keep that gate if the steam or the cup changes.
- Replacing a picture under the same file name: delete `.next/cache/images` and
  `.next/dev/cache/images`, or give it a new name (the build script versions its files).
- A gold layer must not be preloaded: React's server render writes a preload for every `<img>`
  that is not lazy unless its `fetchPriority` is low, and a preloaded leaf wins the race.
- October 14, unexplained: on a server (dev or `next start`) that had already run the long suites,
  one `/_next/image` answer at `w=640` in WebP never came (the Science page's `dark-cell.webp`
  twice, NuriCell's `lantern-unlit-v4.webp` once), so `qa_fda.py` timed out waiting for
  `networkidle`; the same URL without WebP, other widths and a restarted server all answered at
  once. Seen three times on this branch's servers after about an hour of suites, never on a fresh
  server (nor after `qa_support.py` alone), and not in one run of main's own suites on `origin/main`'s
  build. If `qa_fda.py` times out on `goto`, restart the server and run it again before suspecting
  the page.

## Merge notes

- **science-ink** (branch `science-ink`, not on main yet) deletes `science-page.tsx`,
  `science-page.module.css`, `site-chrome.tsx` and `site-chrome.module.css`, which this branch
  edits (their Support links lead to `/support`, the old support panel goes). When the two meet,
  keep science-ink's deletions (Ruling 19), then check that the new Science page's header and
  footer Support still lead to `/support` (`qa_support.py`'s `links` group).
- Merging `main`: use `git -c core.autocrlf=false merge ...` in this checkout, or every touched
  file comes back with CRLF.
