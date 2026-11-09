// Adds the About page's two new chapters (November 9, 2026: the globe and the valley at dawn) and
// the new promise to the five catalogs. DRAFT translation, not native-reviewed: the site's
// understated voice, no new claims. Keys start at m1200, a range of its own, so a session adding
// keys after m1117 at the same time cannot collide. A string that already has a key keeps it and
// its translations ("Turmeric" is m536), so re-running is safe. hken.json stays {} (/hken
// redirects to /cns). The About page's own words: Chinese 您, as its promises say it; "Made in
// California." and "By GMP-certified manufacturers." (m562, m563) keep theirs; supplements as the
// catalogs say them (补充剂 / 보충제 / thực phẩm bổ sung / サプリメント). No place is named.
// Run from the repo root:
//   node reference/ink-pages/about-plants/translations-about-chapters.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  ["Our ingredients", "我们的原料", "우리의 원료", "Nguyên liệu của chúng tôi", "私たちの原料"],
  [
    "Each plant, from where it grows best.",
    "每一种植物，都取自最宜生长之地。",
    "식물마다, 가장 잘 자라는 곳에서.",
    "Mỗi loại cây, từ nơi nó phát triển tốt nhất.",
    "それぞれの植物を、いちばんよく育つ場所から。",
  ],
  [
    "We look around the world for our plants, and bring each one home from the place it grows best.",
    "我们在世界各地寻找植物，把每一种从它长得最好的地方带回家。",
    "우리는 세계 곳곳에서 식물을 찾고, 각 식물을 가장 잘 자라는 곳에서 집으로 가져옵니다.",
    "Chúng tôi tìm kiếm cây trồng khắp thế giới, và mang từng loại về nhà từ nơi nó phát triển tốt nhất.",
    "私たちは世界中で植物を探し、それぞれがいちばんよく育つ場所から持ち帰ります。",
  ],
  ["California", "加州", "캘리포니아", "California", "カリフォルニア"],
  ["where we make them", "我们在这里生产", "우리가 만드는 곳", "nơi chúng tôi sản xuất", "私たちがつくる場所"],
  ["Green propolis", "绿蜂胶", "그린 프로폴리스", "Keo ong xanh", "グリーンプロポリス"],
  [
    "Warm, wild hillsides",
    "温暖的野生山坡",
    "따뜻한 야생의 언덕",
    "Những sườn đồi hoang dã, ấm áp",
    "暖かな野生の丘",
  ],
  ["Hot, rainy fields", "炎热多雨的田野", "덥고 비가 많은 들판", "Những cánh đồng nóng và nhiều mưa", "暑く雨の多い畑"],
  ["Grape seed", "葡萄籽", "포도씨", "Hạt nho", "ブドウ種子"],
  ["Sunny slopes", "阳光充足的山坡", "햇살 가득한 비탈", "Những sườn dốc đầy nắng", "日当たりのよい斜面"],
  ["Pine bark", "松树皮", "소나무 껍질", "Vỏ thông", "松の樹皮"],
  ["Old pine forests", "古老的松林", "오래된 소나무 숲", "Những rừng thông lâu năm", "古い松の森"],
  [
    "A globe painted in ink and watercolour, California facing you. Four plants stand round its edge, and a gold dotted line runs from each over the globe to California.",
    "水墨淡彩画：一个地球，加州朝向您。四种植物立在它的边缘，每一种都有一条金色虚线越过地球通向加州。",
    "수묵 담채화: 캘리포니아가 앞을 향한 지구. 가장자리에 네 가지 식물이 서 있고, 각 식물에서 금빛 점선이 지구를 넘어 캘리포니아로 이어집니다.",
    "Tranh mực và màu nước: một quả địa cầu với California hướng về phía bạn. Bốn loại cây đứng quanh rìa, và từ mỗi cây một đường chấm vàng chạy qua địa cầu đến California.",
    "水墨淡彩画：カリフォルニアがこちらを向いた地球。縁に四つの植物が立ち、それぞれから金色の点線が地球を越えてカリフォルニアへ続きます。",
  ],
  ["Our home", "我们的家园", "우리의 터전", "Quê nhà của chúng tôi", "私たちの拠点"],
  [
    "Proudly made in California.",
    "骄傲地在加州制造。",
    "자랑스럽게 캘리포니아에서 만듭니다.",
    "Tự hào sản xuất tại California.",
    "誇りをもって、カリフォルニアでつくっています。",
  ],
  [
    "Every bottle we sell is made here, by GMP-certified manufacturers.",
    "我们出售的每一瓶产品都在这里生产，由GMP认证厂商制造。",
    "우리가 판매하는 모든 제품은 이곳에서 GMP 인증 제조업체가 만듭니다.",
    "Mỗi lọ chúng tôi bán đều được sản xuất tại đây, bởi các nhà sản xuất đạt chứng nhận GMP.",
    "私たちが販売するすべてのボトルは、ここで GMP 認証を取得した製造元がつくっています。",
  ],
  [
    "Early morning over California’s Central Valley from a golden foothill: rows of fields, some in gold, the snowy Sierra behind",
    "水墨淡彩画：清晨，从金色的山麓望向加州中央谷地：一排排田地，其中几块是金色的，远处是积雪的内华达山脉",
    "수묵 담채화: 금빛 구릉에서 바라본 이른 아침의 캘리포니아 센트럴밸리. 줄지은 밭 몇 곳은 금빛이고, 뒤로 눈 덮인 시에라네바다가 보입니다",
    "Tranh mực và màu nước: sáng sớm trên Thung lũng Trung tâm California nhìn từ một chân đồi vàng, những hàng ruộng với vài thửa ánh vàng, phía sau là dãy Sierra phủ tuyết",
    "水墨淡彩画：金色の丘のふもとから見た、早朝のカリフォルニア・セントラルバレー。並ぶ畑のいくつかは金色で、奥に雪のシエラネバダ",
  ],
  [
    "GMP means Good Manufacturing Practice: the rules for making supplements with care.",
    "GMP 即“良好生产规范”：用心生产补充剂的规则。",
    "GMP는 우수 제조 관리 기준(Good Manufacturing Practice), 곧 보충제를 정성껏 만들기 위한 규칙입니다.",
    "GMP là Thực hành Sản xuất Tốt: những quy tắc để sản xuất thực phẩm bổ sung một cách cẩn thận.",
    "GMP とは適正製造規範（Good Manufacturing Practice）のこと。サプリメントを丁寧につくるためのルールです。",
  ],
  [
    "Every ingredient is checked before it’s used.",
    "每一种原料在使用前都经过检验。",
    "모든 원료는 사용 전에 검사합니다.",
    "Mỗi nguyên liệu đều được kiểm tra trước khi sử dụng.",
    "すべての原料は、使う前に検査します。",
  ],
  [
    "Every batch follows a written recipe.",
    "每一批都按照书面配方生产。",
    "모든 배치는 문서로 정해진 제조법을 따릅니다.",
    "Mỗi mẻ sản xuất đều theo một công thức thành văn.",
    "どのロットも、文書に定めた製法に従ってつくります。",
  ],
  [
    "Every batch is recorded, so it can be traced.",
    "每一批都有记录，可以追溯。",
    "모든 배치는 기록되어 추적할 수 있습니다.",
    "Mỗi mẻ đều được ghi chép lại, để có thể truy xuất.",
    "どのロットも記録され、さかのぼって確かめられます。",
  ],
  ["Honest about the research.", "如实呈现研究。", "연구에 대해 정직하게.", "Trung thực về nghiên cứu.", "研究について、正直に。"],
  [
    "We show you the studies, and say what they don’t prove.",
    "我们向您展示研究，也说明它们不能证明什么。",
    "연구를 보여 드리고, 그 연구가 증명하지 못하는 것도 말씀드립니다.",
    "Chúng tôi cho bạn xem các nghiên cứu, và nói rõ những gì chúng không chứng minh được.",
    "研究をお見せし、それが何を証明していないかもお伝えします。",
  ],
];
const path = "src/i18n/copy-keys.json";
const keys = JSON.parse(fs.readFileSync(path, "utf8"));
const locales = ["en", "cns", "kr", "vn", "jp"];
const catalogs = locales.map((l) => JSON.parse(fs.readFileSync("messages/" + l + ".json", "utf8")));
const used = new Set(Object.values(keys));
let next = 1200;
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
