// Adds NuriCell's ink page strings (October 9, 2026) to the five catalogs. DRAFT translation, not
// native-reviewed: the site's understated voice, no new claims; Dr. Liu named as in m198. hken.json
// stays {} (/hken redirects to /cns). Run from the repo root:
//   node reference/ink-pages/nuricell/translations-nuricell.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  ["Portrait painting", "肖像画", "초상화", "Tranh chân dung", "肖像画"],
  ["The research", "研究", "연구", "Nghiên cứu", "研究"],
  [
    "Show all {count} studies",
    "显示全部{count}项研究",
    "연구 {count}건 모두 보기",
    "Xem tất cả {count} nghiên cứu",
    "{count}件の研究をすべて表示",
  ],
  ["Show fewer studies", "收起研究", "연구 접기", "Thu gọn nghiên cứu", "研究を折りたたむ"],
  // The sum's captions (painted under each numeral, a few characters wide) hold a zero-width space
  // (\u200b) where the word may wrap: with word-break: keep-all on the captions, jp and cns would
  // otherwise have no break at all, and without it they split カプセル / 胶囊 across two lines.
  ["capsules a day", "每日\u200b胶囊数", "하루 캡슐 수", "viên mỗi ngày", "1日の\u200bカプセル数"],
  ["days", "天", "일", "ngày", "日"],
  [
    "capsules in each bottle",
    "每瓶\u200b胶囊数",
    "한 병의 캡슐 수",
    "viên mỗi lọ",
    "1本の\u200bカプセル数",
  ],
  [
    "{perDay} capsules a day for {days} days: {total} capsules in each bottle.",
    "每日{perDay}粒，共{days}天：每瓶{total}粒。",
    "하루 {perDay}캡슐씩 {days}일: 한 병에 {total}캡슐.",
    "Mỗi ngày {perDay} viên trong {days} ngày: mỗi lọ {total} viên.",
    "1日{perDay}カプセルを{days}日間：1本に{total}カプセル。",
  ],
  [
    "A paper lantern whose light comes on, painted in ink and gold leaf",
    "一盏纸灯笼亮起，以水墨与金箔绘成。",
    "불이 켜지는 종이 초롱을 먹과 금박으로 그린 그림.",
    "Chiếc đèn lồng giấy sáng lên, vẽ bằng mực và lá vàng.",
    "明かりがともる紙の提灯を墨と金箔で描いた絵。",
  ],
  [
    "An opened capsule with its four powders in a row and gold sparks rising, painted in ink",
    "打开的胶囊，四堆粉末排成一行，金色火花升起，以水墨绘成。",
    "열린 캡슐과 나란히 놓인 네 가지 가루, 피어오르는 금빛 불꽃을 먹으로 그린 그림.",
    "Viên nang mở ra, bốn đống bột xếp thành hàng và những tia lửa vàng bay lên, vẽ bằng mực.",
    "開いたカプセルと一列に並ぶ4種類の粉末、立ちのぼる金色の火花を墨で描いた絵。",
  ],
  [
    "Seven books as stepping stones across a calm stream, painted in ink",
    "七本书如踏脚石横跨平静的溪流，以水墨绘成。",
    "잔잔한 시냇물을 건너는 징검돌이 된 일곱 권의 책을 먹으로 그린 그림.",
    "Bảy cuốn sách như những phiến đá lót lối băng qua dòng suối êm, vẽ bằng mực.",
    "静かな小川に渡した飛び石のような7冊の本を墨で描いた絵。",
  ],
  [
    "A portrait painting of Dr. Jiankang Liu in ink and colour",
    "刘健康博士的水墨设色肖像画。",
    "Dr. Jiankang Liu의 먹과 채색 초상화.",
    "Tranh chân dung Dr. Jiankang Liu vẽ bằng mực và màu.",
    "Dr. Jiankang Liu の墨と彩色による肖像画。",
  ],
  [
    "A soft-boiled egg with a gold yolk beside a dish of three capsules, painted in ink",
    "金色蛋黄的半熟蛋，旁边一小碟三粒胶囊，以水墨绘成。",
    "금빛 노른자의 반숙 달걀과 캡슐 세 개가 담긴 접시를 먹으로 그린 그림.",
    "Quả trứng lòng đào với lòng đỏ vàng óng bên đĩa ba viên nang, vẽ bằng mực.",
    "金色の黄身の半熟卵と、3つのカプセルをのせた小皿を墨で描いた絵。",
  ],
  // The ingredient table's visually hidden header (Task 5).
  ["Per serving", "每份含量", "1회 섭취량", "Mỗi khẩu phần", "1回分あたり"],
  ["Ingredient", "成分", "성분", "Thành phần", "成分"],
  ["About it", "说明", "설명", "Giới thiệu", "説明"],
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
