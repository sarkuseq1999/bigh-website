import sharp from "sharp";
import path from "node:path";
import { fileURLToPath } from "node:url";

const directory = path.dirname(fileURLToPath(import.meta.url));
const enhanced = path.join(directory, "nuricell-enhanced-v1.png");
const original = path.resolve(directory, "../../../public/images/nuricell.png");
const output = path.join(directory, "nuricell-enhanced-transparent.png");
const { width, height } = await sharp(enhanced).metadata();

// Both photographs share the same normalized framing. Reuse the original
// solid silhouette, slightly inset to avoid retaining the studio backdrop.
// Visible enhanced RGB pixels remain untouched. Fully transparent pixels are
// cleared so viewers that ignore alpha do not display the discarded backdrop.
const alpha = await sharp(original)
  .resize(width, height, { fit: "fill" })
  .extractChannel("alpha")
  .erode(2)
  .raw()
  .toBuffer();

const before = await sharp(enhanced).raw().toBuffer();
const rgba = Buffer.alloc(width * height * 4);
for (let pixel = 0; pixel < width * height; pixel++) {
  if (alpha[pixel] > 0) {
    for (let channel = 0; channel < 3; channel++) {
      rgba[pixel * 4 + channel] = before[pixel * 3 + channel];
    }
  }
  rgba[pixel * 4 + 3] = alpha[pixel];
}
await sharp(rgba, { raw: { width, height, channels: 4 } })
  .png()
  .toFile(output);

const after = await sharp(output).raw().toBuffer();
let changedColorPixels = 0;
let transparentPixels = 0;
let opaquePixels = 0;
for (let pixel = 0; pixel < width * height; pixel++) {
  if (after[pixel * 4 + 3] > 0 && [0, 1, 2].some((channel) => before[pixel * 3 + channel] !== after[pixel * 4 + channel])) {
    changedColorPixels++;
  }
  if (after[pixel * 4 + 3] === 0) transparentPixels++;
  if (after[pixel * 4 + 3] === 255) opaquePixels++;
}
const alphaAt = (x, y) => after[(y * width + x) * 4 + 3];
console.log(JSON.stringify({
  output, width, height, changedColorPixels, transparentPixels, opaquePixels,
  whiteCapAlpha: alphaAt(615, 150),
  whiteShoulderAlpha: alphaAt(615, 365),
  whiteBaseAlpha: alphaAt(615, 1170),
  cornerAlpha: alphaAt(0, 0),
}));
if (changedColorPixels !== 0 || alphaAt(615, 150) !== 255 || alphaAt(0, 0) !== 0) {
  throw new Error("Transparent-image verification failed.");
}
