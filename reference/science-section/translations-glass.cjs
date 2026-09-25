// Adds the Glass cell refinement strings (topic tabs and topic labels, September 24) to the five
// catalogs. Draft translations for review.
// Run from the repo root: node reference/science-section/translations-glass.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  ["Topics", "主题", "주제", "Chủ đề", "トピック"],
  ["Mitochondria", "线粒体", "미토콘드리아", "Ty thể", "ミトコンドリア"],
  ["Free radicals", "自由基", "자유 라디칼", "Gốc tự do", "フリーラジカル"],
  ["Aging cells", "细胞老化", "세포의 노화", "Tế bào lão hóa", "細胞の老化"],
  [
    "Inner folds: where energy is made",
    "内部褶皱：产生能量的地方",
    "안쪽 주름: 에너지가 만들어지는 곳",
    "Nếp gấp bên trong: nơi tạo ra năng lượng",
    "内側のひだ：エネルギーがつくられる場所",
  ],
  ["Natural defenses", "天然防御", "자연 방어 체계", "Hệ phòng vệ tự nhiên", "もともと備わる防御"],
  ["Age", "年龄", "나이", "Tuổi", "年齢"],
  [
    "Illustration, not a measurement",
    "示意图，并非测量数据",
    "측정값이 아닌 그림 설명입니다",
    "Hình minh họa, không phải số đo",
    "測定値ではなくイメージです",
  ],
  ["Making energy also makes a few free radicals", "制造能量的同时，也会产生少量自由基", "에너지를 만들 때 자유 라디칼도 조금 생깁니다", "Khi tạo năng lượng, tế bào cũng sinh ra một ít gốc tự do", "エネルギーをつくるとき、フリーラジカルも少しできる"],
  ["Too many can damage parts of the cell", "过多时可能损伤细胞的组成部分", "너무 많으면 세포의 여러 부분이 손상될 수 있습니다", "Quá nhiều có thể làm tổn thương các bộ phận của tế bào", "多すぎると細胞の一部を傷つけることがある"],
  ["Natural defenses keep them in balance", "天然防御让它们保持平衡", "자연 방어 체계가 균형을 지킵니다", "Hệ phòng vệ tự nhiên giữ chúng ở mức cân bằng", "もともと備わる防御がバランスを保つ"],
  ["More antioxidants are not automatically better", "抗氧化剂更多并不一定更好", "항산화제가 많다고 반드시 좋은 것은 아닙니다", "Nhiều chất chống oxy hóa hơn không có nghĩa là tốt hơn", "抗酸化物質は多ければよいとは限らない"],
  ["Drag to change the age", "拖动以改变年龄", "드래그해서 나이를 바꿔 보세요", "Kéo để thay đổi độ tuổi", "ドラッグして年齢を変えられます"],
  ["Mitochondria are one of the main sources of free radicals", "线粒体是自由基的主要来源之一", "미토콘드리아는 자유 라디칼의 주요 발생원 중 하나입니다", "Ty thể là một trong những nguồn chính tạo ra gốc tự do", "ミトコンドリアはフリーラジカルの主な発生源のひとつ"],
  ["Your body also makes its own antioxidants", "身体自己也会产生抗氧化物质", "우리 몸은 스스로 항산화 물질도 만듭니다", "Cơ thể cũng tự tạo ra chất chống oxy hóa", "体は自分でも抗酸化物質をつくっている"],
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
console.log("Updated " + entries.length + " Glass cell strings in five languages.");
