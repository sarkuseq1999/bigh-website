// Adds Green Bee Propolis's ink page strings (October 14, 2026) to the five catalogs. DRAFT
// translation, not native-reviewed: the site's understated voice, no new claims. hken.json stays {}
// (/hken redirects to /cns). Run from the repo root:
//   node reference/ink-pages/propolis/translations-propolis.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  [
    "Inside every capsule, one ingredient.",
    "每粒胶囊，只有一种成分。",
    "캡슐 하나에 성분 하나.",
    "Mỗi viên nang, một thành phần.",
    "1カプセルに、成分はひとつ。",
  ],
  [
    "An old tree where wild bees live, its cracks filling with gold, painted in ink and gold leaf",
    "一棵野蜂栖居的老树，裂缝渐渐被金色填满，以水墨与金箔绘成。",
    "야생 벌이 사는 오래된 나무, 갈라진 틈이 금빛으로 채워지는 모습을 먹과 금박으로 그린 그림.",
    "Một thân cây già nơi đàn ong rừng sinh sống, các vết nứt dần lấp đầy sắc vàng, vẽ bằng mực và lá vàng.",
    "野生のミツバチが棲む古木。その割れ目が金で満たされていく様子を、墨と金箔で描いた絵。",
  ],
  [
    "Pieces of raw green propolis in a small dish, one yellow capsule beside it, painted in watercolour",
    "小碟中的几块天然绿蜂胶，旁边一粒黄色胶囊，水彩绘成。",
    "작은 접시에 담긴 천연 그린 프로폴리스 조각과 그 옆의 노란 캡슐 하나를 수채로 그린 그림.",
    "Vài mẩu keo ong xanh thô trong chiếc đĩa nhỏ, bên cạnh là một viên nang màu vàng, vẽ bằng màu nước.",
    "小皿に入った天然のグリーンプロポリスのかけらと、その横の黄色いカプセルひとつを水彩で描いた絵。",
  ],
  [
    "A sprig of alecrim pressed on a botanist's specimen sheet, painted in ink",
    "压在植物标本纸上的一枝 alecrim，以水墨绘成。",
    "식물 표본지에 눌러 붙인 알레크림 한 가지를 먹으로 그린 그림.",
    "Một nhánh alecrim ép trên tờ tiêu bản thực vật, vẽ bằng mực.",
    "植物標本の台紙に押されたアレクリンの小枝を墨で描いた絵。",
  ],
  [
    "A mug of tea with one gold capsule beside it, painted in ink and watercolour",
    "一杯茶，旁边一粒金色胶囊，以水墨与水彩绘成。",
    "차 한 잔과 그 옆의 금빛 캡슐 하나를 먹과 수채로 그린 그림.",
    "Một cốc trà và một viên nang màu vàng bên cạnh, vẽ bằng mực và màu nước.",
    "お茶の入ったマグと、その横の金色のカプセルひとつを墨と水彩で描いた絵。",
  ],
  [
    "Sprigs of alecrim and fallen golden ipê blossoms painted in watercolour, a bee flying above",
    "水彩绘成的几枝 alecrim 与飘落的金色黄钟木花，上方一只蜜蜂飞过。",
    "수채로 그린 알레크림 가지와 떨어진 황금빛 이페 꽃, 그 위를 나는 벌 한 마리.",
    "Những nhánh alecrim và hoa ipê vàng rơi, vẽ bằng màu nước, một chú ong bay phía trên.",
    "水彩で描いたアレクリンの小枝と散った金色のイペーの花、その上を飛ぶミツバチ一匹。",
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
