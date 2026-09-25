"use client";

import { StoriesLight } from "./stories-light";
import { StoriesMoments } from "./stories-moments";
import { StoriesPortraits } from "./stories-portraits";
import styles from "./customer-stories.module.css";

// Mo chose the Portraits layout with the Still life picture on September 24 ("okay for this
// section"; polish later). The other pictures (daylight, showroom, hands, a single object, words,
// ink drawings) stay available via StoriesPortraits' `visual` prop; the Moments and Scroll story
// alternates via `design`, as ProductsSection does.
// The earlier Daybook / Story Wall / Spotlight version lives in reference/customer-stories/.
export function CustomerStories({
  onOpenProduct,
  design = "portraits",
}: {
  onOpenProduct: (index: number) => void;
  design?: "portraits" | "moments" | "light";
}) {
  return (
    <section
      id="stories"
      className={styles.section}
      data-design={design}
      aria-labelledby="stories-title"
    >
      {design === "portraits" && (
        <StoriesPortraits onOpenProduct={onOpenProduct} visual="stilllife" />
      )}
      {design === "moments" && <StoriesMoments onOpenProduct={onOpenProduct} />}
      {design === "light" && <StoriesLight onOpenProduct={onOpenProduct} />}
    </section>
  );
}
