"use client";

import { useState } from "react";
import Image from "next/image";
import { Menu } from "lucide-react";
import { useTranslations } from "next-intl";

import { Link } from "@/i18n/navigation";
import { Button } from "@/components/ui/button";
import {
  Sheet,
  SheetContent,
  SheetTrigger,
  SheetTitle,
  SheetDescription,
  SheetHeader,
} from "@/components/ui/sheet";

const NAV_KEYS = ["home", "products", "science", "about", "support"] as const;
const NAV_HREFS: Record<(typeof NAV_KEYS)[number], string> = {
  home: "/",
  products: "/products",
  science: "/#science",
  about: "/about",
  support: "/support",
};

export function SiteHeader() {
  const tNav = useTranslations("Nav");
  const tBrand = useTranslations("Brand");
  const [open, setOpen] = useState(false);

  return (
    <header className="bg-cream-50/70 absolute top-0 right-0 left-0 z-50 w-full backdrop-blur-md">
      <div className="mx-auto flex h-24 max-w-6xl items-center justify-between px-6">
        <Link href="/" aria-label={tBrand("name")} className="inline-flex items-center">
          <Image
            src="/logo-black.png"
            alt={tBrand("name")}
            width={768}
            height={430}
            priority
            className="block h-18 w-auto dark:hidden"
          />
          <Image
            src="/logo-white.png"
            alt={tBrand("name")}
            width={300}
            height={168}
            priority
            className="hidden h-18 w-auto dark:block"
          />
        </Link>

        <nav className="hidden items-center gap-8 md:flex">
          {NAV_KEYS.map((key) => (
            <Link
              key={key}
              href={NAV_HREFS[key]}
              className="text-espresso hover:text-sienna text-xl font-medium transition-colors"
            >
              {tNav(key)}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-1 md:hidden">
          <Sheet open={open} onOpenChange={setOpen}>
            <SheetTrigger
              render={<Button variant="ghost" size="icon" aria-label={tNav("openMenu")} />}
            >
              <Menu />
            </SheetTrigger>
            <SheetContent side="right" className="w-72">
              <SheetHeader>
                <SheetTitle>{tBrand("name")}</SheetTitle>
                <SheetDescription className="sr-only">{tNav("openMenu")}</SheetDescription>
              </SheetHeader>
              <nav className="flex flex-col gap-1 px-4">
                {NAV_KEYS.map((key) => (
                  <Link
                    key={key}
                    href={NAV_HREFS[key]}
                    onClick={() => setOpen(false)}
                    className="text-foreground/80 hover:bg-foreground/5 hover:text-foreground rounded-md px-2 py-2 text-base font-medium transition-colors"
                  >
                    {tNav(key)}
                  </Link>
                ))}
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}
