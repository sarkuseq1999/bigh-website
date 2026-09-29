import type { ProductSummary } from "../product-types";

// Short entries for all five products, from the homepage lineup (products-lineup.tsx). Every
// product has one, page or not: the product pages' footers and the homepage use them.
export const summaries: ProductSummary[] = [
  {
    slug: "nuricell",
    name: "NuriCell",
    focus: "Cellular health & mental energy",
    headline: "Stay sharp. Live fully.",
    bottle: {
      src: "/images/products/nuricell.png",
      width: 1230,
      height: 1278,
      alt: "NuriCell bottle",
    },
    tint: "#edf5fc",
    ink: "#24578e",
  },
  {
    slug: "green-bee-propolis",
    name: "Green Bee Propolis",
    focus: "From Minas Gerais, Brazil",
    headline: "Distinctive green propolis from Minas Gerais, Brazil.",
    bottle: {
      src: "/images/products/green-bee-propolis.png",
      width: 1231,
      height: 1278,
      alt: "Green Bee Propolis bottle",
    },
    tint: "#f2f5e9",
    ink: "#58682e",
  },
  {
    slug: "advanced-opc",
    name: "Advanced OPC Formula",
    focus: "Plant-based antioxidants",
    headline: "Nature’s antioxidant power. Focused on your cells.",
    bottle: {
      src: "/images/products/advanced-opc.png",
      width: 1231,
      height: 1278,
      alt: "Advanced OPC Formula bottle",
    },
    tint: "#fcf0f1",
    ink: "#964758",
  },
  {
    slug: "turmerific",
    name: "Turmerific",
    focus: "Advanced curcumin",
    headline: "Turmeric, advanced by neuroscience.",
    bottle: {
      src: "/images/products/turmerific.png",
      width: 1230,
      height: 1278,
      alt: "Turmerific bottle",
    },
    tint: "#fff4e5",
    ink: "#956123",
  },
  {
    slug: "nature-calm",
    name: "Nature Calm",
    focus: "A cellular approach to everyday stress",
    headline: "Everyday stress. A cellular approach.",
    bottle: {
      src: "/images/products/nature-calm.png",
      width: 1230,
      height: 1278,
      alt: "Nature Calm bottle",
    },
    tint: "#eef6ed",
    ink: "#487249",
  },
];
