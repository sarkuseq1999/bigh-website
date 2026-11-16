import { LegalRoute, legalMetadata } from "@/components/legal/legal-route";

type Params = Promise<{ locale: string }>;

export function generateMetadata({ params }: { params: Params }) {
  return legalMetadata(params, "returns");
}

export default function Page({ params }: { params: Params }) {
  return <LegalRoute params={params} slug="returns" />;
}
