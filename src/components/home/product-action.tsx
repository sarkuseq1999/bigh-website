"use client";

import type { ReactNode } from "react";
import { Link } from "@/i18n/navigation";

// Products with their own page (September 28, 2026: NuriCell). Their "Discover" actions are real
// links to it, in the visitor's language; the rest still open the homepage's preview dialog until
// their pages exist.
const productPages: Record<string, string> = {
  NuriCell: "/products/nuricell",
};

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
  const href = productPages[name];
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
