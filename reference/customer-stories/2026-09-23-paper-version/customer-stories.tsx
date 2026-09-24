"use client";

import Image from "next/image";
import { ArrowRight, ArrowUpRight, ChevronLeft, ChevronRight } from "lucide-react";
import { useRef, useState, type KeyboardEvent } from "react";
import { useCopy } from "@/i18n/use-copy";
import styles from "./customer-stories.module.css";

// Approved design samples. Replace with sourced, permissioned stories before launch.
const stories = [
  {
    name: "Lisa M.",
    initials: "LM",
    topic: "Morning routine",
    title: "It fits into my mornings.",
    quote:
      "Weekday mornings are hectic in our house. I keep NuriCell with my breakfast things so I remember it. I like a routine that feels easy to keep up with.",
    product: "NuriCell",
    image: "nuricell",
    productIndex: 0,
  },
  {
    name: "Michael R.",
    initials: "MR",
    topic: "The science",
    title: "I read up on it first.",
    quote:
      "I don’t buy supplements on impulse. I read about NuriCell and looked into the scientists behind the formula before trying it. Knowing that background mattered to me.",
    product: "NuriCell",
    image: "nuricell",
    productIndex: 0,
  },
  {
    name: "Susan L.",
    initials: "SL",
    topic: "The source",
    title: "The source mattered to me.",
    quote:
      "I’d heard of propolis, but I didn’t know what made the green kind different. Reading about its source in Minas Gerais, Brazil, helped me understand what I was buying.",
    product: "Green Bee Propolis",
    image: "green-bee-propolis",
    productIndex: 1,
  },
] as const;

export function CustomerStories({ onOpenProduct }: { onOpenProduct: (index: number) => void }) {
  const copy = useCopy();
  const [selected, setSelected] = useState(0);
  const choices = useRef<HTMLDivElement>(null);
  const story = stories[selected];

  function navigate(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    const next =
      event.key === "ArrowRight" || event.key === "ArrowDown"
        ? (index + 1) % stories.length
        : event.key === "ArrowLeft" || event.key === "ArrowUp"
          ? (index + stories.length - 1) % stories.length
          : event.key === "Home"
            ? 0
            : event.key === "End"
              ? stories.length - 1
              : null;
    if (next === null) return;
    event.preventDefault();
    setSelected(next);
    choices.current?.querySelectorAll<HTMLButtonElement>("button")[next]?.focus();
  }

  return (
    <section id="stories" className={styles.section} aria-labelledby="stories-title">
      <div className={styles.shell}>
        <div className={styles.sidebar}>
          <header className={styles.intro}>
            <h2 id="stories-title">{copy("In their own words.")}</h2>
            <p>{copy("The routines, questions, and choices behind everyday wellbeing.")}</p>
          </header>
          <div
            ref={choices}
            className={styles.choices}
            role="group"
            aria-label={copy("Choose a sample story")}
          >
            {stories.map((item, index) => (
              <button
                key={item.name}
                type="button"
                aria-pressed={selected === index}
                aria-controls="customer-story"
                onClick={() => setSelected(index)}
                onKeyDown={(event) => navigate(event, index)}
              >
                <span className={styles.choiceNumber} aria-hidden="true">
                  0{index + 1}
                </span>
                <span className={styles.choiceText}>
                  <span>{copy(item.topic)}</span>
                  <small>{item.product}</small>
                </span>
                <ArrowRight size={18} aria-hidden="true" />
              </button>
            ))}
          </div>
          <p className={styles.draftNote}>
            {copy(
              "Design draft — all testimonials and reviewer names below are fictional samples.",
            )}
          </p>
        </div>

        <div className={styles.storyStage}>
          <article id="customer-story" className={styles.paper} aria-labelledby="story-title">
            <div key={selected} className={styles.storyContent}>
              <div className={styles.paperTop}>
                <span>{story.product}</span>
                <span className={styles.sampleTag}>{copy("Fictional sample")}</span>
              </div>
              <span className={styles.quoteMark} aria-hidden="true">
                “
              </span>
              <h3 id="story-title">{copy(story.title)}</h3>
              <blockquote>
                <p>{copy(story.quote)}</p>
              </blockquote>
              <div className={styles.author}>
                <span className={styles.initials} aria-hidden="true">
                  {story.initials}
                </span>
                <div>
                  <p>{story.name}</p>
                  <span>{copy("Illustrative reviewer")}</span>
                </div>
              </div>
            </div>
            <div className={styles.paperFooter}>
              <button
                type="button"
                className={styles.productLink}
                onClick={() => onOpenProduct(story.productIndex)}
              >
                <span className={styles.productThumb}>
                  <Image
                    src={`/images/products/${story.image}.png`}
                    width={90}
                    height={94}
                    sizes="70px"
                    alt=""
                  />
                </span>
                <span>{copy("Discover {name}", { name: story.product })}</span>
                <ArrowUpRight size={17} aria-hidden="true" />
              </button>
              <div className={styles.pageNumber} aria-hidden="true">
                0{selected + 1}
                <span> / 0{stories.length}</span>
              </div>
            </div>
          </article>
          <div className={styles.navigation}>
            <button
              type="button"
              aria-label={copy("Previous sample story")}
              onClick={() => setSelected((selected + stories.length - 1) % stories.length)}
            >
              <ChevronLeft size={20} aria-hidden="true" />
            </button>
            <span>{copy("A different perspective")}</span>
            <button
              type="button"
              aria-label={copy("Next sample story")}
              onClick={() => setSelected((selected + 1) % stories.length)}
            >
              <ChevronRight size={20} aria-hidden="true" />
            </button>
          </div>
        </div>
        <p className={styles.status} role="status">
          {copy("Sample story {number} of {count}: {name}", {
            number: selected + 1,
            count: stories.length,
            name: story.name,
          })}
        </p>
      </div>
    </section>
  );
}
