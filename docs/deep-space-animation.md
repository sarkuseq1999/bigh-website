# Deep Space animated hero — September 22, 2026

**Superseded:** Mo rejected the original movement and the half-speed adjustment. See [the independent movement redesign](deep-space-natural-motion.md) for the current hero and preview. The details below preserve the earlier implementation history.

Mo chose Deep Space and approved animating the cell itself with a gentle jellyfish-inspired pulse, drifting particles, and stationary text.

Archived half-speed preview: https://bigh-website-ieefy8hzq-sarkuseq1999s-projects.vercel.app

Earlier full-speed preview: https://bigh-website-c65me4fy8-sarkuseq1999s-projects.vercel.app

Slower revision: Vercel deployment `dpl_H2YhpudMbFTiACP3waNaDGTRYXtk` reported READY. The hosted build compiled, completed TypeScript and generated all 10 pages. Existing login protection is unchanged; production was not promoted. Browser interaction and visual checks were local; the remote UI was not rechecked behind the login gate.

## Current behavior

- After Mo said the motion felt too fast and artificial, the same silent video now plays at 0.5× speed: one loop takes about 20.08 seconds. Both the default and active playback rates are set before autoplay, preserving the slower pace after pause, scrolling, preference changes and looping. The underlying generated deformation remains unchanged; this is a pacing adjustment, not a new generation.
- Eight subtle particles drift across the artwork at half their previous pace (40–56 seconds per direction), with shorter travel and a lower opacity range of 0.1–0.3. Headline, introduction, navigation, and both actions remain real stationary page content.
- Pause/play controls the video and particles together. A visitor's pause choice survives scrolling away and back. Playback also pauses offscreen and when the document is hidden.
- Reduced-motion visitors see the approved still without downloading the video. If video loading fails, the still remains and the unavailable motion control is removed. The video stays transparent until its first frame is available.
- The desktop background fills the hero. On phone/tablet, the artwork appears between the headline and description with the existing feathered edges.

## Media and implementation

- `src/components/home/hero-comparison.tsx` exports the selected `DeepSpaceHero`; its CSS module handles layout and particles. The old comparison controls remain removed.
- Original generation: `reference/hero-concepts/deep-space-motion-v1-source.mp4` (HEVC, 3,077,796 bytes).
- Served version: `public/media/hero/deep-space-motion-v1.mp4` (H.264, 1,923,780 bytes, 1920 × 1080, 24 fps, 241 frames, 10.041667 seconds, no audio, fast-start metadata).
- Served SHA-256: `6A6A51A18E59CCF42EA36E4788B7562993DEF68A2C6F9D8B5A0F0E8B81A9EEE0`.
- Exact prompt, generation settings and provenance: `reference/hero-concepts/deep-space-motion-v1.txt`.
- Original still, previous videos, and comparison concepts remain preserved.

## Verification

- Slower revision: measured video advancement at 0.49999 seconds per wall-clock second. The rate remained 0.5 after a loop, offscreen resume, and reduced-motion preference changes. Confirmed pause, zero animations with reduced motion, a stationary headline, and no phone overflow. Desktop and phone screenshots inspected: `deep-space-slower-desktop.png` and `deep-space-slower-phone.png`. Lint, TypeScript, formatting and the local production build passed; normal browser playback had no console errors or warnings.
- Fully decoded the served video with ffmpeg without errors and inspected its metadata with ffprobe.
- Inspected six chronological frames: the cell remains intact while its outline and internal folds change. Inspected first/last frames together: composition and lighting match closely. Browser playback crossed the loop boundary and resumed; this is a closely matching generated loop, not a guarantee of pixel-perfect continuity.
- Inspected actual desktop and phone screenshots. No horizontal overflow at 320, 390, 768, 1024, or 1440 pixels.
- Browser confirmed the exact new video source, muted inline playback, loop restart, advancing video, stationary headline, eight particles, and pause freezing both video and particles after animation state settled.
- Confirmed offscreen pause/resume and persistence of a visitor pause. Product dialog, Escape dismissal and scientist navigation work.
- A fresh reduced-motion visit requested zero MP4 files and had zero animations. An intentionally blocked video left the still, paused particles, and removed the control.
- Normal local playback reported zero console errors or warnings. Lint, TypeScript, formatting and the local production build passed; all 10 pages generated.
- UI checks use a local desktop browser at responsive sizes, not physical phone/Safari testing. The remote preview retains the existing Vercel login gate.

Review images: `reference/hero-concepts/qa/deep-space-motion-v1-frames.jpg`, `deep-space-motion-v1-loop-endpoints.jpg`, `deep-space-motion-v1-desktop.png`, and `deep-space-motion-v1-phone.png`.

Later homepage sections and the shopping flow remain outside this hero animation change.
