"use client";

import Image from "next/image";
import { ArrowUpRight, ChevronLeft, ChevronRight, MoveUpRight } from "lucide-react";
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
    artwork: "morning-v1",
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
    artwork: "curiosity-v1",
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
    artwork: "botanical-v1",
  },
] as const;

const designs = [
  { id: "daybook", name: "Daybook" },
  { id: "wall", name: "Story Wall" },
  { id: "spotlight", name: "Spotlight" },
] as const;
type Story = (typeof stories)[number];

function Flower({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 100 100" fill="currentColor" aria-hidden="true">
      {[0, 45, 90, 135].map((rotation) => (
        <ellipse
          key={rotation}
          cx="50"
          cy="50"
          rx="16"
          ry="48"
          transform={`rotate(${rotation} 50 50)`}
        />
      ))}
      <circle cx="50" cy="50" r="12" fill="var(--flower-center, #fff6de)" />
    </svg>
  );
}

function StoryImage({ story, className }: { story: Story; className?: string }) {
  return (
    <Image
      className={className}
      src={`/images/stories/${story.artwork}.webp`}
      width={1000}
      height={1000}
      sizes="(max-width: 700px) 90vw, 45vw"
      alt=""
    />
  );
}

function Author({ story }: { story: Story }) {
  const copy = useCopy();
  return (
    <div className={styles.author}>
      <span className={styles.initials} aria-hidden="true">
        {story.initials}
      </span>
      <div>
        <p>{story.name}</p>
        <span>{copy("Illustrative reviewer")}</span>
      </div>
    </div>
  );
}

export function CustomerStories({ onOpenProduct }: { onOpenProduct: (index: number) => void }) {
  const copy = useCopy();
  const [selected, setSelected] = useState(0);
  const section = useRef<HTMLElement>(null);
  const [design, setDesign] = useState<(typeof designs)[number]["id"]>("daybook");
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

  function productLink(item: Story) {
    return (
      <button
        type="button"
        className={styles.productLink}
        onClick={() => onOpenProduct(item.productIndex)}
      >
        <span>{copy("Discover {name}", { name: item.product })}</span>
        <span className={styles.linkArrow}>
          <ArrowUpRight size={19} aria-hidden="true" />
        </span>
      </button>
    );
  }

  const storyChoices = (
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
          <StoryImage story={item} />
          <span>
            <small>0{index + 1}</small>
            {copy(item.topic)}
          </span>
        </button>
      ))}
    </div>
  );

  const navigation = (
    <div className={styles.navigation}>
      <button
        type="button"
        aria-label={copy("Previous sample story")}
        onClick={() => setSelected((selected + stories.length - 1) % stories.length)}
      >
        <ChevronLeft size={22} aria-hidden="true" />
      </button>
      <span aria-hidden="true">
        0{selected + 1}
        <span> / 03</span>
      </span>
      <button
        type="button"
        aria-label={copy("Next sample story")}
        onClick={() => setSelected((selected + 1) % stories.length)}
      >
        <ChevronRight size={22} aria-hidden="true" />
      </button>
    </div>
  );

  return (
    <section
      ref={section}
      id="stories"
      className={styles.section}
      data-design={design}
      aria-labelledby="stories-title"
    >
      <div className={styles.reviewBar}>
        <span>{copy("Choose a design")}</span>
        <div role="group" aria-label={copy("Testimonial design choices")}>
          {designs.map((item, index) => (
            <button
              type="button"
              key={item.id}
              aria-pressed={design === item.id}
              onClick={() => {
                setDesign(item.id);
                section.current?.scrollIntoView({ block: "start", behavior: "instant" });
              }}
            >
              <span>{index + 1}</span>
              <span className={styles.designName}>{copy(item.name)}</span>
            </button>
          ))}
        </div>
      </div>
      <div className={styles.shell} key={design}>
        <div className={styles.headingRow}>
          <header className={styles.intro}>
            <h2 id="stories-title">{copy("In their own words.")}</h2>
            <p>{copy("The routines, questions, and choices behind everyday wellbeing.")}</p>
          </header>
          <div className={styles.headingAccent} aria-hidden="true">
            <Flower />
            <span>BiGH</span>
          </div>
        </div>
        <p className={styles.draftNote}>
          {copy("Design draft — all testimonials and reviewer names below are fictional samples.")}
        </p>

        {design === "wall" ? (
          <div className={styles.wall}>
            {stories.map((item, index) => (
              <article
                className={styles.wallCard}
                key={item.name}
                aria-labelledby={`wall-story-${index}`}
              >
                <div className={styles.wallVisual}>
                  <StoryImage story={item} />
                  <span className={styles.wallNumber} aria-hidden="true">
                    0{index + 1}
                  </span>
                  <span className={styles.topicSticker}>{copy(item.topic)}</span>
                </div>
                <div className={styles.wallCopy}>
                  <div className={styles.meta}>
                    <span>{item.product}</span>
                    <span className={styles.sampleTag}>{copy("Fictional sample")}</span>
                  </div>
                  <h3 id={`wall-story-${index}`}>{copy(item.title)}</h3>
                  <blockquote>
                    <p>{copy(item.quote)}</p>
                  </blockquote>
                  <Author story={item} />
                  {productLink(item)}
                </div>
              </article>
            ))}
            <Flower className={styles.wallFlower} />
          </div>
        ) : (
          <>
            <div id="customer-story" className={styles.feature}>
              <div className={styles.visual}>
                <div className={styles.photoFrame} key={story.artwork}>
                  <StoryImage story={story} className={styles.scene} />
                  <div className={styles.photoCaption}>
                    <span>{copy(story.topic)}</span>
                    <span>0{selected + 1} / 03</span>
                  </div>
                </div>
                <div className={styles.productBubble} aria-hidden="true">
                  <Image
                    src={`/images/products/${story.image}.png`}
                    width={240}
                    height={280}
                    sizes="(max-width: 700px) 115px, 180px"
                    alt=""
                  />
                </div>
                <Flower className={styles.visualFlower} />
                <span className={styles.visualArrow} aria-hidden="true">
                  <MoveUpRight />
                </span>
              </div>
              <article className={styles.storyCopy} aria-labelledby="story-title">
                <div key={selected} className={styles.storyText}>
                  <div className={styles.meta}>
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
                  <Author story={story} />
                </div>
                {productLink(story)}
              </article>
            </div>
            <div className={styles.browseRow}>
              {storyChoices}
              {navigation}
            </div>
          </>
        )}
        <p className={styles.artworkNote}>
          {copy("Illustrative scenes. Sample stories for design review.")}
        </p>
        <p className={styles.status} role="status" aria-atomic="true">
          {design === "wall"
            ? copy("All three sample stories are shown.")
            : copy("Sample story {number} of {count}: {name}", {
                number: selected + 1,
                count: stories.length,
                name: story.name,
              })}
        </p>
      </div>
    </section>
  );
}
