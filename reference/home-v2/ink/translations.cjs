// Adds the Ink & Gold homepage's new strings (October 2, 2026) to the five catalogs.
// DRAFT translations, not native-reviewed: same understated voice, no new claims; terms follow
// the catalogs (首席科学顾问 / 수석 과학 자문 / Cố vấn Khoa học trưởng / 最高科学顧問, as in m553).
// hken.json stays {} (/hken redirects to /cns). Run from the repo root:
//   node reference/home-v2/ink/translations.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  ["Why cellular health matters", "为什么细胞健康很重要", "세포 건강이 중요한 이유", "Vì sao sức khỏe tế bào quan trọng", "細胞の健康が大切な理由"],
  [
    "A lifetime of asking better questions",
    "一生都在提出更好的问题",
    "더 나은 질문을 던져 온 삶",
    "Một đời đặt ra những câu hỏi tốt hơn",
    "より良い問いを重ねてきた歩み",
  ],
  ["Follow the evidence", "跟随证据", "근거를 따라가 보세요", "Theo dấu bằng chứng", "根拠をたどる"],
  ["Be in good health", "保持健康", "건강하게", "Luôn khỏe mạnh", "健やかに"],
  [
    "Chief Scientific Advisor, BiGH",
    "BiGH 首席科学顾问",
    "BiGH 수석 과학 자문",
    "Cố vấn Khoa học trưởng, BiGH",
    "BiGH 最高科学顧問",
  ],
  ["20+ years", "20 余年", "20년 이상", "Hơn 20 năm", "20年以上"],
  [
    "A mitochondrion, painted in ink, with two gold folds where energy is made",
    "一幅水墨线粒体，其中两道金色褶皱是产生能量的地方",
    "먹으로 그린 미토콘드리아. 에너지가 만들어지는 두 개의 금빛 주름이 보입니다",
    "Một ty thể vẽ bằng mực tàu, với hai nếp gấp vàng là nơi tạo ra năng lượng",
    "墨で描いたミトコンドリア。エネルギーが生まれる二つの金色のひだ",
  ],
  ["Illustrations", "示意图", "일러스트", "Hình minh họa", "イメージ図"],
  ["BiGH products", "BiGH 产品", "BiGH 제품", "Sản phẩm BiGH", "BiGH の製品"],
  ["Choose a story", "选择一个故事", "이야기 선택", "Chọn một câu chuyện", "ストーリーを選ぶ"],
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
