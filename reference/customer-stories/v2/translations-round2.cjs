// Adds the September 24 picture-choice strings (Hands / Objects / Words) to the five catalogs.
// Run from the repo root: node reference/customer-stories/v2/translations-round2.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  ["Hands", "双手", "손", "Đôi tay", "手元"],
  ["Objects", "日常物件", "일상의 물건", "Đồ vật", "身近なもの"],
  ["Words", "文字", "글", "Lời kể", "ことば"],
  ["Illustrative photo", "示意图片", "연출 사진", "Ảnh minh họa", "イメージ写真"],
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
console.log("Updated " + entries.length + " customer-story strings in five languages.");
