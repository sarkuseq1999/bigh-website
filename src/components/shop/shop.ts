// Where BiGH's own shop plugs into the website (Mo, November 16, 2026: "we're gonna start to use
// our own back office and shopping cart", so the old iMatrix cart is not linked anywhere).
// Everything the site needs from the shop lives here, so connecting it is a change to this file
// only: the prices, where Add to cart goes, and where Log in and Sign up go. Until a link is set,
// its button stays a polite placeholder (add-to-cart.tsx, header-utilities.tsx).

/** Retail prices in US dollars, by product page slug. Mo picked the current bighnow.com prices
 *  for launch (November 16, 2026): NuriCell and Nature Calm $80, Advanced OPC Formula $65,
 *  Turmerific $50, Green Bee Propolis $36. A product left out here shows no price. */
const PRICES: Record<string, number> = {
  nuricell: 80,
  "nature-calm": 80,
  "advanced-opc": 65,
  turmerific: 50,
  "green-bee-propolis": 36,
};

/** The new shop's cart, per product. `null` until the shop (bigh-backend) is connected; then
 *  return the product's add-to-cart or product URL in the shop, for example
 *  `https://shop.bighnow.com/cart/add?sku=${slug}`. */
export function checkoutUrl(slug: string): string | null {
  void slug;
  return null;
}

/** Where Log in goes. The back office demo Mo linked on the menu bar; replace it with the new
 *  back office's sign-in page when it is live. */
export const LOGIN_URL: string | null = "https://bigh-vn-demo.vercel.app";

/** Where Sign up goes. `null` keeps the button a quiet placeholder (it promises nothing). */
export const SIGNUP_URL: string | null = null;

export function priceOf(slug: string): number | null {
  return PRICES[slug] ?? null;
}

/** "$80", or "$36.50" when there are cents. Always US dollars: the shop sells in the USA. */
export function formatPrice(amount: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: Number.isInteger(amount) ? 0 : 2,
    maximumFractionDigits: 2,
  }).format(amount);
}
