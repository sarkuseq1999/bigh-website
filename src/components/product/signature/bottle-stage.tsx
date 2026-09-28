"use client";

import Image from "next/image";
import gsap from "gsap";
import { useEffect, useRef, useState } from "react";
import { useCopy } from "@/i18n/use-copy";
import type { ProductPage } from "../product-types";
import { bottles } from "../template-object-bottle";
import type { HeroScene } from "./hero-scene";
import styles from "./bottle-stage.module.css";

/**
 * The product's 3D bottle in a soft studio, turning a little toward the pointer, for places after
 * the opening (the buy chapter). It arrives with one slow turn the first time it comes into view.
 * Products without a 3D bottle yet, and devices without WebGL, show the approved photo.
 */
export function BottleStage({ product, reduced }: { product: ProductPage; reduced: boolean }) {
  const copy = useCopy();
  const stage = useRef<HTMLDivElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  const model = bottles[product.slug];
  const [status, setStatus] = useState<"loading" | "ready" | "flat">(model ? "loading" : "flat");

  useEffect(() => {
    const element = stage.current;
    const surface = canvas.current;
    if (!model || !element || !surface) return;
    let cancelled = false;
    let scene: HeroScene | null = null;
    let observer: IntersectionObserver | null = null;
    let tween: gsap.core.Tween | null = null;

    // Build only when it is near the screen, so the page's first load stays light.
    observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        observer?.disconnect();
        Promise.all([import("three"), import("./hero-scene")])
          .then(([three, { createHeroScene }]) => {
            if (cancelled) return;
            scene = createHeroScene(three, surface, element, model, { still: reduced, size: 0.78 });
            const { state } = scene;
            if (reduced) state.enter = 1;
            void scene.ready.then(() => {
              if (cancelled) return;
              setStatus("ready");
              if (!reduced) tween = gsap.to(state, { enter: 1, duration: 2.4, ease: "power2.out" });
            });
          })
          .catch(() => {
            if (!cancelled) setStatus("flat");
          });
      },
      { rootMargin: "300px 0px" },
    );
    observer.observe(element);
    return () => {
      cancelled = true;
      observer?.disconnect();
      tween?.kill();
      scene?.dispose();
    };
  }, [model, reduced]);

  return (
    <div ref={stage} className={styles.stage} data-status={status}>
      <canvas ref={canvas} className={styles.canvas} aria-hidden="true" />
      {status === "flat" && (
        <Image
          className={styles.flat}
          src={product.bottle.src}
          width={product.bottle.width}
          height={product.bottle.height}
          alt={copy(product.bottle.alt)}
          sizes="(max-width: 860px) 420px, 560px"
        />
      )}
      {status !== "flat" && <span className={styles.srOnly}>{copy(product.bottle.alt)}</span>}
    </div>
  );
}
