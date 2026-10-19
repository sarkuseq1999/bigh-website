// Adds the description of About C's "Our purpose" oak (Mo, October 19, 2026; it replaced the oak
// seedling, whose m589 stays in the catalogs unused) to the five catalogs. DRAFT translation, not
// native-reviewed: same understated voice, no new claims. Its key is m900, clear of the ranges other
// pages reserve (m700-m819) so a page built in parallel cannot take the same id. hken.json stays {}
// (/hken redirects to /cns). Run from the repo root:
//   node reference/ink-pages/about-bc/translations-oak.cjs
// Row order: [key, en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  [
    "m900",
    "A great valley oak with a rope swing, painted in ink; below the ground, a gold light glows among its roots",
    "水墨绘制的一棵大橡树，枝上挂着秋千；地面之下，金色的光在树根之间闪亮。",
    "먹으로 그린 커다란 참나무와 가지에 매단 그네. 땅 아래 뿌리 사이에서 금빛이 빛난다.",
    "Cây sồi lớn có chiếc xích đu, vẽ bằng mực; dưới mặt đất, ánh vàng tỏa sáng giữa những rễ cây.",
    "墨で描いた大きなオークの木と枝のぶらんこ。地面の下、根のあいだに金色の光が灯る。",
  ],
];
const path = "src/i18n/copy-keys.json";
const keys = JSON.parse(fs.readFileSync(path, "utf8"));
const locales = ["en", "cns", "kr", "vn", "jp"];
const catalogs = locales.map((l) => JSON.parse(fs.readFileSync("messages/" + l + ".json", "utf8")));
for (const [key, ...row] of entries) {
  const taken = Object.entries(keys).find(([text, k]) => k === key && text !== row[0]);
  if (taken) throw new Error(key + " is already used for: " + taken[0]);
  keys[row[0]] = key;
  row.forEach((value, i) => {
    catalogs[i].Copy[key] = value;
  });
  console.log(key + " " + row[0]);
}
fs.writeFileSync(path, JSON.stringify(keys, null, 2) + "\n");
locales.forEach((l, i) =>
  fs.writeFileSync("messages/" + l + ".json", JSON.stringify(catalogs[i], null, 2) + "\n"),
);
