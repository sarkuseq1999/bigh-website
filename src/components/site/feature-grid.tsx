import { FlaskConical, Leaf, Users, type LucideIcon } from "lucide-react";
import { useTranslations } from "next-intl";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

type FeatureKey = "science" | "ingredients" | "trusted";

const FEATURES: { key: FeatureKey; Icon: LucideIcon }[] = [
  { key: "science", Icon: FlaskConical },
  { key: "ingredients", Icon: Leaf },
  { key: "trusted", Icon: Users },
];

export function FeatureGrid() {
  const t = useTranslations("Features");

  return (
    <section className="border-foreground/5 bg-card/40 border-y">
      <div className="mx-auto grid max-w-6xl gap-6 px-6 py-20 sm:py-24 md:grid-cols-3">
        {FEATURES.map(({ key, Icon }) => (
          <Card key={key} className="p-6">
            <CardHeader className="px-0">
              <div className="bg-brand-50 text-brand-900 mb-4 flex h-11 w-11 items-center justify-center rounded-lg">
                <Icon className="h-5 w-5" />
              </div>
              <CardTitle className="text-lg">{t(`${key}.title`)}</CardTitle>
            </CardHeader>
            <CardContent className="px-0">
              <CardDescription className="text-[0.95rem] leading-relaxed">
                {t(`${key}.body`)}
              </CardDescription>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}
