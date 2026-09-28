import type { ProductIngredient, ProductPage } from "./product-types";

// Development only (the template ignores it in production builds): ?chapters-fixture=lean|full
// reshapes NuriCell's data so the QA script can prove Template 2 holds up for other products.
// Every added word and number is a placeholder for a layout check, never a product fact.
//
// lean: one headline line, one ingredient, no why, photo, people, credit, signature or studies,
//       one capsule a day, a 60-day bottle.
// full: three headline lines, 18 ingredients (mg, mcg and IU; some without a role), 14 studies,
//       a third person without a photo, six capsules a day, a "why" with four lines and no picture.

export type ChaptersFixture = "lean" | "full";

function placeholderIngredients(count: number): ProductIngredient[] {
  const units: ProductIngredient["unit"][] = ["mg", "mcg", "IU", "mg"];
  const amounts = [25, 1000, 400, 5];
  return Array.from({ length: count }, (_, index) => ({
    key: `placeholder-${index}`,
    name: `Placeholder ingredient ${index + 5}`,
    form: `Placeholder label form ${index + 5}`,
    amount: amounts[index % amounts.length],
    unit: units[index % units.length],
    role:
      index % 3 === 0
        ? undefined
        : "Placeholder role, about as long as a real one, for checking how the rows wrap.",
  }));
}

export function chaptersFixture(product: ProductPage, name: string | null): ProductPage {
  if (name === "lean") {
    return {
      ...product,
      headlineLines: [product.headlineLines.join(" ")],
      credit: undefined,
      photo: undefined,
      why: undefined,
      signature: undefined,
      people: [],
      studies: [],
      ingredients: product.ingredients.slice(0, 1),
      serving: { ...product.serving, capsules: 1, perBottle: 60, days: 60 },
      faq: product.faq.slice(0, 2),
      related: product.related.slice(0, 2),
    };
  }
  if (name === "full") {
    return {
      ...product,
      headlineLines: [...product.headlineLines, "Placeholder third line."],
      ingredients: [...product.ingredients, ...placeholderIngredients(14)],
      studies: [...product.studies, ...product.studies],
      people: [
        ...product.people,
        { name: "Placeholder person", title: "Placeholder title", lines: ["Placeholder line."] },
      ],
      serving: { ...product.serving, capsules: 6 },
      why: product.why && {
        ...product.why,
        visual: undefined,
        lines: [...product.why.lines, "Placeholder fourth line."],
      },
    };
  }
  return product;
}
