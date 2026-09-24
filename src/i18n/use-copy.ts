"use client";

import { useTranslations } from "next-intl";
import copyKeys from "./copy-keys.json";

// Source text remains readable in components; stable IDs connect it to the catalogs.
export function useCopy() {
  const translate = useTranslations("Copy");
  return (source: string, values?: Record<string, string | number>) => {
    const key = (copyKeys as Record<string, string>)[source];
    return key ? translate(key, values) : source;
  };
}
