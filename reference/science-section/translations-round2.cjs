// Adds the round-2 science-section strings (Glass cell, Kitchen table, Picture words) to the five
// catalogs. Draft translations for review. Sentences with photos inside are split around each photo.
// Run from the repo root: node reference/science-section/translations-round2.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  ["Glass cell", "玻璃细胞", "유리 세포", "Tế bào thủy tinh", "ガラスの細胞"],
  ["Kitchen table", "厨房餐桌", "부엌 식탁", "Bàn bếp", "キッチンテーブル"],
  ["Picture words", "图文句子", "그림 문장", "Chữ và hình", "写真入りの言葉"],
  ["Energy", "能量", "에너지", "Năng lượng", "エネルギー"],
  ["Balance", "平衡", "균형", "Cân bằng", "バランス"],
  ["Time", "时间", "시간", "Thời gian", "時間"],
  ["Chapters", "章节", "챕터", "Các phần", "チャプター"],
  ["Inside most of your cells", "存在于你大多数的细胞中", "우리 몸 대부분의 세포 안에", "Có trong hầu hết các tế bào của bạn", "体のほとんどの細胞の中に"],
  ["Turn food into usable energy", "把食物变成可用的能量", "음식을 쓸 수 있는 에너지로 바꿉니다", "Biến thức ăn thành năng lượng sử dụng được", "食べ物を使えるエネルギーに変える"],
  ["A small part with a big job", "体积虽小，作用很大", "작지만 큰 역할", "Nhỏ bé nhưng việc lớn", "小さくても大きな役目"],
  ["Many processes change with age", "许多过程会随年龄变化", "나이가 들며 많은 과정이 달라집니다", "Nhiều quá trình thay đổi theo tuổi tác", "年齢とともに多くの仕組みが変わる"],
  ["Mitochondria are one part of the story", "线粒体只是其中一部分", "미토콘드리아는 그중 한 부분입니다", "Ty thể chỉ là một phần của câu chuyện", "ミトコンドリアはその一部"],
  ["No single ingredient explains it all", "没有任何单一成分能解释一切", "한 가지 성분이 모든 것을 설명하지는 않습니다", "Không một thành phần nào giải thích được tất cả", "一つの成分ですべては説明できない"],
  ["One ring a year", "一年一圈", "1년에 나이테 하나", "Mỗi năm một vòng", "1年に1本の年輪"],
  ["Your cells run on tiny", "你的细胞靠微小的", "세포는 작은", "Tế bào của bạn vận hành nhờ những", "細胞は、小さな"],
  ["power plants.", "发电厂运转。", "발전소로 움직입니다.", "nhà máy điện tí hon.", "発電所で動いています。"],
  ["A cut apple", "切开的苹果", "자른 사과는", "Táo cắt đôi", "切ったりんごは"],
  ["browns in the air.", "在空气中会变褐。", "공기에 닿으면 갈색으로 변합니다.", "sẽ bị thâm khi gặp không khí.", "空気にふれると茶色くなります。"],
  ["A squeeze of lemon", "挤一点柠檬汁", "레몬즙을 조금 뿌리면", "Vắt một chút chanh", "レモン汁を少しかけると"],
  ["slows it down.", "就能减缓这个过程。", "그 속도가 느려집니다.", "sẽ làm chậm lại.", "それがゆっくりになります。"],
  ["Like the rings of a tree,", "就像树木的年轮，", "나무의 나이테처럼", "Như những vòng gỗ của cây,", "木の年輪のように、"],
  [
    "your cells change with time.",
    "细胞也会随时间变化。",
    "세포도 시간이 흐르며 변합니다.",
    "tế bào của bạn cũng thay đổi theo thời gian.",
    "細胞も時間とともに変わっていきます。",
  ],
];
const path = "src/i18n/copy-keys.json";
const keys = JSON.parse(fs.readFileSync(path, "utf8"));
const locales = ["en", "cns", "kr", "vn", "jp"];
const catalogs = locales.map((l) => JSON.parse(fs.readFileSync("messages/" + l + ".json", "utf8")));
let next = Math.max(...Object.values(keys).map((k) => Number(k.slice(1)))) + 1;
for (const row of entries) {
  const key = keys[row[0]] ?? "m" + next++;
  keys[row[0]] = key;
  row.forEach((value, i) => {
    catalogs[i].Copy[key] = value;
  });
}
fs.writeFileSync(path, JSON.stringify(keys, null, 2) + "\n");
locales.forEach((l, i) => fs.writeFileSync("messages/" + l + ".json", JSON.stringify(catalogs[i], null, 2) + "\n"));
console.log("Updated " + entries.length + " round-2 science strings in five languages.");
