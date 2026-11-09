// Adds the Science page's zoom-opening strings (November 9, 2026) to the five catalogs. DRAFT
// translation, not native-reviewed: the site's understated voice, no new claims. Keys start at
// m1120, after round 3's m1100-m1117 (re-running is safe: a string that already has a key keeps
// it). hken.json stays {} (/hken redirects to /cns). Mitochondria as the catalogs already say it
// (线粒体 / 미토콘드리아 / ty thể / ミトコンドリア). Round 3's desk and town strings (m1102, m1111,
// m1112) are no longer shown.
// Run from the repo root:
//   node reference/ink-pages/science/translations-science-zoom.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  [
    "A walker with a sun hat and a stick on a trail through golden California hills and oaks, painted in ink and watercolour",
    "水墨淡彩画：一位戴着遮阳帽、拄着手杖的行人，走在金色加州山丘和橡树间的小路上",
    "수묵 담채화: 햇빛 가리는 모자를 쓰고 지팡이를 짚은 사람이 금빛 캘리포니아 언덕과 참나무 사이 오솔길을 걷고 있습니다",
    "Tranh mực và màu nước: một người đội mũ rộng vành, chống gậy, đi trên lối mòn giữa những ngọn đồi vàng và cây sồi California",
    "水墨淡彩画：日よけ帽をかぶり杖を持った人が、金色のカリフォルニアの丘とオークの間の小道を歩いている",
  ],
  [
    "In gold: its mitochondria, where the cell makes most of its energy.",
    "金色的部分是线粒体，细胞的大部分能量在这里产生。",
    "금색으로 그린 것은 미토콘드리아입니다. 세포는 에너지의 대부분을 여기서 만듭니다.",
    "Màu vàng là ty thể, nơi tế bào tạo ra phần lớn năng lượng của mình.",
    "金色の部分はミトコンドリア。細胞はエネルギーの大部分をここでつくります。",
  ],
  [
    "One cell painted in pale washes, its mitochondria as slivers of gold round a dark blue nucleus",
    "淡彩画出的一个细胞：深蓝色的细胞核周围，线粒体画成细细的金色笔触",
    "옅은 담채로 그린 세포 하나. 짙은 푸른 핵 둘레에 미토콘드리아를 가는 금빛 붓 자국으로 그렸습니다",
    "Một tế bào vẽ bằng những lớp màu nhạt, ty thể là những nét vàng mảnh quanh nhân màu xanh đậm",
    "淡い彩色で描いた一つの細胞。濃い青の核のまわりに、ミトコンドリアが細い金色の筆あとで描かれている",
  ],
];
const path = "src/i18n/copy-keys.json";
const keys = JSON.parse(fs.readFileSync(path, "utf8"));
const locales = ["en", "cns", "kr", "vn", "jp"];
const catalogs = locales.map((l) => JSON.parse(fs.readFileSync("messages/" + l + ".json", "utf8")));
const used = new Set(Object.values(keys));
let next = 1120;
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
