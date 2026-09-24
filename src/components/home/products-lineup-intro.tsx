"use client";

import { useCopy } from "@/i18n/use-copy";
import styles from "./products-lineup-intro.module.css";

export function ProductsLineupIntro() {
  const copy = useCopy();

  return (
    <header className={styles.intro}>
      <h2 id="collection-title">
        <span className={styles.first}>{copy("Explore our products.")}</span>{" "}
        <span className={styles.second}>{copy("Find your starting point.")}</span>
      </h2>
      <p className={styles.description}>
        {copy("Discover the science, ingredients, and purpose behind each BiGH product.")}
      </p>
    </header>
  );
}
