// Adds Nature Calm's ink page strings (October 16, 2026) to the five catalogs. DRAFT translation,
// not native-reviewed: the site's understated voice, no new claims. hken.json stays {} (/hken
// redirects to /cns). Keys start at m780 (the range reserved for this page, m780-m819; other
// product sessions take m700-m739 and m740-m779). Run from the repo root:
//   node reference/ink-pages/nature-calm/translations-nature-calm.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const FIRST_KEY = 780;
const entries = [
  [
    "A still lake at dusk, its gold reflection scattered by wind and then gathered into one line as the water stills, painted in ink and gold leaf",
    "黄昏时分平静的湖面，金色的倒影被风吹散，又随着水面归于平静汇成一道金线，以水墨与金箔绘成。",
    "해 질 녘의 고요한 호수. 바람에 흩어진 금빛 반영이 물이 잔잔해지며 한 줄기로 모이는 모습을 먹과 금박으로 그린 그림.",
    "Mặt hồ tĩnh lặng lúc hoàng hôn, ánh phản chiếu vàng bị gió làm tan rồi tụ lại thành một vệt khi mặt nước lặng, vẽ bằng mực và lá vàng.",
    "夕暮れの静かな湖。風に散った金色の反射が、水面が静まるにつれて一筋に集まる様子を、墨と金箔で描いた絵。",
  ],
  [
    "A long sugar pine cone with many scales and three small beads of gold resin, painted in ink",
    "一枚长长的糖松球果，鳞片繁多，缀着三小滴金色树脂，以水墨绘成。",
    "비늘이 많은 긴 설탕소나무 솔방울과 세 방울의 금빛 송진을 먹으로 그린 그림.",
    "Một quả thông đường dài với nhiều vảy và ba giọt nhựa vàng nhỏ, vẽ bằng mực.",
    "鱗片の多い長いシュガーパインの松ぼっくりと、三粒の小さな金色の樹脂を墨で描いた絵。",
  ],
  [
    "The seven stars of the Big Dipper in gold leaf over one dark ridge, painted in ink",
    "北斗七星以金箔绘于一道深色山脊之上，以水墨绘成。",
    "어두운 능선 위에 금박으로 그린 북두칠성의 일곱 별을 먹으로 그린 그림.",
    "Bảy ngôi sao của chòm Bắc Đẩu bằng lá vàng trên một dải núi sẫm, vẽ bằng mực.",
    "暗い尾根の上に金箔で描いた北斗七星の七つの星を、墨で描いた絵。",
  ],
  [
    "A glass of water and three capsules, the moon's phases above them with the full moon in gold leaf, painted in ink",
    "一杯水与三粒胶囊，上方是月相变化，满月以金箔绘成，以水墨绘成。",
    "물 한 잔과 캡슐 세 알, 그 위로 달의 위상이 이어지고 보름달은 금박으로 그린 먹 그림.",
    "Một ly nước và ba viên nang, phía trên là các pha của mặt trăng với trăng tròn bằng lá vàng, vẽ bằng mực.",
    "水の入ったグラスとカプセル三粒、その上に月の満ち欠け、満月は金箔で、墨で描いた絵。",
  ],
  [
    "Rows of lavender in a California field, painted in watercolour",
    "加州田野中的几排薰衣草，水彩绘成。",
    "캘리포니아 들판의 라벤더 줄기들을 수채로 그린 그림.",
    "Những luống oải hương trên cánh đồng California, vẽ bằng màu nước.",
    "カリフォルニアの畑に並ぶラベンダーの列を水彩で描いた絵。",
  ],
];
const path = "src/i18n/copy-keys.json";
const keys = JSON.parse(fs.readFileSync(path, "utf8"));
const locales = ["en", "cns", "kr", "vn", "jp"];
const catalogs = locales.map((l) => JSON.parse(fs.readFileSync("messages/" + l + ".json", "utf8")));
const taken = new Set(Object.values(keys));
let next = FIRST_KEY;
const added = [];
for (const row of entries) {
  let key = keys[row[0]];
  if (!key) {
    while (taken.has("m" + next)) next++;
    key = "m" + next++;
    taken.add(key);
  }
  keys[row[0]] = key;
  added.push(key + " " + row[0].slice(0, 50));
  catalogs.forEach((catalog, i) => {
    catalog.Copy[key] = row[i];
  });
}
if (next > 820) throw new Error("ran past the reserved range m780-m819");
fs.writeFileSync(path, JSON.stringify(keys, null, 2) + "\n");
locales.forEach((l, i) => fs.writeFileSync("messages/" + l + ".json", JSON.stringify(catalogs[i], null, 2) + "\n"));
console.log(added.join("\n"));
