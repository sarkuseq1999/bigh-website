// Adds the description of the About page's new closing painting (November 13, 2026: the tide pool
// with a guide, Mo picked B) to the five catalogs. DRAFT translation, not native-reviewed, in the
// manner of the sequoia's (m1250). The grey glasses' description (m593) stays in the catalogs,
// unused. Keys continue from m1250, the first unused one is taken, so a session adding keys at the
// same time cannot collide. A string that already has a key keeps it and its translations, so
// re-running is safe. hken.json stays {} (/hken redirects to /cns).
// Run from the repo root:
//   node reference/ink-pages/about-closing/translations-closing.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  [
    "An older woman looks into a tide pool on the California coast with a hand lens while a park naturalist points to a sea star, painted in soft watercolour",
    "淡彩水彩画：加州海岸的潮池边，一位年长的女士拿着放大镜往池里看，身旁的公园自然讲解员指着一只海星。",
    "은은한 수채화: 캘리포니아 해안의 조수 웅덩이에서 나이 지긋한 여성이 돋보기로 물속을 들여다보고, 옆에서 공원 자연 해설사가 불가사리를 가리킨다.",
    "Tranh màu nước nhạt: bên một hồ nước triều trên bờ biển California, một phụ nữ lớn tuổi cầm kính lúp nhìn xuống nước, bên cạnh một hướng dẫn viên thiên nhiên của công viên chỉ vào một con sao biển.",
    "淡い水彩画。カリフォルニアの海岸の潮だまりで、年配の女性がルーペで水の中をのぞき、隣で公園のナチュラリストがヒトデを指さしている。",
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
