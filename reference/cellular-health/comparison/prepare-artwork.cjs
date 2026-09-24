const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const sharp = require('sharp');

async function main() {
  const root = path.resolve(__dirname, '../../..');
  const manifest = process.argv[2] || 'artwork.json';
  const {records} = JSON.parse(await fs.readFile(path.join(__dirname, manifest), 'utf8'));
  for (const record of records) {
    const png = path.join(root, record.savedPng);
    const webp = path.join(root, record.servedImage);
    await fs.mkdir(path.dirname(webp), {recursive: true});
    await fs.copyFile(record.generatedSource, png);
    const original = await fs.readFile(record.generatedSource);
    const saved = await fs.readFile(png);
    if (!original.equals(saved)) throw new Error(`Copy mismatch: ${png}`);
    const info = await sharp(png).webp({quality: 88, effort: 6}).toFile(webp);
    const hash = crypto.createHash('sha256').update(saved).digest('hex');
    console.log(JSON.stringify({design: record.n, width: info.width, height: info.height, bytes: info.size, sourceSha256: hash, webp: record.servedImage}));
  }
}
main().catch(error => { console.error(error); process.exit(1); });
