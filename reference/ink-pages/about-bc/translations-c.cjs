// Adds About C, "The circle" (October 7, 2026): the description of its one new painting, the reading
// glasses, to the five catalogs (its seedling and sequoia are translated by translations-b.cjs, run
// first). DRAFT translation, not native-reviewed: same understated voice, no new claims. hken.json
// stays {} (/hken redirects to /cns). Run from the repo root:
//   node reference/ink-pages/about-bc/translations-c.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  [
    "Reading glasses resting on an open notebook, painted in ink",
    "水墨绘制的老花镜，放在打开的笔记本上。",
    "펼친 노트 위에 놓인 돋보기안경을 먹으로 그린 그림.",
    "Cặp kính đọc sách đặt trên cuốn sổ đang mở, vẽ bằng mực.",
    "開いたノートの上に置かれた老眼鏡を墨で描いた絵。",
  ],
];
const path = "src/i18n/copy-keys.json";
const keys = JSON.parse(fs.readFileSync(path, "utf8"));
const locales = ["en", "cns", "kr", "vn", "jp"];
const catalogs = locales.map((l) => JSON.parse(fs.readFileSync("messages/" + l + ".json", "utf8")));
let next = Math.max(...Object.values(keys).map((k) => Number(k.slice(1)))) + 1;
const added = [];
for (const row of entries) {
  const key = keys[row[0]] ?? "m" + next++;
  keys[row[0]] = key;
  added.push(key + " " + row[0]);
  row.forEach((value, i) => {
    catalogs[i].Copy[key] = value;
  });
}
fs.writeFileSync(path, JSON.stringify(keys, null, 2) + "\n");
locales.forEach((l, i) =>
  fs.writeFileSync("messages/" + l + ".json", JSON.stringify(catalogs[i], null, 2) + "\n"),
);
console.log(added.join("\n"));
console.log("next id m" + next);
