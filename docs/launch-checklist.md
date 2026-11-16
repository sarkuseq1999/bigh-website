# English launch checklist

November 16, 2026. What the English site needs on launch day, and where each switch lives. The
site itself is ready (Mo's goal of November 16: no placeholder words, nothing that reads as
unfinished); the items below are the outside services and decisions it plugs into.

## On launch day (Vercel → Project → Settings → Environment Variables, Production, then redeploy)

| Setting                | Value                                   | What it does                                                                                                                                                                                                                    |
| ---------------------- | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SITE_INDEXING`        | `on`                                    | Opens the site to search engines: `robots.txt` allows it and lists the sitemap, every page's robots tag says index. Leave it unset on the demo and previews. (`src/lib/seo.ts`)                                                 |
| `NEXT_PUBLIC_SITE_URL` | usually leave unset                     | The site's address for canonical links, the sitemap, link previews and structured data. Unset, it is https://bighnow.com once `SITE_INDEXING` is on, and the public demo before then. Set it only to launch on another address. |
| `RESEND_API_KEY`       | from resend.com                         | The Support form sends real email (`src/lib/support-mail.ts`, `/api/support`).                                                                                                                                                  |
| `SUPPORT_EMAIL_FROM`   | e.g. `BiGH <support@bighnow.com>`       | The sender. Its domain (bighnow.com) must be verified in Resend: Resend shows the DNS records to add at GoDaddy.                                                                                                                |
| `SUPPORT_EMAIL_TO`     | optional, default `support@bighnow.com` | Where messages arrive.                                                                                                                                                                                                          |

Until `RESEND_API_KEY` and `SUPPORT_EMAIL_FROM` are both set, the form keeps its placeholder line
("Preview: messages aren't sent yet") and sends nothing; once set, the form sends the message to the
support inbox (reply-to the customer, the photo attached, a reaction report marked URGENT) and a
confirmation with the ticket number to the customer.

## The shop (BiGH's own back office, Mo, November 16, 2026)

Everything the site needs from the shop is in `src/components/shop/shop.ts`:

- `checkoutUrl(slug)`: where Add to cart goes for each product. While it returns `null`, Add to
  cart says "Our online shop opens soon. Until then, call us at 800-919-2089 and we'll help."
- `LOGIN_URL`: Log in (now the back office demo, `bigh-vn-demo.vercel.app`; change it to the new
  back office's sign-in page).
- `SIGNUP_URL`: Sign up (`null` keeps the button a quiet placeholder).
- `PRICES`: NuriCell and Nature Calm $80, Advanced OPC Formula $65, Turmerific $50, Green Bee
  Propolis $36 (bighnow.com's prices; Mo picked them November 16). The product pages and their
  search data show them; keep them equal to the shop's.

When the shop is live, also change the Support page's "Orders and shipping" line
(`support-content.ts` `returns.orders`).

## Still Mo's call

- **Legal pages** (`/privacy`, `/terms`, `/returns`): BiGH's 2016 documents from bighnow.com, wording
  kept, typos fixed, every mailbox now support@bighnow.com (`src/components/legal/legal-content.ts`).
  Have a lawyer review them: they predate California's newer privacy rules (no "Do Not Track" or
  CCPA wording).
- **Studies of people with a disease on product pages**: NuriCell's memory-problem and mild
  Alzheimer's reviews, Green Bee Propolis's type 2 diabetes trial, Advanced OPC Formula's
  blood-pressure study. Each is labeled honestly, but 21 CFR 101.93 can read a disease study shown
  next to a product as an implied disease claim. Worth the same lawyer's look (or keep them in the
  Science page's library only).
- **Two label quotes to check** against the printed Advanced OPC Formula label: "green tea 45" (no
  %) and "d-alpha-tocopherol succinate" (usually "tocopheryl").
- **Customer stories**: still the three fictional samples (Mo, November 16: keep them), labeled
  "Illustrative stories: the people and names below are fictional, not real customers." Replace them
  with real customers' words (with permission) when there are some.
- **Translations**: the other four languages' new lines are drafts (keys m1260-m1273 and the rewritten
  m064-m071, m113, m115, m320, m334), not checked by native speakers.

## Checked

`reference/launch/` holds the scripts of this pass: `copy_launch.py` (American spelling and the
launch rewrites, keeping each line's translations), `make_icons.py` (the site icons from the logo's
leaves).
