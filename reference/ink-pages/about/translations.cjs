// Adds the folded-letter About page's new strings (October 6, 2026) to the five catalogs.
// DRAFT translations, not native-reviewed: same understated voice, no new claims. hken.json stays
// {} (/hken redirects to /cns). Run from the repo root:
//   node reference/ink-pages/about/translations.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  [
    "Tree rings in ink. A gold ring marks 2016, when BiGH began; the rings inside it are the years the formula is older.",
    "水墨绘制的树木年轮。一圈金色年轮标记着 BiGH 创立的 2016 年；其内的年轮，是这个配方早于 BiGH 的岁月。",
    "먹으로 그린 나이테. 금빛 나이테 하나가 BiGH가 시작된 2016년을 표시하고, 그 안쪽의 나이테는 포뮬러가 BiGH보다 앞선 세월입니다.",
    "Vân gỗ vẽ bằng mực. Một vòng vàng đánh dấu năm 2016, khi BiGH ra đời; những vòng bên trong là những năm công thức đã có trước đó.",
    "墨で描いた年輪。金の輪は BiGH が始まった2016年を示し、その内側の輪はフォーミュラが BiGH より古い年月です。",
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
