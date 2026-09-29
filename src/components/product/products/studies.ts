import { researchItems } from "@/components/home/research-data";
import type { ProductStudy } from "../product-types";

/** Studies from the homepage's checked research list (research-data.ts), by the end of their URL. */
export function studies(urls: string[]): ProductStudy[] {
  return urls.map((url) => {
    const item = researchItems.find((entry) => entry.url.endsWith(url));
    if (!item) throw new Error(`Unknown study ${url}`);
    return {
      year: item.year,
      kind: item.category.split(" · ")[0],
      title: item.title,
      journal: item.journal,
      note: item.text,
      url: item.url,
    };
  });
}
