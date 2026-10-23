// Switzer, the brand face, is served from this site's own /fonts (Mo, October 23, 2026): Fontshare's
// stylesheet kept dropping the browser's connection, and the page then fell back to another face.
// Its licence (ITF Free Font License 2.0, fontshare.com/licenses/itf-ffl) allows self-hosting on
// our own servers but not sharing the files through a public repository, and this repository is
// public. So the official files are fetched from Fontshare before every build and dev run, into
// public/fonts/switzer/ (git-ignored), byte for byte as Fontshare serves them (only the file names
// are ours). Never commit them, and never subset or convert them: the licence forbids both.
//
// If a file cannot be fetched the build stops, so a deployment never ships without Switzer.

import { mkdir, readFile, rename, writeFile } from "node:fs/promises";
import path from "node:path";

const DIR = path.join(process.cwd(), "public", "fonts", "switzer");

// The variable fonts (weights 100-900) behind api.fontshare.com/v2/css?f[]=switzer@1,2.
const FILES = [
  {
    name: "switzer-variable-v1.woff2",
    url: "https://cdn.fontshare.com/wf/HJHZ26OECMTXRH7JXPFC7EVIHDSLT2RA/LJRNLR7WCPF3PY3SZ7B2LHNUTQMFNCHL/4MCJYGQDIOOXHWSIIB2OYNDBEALJSOGN.woff2",
  },
  {
    name: "switzer-variable-italic-v1.woff2",
    url: "https://cdn.fontshare.com/wf/KDSQNRHYYJCWSLSNMQTKJOY7QNC2IBLM/HGYBIGJ4X7DYUETLTGW4BIVO3FCWLJUR/AFY5UJBPUVSDM77Q42DSHPT5JUNR7N4Y.woff2",
  },
];

const ATTEMPTS = 5;

/** A real WOFF2 file: its signature, and more than a stub's size. */
const isFont = (bytes) =>
  bytes.length > 10_000 && bytes.subarray(0, 4).toString("latin1") === "wOF2";

async function have(file) {
  try {
    return isFont(await readFile(path.join(DIR, file.name)));
  } catch {
    return false;
  }
}

async function download(file) {
  let reason = "";
  for (let attempt = 1; attempt <= ATTEMPTS; attempt++) {
    try {
      const response = await fetch(file.url, { signal: AbortSignal.timeout(20_000) });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const bytes = Buffer.from(await response.arrayBuffer());
      if (!isFont(bytes)) throw new Error(`not a WOFF2 file (${bytes.length} bytes)`);
      const target = path.join(DIR, file.name);
      await writeFile(`${target}.part`, bytes);
      await rename(`${target}.part`, target);
      return bytes.length;
    } catch (error) {
      reason = error instanceof Error ? error.message : String(error);
      if (attempt < ATTEMPTS)
        await new Promise((done) => setTimeout(done, 1000 * 2 ** (attempt - 1)));
    }
  }
  throw new Error(`Switzer: could not fetch ${file.name} from Fontshare (${reason})`);
}

await mkdir(DIR, { recursive: true });
for (const file of FILES) {
  if (await have(file)) continue;
  const size = await download(file);
  console.log(`Switzer: fetched ${file.name} (${Math.round(size / 1024)} KB)`);
}
