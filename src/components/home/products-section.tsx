"use client";

import Image from "next/image";
import { ArrowDown, ArrowRight, ArrowUpRight, Plus } from "lucide-react";
import legacy from "./homepage.module.css";
import styles from "./nuricell-spotlight.module.css";
import { NuriCellSpotlight } from "./nuricell-spotlight";
import { ProductsCollectionComparison } from "./products-collection-comparison";
import { ProductsLineup } from "./products-lineup";

type ProductPreview = {
  name: string;
  image: string;
  category: string;
  tone: string;
};

export function ProductsSection({
  products,
  onOpenProduct,
  design = "spotlight",
}: {
  products: ProductPreview[];
  onOpenProduct: (index: number) => void;
  design?: "original" | "spotlight" | "comparison" | "lineup";
}) {
  if (design === "lineup") return <ProductsLineup onOpenProduct={onOpenProduct} />;
  if (design === "comparison")
    return <ProductsCollectionComparison onOpenProduct={onOpenProduct} />;
  const isOriginal = design === "original";

  return (
    <section
      id="products"
      data-products-design={design}
      className={isOriginal ? legacy.productsSection : styles.products}
    >
      {isOriginal ? (
        <>
          <div className={legacy.productIntro}>
            <p className={legacy.eyebrow}>03 / THOUGHTFULLY FORMULATED</p>
            <h2>
              Meet your
              <br />
              everyday possibilities<span>.</span>
            </h2>
            <p>
              Get to know the BiGH collection.
              <br />
              Start with what’s inside.
            </p>
          </div>
          <div className={legacy.flagship}>
            <div className={legacy.flagshipVisual}>
              <span className={legacy.flagshipTag}>THE BIGH FLAGSHIP</span>
              <span className={legacy.bottleHalo} />
              <span className={legacy.bottleWord} aria-hidden="true">
                NuriCell
              </span>
              <Image
                src="/images/nuricell.png"
                alt="NuriCell dietary supplement bottle"
                width={550}
                height={580}
                sizes="(max-width: 760px) 80vw, 42vw"
              />
              <span className={legacy.packagingNote}>Existing packaging shown</span>
            </div>
            <div className={legacy.flagshipCopy}>
              <span className={legacy.eyebrow}>OUR STARTING POINT</span>
              <h3>NuriCell.</h3>
              <p className={legacy.serifLead}>
                Cellular health.
                <br />
                Mental energy.
                <br />A life to get on with.
              </p>
              <p>
                Our flagship formula brings BiGH’s focus into one place. Four ingredients, with a
                scientific story worth understanding.
              </p>
              <div className={legacy.ingredientPills}>
                <span>Acetyl-L-carnitine</span>
                <span>Creatine</span>
                <span>Alpha-lipoic acid</span>
                <span>Choline</span>
              </div>
              <button onClick={() => onOpenProduct(0)} className={legacy.darkButton}>
                Discover NuriCell <ArrowUpRight size={20} />
              </button>
              <a href="#research" className={legacy.textLink}>
                Explore the research <ArrowRight size={18} />
              </a>
            </div>
          </div>
        </>
      ) : (
        <NuriCellSpotlight onDiscover={() => onOpenProduct(0)} />
      )}
      <div className={isOriginal ? undefined : styles.collection}>
        <div className={legacy.collectionHeader}>
          <h3>A considered collection.</h3>
          <span>
            Find your starting point <ArrowDown size={18} />
          </span>
        </div>
        <div className={legacy.productGrid}>
          {products.slice(1).map((product, index) => (
            <button
              className={legacy.productCard}
              key={product.name}
              onClick={() => onOpenProduct(index + 1)}
            >
              <div className={`${legacy.productImage} ${legacy[product.tone]}`}>
                <span className={legacy.productIndex}>0{index + 2}</span>
                <Image
                  src={`/images/${product.image}.png`}
                  alt={`${product.name} bottle`}
                  width={310}
                  height={330}
                  sizes="(max-width: 600px) 44vw, 23vw"
                />
                <span className={legacy.productArrow}>
                  <Plus size={23} />
                </span>
              </div>
              <h4>{product.name}</h4>
              <p>{product.category}</p>
              <span className={legacy.productLink}>
                Explore formula <ArrowUpRight size={16} />
              </span>
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}
