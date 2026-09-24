"use client";

import Image from "next/image";
import { ArrowDown, ArrowUpRight, ChevronLeft, ChevronRight } from "lucide-react";
import { useRef, useState, type CSSProperties, type KeyboardEvent } from "react";
import { useCopy } from "@/i18n/use-copy";
import styles from "./products-lineup.module.css";
import { ProductsLineupIntro } from "./products-lineup-intro";

const collection = [
  {
    name: "NuriCell",
    image: "nuricell",
    focus: "Cellular health & mental energy",
    headline: "Stay sharp. Live fully.",
    description:
      "Our flagship supplement focuses on the health of your mitochondria—the tiny power plants that supply energy for your brain and body.",
    detail: "Formulated by mitochondrial researcher Dr. Jian Kang Liu and Dr. Iris Wang.",
    tint: "#edf5fc",
    ink: "#24578e",
  },
  {
    name: "Green Bee Propolis",
    image: "green-bee-propolis",
    focus: "From Minas Gerais, Brazil",
    headline: "Distinctive green propolis from Minas Gerais, Brazil.",
    description:
      "Bees produce this green propolis from local plant resins. Its characteristic compounds include artepillin C—one reason researchers study Brazilian green propolis for its antioxidant properties.",
    detail: "",
    tint: "#f2f5e9",
    ink: "#58682e",
  },
  {
    name: "Advanced OPC Formula",
    image: "advanced-opc",
    focus: "Plant-based antioxidants",
    headline: "Nature’s antioxidant power. Focused on your cells.",
    description:
      "A diverse blend of concentrated plant extracts, bringing together antioxidant compounds from grape seeds, pine bark, and other botanical sources.",
    detail:
      "Designed to support your cells’ natural defenses against free radicals—unstable molecules that can damage cells.",
    tint: "#fcf0f1",
    ink: "#964758",
  },
  {
    name: "Turmerific",
    image: "turmerific",
    focus: "Advanced curcumin",
    headline: "Turmeric, advanced by neuroscience.",
    description:
      "Featuring Longvida® curcumin, developed with neuroscientists at the University of California, Los Angeles. Its specialized delivery system is designed to improve how your body absorbs turmeric’s active compound.",
    detail: "",
    tint: "#fff4e5",
    ink: "#956123",
  },
  {
    name: "Nature Calm",
    image: "nature-calm",
    focus: "A cellular approach to everyday stress",
    headline: "Everyday stress. A cellular approach.",
    description:
      "Developed by Dr. Jian Kang Liu and Dr. Iris Wang, bringing their research on stress and cellular health into a formula designed for life’s demanding days.",
    detail:
      "Nature Calm brings together nutrients involved in cellular energy and antioxidant defenses, with everyday stress in mind.",
    tint: "#eef6ed",
    ink: "#487249",
  },
] as const;

// Preserve the central flagship and the original left-to-right bottle arrangement.
const shelfOrder = [1, 2, 0, 3, 4];

function colors(index: number): CSSProperties {
  return {
    "--product-tint": collection[index].tint,
    "--product-ink": collection[index].ink,
  } as CSSProperties;
}

export function ProductsLineup({ onOpenProduct }: { onOpenProduct: (index: number) => void }) {
  const copy = useCopy();
  const [selected, setSelected] = useState(0);
  const [design, setDesign] = useState(0);
  const tabs = useRef<HTMLDivElement>(null);
  const storyFrame = useRef<HTMLDivElement>(null);
  const product = collection[selected];

  function choose(index: number) {
    setSelected(index);
    if (window.matchMedia("(max-width: 760px)").matches) {
      requestAnimationFrame(() => {
        const panel = storyFrame.current?.querySelector<HTMLElement>(
          "[role=tabpanel]:not([hidden])",
        );
        panel?.focus({ preventScroll: true });
        storyFrame.current?.scrollIntoView({
          block: "start",
          behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
            ? "instant"
            : "smooth",
        });
      });
    }
  }

  function navigate(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    // The flagship comes first on the stacked phone layout.
    const order = window.matchMedia("(max-width: 760px)").matches ? [0, 1, 2, 3, 4] : shelfOrder;
    const position = order.indexOf(index);
    const next =
      event.key === "ArrowRight"
        ? order[(position + 1) % order.length]
        : event.key === "ArrowLeft"
          ? order[(position + order.length - 1) % order.length]
          : event.key === "Home"
            ? order[0]
            : event.key === "End"
              ? order[order.length - 1]
              : null;
    if (next === null) return;
    event.preventDefault();
    setSelected(next);
    tabs.current?.querySelector<HTMLButtonElement>(`[data-product="${next}"]`)?.focus();
  }

  return (
    <section
      id="products"
      className={styles.section}
      data-products-design="lineup"
      data-lineup-design={design + 1}
      aria-labelledby="collection-title"
    >
      <div className={styles.shell}>
        <ProductsLineupIntro selected={design} onSelect={setDesign} />

        <p className={styles.hint}>
          {copy("Select a bottle to explore")} <ArrowDown size={14} aria-hidden="true" />
        </p>
        <div
          ref={tabs}
          className={styles.shelf}
          role="tablist"
          aria-label={copy("THE BIGH COLLECTION")}
        >
          {collection.map((item, index) => (
            <button
              key={item.name}
              id={`collection-tab-${index}`}
              type="button"
              role="tab"
              aria-selected={selected === index}
              aria-controls={`collection-story-${index}`}
              tabIndex={selected === index ? 0 : -1}
              className={styles.product}
              style={colors(index)}
              data-product={index}
              data-flagship={index === 0}
              onClick={() => choose(index)}
              onKeyDown={(event) => navigate(event, index)}
            >
              <span className={styles.visual}>
                <span className={styles.halo} aria-hidden="true" />
                <Image
                  src={`/images/products/${item.image}.png`}
                  alt=""
                  width={index === 1 || index === 2 ? 1231 : 1230}
                  height={1278}
                  sizes={
                    index === 0
                      ? "(max-width: 760px) 90vw, (max-width: 1100px) 40vw, 520px"
                      : "(max-width: 760px) 55vw, (max-width: 1100px) 25vw, 310px"
                  }
                  className={styles.bottle}
                />
              </span>
              <span className={styles.nameGroup}>
                <span className={styles.name}>{item.name}</span>
                {index === 0 && (
                  <span className={styles.signature}>{copy("BiGH’s flagship formula")}</span>
                )}
              </span>
              <span className={styles.focus}>{copy(item.focus)}</span>
              <span className={styles.indicator} aria-hidden="true">
                <ArrowDown size={15} />
              </span>
            </button>
          ))}
        </div>

        <div ref={storyFrame} className={styles.storyFrame} style={colors(selected)}>
          {collection.map((item, index) => (
            <div
              key={item.name}
              id={`collection-story-${index}`}
              role="tabpanel"
              aria-labelledby={`collection-tab-${index}`}
              hidden={selected !== index}
              tabIndex={0}
              className={styles.story}
            >
              <div className={styles.storyHeading}>
                <p className={styles.storyLabel}>{item.name}</p>
                <h3>{copy(item.headline)}</h3>
              </div>
              <div className={styles.storyCopy}>
                <p className={styles.description}>{copy(item.description)}</p>
                {item.detail && <p className={styles.detail}>{copy(item.detail)}</p>}
                <button
                  type="button"
                  className={styles.discover}
                  onClick={() => onOpenProduct(index)}
                >
                  {copy("Discover {name}", { name: item.name })}
                  <ArrowUpRight size={19} aria-hidden="true" />
                </button>
              </div>
            </div>
          ))}
          <div className={styles.storyNavigation}>
            <button
              type="button"
              onClick={() => choose((selected + collection.length - 1) % collection.length)}
              aria-label={copy("Previous product")}
            >
              <ChevronLeft size={17} aria-hidden="true" />
            </button>
            <span className={styles.storyNumber} aria-hidden="true">
              0{selected + 1}
              <span> / 05</span>
            </span>
            <button
              type="button"
              onClick={() => choose((selected + 1) % collection.length)}
              aria-label={copy("Next product")}
            >
              <ChevronRight size={17} aria-hidden="true" />
            </button>
          </div>
        </div>
        <p className={styles.selectedStatus} role="status">
          {copy("Exploring {name}", { name: product.name })}
        </p>
      </div>
    </section>
  );
}
