// Adds the description of the About page's new experience painting (November 11, 2026: the giant
// sequoia repainted with soft colour, Mo picked 3) to the five catalogs. DRAFT translation, not
// native-reviewed, in the manner of the ink sequoia's description (m591, which stays in the
// catalogs, unused). Keys start at m1250, a range of its own, so a session adding keys at the same
// time cannot collide. A string that already has a key keeps it and its translations, so
// re-running is safe. hken.json stays {} (/hken redirects to /cns).
// Run from the repo root:
//   node reference/ink-pages/about-experience/translations-experience.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  [
    "An ancient giant sequoia rising from mist beside a young sequoia, painted in soft watercolour, a patch of gold leaf on its trunk",
    "淡彩水彩绘制的古老巨杉从雾中升起，旁边是一棵年轻的巨杉；树干上贴着一小片金箔。",
    "안개 속에서 솟은 오래된 자이언트 세쿼이아와 그 옆의 어린 세쿼이아를 은은한 수채화로 그린 그림. 줄기에 금박 한 조각이 붙어 있다.",
    "Cây cự sam cổ thụ vươn lên giữa sương mù bên cạnh một cây cự sam non, vẽ bằng màu nước nhạt; trên thân cây có một mảng vàng lá.",
    "霧の中にそびえる古いジャイアントセコイアと、その隣の若いセコイアを淡い水彩で描いた絵。幹に金箔がひとひら。",
  ],
];
const path = "src/i18n/copy-keys.json";
const keys = JSON.parse(fs.readFileSync(path, "utf8"));
const locales = ["en", "cns", "kr", "vn", "jp"];
const catalogs = locales.map((l) => JSON.parse(fs.readFileSync("messages/" + l + ".json", "utf8")));
const used = new Set(Object.values(keys));
let next = 1250;
const added = [];
for (const row of entries) {
  if (keys[row[0]]) {
    added.push(keys[row[0]] + " (kept) " + row[0]);
    continue;
  }
  while (used.has("m" + next)) next++;
  const key = "m" + next;
  used.add(key);
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
