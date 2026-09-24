# Deep Space: movement redesign — September 22, 2026

Mo rejected the original cell movement and the subsequent half-speed adjustment as artificial. He asked for a fresh motion design using independent judgment, with the earlier movement instructions set aside.

Current protected preview: https://bigh-website-ngmivb1pe-sarkuseq1999s-projects.vercel.app

Deployment `dpl_CuQjktokpsb9wQ1GuXMMZGaR1cHa` reported READY. The hosted build compiled, completed TypeScript and generated all 10 pages. Existing Vercel login protection is unchanged; production was not promoted. Visual and interaction checks were local.

## Direction

Preserve the selected Deep Space artwork and approved text. Give the cell a stable overall shape, very small buoyant drift and localized surface movement at different times. Internal detail should move quietly with depth; illumination should stay steady. The design aims to feel calm and alive without a regular contraction-and-expansion beat.

The new clip is generated for its own pace and plays at normal speed. The previous playback-rate override and the separate CSS particle overlay are removed. Text and navigation remain stationary. Pause/play, offscreen pausing, reduced-motion still and failed-video fallback remain in the component. The result remains a stylized cell visualization, not biological footage. Mo subsequently approved this movement (“looks much better now … this is good”) and authorized the [cellular-health section](cellular-health-section.md), whose notes contain the latest whole-site preview.

## Assets

- Source still: `public/media/hero/deep-space-background-v1.png`.
- New generation settings, prompt and job ID: `reference/hero-concepts/deep-space-motion-v2.txt`.
- Original generation: `reference/hero-concepts/deep-space-motion-v2-source.mp4` (HEVC, 2,896,768 bytes).
- Served file: `public/media/hero/deep-space-motion-v2.mp4` (H.264, 2,674,967 bytes, fast-start metadata, no audio).
- Dimensions and timing: 1920 × 1080, 24 fps, 385 frames, 16.041667 seconds at native 1× playback.
- Served SHA-256: `638AD9C3D2D78829C03078B463A6B9A58A2AA2E4B8BA64F29317C1E5ACE20DB9`.
- Component: `src/components/home/hero-comparison.tsx`; styles: `hero-comparison.module.css`.
- Prior animation and pacing history: [deep-space-animation.md](deep-space-animation.md). All earlier assets and preview deployments are preserved.

## Verification

- Lint, TypeScript, formatting and the local production build passed after the component changes; all 10 pages generated.
- ffprobe confirmed metadata. ffmpeg decoded the entire served clip without errors.
- Inspected eight chronological frames and first/last frames. The cell remains intact; local contour and internal details change, with quieter overall movement than the repeated full-cell contraction brief. Endpoints match closely in shape and lighting. This is a visual judgment from sampled frames, not a guarantee of pixel-perfect continuity or physical realism.
- Actual local browser uses the new v2 MP4, muted, at 1× speed; no separate CSS animations remain. Playback advances, the headline stays fixed, and the loop restarts.
- Pause freezes playback. A visitor pause survives scrolling; ordinary offscreen pause/resume also works. Product dialog and Escape dismissal checked.
- No horizontal overflow at 320, 390, 768, 1024 or 1440 pixels. Desktop and phone screenshots visually inspected.
- Fresh reduced-motion visit requested zero MP4 files and had zero animations. Blocking the new MP4 retained the still and removed the motion control. Normal playback reported no console errors or warnings.
- Review files: `reference/hero-concepts/qa/deep-space-motion-v2-frames.jpg`, `deep-space-motion-v2-loop-endpoints.jpg`, `deep-space-motion-v2-desktop.png`, and `deep-space-motion-v2-phone.png`.
- Checks use a desktop browser at responsive sizes; a physical iPhone/Safari was not tested. Remote UI review remains limited by the existing Vercel login gate.
