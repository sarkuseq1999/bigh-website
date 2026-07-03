import type { Locale } from "@/i18n/routing";

// Product registry — order mirrors the legacy site's Product menu.
// Localized display names were extracted from each legacy page's own heading
// (content/harvest/<locale>/<slug>.md); missing translations fall back to English,
// exactly as the legacy site did.
export const PRODUCT_SLUGS = [
  "advanced-opc-formula",
  "deer-horn-reishi",
  "green-bee-propolis",
  "heart-q10",
  "nature-calm",
  "nano-detoxifier",
  "nuricell",
  "super-green",
  "turmerific",
  "uber-calcium",
] as const;

export type ProductSlug = (typeof PRODUCT_SLUGS)[number];

const NAMES: Record<ProductSlug, Partial<Record<Locale, string>> & { en: string }> = {
  "advanced-opc-formula": {
    en: "Advanced OPC Formula",
    kr: "어드벤스드 오피씨 포뮬러",
    jp: "アドバンスドＯＰＣフォーミュラ",
    cns: "综合OPC",
    hken: "综合OPC",
    vn: "Công thức OPC cao cấp",
  },
  "deer-horn-reishi": {
    en: "Deer Horn Reishi",
    kr: "녹각영지",
    jp: "鹿角霊芝",
    cns: "鹿角灵芝",
    hken: "鹿角灵芝",
    vn: "Linh Chi Sừng Hươu",
  },
  "green-bee-propolis": {
    en: "Green Bee Propolis",
    kr: "그린비 프로폴리스",
    jp: "グリーンプロポリス",
    cns: "巴西绿蜂胶",
    hken: "巴西绿蜂胶",
    vn: "Keo Ong Xanh",
  },
  "heart-q10": {
    en: "Heart Q10",
    kr: "하트 큐텐",
    jp: "ハートQ10",
    cns: "安心源",
    hken: "安心源",
    vn: "Bổ tim Q10",
  },
  "nature-calm": {
    en: "Nature Calm",
    kr: "네이쳐 캄",
    jp: "ネーチャーカーム",
    cns: "轻松源",
    hken: "轻松源",
    vn: "Thư giãn nguyên",
  },
  "nano-detoxifier": {
    en: "Nano Detoxifier",
    kr: "나노 디톡시파이어",
    jp: "ナノデトキシファイアー",
    cns: "纳米清毒剂",
    hken: "纳米清毒剂",
    vn: "Nano Detoxifier",
  },
  nuricell: {
    en: "NuriCell",
    kr: "누리셀",
    jp: "ニューリセル",
    cns: "细胞源",
    hken: "细胞源",
    vn: "Tế Bào Nguyên",
  },
  "super-green": {
    en: "Super Green",
    kr: "슈퍼 그린",
    jp: "スーパーグリーン",
    cns: "麦绿王",
    hken: "麦绿王",
    vn: "Siêu Xanh",
  },
  turmerific: {
    en: "Turmerific",
    kr: "투메리픽",
    jp: "ターメリフィック",
    cns: "长效优化姜黄素",
    hken: "长效优化姜黄素",
    vn: "Tinh chất curcumin",
  },
  "uber-calcium": {
    en: "Uber Calcium",
    kr: "우버 칼슘",
    jp: "ウバーカルシウム",
    cns: "优步钙",
    hken: "优步钙",
    vn: "Uber Calcium",
  },
};

export function productName(slug: ProductSlug, locale: Locale): string {
  return NAMES[slug][locale] ?? NAMES[slug].en;
}

export function isProductSlug(slug: string): slug is ProductSlug {
  return (PRODUCT_SLUGS as readonly string[]).includes(slug);
}

// Pages grouped under the legacy "About" menu
export const ABOUT_SLUGS = ["about", "organic", "non-gmo", "gluten-free", "vegan"] as const;

// The new-brand family shown on the Golden Hour site — NuriCell the hero,
// then the supporting cast in design-doc order. The other legacy products
// stay reachable by URL but are not part of the new story.
export const GH_PRODUCT_SLUGS: readonly ProductSlug[] = [
  "nuricell",
  "turmerific",
  "advanced-opc-formula",
  "green-bee-propolis",
  "nature-calm",
  "deer-horn-reishi",
] as const;

// Label hue per product — drives each product page's wave-gradient hero,
// mirroring the original site's per-product color theming (NuriCell blue, …).
export const PRODUCT_HUES: Record<ProductSlug, string> = {
  nuricell: "#2d9fd8",
  "advanced-opc-formula": "#c05b52",
  "green-bee-propolis": "#caa63d",
  "heart-q10": "#ef8f3a",
  "nature-calm": "#5cb85f",
  "nano-detoxifier": "#41b0b8",
  "super-green": "#b6444f",
  turmerific: "#e78b2e",
  "uber-calcium": "#3fc3cf",
  "deer-horn-reishi": "#8a5a33",
};
