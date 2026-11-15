# California science set: public demo, November 14, 2026

https://bigh-website-demo.vercel.app/#science

Release: `f5cc4c69a6ebdee2e666879051c05bf36734c530` on `main`.
Vercel production: `dpl_6VDnDcX8WQ7iQdLiQBZm1vLiaRuv` (Ready).
The stable alias was assigned to this release after Mo explicitly requested public deployment.
The project-wide authentication setting was not changed.

Fresh browser contexts without login or share tokens opened the plain public URL at 1440x1000
and 390x844. `../actual-page/check.py` passed at both sizes: HTTP 200, all three topics select,
all five new paintings decode at 1448px, labels sit above the art, no horizontal overflow or
page errors, and ages 30/42/43/67/68/80/45 select the correct cell. Comparing the old cell with
the younger layers hidden confirms they do not show through at rest (within one channel step
of GPU compositing rounding).

Viewed desktop and phone captures and arrival states: **9/10**. The workshop and chimney form
one story; the cell shares their colours. The worker and gold cell details remain small on phones.
The existing transitions and layout remain. `*-section.jpg` is a tall diagnostic capture whose
sticky header lands mid-image; use the ordinary viewport captures for review.

Full public checks completed sequentially: `qa_home_ink` **290/290 passed**, `qa_nav`
**326/326 passed**, with no page or console errors. Logs are saved locally here as `qa-home.log`
and `qa-nav.log`. Results are also recorded in `docs/public-demo.md`. The matching local build
passed the same 290/290 and 326/326 before publication.
