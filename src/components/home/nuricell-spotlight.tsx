"use client";

import Image from "next/image";
import { ArrowUpRight, FlaskConical } from "lucide-react";
import styles from "./nuricell-spotlight.module.css";

export function NuriCellSpotlight({ onDiscover }: { onDiscover: () => void }) {
  return (
    <div id="nuricell" className={styles.spotlight} role="region" aria-labelledby="nuricell-title">
      <header className={styles.heading}>
        <p className={styles.eyebrow}>MEET NURICELL</p>
        <h2 id="nuricell-title" className={styles.title}>
          Stay sharp.<span>Live fully.</span>
        </h2>
      </header>
      <div className={styles.visual}>
        <span className={styles.flagshipLabel}>THE BIGH FLAGSHIP</span>
        <span className={styles.productWord} aria-hidden="true">
          NuriCell
        </span>
        <span className={styles.groundShadow} aria-hidden="true" />
        <Image
          src="/images/products/nuricell.png"
          alt="NuriCell dietary supplement bottle"
          width={1230}
          height={1278}
          sizes="(max-width: 800px) 100vw, (max-width: 1440px) 48vw, 650px"
          className={styles.bottle}
        />
        <span className={styles.visualCaption}>NuriCell / Dietary supplement</span>
      </div>
      <div className={styles.details}>
        <p className={styles.description}>
          Our flagship supplement focuses on the health of your <strong>mitochondria</strong>—the
          tiny power plants that supply energy for your brain and body.
        </p>
        <div className={styles.credit}>
          <FlaskConical size={25} strokeWidth={1.3} aria-hidden="true" />
          <p>
            Formulated by mitochondrial researcher <strong>Dr. Jian Kang Liu</strong> and{" "}
            <strong>Dr. Iris Wang.</strong>
          </p>
        </div>
        <button type="button" onClick={onDiscover} className={styles.discover}>
          Discover NuriCell <ArrowUpRight size={21} aria-hidden="true" />
        </button>
      </div>
    </div>
  );
}
