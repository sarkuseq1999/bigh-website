# Support page: handoff ("Pull up a chair", October 14, 2026)

Worktree `C:\Users\mcbig\Documents\codes\bigh-support`, branch `support-page` (from `main` c31650f).
Nothing is pushed: ask Mo before every push, merge or demo-alias change. Spec:
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
   bloomed and both its pictures are in (never alone on bare paper). The porch shrinks with the
   window's height so that at 1440x900 the first screen also holds the three ways to reach us
   (never under 560px wide; 590px at 1440x900; on windows under about 880px tall the contact row
   starts at the fold).
2. **Write to us** (mailbox, left): the form, writing lines on the paper, never boxes.
3. **Returns** (parcel on the steps, right): 45 days, the return address, orders and shipping.
4. **Questions** (an open book on the rail, left): four questions, one open at a time, then "Ask
   BiGH Science" (the site's existing sheet).

From 960px each part is one painting beside its words, sides taking turns (About's `Spread`); under
960px one column, painting first. The three paintings read about the same size: each takes a share
of its column by its shape (book 100%, parcel 86%, mailbox 68%), so their areas stay within 15% of
each other at every width. The book stands level with the first question and does not move when
an answer opens.

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
steam and a ticket number, and sends nothing. The page says so twice: the tag "Preview: messages
aren't sent yet" beside Send, and on the thank-you "This is a preview, so nothing was sent. To
reach us today, call ... or email ...". Setting the switch to `true` removes both lines; it does
not make anything send. Real sending still needs:

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
- A copy to the customer, if the lead "Your ticket number comes by email." is to stay true.

Without script the page shows no form at all, only a line with the email and the phone as real
links (a form without script would send its fields in the address).

## Words and languages

English only. None of the page's new words has a copy key yet, so every other language shows them
in English (the menu, footer and sheets stay translated). Translations come later through a
`reference/ink-pages/support/translations-support.cjs` written like
`reference/ink-pages/about-bc/translations-c.cjs`, from the next free key: m612 on October 14. The
four answers are drafts for Mo's check. The old pop-up's keys (m072, m073 and its FAQ) are now
used only by the unused `src/components/home/homepage.tsx`.

## Checks

Run each against the dev server and against the built site (the built site orders CSS differently):

- `python -X utf8 scripts/qa/qa_support.py <url>` (groups `opening`, `motion`, `rhythm`,
  `questions`, `form`, `links`, `languages`; `--only=` runs some): 293 checks. It covers the first
  screen, the steam's gate (slow and failed pictures), the sides and the sizes, every painting
  multiplying with no stacking context up to the page root, the form's every check, the
  thank-you and its focus, a double send, no script, forced colors, every Support link (and the
  phone menu closing when Support is chosen on /support), and the four languages.
- `scripts/qa/qa_nav.py`, `qa_home_ink.py`, `qa_about.py` (they expect the page, not the pop-up).
- `scripts/qa/home_snapshot.py nav <url> -`, then the homepage stays pixel-identical:
  `home_snapshot.py compare <url> <new-tag> baseline-support` on dev, or the same with
  `baseline-support-prod` on the built site.

## Traps

- Multiply: nothing between a painting and the page root (`[data-look]`) may make a stacking
  context (z-index on a positioned or grid item, isolation, opacity, transform, filter, mask,
  will-change). `qa_support.py` checks every painting and the cup.
- The steam's rise is keyed to `data-steam="ready"`, which script sets only once both pictures are
  in; keep that gate if the steam or the cup changes.
- Replacing a picture under the same file name: delete `.next/cache/images` and
  `.next/dev/cache/images`, or give it a new name (the build script versions its files).
