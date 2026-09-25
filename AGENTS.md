<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.

<!-- END:nextjs-agent-rules -->

## Fresh start

This is a brand-new website using the existing tech stack. Do not carry over old
design, content, or product assumptions unless Mo explicitly asks.

- `old-storage/` is the archived previous website. Do not use it as design guidance
  or reuse its layouts, colors, fonts, images, wording, or animations unless asked.
- `reference/` is reserved for new reference materials for the new website.

## Homepage CSS specificity

`src/components/home/homepage.module.css` resets `.site p`, `.site button`, and `.site h2`
(specificity 0,1,1). A single-class CSS-module rule such as `.cta { background: … }` or
`.quote { margin-top: … }` loses to them silently. Scope component rules under the
component's root class (for example `.portraits .cta`).

## Line endings

Files are LF, but this checkout has `core.autocrlf=true`. `git stash` / `git checkout`
rewrite every touched file with CRLF, and `npm run format:check` then fails on all of them.
Don't stash to compare states. On Windows, Python's `write_text` also writes CRLF unless you
pass `newline="\n"`. To repair, rewrite the files with LF endings. `prettier --write` also
restores LF.

## Approved product images

Mo approved all five enhanced transparent product PNGs on September 18, 2026.
Use `public/images/products/` for future product-image work. See
`docs/brand-assets.md` for the product-to-file mapping. Preserve the originals and
the comparison assets for reference.

## Public demo address

Mo requested a public demo without login or share tokens after colleagues could not open earlier preview links.

- Use `https://bigh-website-demo.vercel.app/` as the single demo address. Do not send a new deployment URL or tokenized share link for routine updates.
- After publishing and checking a new preview, point this alias at that deployment with `vercel alias set <deployment-hostname> bigh-website-demo.vercel.app --scope sarkuseq1999s-projects`.
- Verify the plain demo URL in a fresh unauthenticated browser after every alias update, including the new feature.
- The demo alias has a domain-specific public-access exception. Keep the project’s general Vercel Authentication setting intact. A project-wide removal was rejected by automatic approval review; the narrower demo exception succeeded.
- See `docs/public-demo.md` for the current deployment and access details.

## Higgsfield video and animation connection

For Higgsfield video or animation requests, first read
`C:/Users/mcbig/.codex/skills/higgsfield-api/SKILL.md`.
It records Mo's subscription-first preference through September 27, 2026 and
the switch to the separate dollar-billed API after credits or access end.
The API helper and encrypted credential live outside this website repository.
