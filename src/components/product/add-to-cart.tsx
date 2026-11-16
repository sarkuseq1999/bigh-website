"use client";

import { useState } from "react";
import { checkoutUrl } from "@/components/shop/shop";
import { useCopy } from "@/i18n/use-copy";
import styles from "./add-to-cart.module.css";

const note = "Our online shop opens soon. Until then, call us at 800-919-2089 and we’ll help.";

/** Add to cart goes to BiGH's own shop once `checkoutUrl` (shop.ts) returns a link for this
 *  product. Until then it stays a placeholder that says so politely, with a way to reach us. */
export function AddToCart({
  slug,
  tone = "ink",
  align = "start",
  wide = false,
  className = "",
}: {
  /** The product page's slug, so the shop knows which product to add. */
  slug?: string;
  tone?: "ink" | "cream";
  align?: "start" | "center";
  wide?: boolean;
  className?: string;
}) {
  const copy = useCopy();
  const [asked, setAsked] = useState(false);
  const href = slug ? checkoutUrl(slug) : null;
  return (
    <div
      className={`${styles.wrap} ${align === "center" ? styles.center : ""} ${className}`}
      data-tone={tone}
    >
      {href ? (
        <a className={`${styles.button} ${wide ? styles.wide : ""}`} href={href} data-cart="">
          {copy("Add to cart")}
        </a>
      ) : (
        <button
          type="button"
          className={`${styles.button} ${wide ? styles.wide : ""}`}
          data-cart=""
          onClick={() => setAsked(true)}
        >
          {copy("Add to cart")}
        </button>
      )}
      <p className={styles.note} aria-live="polite">
        {asked ? copy(note) : ""}
      </p>
    </div>
  );
}
