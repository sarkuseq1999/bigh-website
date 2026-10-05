"use client";

import Image from "next/image";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { useState } from "react";
import { ProductAction } from "@/components/home/product-action";
import { useCopy } from "@/i18n/use-copy";
import { stories, storiesIntro } from "../content";
import { useHomeDialogs } from "@/components/ink/dialogs";
import { storyPaintings } from "./assets";
import base from "@/components/ink/ink.module.css";
import styles from "./stories.module.css";

// "In their own words." Each fictional sample pairs a quiet ink still life of its everyday moment
// (objects only, never a face; labelled "Illustration") with its words set large beside it; the
// byline carries the name, the moment and the "Fictional sample" label. The three names below
// choose a story.
export function Stories() {
  const copy = useCopy();
  const dialogs = useHomeDialogs();
  const [index, setIndex] = useState(0);
  // Once a reader changes the story, each new still life blooms through the ink blot (round 10);
  // the first one arrives with the figure's own bloom.
  const [turned, setTurned] = useState(false);
  const story = stories[index];
  const choose = (next: number) => {
    if (next === index) return;
    setTurned(true);
    setIndex(next);
  };
  const go = (step: number) => choose((index + step + stories.length) % stories.length);

  return (
    <section
      id="stories"
      className={styles.stories}
      aria-labelledby="stories-title"
      data-brush="stories"
    >
      <div className={`${base.wrap} ${styles.inner}`}>
        <div className={styles.spread}>
          <figure
            className={styles.painting}
            data-brush="story-painting"
            data-bloom=""
            data-turned={turned}
          >
            {stories.map((item, i) => (
              <Image
                key={item.id}
                className={`${base.ink} ${styles.still}`}
                src={storyPaintings[item.id].src}
                alt={i === index ? copy(item.topic) : ""}
                aria-hidden={i !== index}
                width={storyPaintings[item.id].width}
                height={storyPaintings[item.id].height}
                sizes="(max-width: 899px) 100vw, min(52vw, 860px)"
                data-on={i === index}
              />
            ))}
            <figcaption className={`${base.caption} ${styles.tag}`}>
              {copy("Illustration")}
            </figcaption>
          </figure>

          <div className={styles.words} data-brush="story-words">
            <header className={styles.head}>
              <h2 id="stories-title" className={base.display}>
                {copy(storiesIntro.title)}
              </h2>
              <p className={`${base.body} ${styles.intro}`}>{copy(storiesIntro.text)}</p>
              <p className={styles.note}>{copy(storiesIntro.note)}</p>
            </header>

            <article key={story.id} className={styles.story} aria-live="polite">
              <h3 className={styles.quoteTitle}>
                <span className={styles.hang}>“</span>
                {copy(story.title)}”
              </h3>
              <blockquote className={styles.quote}>
                <p>{copy(story.quote)}</p>
              </blockquote>
              <div className={styles.by}>
                <span className={styles.name}>{story.name}</span>
                <span className={styles.topic}>{copy(story.topic)}</span>
                <span className={styles.sample}>{copy(storiesIntro.sample)}</span>
                <ProductAction
                  name={story.product}
                  onOpen={() => dialogs.openProduct(story.productIndex)}
                  className={base.textLink}
                >
                  {copy(story.product)} <ArrowRight size={17} aria-hidden="true" />
                </ProductAction>
              </div>
            </article>
          </div>
        </div>

        <div className={styles.controls}>
          <div
            className={styles.choices}
            role="group"
            aria-label={copy("Choose a story")}
            data-brush="story-choices"
          >
            {stories.map((item, i) => (
              <button
                key={item.id}
                type="button"
                className={styles.choice}
                aria-pressed={index === i}
                onClick={() => choose(i)}
              >
                <span className={styles.choiceName}>{item.name}</span>
                <span className={styles.choiceTopic}>{copy(item.topic)}</span>
              </button>
            ))}
          </div>
          <div className={styles.arrows}>
            <button
              type="button"
              className={styles.arrow}
              aria-label={copy("Previous sample story")}
              onClick={() => go(-1)}
            >
              <ArrowLeft size={20} aria-hidden="true" />
            </button>
            <button
              type="button"
              className={styles.arrow}
              aria-label={copy("Next sample story")}
              onClick={() => go(1)}
            >
              <ArrowRight size={20} aria-hidden="true" />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
