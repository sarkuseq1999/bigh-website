"use client";

import { createContext, useContext, type ReactNode } from "react";
import { Link } from "@/i18n/navigation";

// Products with their own page open it from the homepage: their "Discover" actions become real
// links (in the visitor's language), and their pictures open it too. The rest still open the
// homepage's preview dialog. The list comes from the product catalog (catalog.ts, read on the
// server by the homepage route), so a product's page links itself here as soon as it exists.
const ProductPages = createContext<Record<string, string>>({});

export function ProductPagesProvider({
  pages,
  children,
}: {
  pages: Record<string, string>;
  children: ReactNode;
}) {
  return <ProductPages.Provider value={pages}>{children}</ProductPages.Provider>;
}

/** Look up a product's own page by its name; undefined when it has none yet. */
export function useProductPage() {
  const pages = useContext(ProductPages);
  return (name: string): string | undefined => pages[name];
}

export function ProductAction({
  name,
  onOpen,
  className,
  children,
}: {
  name: string;
  onOpen: () => void;
  className?: string;
  children: ReactNode;
}) {
  const href = useProductPage()(name);
  if (href) {
    return (
      <Link href={href} className={className}>
        {children}
      </Link>
    );
  }
  return (
    <button type="button" className={className} onClick={onOpen}>
      {children}
    </button>
  );
}
