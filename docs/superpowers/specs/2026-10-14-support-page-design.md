# Support in Ink & Gold: "Pull up a chair"

October 14, 2026. Branch `support-page` (worktree `codes/bigh-support`), from `origin/main` c31650f.
The last page of the site-wide restyle (`2026-10-05-ink-pages-design.md`, which left Support for
later). Today "Support" in the menu and the footer opens a pop-up sheet; this spec gives it a real page.

## Decisions (Mo, October 13-14, 2026)

- **Content** (October 13): talk to us (phone, email, hours); a message form with a ticket number;
  report a reaction; returns; orders and shipping; common questions; health and science questions
  go to Ask BiGH Science. The 2016 contact and return details are still true. One email address only.
- **Three ideas were mocked** (A the porch, B the open door, C four circles). Mo picked **A**
  ("It's pretty cool"). Approved screens: `reference/ink-pages/mockups/support/`.
- **California, not Asian** (October 13): the first A was tea offered with two hands; it became a
  California porch. No seals, stamps or Chinese motifs (`DESIGN.md`'s No Red, No Seal Rule).
- **The form looks and behaves completely but sends nothing yet** (October 14). The email service
  (Resend through Vercel) and the GoDaddy DNS records for bighnow.com come later. Until then the
  form says so (see "Honesty").
- **English only for now.** The team can reply in all five languages; translations come later.

## Shared, and its own

Shared (the theme): the kit's rice paper, sumi ink, gold leaf only for energy, the site menu bar
(`SiteHeader`, current "Support"), the footer with the crane at rest and the FDA statement
(`SiteFooter`), the ink bloom, honesty captions, the one breath and its ease, reduced motion complete
and still, Switzer for reading text and the homepage's Ysabeau for titles. `DESIGN.md` applies unless
named here.

Its own: a California porch and the things around it (a mailbox, a parcel on the steps, a book on the
rail), and its signature moment: **the cup's gold steam rises**, once when the page opens and again
when a message is sent. No brush line, no stations, no ensō, no lantern, no reused painting.

## The page, top to bottom

From 960px, every part after the opening is **one painting on one side, its words on the other**
(About's `Spread`: 5/7 columns), sides taking turns. Under 960px it is one column, the painting first,
then its words. Gaps follow About's rhythm.

1. **Opening, centred.** The porch painting (about 780px wide on a desktop, the column's width on a
   phone): two empty chairs turned toward each other, a small table, one cup, golden hills and a valley
   oak in mist, the steam in gold leaf. Under it the title "How can we help?" and "Pull up a chair.
   We're listening." Then one row of three, split by hairlines (stacked on a phone): Call us
   **800-919-2089**, Email us **support@bighnow.com**, Hours "Monday to Friday, 9am to 6pm Pacific".
   The number and the address are real links (`tel:`, `mailto:`). The number is set in Switzer, never
   Ysabeau, whose old-style digits rise and fall.
2. **Write to us** (mailbox at the left). The form, described below.
3. **Returns** (parcel on the porch steps, at the right). "45 days to decide." Not happy? Send it back
   within 45 days for a full refund, no questions asked; shipping isn't refunded. After 45 days,
   unopened bottles can still be returned for up to a year. "Send returns to" BiGH, 2200 E Route 66,
   Suite 103, Glendora, CA 91740. A hairline, then "Orders and shipping": the new store opens soon;
   until then no orders or payments are taken on this site.
4. **Questions** (an open book on the porch rail, at the left; repainted, see "Paintings"). "Common
   questions." Four questions on hairlines, each opening its answer (one open at a time, the first open
   at rest), answers drafted for Mo's check:
   - "How do I take my supplements?" Follow the directions on your bottle's label. For questions about
     your own health, ask your doctor or pharmacist.
   - "Can I take them with my medicines?" Please ask your doctor or pharmacist first. They know your
     medicines and your health.
   - "Where is my order?" Our new store opens soon. Until then, call or email us and we'll help.
   - "Is this site in my language?" Choose English, Chinese, Korean, Vietnamese or Japanese at the top of
     any page. Write to us in any of them, and we'll reply in yours.

   Under them "A question about health or science?" and the outlined pill "Ask BiGH
   Science", which opens the site's existing Ask BiGH Science sheet.
5. **The footer**, as on every page.

## The form

Writing lines on the paper, never boxes (`DESIGN.md`: nothing is boxed). Each field is its label
(17px, Ink Grey) over one hairline that darkens to ink with focus. Every control is at least 48px tall.

- **Your name**, **Email**, **Order number (optional)**.
- **What is it about?** One choice, as the kit's filter chips: An order · A return · A product
  question · I had a reaction · Something else. They break three and two, never one alone on a row.
- **Your message**: ruled writing lines (four on a desktop), growing as it fills.
- **Add a photo (optional)**: a text link that opens the file picker; the chosen file's name shows
  with a way to remove it. Pictures only, up to 4 MB.
- **Send message**, the solid ink pill.
- Under it: "Had a reaction to a product? Choose “I had a reaction” and a person reads it first. In an
  emergency, call 911."
- **Checks** happen on Send, in plain words beside the field, and focus goes to the first one:
  "Please add your name." / "Please add an email we can reply to." / "Please choose what it's about." /
  "Please write your message." / "Photos up to 4 MB, please."

## The moment

1. **On arrival** the porch blooms in like every painting, then its gold steam rises: the gold layer is
   revealed from the cup upward through a soft mask over one breath (about 2.4s).
2. **On Send** (all checks passed) the form fades out (0.3s) and in its place the cup blooms (a cut of
   the porch painting, the cup and its steam only), its steam rises again, and under it: "Thank you.",
   "Your ticket number", the number in large type (`BH-` + month and day + four letters and digits,
   for example BH-1014-7K3Q), and "We'll reply by email within 1–2 business days." Focus moves to
   "Thank you." A text link "Write another message" brings back an empty form.
3. **Reduced motion:** the steam is simply there; Send swaps the form for the thank-you at once.

## Honesty

While nothing is sent, the page says so plainly, in the kit's honesty tag (caption type, Ink Grey
outlined pill): "Preview: messages aren't sent yet" beside Send. The thank-you adds: "This is a
preview, so nothing was sent. To reach us today, call 800-919-2089 or email support@bighnow.com."
One switch in the code removes both lines when real sending arrives.

## Links that change

- **Menu bar:** "Support" becomes a link to `/support` (desktop line and phone sheet) and carries the
  current-page stroke there, as About does on `/about`.
- **Footer:** "Support & FAQs" links to `/support`.
- **Science page's own menu and footer** (`src/components/science/site-chrome.tsx`): Support links to
  `/support`; its own support panel goes.
- **The Support pop-up goes** (`openSupport` in `src/components/ink/dialogs.tsx`).
- `src/components/home/homepage.tsx` is unused and is left alone.

## Paintings

Loose sumi-e brushwork like the homepage's crane (GPT Image 2.5, the crane painting as the brushwork
reference). From the mockup round: the porch (second, looser try), the mailbox, the parcel. **The book
is repainted** (one job, about 5¢; the mockup's was the plainest). The porch is split into an ink plate
and a gold steam layer, plus a cup-and-steam cut for the moment. Originals, prompts and sidecars go to
`reference/ink-pages/support/originals/`; plates are made the way About's are (`build_bc.py`'s divide,
level and gold mask) into `public/images/support/` with a generated `support-art.ts`.

## Words and languages

New copy keys start at m612 and go into the English catalog only; every other language shows the
English words until the translations are made. `/hken` redirects to `/cns` as on every page.

## Checks

- New `scripts/qa/qa_support.py`, on the dev server and on the built site (`next start`): desktop and
  phone layout, no sideways scroll, the rhythm, every field's check, the thank-you and its focus,
  "Write another message", reduced motion, the menu's and footer's links arriving here, the current
  stroke, the other four languages showing English cleanly.
- Update the checks that expect the pop-up (`qa_nav.py`, `qa_home_ink.py`, `qa_about.py`,
  `home_snapshot.py nav`) to expect the page.
- The homepage stays pixel-identical (`home_snapshot.py compare`).
- Before showing Mo: my own full-size, scrolled look on desktop and phone, scored honestly.

## Not in this spec

Real sending (Resend), the GoDaddy DNS records, storing tickets, "track my order", "start a return",
login help, translations. Pushing and the demo alias each need Mo's yes.

## Risks

- **Other sessions edit the same files.** The Science session may replace the Science page's chrome;
  the menu bar and footer are shared by every page. Merge `origin/main` before any push and resolve by
  hand.
- **A preview form on a public site.** A real customer could try it; the honesty lines and the real
  phone number and email next to it cover that.
