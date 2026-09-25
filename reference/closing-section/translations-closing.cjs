// Adds the closing block strings ("Start with your cells.", September 24) to the five catalogs.
// Draft translations for review. "Discover NuriCell" already exists.
// Run from the repo root: node reference/closing-section/translations-closing.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  [
    "Start with your cells.",
    "从你的细胞开始。",
    "당신의 세포에서 시작하세요.",
    "Hãy bắt đầu từ tế bào của bạn.",
    "あなたの細胞から始めよう。",
  ],
  [
    "Discover NuriCell, our flagship formula focused on mitochondrial health, or explore the full BiGH range.",
    "了解我们专注于线粒体健康的旗舰配方 NuriCell，或探索 BiGH 的全部产品。",
    "미토콘드리아 건강에 초점을 맞춘 대표 제품 NuriCell을 만나 보거나, BiGH의 전체 제품을 둘러보세요.",
    "Khám phá NuriCell, công thức chủ lực của chúng tôi tập trung vào sức khỏe ty thể, hoặc xem toàn bộ các sản phẩm BiGH.",
    "ミトコンドリアの健康に焦点を当てた主力製品 NuriCell を知る。または BiGH の全製品を見る。",
  ],
  ["Explore all products", "查看全部产品", "전체 제품 보기", "Xem tất cả sản phẩm", "すべての製品を見る"],
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
console.log("Updated " + entries.length + " closing strings in five languages; next id m" + next);
