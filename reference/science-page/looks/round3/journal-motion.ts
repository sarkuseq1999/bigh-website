import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { SplitText } from "gsap/SplitText";

// Look C's motion. One moving moment, done slowly: the cover (the headline rises line by line out
// of its masks while the plate is wiped open) and the chronology (pinned, it slides sideways; an ink
// line draws through the years). Everything else is a quiet reveal. With reduced motion none of
// this runs and the CSS shows everything at once; phones get no sideways pin.
export function startJournalMotion(root: HTMLElement) {
  gsap.registerPlugin(ScrollTrigger, SplitText);
  const q = (selector: string, scope: ParentNode = root) => [
    ...scope.querySelectorAll<HTMLElement>(selector),
  ];
  const one = (selector: string) => root.querySelector<HTMLElement>(selector);
  const media = gsap.matchMedia();
  const born = performance.now();

  // Fonts change line breaks: split and measure only after they arrive (or after 1.2 s at most).
  const fontsReady = Promise.race([
    document.fonts?.ready ?? Promise.resolve(),
    new Promise((resolve) => window.setTimeout(resolve, 1200)),
  ]);
  let alive = true;
  fontsReady.then(() => alive && ScrollTrigger.refresh());

  // Quiet reveals: a short fade and a 14px rise, once.
  const reveal = (targets: HTMLElement[]) => {
    if (!targets.length) return;
    gsap.set(targets, { opacity: 0, y: 14 });
    ScrollTrigger.batch(targets, {
      start: "top 90%",
      once: true,
      onEnter: (batch) =>
        gsap.to(batch, {
          opacity: 1,
          y: 0,
          duration: 0.35,
          ease: "power2.out",
          stagger: 0.07,
          overwrite: true,
        }),
    });
  };

  media.add("(prefers-reduced-motion: no-preference)", (context) => {
    // 1. The cover. The CSS keeps it hidden (with a 3 s failsafe) until this takes over.
    root.dataset.intro = "on";
    const title = one("[data-cover-title]");
    const plate = one("[data-cover-plate]");
    const image = one("[data-cover-image]");
    const drift = one("[data-cover-drift]");
    const folio = q("[data-folio-text]");
    const rule = one("[data-folio-rule]");
    const contents = q("[data-contents] li, [data-contents-head]");
    const caption = one("[data-cover-caption]");

    gsap.set([...folio, ...contents, caption].filter(Boolean), { opacity: 0 });
    gsap.set(contents, { y: 10 });
    if (rule) gsap.set(rule, { scaleX: 0, transformOrigin: "0% 50%" });
    if (plate) gsap.set(plate, { clipPath: "inset(0% 100% 0% 0%)" });
    if (image) gsap.set(image, { scale: 1.16 });

    // Added as a context method, so what it creates later is still reverted with the context.
    const playIntro = context.add("intro", () => {
      if (!alive) return;
      const late = performance.now() - born > 2600;
      const cjk = /^(zh|ja)/.test(document.documentElement.lang);
      const intro = gsap.timeline({ defaults: { ease: "power3.out" } });
      if (rule) intro.to(rule, { scaleX: 1, duration: 1.1, ease: "power3.inOut" }, 0);
      intro.to(folio, { opacity: 1, duration: 0.6, stagger: 0.08 }, 0.2);

      if (title) {
        gsap.set(title, { opacity: 1 });
        if (late || cjk) {
          intro.from(title, { opacity: 0, y: 18, duration: 0.8 }, 0.1);
        } else {
          SplitText.create(title, {
            type: "lines",
            mask: "lines",
            linesClass: "journal-line",
            autoSplit: true,
            onSplit: (self) =>
              gsap.from(self.lines, {
                yPercent: 110,
                duration: 1.6,
                ease: "power3.out",
                stagger: 0.18,
                delay: 0.2,
                onComplete: () => title.setAttribute("data-settled", ""),
              }),
          });
        }
      }
      if (plate) {
        intro.to(plate, { clipPath: "inset(0% 0% 0% 0%)", duration: 2, ease: "expo.inOut" }, 0.45);
      }
      if (image) intro.to(image, { scale: 1, duration: 2.8 }, 0.45);
      intro.to(contents, { opacity: 1, y: 0, duration: 0.5, stagger: 0.05 }, 1.1);
      if (caption) intro.to(caption, { opacity: 1, duration: 0.6 }, 1.9);
    });
    fontsReady.then(() => playIntro());

    // Scrolling away, the specimen drifts a little inside its plate.
    const cover = one("[data-cover]");
    if (cover && drift) {
      gsap.to(drift, {
        yPercent: 7,
        ease: "none",
        scrollTrigger: { trigger: cover, start: "top top", end: "bottom top", scrub: true },
      });
    }

    // 2. Dr. Liu's portrait comes into focus as it arrives. His face is never altered: only the
    // focus and the frame's scale change.
    const portrait = one("[data-portrait]");
    const photo = one("[data-portrait-image]");
    if (portrait && photo) {
      gsap.set(photo, { filter: "blur(16px)", scale: 1.06 });
      gsap.to(photo, {
        filter: "blur(0px)",
        scale: 1,
        duration: 1.4,
        ease: "power2.out",
        clearProps: "filter",
        scrollTrigger: { trigger: portrait, start: "top 82%", once: true },
      });
    }

    // 3. Everything else: quiet reveals.
    reveal(q("[data-reveal]"));

    // The dark plate: the cell settles as the page passes over it.
    const spread = one("[data-spread]");
    const spreadMedia = one("[data-spread-media]");
    if (spread && spreadMedia) {
      gsap.fromTo(
        spreadMedia,
        { scale: 1.1 },
        {
          scale: 1,
          ease: "none",
          scrollTrigger: { trigger: spread, start: "top bottom", end: "bottom top", scrub: true },
        },
      );
    }

    return () => {
      delete root.dataset.intro;
      title?.removeAttribute("data-settled");
    };
  });

  // 4. The chronology, pinned on wide screens: the band slides sideways, the ink line draws
  // through the years, each year darkens as the line reaches it, and each small plate settles as
  // it comes in. Years, plates and words stay aligned on one edge.
  media.add("(prefers-reduced-motion: no-preference) and (min-width: 901px)", () => {
    const section = one("[data-chron]");
    const track = one("[data-chron-track]");
    const fill = one("[data-chron-fill]");
    if (!section || !track || !fill) return;
    section.dataset.live = "true";
    const stops = q("[data-stop]");
    const distance = () => Math.max(0, track.scrollWidth - section.clientWidth);

    // The callbacks can fire while the tween is still being made, so they read it from a holder.
    const holder: { slide?: gsap.core.Tween } = {};
    const progress = () => holder.slide?.progress() ?? 0;
    const draw = (amount: number) => {
      // The reading point moves from the middle of the screen to its right edge, so the line
      // reaches the last year as the slide ends.
      const reach = distance() * amount + section.clientWidth * (0.5 + 0.5 * amount);
      gsap.set(fill, { scaleX: Math.min(1, reach / track.scrollWidth) });
      stops.forEach((stop) => stop.toggleAttribute("data-lit", stop.offsetLeft + 40 <= reach));
    };

    const slide = gsap.to(track, {
      x: () => -distance(),
      ease: "none",
      onUpdate: () => draw(progress()),
      scrollTrigger: {
        trigger: section,
        start: "top top",
        end: () => `+=${distance()}`,
        pin: true,
        scrub: 0.8,
        refreshPriority: 1,
        invalidateOnRefresh: true,
        onRefresh: () => draw(progress()),
      },
    });

    holder.slide = slide;
    q("[data-stop-plate] img").forEach((picture) => {
      gsap.fromTo(
        picture,
        { scale: 1.14 },
        {
          scale: 1,
          ease: "none",
          scrollTrigger: {
            trigger: picture.closest("[data-stop]"),
            containerAnimation: slide,
            start: "left right",
            end: "center center",
            scrub: true,
          },
        },
      );
    });

    return () => {
      delete section.dataset.live;
      stops.forEach((stop) => stop.removeAttribute("data-lit"));
    };
  });

  // Phones: the same stops, top to bottom, with quiet reveals.
  media.add("(prefers-reduced-motion: no-preference) and (max-width: 900px)", () => {
    reveal(q("[data-stop]"));
  });

  return () => {
    alive = false;
    media.revert();
  };
}
