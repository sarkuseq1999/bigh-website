// Adds the second Glass cell refinement strings (September 24: the free-radical scene redrawn inside
// the glass, antioxidant droplets) to the five catalogs. Draft translations for review.
// Run from the repo root: node reference/science-section/translations-glass2.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  [
    "Too many can damage the cell, starting with the mitochondria",
    "过多时会损伤细胞，首先受损的就是线粒体",
    "너무 많으면 세포가 손상되며, 미토콘드리아가 가장 먼저 손상됩니다",
    "Quá nhiều sẽ gây hại cho tế bào, bắt đầu từ chính ty thể",
    "多すぎると細胞を傷つけ、まずミトコンドリア自身が傷む",
  ],
  [
    "Antioxidants keep them in balance",
    "抗氧化物质让它们保持平衡",
    "항산화 물질이 균형을 지킵니다",
    "Chất chống oxy hóa giữ chúng ở mức cân bằng",
    "抗酸化物質がバランスを保つ",
  ],
  ["Antioxidants", "抗氧化物质", "항산화 물질", "Chất chống oxy hóa", "抗酸化物質"],
];
const path = "src/i18n/copy-keys.json";
const keys = JSON.parse(fs.readFileSync(path, "utf8"));
const locales = ["en", "cns", "kr", "vn", "jp"];
const catalogs = locales.map((l) => JSON.parse(fs.readFileSync("messages/" + l + ".json", "utf8")));
let next = Math.max(...Object.values(keys).map((k) => Number(k.slice(1)))) + 1;
for (const row of entries) {
  const key = keys[row[0]] ?? "m" + next++;
  keys[row[0]] = key;
  row.forEach((value, i) => {
    catalogs[i].Copy[key] = value;
  });
}
fs.writeFileSync(path, JSON.stringify(keys, null, 2) + "\n");
locales.forEach((l, i) => fs.writeFileSync("messages/" + l + ".json", JSON.stringify(catalogs[i], null, 2) + "\n"));
console.log("added", entries.length, "strings; next id m" + next);
