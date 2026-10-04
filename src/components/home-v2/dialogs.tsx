"use client";

import Image from "next/image";
import { ArrowUpRight, Plus, X } from "lucide-react";
import { createContext, useContext, useEffect, useRef, useState, type ReactNode } from "react";
import { useCopy } from "@/i18n/use-copy";
import { products, scienceImages } from "./content";
import { lockPageScroll } from "./lock-scroll";
import styles from "./dialogs.module.css";

// The homepage's preview dialogs (product, Dr. Liu, Ask BiGH Science, support, the three short
// explainers), moved out of home/homepage.tsx unchanged in wording so every look shares them.
// The explainers show pictures only when the page passes its own (`articleImages`); the Ink & Gold
// homepage passes none (its paintings carry the science).
// One sheet of the page's paper for all of them: the label and the close button stay at its top
// while the words scroll under; it settles in and leaves in CSS (dialogs.module.css), so the words
// stay in it while it leaves. Focus moves in when it opens and goes back to the button that
// opened it (the browser's own dialog behaviour).

type Dialogs = {
  openProduct: (index: number) => void;
  openScientist: () => void;
  openAsk: () => void;
  openSupport: () => void;
  openArticle: (index: number) => void;
};

const DialogContext = createContext<Dialogs | null>(null);

export function useHomeDialogs(): Dialogs {
  const value = useContext(DialogContext);
  if (!value) throw new Error("useHomeDialogs needs <HomeDialogs>");
  return value;
}

type Content = { eyebrow: string; title: string; body: ReactNode };

// Details for the product dialog (products without their own page yet).
const productDetails = [
  {
    category: "Our flagship formula",
    detail:
      "NuriCell brings four ingredients together in one capsule formula. Explore the ingredients and the research behind the thinking, with a clear distinction between ingredient studies and evidence for the finished product.",
    ingredients: "Acetyl-L-carnitine, creatine, alpha-lipoic acid, and choline.",
  },
  {
    category: "Brazilian green propolis",
    detail:
      "Propolis is a resinous material collected by bees. Its composition varies with its botanical source. Research on one standardized extract does not automatically apply to every propolis product.",
    ingredients: "Green bee propolis extract.",
  },
  {
    category: "Botanical & nutrient blend",
    detail:
      "A multi-ingredient formula. Each ingredient has its own research background, and the amounts and preparation used in a study matter when interpreting its findings.",
    ingredients:
      "Includes grape seed and pine bark extracts, vitamins C and E, and other nutrients.",
  },
  {
    category: "Curcumin formula",
    detail:
      "Curcumin is a compound found in turmeric. Different curcumin preparations are not interchangeable. Research findings depend on the preparation, dose, people studied, and outcome measured.",
    ingredients: "Longvida® Optimized Curcumin Extract.",
  },
  {
    category: "Multi-ingredient formula",
    detail:
      "Nature Calm combines several ingredients in one formula. Its name is not a sleep or treatment claim. The full current label and product-specific evidence will guide the final product information.",
    ingredients: "Includes CoQ10, theanine, phosphatidylserine, vitamins, and other nutrients.",
  },
];

const explainers = [
  {
    title: "Energy starts small.",
    text: "Inside most of your cells are mitochondria. They turn energy from food into a form your cells can use. Think of them as tiny energy converters.",
    note: "A small part of a cell. A big part of how it works.",
    source: "https://www.genome.gov/genetics-glossary/Mitochondria",
    sourceLabel: "National Human Genome Research Institute",
    image: scienceImages.glass.src,
  },
  {
    title: "Balance matters.",
    text: "Normal cell activity produces reactive molecules. Your body has defenses that help keep them in balance. Too much oxidative stress can damage cells.",
    note: "More antioxidants do not automatically mean better health.",
    source: "https://www.nccih.nih.gov/health/antioxidant-supplements-what-you-need-to-know",
    sourceLabel: "National Center for Complementary and Integrative Health",
    image: scienceImages.drop,
  },
  {
    title: "Aging is a bigger story.",
    text: "As we age, many processes in our cells change. Mitochondrial function is one part of that story. No single ingredient explains all of healthy aging.",
    note: "Understand the whole picture, one idea at a time.",
    source: "https://pubmed.ncbi.nlm.nih.gov/36599349/",
    sourceLabel: "Hallmarks of Aging, Cell, 2023",
    image: scienceImages.glassAged,
  },
];

export function HomeDialogs({
  children,
  articleImages,
}: {
  children: ReactNode;
  /** One picture per explainer (mitochondria, free radicals, aging), or none. */
  articleImages?: readonly (string | undefined)[];
}) {
  const copy = useCopy();
  const dialog = useRef<HTMLDialogElement>(null);
  const [content, setContent] = useState<Content | null>(null);
  const [open, setOpen] = useState(false);
  // Each opening starts fresh: at the top, with every question closed.
  const [round, setRound] = useState(0);

  useEffect(() => {
    if (!open) return;
    const element = dialog.current;
    if (element && !element.open) {
      element.scrollTop = 0;
      element.showModal();
    }
    return lockPageScroll();
  }, [open]);

  const show = (next: Content) => {
    setContent(next);
    setRound((count) => count + 1);
    setOpen(true);
  };

  // Closing fires the dialog's own "close" event (as Escape does), which lets the page go.
  const close = () => dialog.current?.close();

  const link = (href: string, label: string) => (
    <a className={styles.textLink} href={href} target="_blank" rel="noreferrer">
      {copy(label)} <ArrowUpRight size={18} aria-hidden="true" />
    </a>
  );

  const value: Dialogs = {
    openProduct(index) {
      const product = products[index];
      const details = productDetails[index];
      show({
        eyebrow: copy(details.category),
        title: product.name,
        body: (
          <>
            <div className={styles.productPicture}>
              <Image
                src={product.image}
                alt={copy("{name} bottle", { name: product.name })}
                width={260}
                height={270}
              />
            </div>
            <p>{copy(details.detail)}</p>
            <h3>{copy("Inside the formula")}</h3>
            <p>{copy(details.ingredients)}</p>
            <div className={styles.note}>
              <strong>{copy("Product preview")}</strong>
              <p>
                {copy(
                  "These details use the available product materials. Current labels, directions, availability, and pricing still need confirmation. Ordering is not open in this preview.",
                )}
              </p>
            </div>
          </>
        ),
      });
    },
    openScientist() {
      show({
        eyebrow: copy("Meet the scientists"),
        title: copy("Dr. Jiankang Liu"),
        body: (
          <>
            <p>
              {copy(
                "Dr. Liu studies mitochondrial function, oxidative stress, and the biology of aging. His scientific background is central to BiGH’s approach to cellular health.",
              )}
            </p>
            <h3>{copy("A career in cell science")}</h3>
            <p>
              {copy(
                "He earned his doctorate at Okayama University in Japan and completed postdoctoral work in biochemistry and molecular biology at the University of California, Berkeley.",
              )}
            </p>
            <p>
              {copy(
                "In 2025, his university announced his election to the European Academy of Sciences and Arts.",
              )}
            </p>
            <h3>{copy("Read the research in context")}</h3>
            {link("https://www.uhrs.edu.cn/info/1050/1805.htm", "University biography (Chinese)")}
            {link("https://pubmed.ncbi.nlm.nih.gov/11854529/", "Read the 2002 study")}
          </>
        ),
      });
    },
    openAsk() {
      show({
        eyebrow: copy("A planned customer benefit"),
        title: copy("Ask BiGH Science"),
        body: (
          <>
            <p>
              {copy(
                "Good questions deserve clear explanations. We are developing a way for BiGH customers to explore broader health and science questions with input from participating scientists.",
              )}
            </p>
            <ol className={styles.list} role="list">
              <li>
                {copy(
                  "Start with a question about topics such as cellular health, nutrition, or healthy aging.",
                )}
              </li>
              <li>
                {copy(
                  "BiGH explains what the research says and involves scientific advisors when deeper input is needed.",
                )}
              </li>
              <li>
                {copy(
                  "Each answer identifies its contributors and where the science remains uncertain.",
                )}
              </li>
            </ol>
            <div className={styles.note}>
              <strong>{copy("In development")}</strong>
              <p>
                {copy(
                  "The question service is not accepting submissions yet. Eligibility and response arrangements are still being agreed. This will be general science education, not personal medical care.",
                )}
              </p>
            </div>
          </>
        ),
      });
    },
    openSupport() {
      show({
        eyebrow: copy("Here to help"),
        title: copy("BiGH support"),
        body: (
          <>
            <p>
              {copy(
                "This is a preview of the new BiGH website. You can explore the range and science, but purchases and account services are not connected yet.",
              )}
            </p>
            <div className={styles.faq}>
              {[
                [
                  "Can I place an order here?",
                  "Not yet. Ordering will be available when the new store is connected. No payments are taken in this preview.",
                ],
                [
                  "Where are shipping and return details?",
                  "Market-specific shipping and return information will be added before the store opens.",
                ],
                [
                  "Can I ask a health or science question?",
                  "Ask BiGH Science is in development. It will explain research in everyday language. For personal treatment or medication questions, speak with your healthcare professional.",
                ],
                [
                  "Will other languages be available?",
                  "Use the language selector at the top of the page to switch between English, Simplified Chinese, Korean, Vietnamese, and Japanese.",
                ],
              ].map(([question, answer]) => (
                <details key={question} name="home-support">
                  <summary>
                    <span>{copy(question)}</span>
                    <span className={styles.toggle} aria-hidden="true">
                      <Plus size={20} />
                    </span>
                  </summary>
                  <p>{copy(answer)}</p>
                </details>
              ))}
            </div>
          </>
        ),
      });
    },
    openArticle(index) {
      const item = explainers[index];
      show({
        eyebrow: copy("Health, explained simply"),
        title: copy(item.title),
        body: (
          <>
            {articleImages?.[index] && (
              <div className={styles.articlePicture}>
                <Image src={articleImages[index]} alt="" width={640} height={362} />
              </div>
            )}
            <p>{copy(item.text)}</p>
            <p className={styles.key}>{copy(item.note)}</p>
            <p>
              {copy(
                "Understanding a biological process is a starting point. It does not tell us whether a particular supplement will change that process or improve health.",
              )}
            </p>
            {link(item.source, "Read the source")}
            <p className={styles.small}>{copy(item.sourceLabel)}</p>
          </>
        ),
      });
    },
  };

  return (
    <DialogContext.Provider value={value}>
      {children}
      <dialog
        ref={dialog}
        className={styles.dialog}
        aria-labelledby="home-dialog-title"
        // Lenis (the page's smooth scrolling) leaves the wheel alone here: the sheet scrolls, and
        // the page under it stays put.
        data-lenis-prevent=""
        onClose={() => setOpen(false)}
        onClick={(event) => {
          if (event.target !== event.currentTarget) return;
          const box = event.currentTarget.getBoundingClientRect();
          if (
            event.clientX < box.left ||
            event.clientX > box.right ||
            event.clientY < box.top ||
            event.clientY > box.bottom
          )
            close();
        }}
      >
        {content && (
          <>
            <div className={styles.head}>
              <p className={styles.eyebrow}>{content.eyebrow}</p>
              <button
                type="button"
                className={styles.close}
                onClick={close}
                aria-label={copy("Close details")}
              >
                <X size={24} aria-hidden="true" />
              </button>
            </div>
            <div className={styles.words} key={round}>
              <h2 id="home-dialog-title" className={styles.title}>
                {content.title}
              </h2>
              <div className={styles.body}>{content.body}</div>
            </div>
          </>
        )}
      </dialog>
    </DialogContext.Provider>
  );
}
