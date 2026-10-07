// Adds About B, "The album" (October 7, 2026): the descriptions of its five paintings, to the five
// catalogs (About C, "The circle", reuses the seedling and the sequoia). DRAFT translations, not
// native-reviewed: same understated voice, no new claims. hken.json stays {} (/hken redirects to
// /cns). Run from the repo root:
//   node reference/ink-pages/about-bc/translations-b.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  [
    "An old open book, painted in ink, with a gold ribbon bookmark",
    "一本水墨绘制的旧书，夹着金色丝带书签。",
    "금색 리본 책갈피가 끼워진, 먹으로 그린 오래된 펼친 책.",
    "Một cuốn sách cũ mở ra, vẽ bằng mực, với dải ruy băng đánh dấu màu vàng.",
    "金色のしおり紐をはさんだ、墨で描いた古い本。",
  ],
  [
    "An oak seedling growing from an acorn, painted in ink; a gold acorn lies among its roots",
    "水墨绘制的橡树幼苗从橡子中长出，根间有一颗金色的橡子。",
    "도토리에서 자라난 참나무 새싹을 먹으로 그린 그림. 뿌리 사이에 금빛 도토리가 있습니다.",
    "Cây sồi non mọc lên từ quả sồi, vẽ bằng mực; một quả sồi vàng nằm giữa rễ cây.",
    "どんぐりから芽吹いたオークの若木を墨で描いた絵。根のあいだに金色のどんぐりがあります。",
  ],
  [
    "A scientist's desk in ink: a brush on its rest, a microscope and a stack of books",
    "水墨绘制的科学家书桌：笔架上的毛笔、显微镜和一摞书。",
    "먹으로 그린 과학자의 책상: 붓걸이의 붓, 현미경, 쌓인 책.",
    "Bàn làm việc của nhà khoa học vẽ bằng mực: cây bút lông trên giá, kính hiển vi và chồng sách.",
    "墨で描いた研究者の机。筆置きの筆、顕微鏡、積まれた本。",
  ],
  [
    "An ancient giant sequoia rising from mist beside a young sequoia, painted in ink",
    "水墨绘制的古老巨杉从雾中升起，旁边是一棵年轻的巨杉。",
    "안개 속에서 솟은 오래된 자이언트 세쿼이아와 그 옆의 어린 세쿼이아를 먹으로 그린 그림.",
    "Cây cự sam cổ thụ vươn lên giữa sương mù bên cạnh một cây cự sam non, vẽ bằng mực.",
    "霧の中にそびえる古いジャイアントセコイアと、その隣の若いセコイアを墨で描いた絵。",
  ],
  [
    "A desk lamp casting gold light onto an open journal, painted in ink",
    "水墨绘制的台灯，在打开的笔记本上投下金色的光。",
    "펼친 노트 위로 금빛을 비추는 탁상 램프를 먹으로 그린 그림.",
    "Chiếc đèn bàn chiếu ánh vàng lên cuốn sổ đang mở, vẽ bằng mực.",
    "開いたノートに金色の光を落とすデスクランプを墨で描いた絵。",
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
