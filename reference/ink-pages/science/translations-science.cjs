// Adds the Science ink page's new strings (October 14, 2026) to the five catalogs. DRAFT
// translation, not native-reviewed: the site's understated voice, no new claims. Keys start at
// m650 (the Propolis session adds keys from m612). hken.json stays {} (/hken redirects to /cns).
// Dr. Liu is named as the catalogs already name him: 刘健康博士 in Chinese (cns.json), "Dr. Jiankang
// Liu" in Japanese, Korean and Vietnamese (m198).
// Run from the repo root:
//   node reference/ink-pages/science/translations-science.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  ["The formulas", "配方", "포뮬러", "Các công thức", "処方"],
  ["Source", "来源", "출처", "Nguồn", "出典"],
  [
    "Keep scrolling: the scroll unrolls",
    "继续向下滚动：画卷徐徐展开",
    "계속 스크롤하세요: 두루마리가 펼쳐집니다",
    "Tiếp tục cuộn: bức tranh cuộn sẽ mở ra",
    "スクロールを続けると、絵巻が広がります",
  ],
  [
    "Scroll sideways to see the whole painting",
    "左右滚动可查看整幅画",
    "옆으로 스크롤하면 그림 전체를 볼 수 있습니다",
    "Cuộn ngang để xem toàn bộ bức tranh",
    "横にスクロールすると絵の全体が見られます",
  ],
  [
    "A long ink painting of Dr. Liu’s path: Okayama Castle, the ocean, the bell tower at Berkeley, Salzburg, and California hills under a gold sun",
    "一幅描绘刘健康博士求索之路的水墨长卷：冈山城、大海、伯克利的钟楼、萨尔茨堡，以及金色太阳下的加州山丘",
    "Dr. Jiankang Liu의 여정을 그린 긴 수묵화: 오카야마성, 바다, 버클리의 종탑, 잘츠부르크, 그리고 금빛 해 아래 캘리포니아 언덕",
    "Bức tranh thủy mặc dài về hành trình của Dr. Jiankang Liu: thành Okayama, đại dương, tháp chuông ở Berkeley, Salzburg và những ngọn đồi California dưới mặt trời vàng",
    "Dr. Jiankang Liu の歩みを描いた長い水墨画：岡山城、海、バークレーの時計塔、ザルツブルク、金色の太陽の下のカリフォルニアの丘",
  ],
  ["Read the study", "阅读研究", "연구 보기", "Đọc nghiên cứu", "研究を読む"],
  [
    "A shelf of rolled scrolls painted in ink; three lie pulled forward",
    "水墨画：书架上摆满卷轴，其中三卷被抽出放在前面",
    "먹으로 그린 두루마리 선반. 세 개가 앞으로 꺼내져 있습니다",
    "Kệ những cuộn giấy vẽ bằng mực; ba cuộn được kéo ra phía trước",
    "巻物の並ぶ棚の水墨画。三本が手前に引き出されています",
  ],
  [
    "Three small ink paintings: an oil lamp with a gold flame, three balanced stones, and California poppies",
    "三幅小水墨画：一盏燃着金色火焰的油灯、三块叠放平衡的石头、加州罂粟花",
    "작은 수묵화 세 점: 금빛 불꽃의 기름등잔, 균형 잡힌 돌 세 개, 캘리포니아 양귀비",
    "Ba bức tranh mực nhỏ: ngọn đèn dầu với ngọn lửa vàng, ba hòn đá cân bằng và hoa anh túc California",
    "三つの小さな水墨画：金色の炎の油灯、積み重ねた三つの石、カリフォルニアポピー",
  ],
  [
    "An oil lamp with a gold flame, painted in ink",
    "水墨油灯，金色火焰",
    "금빛 불꽃의 기름등잔을 먹으로 그린 그림",
    "Ngọn đèn dầu với ngọn lửa vàng, vẽ bằng mực",
    "金色の炎の油灯の水墨画",
  ],
  [
    "Three balanced stones, painted in ink",
    "水墨画：三块叠放平衡的石头",
    "균형 잡힌 돌 세 개를 먹으로 그린 그림",
    "Ba hòn đá cân bằng, vẽ bằng mực",
    "積み重ねた三つの石の水墨画",
  ],
  [
    "California poppies, painted in ink",
    "水墨加州罂粟花",
    "캘리포니아 양귀비를 먹으로 그린 그림",
    "Hoa anh túc California, vẽ bằng mực",
    "カリフォルニアポピーの水墨画",
  ],
  [
    "Two mugs on a low wooden table, steam rising, painted in ink",
    "水墨画：矮木桌上两只冒着热气的马克杯",
    "낮은 나무 탁자 위 김이 오르는 머그잔 두 개를 먹으로 그린 그림",
    "Hai chiếc cốc bốc hơi trên chiếc bàn gỗ thấp, vẽ bằng mực",
    "低い木の机に湯気の立つマグカップが二つ、水墨画",
  ],
];
const path = "src/i18n/copy-keys.json";
const keys = JSON.parse(fs.readFileSync(path, "utf8"));
const locales = ["en", "cns", "kr", "vn", "jp"];
const catalogs = locales.map((l) => JSON.parse(fs.readFileSync("messages/" + l + ".json", "utf8")));
let next = Math.max(650, Math.max(...Object.values(keys).map((k) => Number(k.slice(1)))) + 1);
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
