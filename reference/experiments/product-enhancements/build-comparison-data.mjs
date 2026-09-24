import sharp from "sharp";
import fs from "node:fs/promises";

const products = [
  { id: "nuricell", name: "NuriCell", note: "Earlier enhancement. Fine circuit artwork and small label geometry differ from the original." },
  { id: "green-bee-propolis", name: "Green Bee Propolis", note: "Review the honeycomb artwork and curved side text. The source wording “Strengths Body Defenses” is retained." },
  { id: "advanced-opc", name: "Advanced OPC Formula", note: "The fruit artwork and small curved text differ from the original. Review these details and the side-panel printing closely." },
  { id: "turmerific", name: "Turmerific", note: "The turmeric illustration and small benefit badges have changed slightly. Review these details and the side-panel printing closely." },
  { id: "nature-calm", name: "Nature Calm", note: "Review the connected-circle artwork, meditation symbol, and small side-panel printing." },
];

async function inspect(url) {
  const filename = `public${url}`;
  const metadata = await sharp(filename).metadata();
  if (metadata.format !== "png" || !metadata.hasAlpha) throw new Error(`PNG with alpha required: ${filename}`);
  const { data, info } = await sharp(filename).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  let left = info.width, top = info.height, right = 0, bottom = 0;
  let transparent = 0, opaque = 0;
  for (let y = 0; y < info.height; y++) {
    for (let x = 0; x < info.width; x++) {
      const alpha = data[(y * info.width + x) * 4 + 3];
      // Ignore almost invisible exterior alpha when aligning the display frames.
      // This only measures the files; their pixels and alpha remain unchanged.
      if (alpha > 8) { left = Math.min(left, x); top = Math.min(top, y); right = Math.max(right, x + 1); bottom = Math.max(bottom, y + 1); }
      if (alpha === 0) transparent++;
      if (alpha === 255) opaque++;
    }
  }
  const centerX = Math.round((left + right) / 2);
  const sample = (fraction) => data[(Math.floor(top + (bottom - top) * fraction) * info.width + centerX) * 4 + 3];
  const samples = { cap: sample(.1), shoulder: sample(.29), label: sample(.6), base: sample(.96) };
  if (!transparent || samples.cap < 250 || samples.label < 250) throw new Error(`Invalid cutout: ${filename}`);
  console.log(JSON.stringify({ filename, width: info.width, height: info.height, bbox: [left, top, right, bottom], transparent, opaque, samples }));
  return { url, width: info.width, height: info.height, bbox: [left, top, right, bottom] };
}

for (const product of products) {
  product.original = await inspect(`/images/${product.id}.png`);
  product.enhanced = await inspect(`/experiments/${product.id}-enhanced-transparent.png`);
}
await fs.writeFile("public/experiments/product-comparison.json", JSON.stringify(products, null, 2) + "\n");
console.log("Wrote five comparison pairs.");
