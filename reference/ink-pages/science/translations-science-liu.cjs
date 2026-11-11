// Adds the two new strings of the Science page's Dr. Liu part, "the gold he studies" (Mo picked C,
// November 11, 2026), to the five catalogs: the line that says what the gold is, and the painting's
// description. DRAFT translation, not native-reviewed. Keys start at m1231, after About's m1230
// (re-running is safe: a string that already has a key keeps it). hken.json stays {} (/hken
// redirects to /cns). Mitochondria as the catalogs already say it (线粒体 / 미토콘드리아 / ty thể /
// ミトコンドリア), and "In gold" as the opening's caption says it (m1121). Each description names him
// as that catalog does (刘健康博士, Tiến sĩ Jiankang Liu, Dr. Jiankang Liu): the language checks look
// for his name in it.
// Run from the repo root:
//   node reference/ink-pages/science/translations-science-liu.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  [
    "In gold: mitochondria. He has studied them since 1994.",
    "金色的部分是线粒体。他从1994年起一直研究它们。",
    "금색으로 그린 것은 미토콘드리아입니다. 그는 1994년부터 이를 연구해 왔습니다.",
    "Màu vàng là ty thể. Ông đã nghiên cứu chúng từ năm 1994.",
    "金色の部分はミトコンドリア。1994年から研究を続けています。",
  ],
  [
    "Dr. Jiankang Liu, a painted portrait, in front of one large cell painted in pale blue watercolour, its mitochondria slivers of gold",
    "刘健康博士的肖像画，身后是一个用淡蓝色水彩画出的大细胞，线粒体画成细细的金色笔触",
    "Dr. Jiankang Liu의 초상화. 뒤에는 옅은 푸른 담채로 그린 커다란 세포가 있고, 미토콘드리아는 가는 금빛 붓 자국으로 그렸습니다",
    "Tranh chân dung Tiến sĩ Jiankang Liu, phía sau là một tế bào lớn vẽ bằng màu nước xanh nhạt, ty thể là những nét vàng mảnh",
    "Dr. Jiankang Liu の肖像画。背後には淡い青の水彩で描いた大きな細胞があり、ミトコンドリアは細い金色の筆あとで描かれている",
  ],
];
const path = "src/i18n/copy-keys.json";
const keys = JSON.parse(fs.readFileSync(path, "utf8"));
const locales = ["en", "cns", "kr", "vn", "jp"];
const catalogs = locales.map((l) => JSON.parse(fs.readFileSync("messages/" + l + ".json", "utf8")));
const used = new Set(Object.values(keys));
let next = 1231;
const added = [];
for (const row of entries) {
  let key = keys[row[0]];
  if (!key) {
    while (used.has("m" + next)) next++;
    key = "m" + next;
    used.add(key);
    keys[row[0]] = key;
  }
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
