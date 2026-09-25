// Approved design samples (fictional). Replace with sourced, permissioned stories before launch.
// No customer photos and no photo-real invented people. Picture options (Sept 24 review round):
// hands-only scenes and loops, everyday objects, or words only. The ink drawings remain as a fallback.
export const stories = [
  {
    id: "lisa",
    name: "Lisa M.",
    topic: "Morning routine",
    title: "It fits into my mornings.",
    quote:
      "Weekday mornings are hectic in our house. I keep NuriCell with my breakfast things so I remember it. I like a routine that feels easy to keep up with.",
    product: "NuriCell",
    productImage: "/images/products/nuricell.png",
    productIndex: 0,
    portrait: "/images/stories/v2/ink-lisa.webp",
    portraitSize: { width: 979, height: 2010 },
    face: "/images/stories/v2/ink-face-lisa.webp",
    object: "/images/stories/v2/object-lisa.webp",
    objectSize: { width: 1400, height: 1147 },
    objectThumb: "/images/stories/v2/object-thumb-lisa.webp",
    sceneThumb: "/images/stories/v2/scene-thumb-morning.webp",
    still: "/images/stories/v2/moment-morning.webp",
    video: "/media/stories/loop-morning.mp4",
  },
  {
    id: "michael",
    name: "Michael R.",
    topic: "The science",
    title: "I read up on it first.",
    quote:
      "I don’t buy supplements on impulse. I read about NuriCell and looked into the scientists behind the formula before trying it. Knowing that background mattered to me.",
    product: "NuriCell",
    productImage: "/images/products/nuricell.png",
    productIndex: 0,
    portrait: "/images/stories/v2/ink-michael.webp",
    portraitSize: { width: 730, height: 2011 },
    face: "/images/stories/v2/ink-face-michael.webp",
    object: "/images/stories/v2/object-michael.webp",
    objectSize: { width: 1400, height: 1018 },
    objectThumb: "/images/stories/v2/object-thumb-michael.webp",
    sceneThumb: "/images/stories/v2/scene-thumb-reading.webp",
    // v2 book pages show botanical drawings only; v1 had round specimens that could read as germs.
    still: "/images/stories/v2/moment-reading-v2.webp",
    video: "/media/stories/loop-reading-v2.mp4",
  },
  {
    id: "susan",
    name: "Susan L.",
    topic: "The source",
    title: "The source mattered to me.",
    quote:
      "I’d heard of propolis, but I didn’t know what made the green kind different. Reading about its source in Minas Gerais, Brazil, helped me understand what I was buying.",
    product: "Green Bee Propolis",
    productImage: "/images/products/green-bee-propolis.png",
    productIndex: 1,
    portrait: "/images/stories/v2/ink-susan.webp",
    portraitSize: { width: 838, height: 1995 },
    face: "/images/stories/v2/ink-face-susan.webp",
    object: "/images/stories/v2/object-susan.webp",
    objectSize: { width: 1400, height: 1125 },
    objectThumb: "/images/stories/v2/object-thumb-susan.webp",
    sceneThumb: "/images/stories/v2/scene-thumb-garden.webp",
    still: "/images/stories/v2/moment-garden.webp",
    video: "/media/stories/loop-garden.mp4",
  },
] as const;

export type Story = (typeof stories)[number];

export type StoriesDesignProps = {
  onOpenProduct: (index: number) => void;
};
