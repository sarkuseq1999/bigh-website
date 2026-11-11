// Adds the two new strings of the Science page's inside-the-cell opening (November 10, 2026) to
// the five catalogs: the first and the last picture's descriptions. DRAFT translation, not
// native-reviewed. Keys start at m1223, after About's m1200-m1222 (re-running is safe: a string
// that already has a key keeps it). hken.json stays {} (/hken redirects to /cns). Mitochondria as
// the catalogs already say it (线粒体 / 미토콘드리아 / ty thể / ミトコンドリア). The whole cell's and
// the lone walker's descriptions (m1122, m1120) are no longer shown.
// Run from the repo root:
//   node reference/ink-pages/science/translations-science-inside.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  [
    "The inside of one cell painted in pale blue washes: a dark blue nucleus, and its mitochondria as drifting slivers of gold",
    "淡蓝色水彩画出的细胞内部：深蓝色的细胞核，线粒体画成漂浮的细细金色笔触",
    "옅은 푸른 담채로 그린 세포의 안쪽. 짙은 푸른 핵이 있고, 미토콘드리아는 떠다니는 가는 금빛 붓 자국으로 그렸습니다",
    "Bên trong một tế bào, vẽ bằng những lớp màu xanh nhạt: nhân màu xanh đậm, và ty thể là những nét vàng mảnh đang trôi",
    "淡い青の彩色で描いた細胞の内側。濃い青の核があり、ミトコンドリアは漂う細い金色の筆あとで描かれている",
  ],
  [
    "A grandfather and a small child walk hand in hand up a trail through golden California hills, painted in ink and watercolour",
    "水墨淡彩画：祖父和年幼的孩子手牵着手，走在金色加州山丘间的小路上",
    "수묵 담채화: 할아버지와 어린아이가 손을 잡고 금빛 캘리포니아 언덕의 오솔길을 걸어 올라갑니다",
    "Tranh mực và màu nước: một người ông và một em bé nắm tay nhau đi trên lối mòn giữa những ngọn đồi vàng của California",
    "水墨淡彩画：祖父と小さな子どもが手をつなぎ、金色のカリフォルニアの丘の小道を歩いている",
  ],
];
const path = "src/i18n/copy-keys.json";
const keys = JSON.parse(fs.readFileSync(path, "utf8"));
const locales = ["en", "cns", "kr", "vn", "jp"];
const catalogs = locales.map((l) => JSON.parse(fs.readFileSync("messages/" + l + ".json", "utf8")));
const used = new Set(Object.values(keys));
let next = 1223;
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
