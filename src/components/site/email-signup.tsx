"use client";

import { useTranslations } from "next-intl";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function EmailSignup() {
  const t = useTranslations("Signup");

  // No backend wiring yet — Resend / ConvertKit lands in a later session.
  return (
    <section className="mx-auto max-w-3xl px-6 py-24 text-center sm:py-32">
      <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">{t("title")}</h2>
      <p className="text-foreground/65 mx-auto mt-4 max-w-md">{t("body")}</p>

      <form
        onSubmit={(e) => e.preventDefault()}
        className="mx-auto mt-10 flex max-w-md flex-col gap-3 sm:flex-row"
      >
        <Input
          type="email"
          required
          placeholder={t("placeholder")}
          className="h-11 flex-1 text-base"
          aria-label={t("placeholder")}
        />
        <Button type="submit" size="lg" className="h-11 px-6 text-base">
          {t("cta")}
        </Button>
      </form>
    </section>
  );
}
