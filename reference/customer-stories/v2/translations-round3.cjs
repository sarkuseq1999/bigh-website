// Adds the September 24 round-3 strings (Still life / Daylight / Showroom) to the five catalogs.
// Run from the repo root: node reference/customer-stories/v2/translations-round3.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  ["Still life", "静物", "정물", "Tĩnh vật", "静物"],
  ["Daylight", "日光", "하루의 빛", "Ánh nắng", "ひかり"],
  ["Showroom", "展示台", "쇼룸", "Phòng trưng bày", "ショールーム"],
  ["Morning", "清晨", "아침", "Buổi sáng", "朝"],
  ["Afternoon", "午后", "오후", "Buổi chiều", "午後"],
  ["Golden hour", "黄昏", "해 질 녘", "Hoàng hôn", "夕暮れ"],
  ["Drag to turn", "拖动即可旋转", "드래그해서 돌려 보세요", "Kéo để xoay", "ドラッグして回せます"],
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
