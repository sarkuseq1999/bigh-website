import { SITE_URL } from "./seo";

// Structured data for search engines (schema.org JSON-LD), November 16, 2026, for launch: who BiGH
// is and how to reach it (homepage), and each product with its price (product pages). Only facts
// the site already states; no ratings or reviews (BiGH has none on the site to cite).

export const ORGANIZATION = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "BiGH",
  legalName: "BiGH Corporation",
  slogan: "Be in Good Health",
  url: SITE_URL,
  logo: `${SITE_URL}/images/brand/bigh-logo-black-green.png`,
  foundingDate: "2016",
  address: {
    "@type": "PostalAddress",
    streetAddress: "2200 E Route 66, Suite 103",
    addressLocality: "Glendora",
    addressRegion: "CA",
    postalCode: "91740",
    addressCountry: "US",
  },
  contactPoint: {
    "@type": "ContactPoint",
    contactType: "customer service",
    telephone: "+1-800-919-2089",
    email: "support@bighnow.com",
    areaServed: "US",
    availableLanguage: ["English", "Chinese", "Korean", "Vietnamese", "Japanese"],
  },
};

export function productLd({
  name,
  description,
  image,
  path,
  price,
}: {
  name: string;
  description: string;
  image: string;
  path: string;
  price: number | null;
}) {
  return {
    "@context": "https://schema.org",
    "@type": "Product",
    name,
    description,
    image: `${SITE_URL}${image}`,
    url: `${SITE_URL}${path}`,
    brand: { "@type": "Brand", name: "BiGH" },
    ...(price !== null
      ? {
          offers: {
            "@type": "Offer",
            price: price.toFixed(2),
            priceCurrency: "USD",
            url: `${SITE_URL}${path}`,
          },
        }
      : {}),
  };
}

/** One JSON-LD block. `<` is escaped so the data can never close the script early. */
export function JsonLd({ data }: { data: object }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data).replace(/</g, "\u003c") }}
    />
  );
}
