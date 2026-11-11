# NuriCell opening, round 7: room and sunshine (November 11, 2026)

Mo sent the live first screen ("A clear day") with three notes: the big name sits right on the
sea line (give it space), "Stay sharp. Live fully." and the highlights need room from the painting,
and "some kind of reflection of the sun" in the upper right corner, "California sunshine".

- Review page: https://claude.ai/artifact/188m1vDatSxUdczs52ssHm (`index.html`, `img/`).
- Both ideas carry the same two spacing fixes (`space.css`: the halves lifted 0.1 of their size from
  960px; the words 0.13 name-sizes under the last grass, 16px more on a phone).
- **A, light from the corner (Mo's pick, 8.5):** Codex take `opening-suncorner-a` (light pouring in
  from beyond the top right corner) plus the sparkle on the sea from `opening-sundisc-b`.
- **B, the sun in the sky (8):** `opening-sundisc-b`, its sun and halo and its sparkle. Crowded
  "Cell" at 1280-1440 wide; the round sun read a little like a sticker up close; the homepage has
  its own sun.
- Unused takes (`opening-suncorner-b`, `opening-sundisc-a`) are in
  `bigh-archive\nuricell-sunshine-2026-11-11\`.

How the mockups were made: `shoot.py <name> <base-url> <css|-> <sizes> <js>` opens
`/products/nuricell`, injects `space.css` and a `cfg-*.js` + `sun.js` script (which lays the sun
layers into the painting's `[data-sky]` group) and screenshots each size. The mock layers were
built by an earlier form of `../../nuricell/build_nuricell_sun.py` (one layer per take); the
shipped build makes only A's two layers, so `sun.js` no longer finds its pictures.

Trap: a first take of A started the light's layer a few pixels inside a tablet's window and left a
hard line along its top. The light's top rows are now mirrored above it and the layer starts at or
above the painting's own top.
