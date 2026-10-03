# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary: people in midlife (about 40–65) who want to stay sharp, energetic and active, and are
deciding whether to try NuriCell or another BiGH product (confirmed by Mo, October 2, 2026).
They read before they buy, care who stands behind a formula, and many are older readers. The site
serves five languages: English, Simplified Chinese, Korean, Vietnamese and Japanese.

## Product Purpose

BiGH ("Be in Good Health") is a dietary-supplement company. Mission: support cellular health and
mental energy, helping people live life to the fullest. Working tagline: "Stay sharp. Live fully."
The homepage introduces the brand, explains cellular health simply, leads to the flagship
NuriCell, and shows the wider range, the scientists, customer stories, the science explainers and
the research behind the thinking. Success: a visitor understands what BiGH is and why to trust it,
and goes on to a product page.

## Positioning

Real scientists, not marketing (confirmed by Mo, October 2, 2026). BiGH's formulas come from
Dr. Jiankang Liu, an internationally recognized researcher in mitochondrial biology and aging
(Chief Scientific Advisor, BiGH; 280+ scientific papers reported by his university; postdoctoral
work at UC Berkeley with Bruce Ames; elected to the European Academy of Sciences and Arts in 2025).
The visitor should believe within ten seconds that real cell scientists stand behind these
formulas. The science is cell-level: mitochondria, the cell's energy makers.

## Operating Context

A marketing homepage in a Next.js site with product pages (/products/<slug>), a Science page and
an About page. Visitors arrive curious and compare brands; ordering is not connected yet in this
preview.

## Capabilities and Constraints

- Products: NuriCell (flagship), Green Bee Propolis, Advanced OPC Formula, Turmerific, Nature Calm.
- Credits: NuriCell "Formulated by Dr. Jiankang Liu." Nature Calm: Dr. Liu and Dr. Iris Wang.
  Advanced OPC: Dr. Iris Wang. Others: "Developed under the direction and guidance of Dr. Jiankang
  Liu and Dr. Iris Wang." Dr. Iris Wang appears as text only, never a photograph.
- Ingredient research does not establish the effects of a finished BiGH product; claims stay
  measured ("support", "focuses on"), never cures or guarantees.
- Purchases, accounts and question submissions are not available in this preview.

## Brand Commitments

- **The words stay:** the current homepage copy is accepted and every concept keeps it
  (`src/components/home-v2/content.ts`).
- **Real assets only:** the approved product bottle photos (`public/images/products/*.png`) and
  Dr. Liu's real photo (`public/images/jiankang-liu.jpg`, 512×768) are used as they are; bottles
  and labels are never generated or faked.
- Logo: `public/images/brand/bigh-logo-*.png` (black wordmark with a green leaf).
- Typeface: Switzer, site-wide (Mo's pick, September 28, 2026; loaded from Fontshare in the locale
  layout, never committed to the public repo). Labels and navigation stay large for older readers.
- Voice: understated, concrete, no hype; "sharpness" over vague wording.

## Evidence on Hand

- Dr. Liu's biography facts above, with sources in BRAND-CHEATSHEET.md.
- 36 checked research sources (`src/components/home/research-data.ts`).
- No real customer testimonials yet: the three stories are fictional samples and must stay
  labeled "Fictional sample". No customer photos. Do not invent reviews, ratings, customer counts,
  prices or clinical results for finished products.

## Product Principles

1. Science you can trust: lead with the real scientists and real research, stated honestly.
2. Clear for everyone: explain cell science simply, one idea at a time.
3. Calm confidence: understated, never hype.
4. Honest labels: illustrations, samples and research limits are always marked.
