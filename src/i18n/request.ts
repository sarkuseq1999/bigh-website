import { getRequestConfig } from "next-intl/server";
import { hasLocale } from "next-intl";
import { routing } from "./routing";

type Messages = Record<string, unknown>;

// English is the fallback for every untranslated key. The merge must be
// deep: a locale file that translates only part of a namespace (e.g. the
// clone's `Home` keys but not the new `Home.hero`) still inherits the
// missing nested keys from English instead of dropping them.
function deepMerge(base: Messages, override: Messages): Messages {
  const out: Messages = { ...base };
  for (const [key, value] of Object.entries(override)) {
    const baseValue = out[key];
    if (
      value !== null &&
      typeof value === "object" &&
      !Array.isArray(value) &&
      baseValue !== null &&
      typeof baseValue === "object" &&
      !Array.isArray(baseValue)
    ) {
      out[key] = deepMerge(baseValue as Messages, value as Messages);
    } else {
      out[key] = value;
    }
  }
  return out;
}

export default getRequestConfig(async ({ requestLocale }) => {
  const requested = await requestLocale;
  const locale = hasLocale(routing.locales, requested) ? requested : routing.defaultLocale;

  const en = (await import("../../messages/en.json")).default as Messages;
  const localeMessages =
    locale === "en" ? en : ((await import(`../../messages/${locale}.json`)).default as Messages);

  return {
    locale,
    messages: (locale === "en" ? en : deepMerge(en, localeMessages)) as never,
  };
});
