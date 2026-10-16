// Adds Turmerific's ink page strings (October 16, 2026) to the five catalogs. DRAFT translation,
// not native-reviewed: the site's understated voice, no new claims. hken.json stays {} (/hken
// redirects to /cns). Turmerific's keys are m740 to m779 (docs/ink-product-prompts.md: the other
// product pages take m700-m739 and m780-m819), so new keys start at m740, never at the highest key.
// Run from the repo root:
//   node reference/ink-pages/turmerific/translations-turmerific.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const FIRST = 740;
const LAST = 779;
const entries = [
  [
    "A turmeric root and a slice cut from it, the gold soaking out into the paper, painted in ink and gold leaf",
    "一段姜黄根和从上面切下的一片，金色渐渐渗入纸中，以水墨与金箔绘成。",
    "강황 뿌리와 거기서 잘라 낸 한 조각, 금빛이 종이로 스며 나가는 모습을 먹과 금박으로 그린 그림.",
    "Một củ nghệ và một lát cắt từ củ, sắc vàng thấm dần ra giấy, vẽ bằng mực và lá vàng.",
    "ターメリックの根と、そこから切った一切れ。金色が紙に染み出していく様子を墨と金箔で描いた絵。",
  ],
  [
    "A wooden spoon of golden curcumin powder and two capsules, painted in watercolour",
    "一把盛着金色姜黄素粉末的木勺和两粒胶囊，水彩绘成。",
    "금빛 커큐민 가루를 담은 나무 숟가락과 캡슐 두 개를 수채로 그린 그림.",
    "Một chiếc thìa gỗ đựng bột curcumin vàng óng và hai viên nang, vẽ bằng màu nước.",
    "金色のクルクミンの粉をのせた木のスプーンと、カプセル二つを水彩で描いた絵。",
  ],
  [
    "Reading glasses on an open notebook, a turmeric leaf as a bookmark, painted in ink",
    "摊开的笔记本上放着一副老花镜，一片姜黄叶当作书签，以水墨绘成。",
    "펼친 공책 위의 돋보기안경과 책갈피로 놓인 강황 잎 하나를 먹으로 그린 그림.",
    "Cặp kính đọc sách trên cuốn sổ đang mở, một chiếc lá nghệ làm dấu trang, vẽ bằng mực.",
    "開いたノートの上の老眼鏡と、しおり代わりのターメリックの葉一枚を墨で描いた絵。",
  ],
  [
    "A glass of water and two gold capsules, painted in ink and watercolour",
    "一杯清水和两粒金色胶囊，以水墨与水彩绘成。",
    "물 한 잔과 금빛 캡슐 두 개를 먹과 수채로 그린 그림.",
    "Một cốc nước và hai viên nang màu vàng, vẽ bằng mực và màu nước.",
    "水の入ったグラスと金色のカプセル二つを墨と水彩で描いた絵。",
  ],
  [
    "A turmeric plant in flower painted in watercolour, gold slices of its root at its foot",
    "水彩绘成的一株开花的姜黄，根旁散落着几片金色的根片。",
    "꽃이 핀 강황 한 포기를 수채로 그린 그림, 그 발치에 금빛 뿌리 조각들.",
    "Một cây nghệ đang nở hoa vẽ bằng màu nước, dưới gốc là những lát củ màu vàng.",
    "花を咲かせたターメリックを水彩で描いた絵。根元には金色の根の切り片。",
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
    if (next > LAST) throw new Error("Turmerific's keys m740-m779 are used up");
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
console.log("next free in Turmerific's range: m" + next);
