// Judging capture protocol for the BiGH homepage (run via Playwright MCP
// browser_run_code_unsafe with {filename: this file}).
//
// Hard-won rules baked in (2026-06-09):
// 1. Emulate prefers-reduced-motion so every scroll-reveal renders statically
//    (site components were fixed to always land visible under reduce).
// 2. Scroll the page in 500px steps with 250ms dwell — useInView(once:true)
//    latches need real dwell time; fast passes leave content at opacity 0.
// 3. Wait for every <img> to decode AND have a non-zero box — a fill-image in
//    an auto-sized grid column can silently collapse to 0px wide.
// 4. Remove <nextjs-portal> (dev tools) before shooting.
// 5. ALWAYS eyeball every crop before sending to judges.
async (page) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('http://localhost:3000/en', { waitUntil: 'networkidle' });
  await page.evaluate(async () => {
    document.querySelectorAll('nextjs-portal').forEach((el) => el.remove());
    const h = document.body.scrollHeight;
    for (let y = 0; y <= h; y += 500) {
      window.scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 250));
    }
  });
  await page.evaluate(async () => {
    const imgs = Array.from(document.querySelectorAll('img'));
    await Promise.all(imgs.map((img) => img.decode().catch(() => {})));
    window.scrollTo(0, 0);
  });
  await page.waitForTimeout(2000);
  const imgStatus = await page.evaluate(() =>
    Array.from(document.querySelectorAll('img')).map((i) => {
      const r = i.getBoundingClientRect();
      return { ok: i.complete && i.naturalWidth > 0, w: Math.round(r.width), h: Math.round(r.height) };
    }),
  );
  const bad = imgStatus.filter((s) => !s.ok || s.w < 10 || s.h < 10);
  await page.screenshot({ path: 'judging-full.jpeg', fullPage: true, type: 'jpeg', quality: 88, scale: 'css' });
  const secs = await page.evaluate(() =>
    Array.from(document.querySelectorAll('main > section')).map((el) => {
      const r = el.getBoundingClientRect();
      return { id: el.id, top: Math.round(r.top + window.scrollY), height: Math.round(r.height) };
    }),
  );
  return { badImages: bad.length, imgStatus, secs };
};
