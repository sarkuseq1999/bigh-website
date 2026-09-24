"use client";

import { useCopy } from "@/i18n/use-copy";

import Image from "next/image";
import { ArrowUpRight, Plus, Sparkle } from "lucide-react";
import { useEffect, useRef, useState, type CSSProperties, type KeyboardEvent } from "react";
import styles from "./products-collection-comparison.module.css";

const collection = [
  {
    name: "NuriCell",
    image: "nuricell",
    headline: "Stay sharp. Live fully.",
    tint: "#e8f1ff",
    ink: "#24578e",
  },
  {
    name: "Green Bee Propolis",
    image: "green-bee-propolis",
    headline: "Distinctive green propolis from Minas Gerais, Brazil.",
    tint: "#eff3e3",
    ink: "#657a29",
  },
  {
    name: "Advanced OPC Formula",
    image: "advanced-opc",
    headline: "Nature’s antioxidant power. Focused on your cells.",
    tint: "#faecec",
    ink: "#9b485a",
  },
  {
    name: "Turmerific",
    image: "turmerific",
    headline: "Turmeric, advanced by neuroscience.",
    tint: "#fff0dd",
    ink: "#b57223",
  },
  {
    name: "Nature Calm",
    image: "nature-calm",
    headline: "Everyday stress. A cellular approach.",
    tint: "#eaf3e9",
    ink: "#487d52",
  },
] as const;

const designs = ["Gallery", "The Lineup", "Editorial"] as const;
type OpenProduct = (index: number) => void;

function productColor(index: number): CSSProperties {
  return {
    "--product-tint": collection[index].tint,
    "--product-ink": collection[index].ink,
  } as CSSProperties;
}

function Bottle({ index, sizes }: { index: number; sizes: string }) {
  const copy = useCopy();
  const product = collection[index];
  return (
    <Image
      src={`/images/products/${product.image}.png`}
      alt={copy("{name} bottle", { name: product.name })}
      width={index === 1 || index === 2 ? 1231 : 1230}
      height={1278}
      sizes={sizes}
      className={styles.bottle}
      loading="eager"
    />
  );
}

function FlagshipHeading() {
  const copy = useCopy();
  return (
    <header className={styles.flagshipHeading}>
      <p className={styles.flagshipLabel}>
        <Sparkle size={14} aria-hidden="true" /> {copy("NURICELL / OUR FLAGSHIP")}
      </p>
      <h3>
        {copy("Stay sharp.")}
        <span>{copy("Live fully.")}</span>
      </h3>
    </header>
  );
}

function FlagshipDetails({ onOpenProduct }: { onOpenProduct: OpenProduct }) {
  const copy = useCopy();
  return (
    <div className={styles.flagshipDetails}>
      <p className={styles.description}>
        {copy(
          "Our flagship supplement focuses on the health of your mitochondria—the tiny power plants that supply energy for your brain and body.",
        )}
      </p>
      <p className={styles.credit}>
        {copy("Formulated by mitochondrial researcher Dr. Jian Kang Liu and Dr. Iris Wang.")}
      </p>
      <button type="button" className={styles.discover} onClick={() => onOpenProduct(0)}>
        {copy("Discover NuriCell")} <ArrowUpRight size={19} aria-hidden="true" />
      </button>
    </div>
  );
}

function FeatureVisual() {
  const copy = useCopy();
  return (
    <div className={styles.featureVisual}>
      <span className={styles.featureWord} aria-hidden="true">
        {copy("NuriCell")}
      </span>
      <Bottle index={0} sizes="(max-width: 760px) 95vw, (max-width: 1100px) 50vw, 520px" />
    </div>
  );
}

function ProductCard({ index, onOpenProduct }: { index: number; onOpenProduct: OpenProduct }) {
  const copy = useCopy();
  const product = collection[index];
  return (
    <button
      type="button"
      className={styles.productCard}
      style={productColor(index)}
      onClick={() => onOpenProduct(index)}
      aria-label={copy("Discover {name}", { name: product.name })}
    >
      <span className={styles.cardVisual}>
        <Bottle index={index} sizes="(max-width: 760px) 46vw, 320px" />
        <span className={styles.cardArrow}>
          <ArrowUpRight size={18} aria-hidden="true" />
        </span>
      </span>
      <span className={styles.cardName}>{product.name}</span>
      <span className={styles.cardHeadline}>{copy(product.headline)}</span>
    </button>
  );
}

function Gallery({ onOpenProduct }: { onOpenProduct: OpenProduct }) {
  const copy = useCopy();
  return (
    <div className={styles.gallery}>
      <article className={styles.galleryFlagship} aria-label={copy("NuriCell flagship")}>
        <FlagshipHeading />
        <FeatureVisual />
        <FlagshipDetails onOpenProduct={onOpenProduct} />
      </article>
      <div className={styles.galleryRange}>
        <p className={styles.rangeLabel}>{copy("MORE TO EXPLORE")}</p>
        <div className={styles.cardGrid}>
          {[1, 2, 3, 4].map((index) => (
            <ProductCard key={index} index={index} onOpenProduct={onOpenProduct} />
          ))}
        </div>
      </div>
    </div>
  );
}

function Lineup({ onOpenProduct }: { onOpenProduct: OpenProduct }) {
  const copy = useCopy();
  return (
    <div className={styles.lineup}>
      <div className={styles.shelf}>
        {[0, 1, 2, 3, 4].map((index) => (
          <button
            key={index}
            type="button"
            className={styles.shelfProduct}
            style={productColor(index)}
            data-flagship={index === 0}
            data-product={index}
            onClick={() => onOpenProduct(index)}
            aria-label={copy("Discover {name}", { name: collection[index].name })}
          >
            <span className={styles.shelfVisual}>
              {index === 0 && (
                <span className={styles.shelfBadge}>
                  <Sparkle size={13} aria-hidden="true" /> {copy("OUR FLAGSHIP")}
                </span>
              )}
              <Bottle
                index={index}
                sizes={
                  index === 0
                    ? "(max-width: 760px) 95vw, (max-width: 1100px) 35vw, 420px"
                    : "(max-width: 760px) 46vw, (max-width: 1100px) 25vw, 420px"
                }
              />
              <span className={styles.shelfPlus}>
                <Plus size={18} aria-hidden="true" />
              </span>
            </span>
            <span className={styles.cardName}>{collection[index].name}</span>
            {index !== 0 && (
              <span className={styles.cardHeadline}>{copy(collection[index].headline)}</span>
            )}
          </button>
        ))}
      </div>
      <article className={styles.lineupStory} aria-label={copy("About our flagship NuriCell")}>
        <FlagshipHeading />
        <FlagshipDetails onOpenProduct={onOpenProduct} />
      </article>
    </div>
  );
}

function Editorial({ onOpenProduct }: { onOpenProduct: OpenProduct }) {
  const copy = useCopy();
  return (
    <div className={styles.editorial}>
      <FlagshipHeading />
      <FeatureVisual />
      <FlagshipDetails onOpenProduct={onOpenProduct} />
      <div className={styles.productIndex}>
        <p className={styles.rangeLabel}>{copy("THE REST OF THE COLLECTION")}</p>
        {[1, 2, 3, 4].map((index) => (
          <button
            key={index}
            type="button"
            className={styles.indexProduct}
            style={productColor(index)}
            onClick={() => onOpenProduct(index)}
            aria-label={copy("Discover {name}", { name: collection[index].name })}
          >
            <span className={styles.indexVisual}>
              <Bottle index={index} sizes="140px" />
            </span>
            <span className={styles.indexCopy}>
              <span className={styles.cardName}>{collection[index].name}</span>
              <span className={styles.cardHeadline}>{copy(collection[index].headline)}</span>
            </span>
            <ArrowUpRight className={styles.indexArrow} size={19} aria-hidden="true" />
          </button>
        ))}
      </div>
    </div>
  );
}

export function ProductsCollectionComparison({ onOpenProduct }: { onOpenProduct: OpenProduct }) {
  const copy = useCopy();
  const [selected, setSelected] = useState(1);
  const [inView, setInView] = useState(false);
  const section = useRef<HTMLElement>(null);
  const controls = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const element = section.current;
    if (!element) return;
    let frame = 0;
    const measure = () => {
      frame = 0;
      const bounds = element.getBoundingClientRect();
      setInView(bounds.bottom > 120 && bounds.top < window.innerHeight - 100);
    };
    const schedule = () => {
      if (!frame) frame = window.requestAnimationFrame(measure);
    };
    const observer = new ResizeObserver(schedule);
    observer.observe(element);
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", schedule);
    schedule();
    return () => {
      observer.disconnect();
      window.cancelAnimationFrame(frame);
      window.removeEventListener("scroll", schedule);
      window.removeEventListener("resize", schedule);
    };
  }, []);

  function choose(id: number) {
    setSelected(id);
    const bounds = section.current?.getBoundingClientRect();
    if (bounds && bounds.top < -80)
      window.scrollTo({ top: window.scrollY + bounds.top - 24, behavior: "instant" });
  }

  function navigate(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    const next =
      event.key === "ArrowRight"
        ? (index + 1) % 3
        : event.key === "ArrowLeft"
          ? (index + 2) % 3
          : event.key === "Home"
            ? 0
            : event.key === "End"
              ? 2
              : null;
    if (next === null) return;
    event.preventDefault();
    choose(next + 1);
    controls.current?.querySelectorAll<HTMLButtonElement>("button")[next]?.focus();
  }

  return (
    <section
      id="products"
      ref={section}
      className={styles.section}
      data-collection-design={selected}
      aria-labelledby="collection-title"
    >
      <div className={styles.shell}>
        <header className={styles.intro}>
          <div>
            <p className={styles.eyebrow}>{copy("THE BIGH COLLECTION")}</p>
            <h2 id="collection-title">
              {copy("Meet the")} <span>{copy("BiGH collection.")}</span>
            </h2>
          </div>
          <p className={styles.introText}>
            {copy("Our flagship, NuriCell.")} <br />
            {copy("Four more formulas to explore.")}
          </p>
        </header>
        {selected === 1 ? (
          <Gallery onOpenProduct={onOpenProduct} />
        ) : selected === 2 ? (
          <Lineup onOpenProduct={onOpenProduct} />
        ) : (
          <Editorial onOpenProduct={onOpenProduct} />
        )}
      </div>
      {inView && (
        <aside className={styles.switcher} aria-label={copy("Product design comparison")}>
          <div className={styles.switcherLabel}>
            <span aria-live="polite" aria-atomic="true">
              {selected} / {copy(designs[selected - 1])}
            </span>
            <span>{copy("Compare designs")}</span>
          </div>
          <div
            ref={controls}
            className={styles.options}
            role="group"
            aria-label={copy("Compare product-section designs")}
          >
            {designs.map((name, index) => (
              <button
                key={name}
                type="button"
                aria-label={copy("Product design {number}: {name}", {
                  number: index + 1,
                  name: copy(name),
                })}
                aria-pressed={selected === index + 1}
                onClick={() => choose(index + 1)}
                onKeyDown={(event) => navigate(event, index)}
              >
                {index + 1}
              </button>
            ))}
          </div>
        </aside>
      )}
    </section>
  );
}
