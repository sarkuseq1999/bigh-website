// Copies harvested legacy images into public/ before every build.
// public/original is gitignored; content/harvest/assets is the committed source.
import { cpSync, existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const src = path.join(root, "content", "harvest", "assets");
const dest = path.join(root, "public", "original");

if (!existsSync(src)) {
  console.error("sync-assets: missing content/harvest/assets — run scripts/harvest_bighnow.py first");
  process.exit(1);
}
cpSync(src, dest, { recursive: true });
console.log("sync-assets: content/harvest/assets -> public/original");
