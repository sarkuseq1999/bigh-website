"use client";

import { useState } from "react";
import { useCopy } from "@/i18n/use-copy";
import styles from "./add-to-cart.module.css";

const note = "Checkout isn't connected yet. This page is a design preview.";

/** Add to cart is a placeholder until the shop (bigh-backend) is connected; it says so politely. */
export function AddToCart({
  tone = "ink",
  align = "start",
  wide = false,
  className = "",
}: {
  tone?: "ink" | "cream";
  align?: "start" | "center";
  wide?: boolean;
  className?: string;
}) {
  const copy = useCopy();
  const [asked, setAsked] = useState(false);
  return (
    <div
      className={`${styles.wrap} ${align === "center" ? styles.center : ""} ${className}`}
      data-tone={tone}
    >
      <button
        type="button"
        className={`${styles.button} ${wide ? styles.wide : ""}`}
        onClick={() => setAsked(true)}
      >
        {copy("Add to cart")}
      </button>
      <p className={styles.note} aria-live="polite">
        {asked ? copy(note) : ""}
      </p>
    </div>
  );
}
