// Adds Advanced OPC Formula's ink page strings (October 16, 2026) to the five catalogs, from key
// m700 (Mo reserved m700-m739 for this page; Turmerific has m740-m779, Nature Calm m780-m819).
// DRAFT translation, not native-reviewed: the site's understated voice, no new claims. hken.json
// stays {} (/hken redirects to /cns). The heading "Inside every capsule, {count} ingredients." is
// English in every language today (as NuriCell's "four"), so the count word "thirteen" is not
// added here. Run from the repo root:
//   node reference/ink-pages/opc/translations-opc.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const FIRST = 700;
const LAST = 739;
const entries = [
  [
    "A bunch of grapes on the vine, lit from inside with gold leaf, painted in ink",
    "藤上的一串葡萄，自内而外被金箔点亮，以水墨绘成。",
    "덩굴에 달린 포도 한 송이가 안에서부터 금박으로 빛나는 모습을 먹으로 그린 그림.",
    "Một chùm nho trên giàn, được lá vàng thắp sáng từ bên trong, vẽ bằng mực.",
    "蔓になった一房のぶどうが金箔で内側から灯るように輝く様子を、墨で描いた絵。",
  ],
  [
    "Grapes, pine bark, bilberries, tea leaves, an orange slice and a marigold, painted in ink",
    "葡萄、松树皮、越橘、茶叶、一片橙子和一朵万寿菊，以水墨绘成。",
    "포도, 소나무 껍질, 빌베리, 찻잎, 오렌지 한 조각과 메리골드 한 송이를 먹으로 그린 그림.",
    "Nho, vỏ thông, việt quất đen, lá trà, một lát cam và một bông cúc vạn thọ, vẽ bằng mực.",
    "ぶどう、松の樹皮、ビルベリー、茶葉、オレンジの輪切り、マリーゴールドを墨で描いた絵。",
  ],
  [
    "A magnifying glass over a few grape seeds and a sliver of pine bark, painted in ink",
    "一枚放大镜置于几粒葡萄籽和一小片松树皮之上，以水墨绘成。",
    "포도씨 몇 알과 소나무 껍질 한 조각 위에 놓인 돋보기를 먹으로 그린 그림.",
    "Một chiếc kính lúp đặt trên vài hạt nho và một mảnh vỏ thông, vẽ bằng mực.",
    "数粒のぶどうの種と松の樹皮のかけらの上に置かれた虫めがねを、墨で描いた絵。",
  ],
  [
    "A stone mortar and pestle with a few marigold petals beside it, painted in ink",
    "一只石臼与杵，旁边几片万寿菊花瓣，以水墨绘成。",
    "돌절구와 절굿공이, 그 옆의 메리골드 꽃잎 몇 장을 먹으로 그린 그림.",
    "Một chiếc cối đá cùng chày, bên cạnh là vài cánh hoa cúc vạn thọ, vẽ bằng mực.",
    "石の乳鉢と乳棒、その横のマリーゴールドの花びら数枚を墨で描いた絵。",
  ],
  [
    "An empty plate with the knife and fork laid together, a glass of water and two capsules, painted in ink",
    "一只空盘，刀叉并放其上，旁边一杯水和两粒胶囊，以水墨绘成。",
    "나이프와 포크를 나란히 올려 둔 빈 접시, 물 한 잔과 캡슐 두 알을 먹으로 그린 그림.",
    "Một chiếc đĩa trống với dao và nĩa đặt cạnh nhau, một ly nước và hai viên nang, vẽ bằng mực.",
    "ナイフとフォークを揃えて置いた空の皿、水の入ったグラス、カプセル2つを墨で描いた絵。",
  ],
  [
    "Grapevine leaves and a bunch of grapes painted in ink and watercolour",
    "葡萄藤叶与一串葡萄，以水墨与水彩绘成。",
    "포도 덩굴잎과 포도 한 송이를 먹과 수채로 그린 그림.",
    "Lá nho và một chùm nho, vẽ bằng mực và màu nước.",
    "ぶどうの葉と一房のぶどうを墨と水彩で描いた絵。",
  ],
];
const path = "src/i18n/copy-keys.json";
const keys = JSON.parse(fs.readFileSync(path, "utf8"));
const locales = ["en", "cns", "kr", "vn", "jp"];
const catalogs = locales.map((l) => JSON.parse(fs.readFileSync("messages/" + l + ".json", "utf8")));
const used = new Set(Object.values(keys));
let next = FIRST;
const added = [];
for (const row of entries) {
  let key = keys[row[0]];
  if (!key) {
    while (used.has("m" + next)) next++;
    if (next > LAST) throw new Error("out of reserved keys (m" + FIRST + "-m" + LAST + ")");
    key = "m" + next++;
    used.add(key);
  }
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
console.log("next free key m" + next);
