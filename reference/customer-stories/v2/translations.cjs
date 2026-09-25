// Adds the September 24 customer-story design strings to the five catalogs.
// Run from the repo root: node reference/customer-stories/v2/translations.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  ["Portraits", "肖像", "초상화", "Chân dung", "ポートレート"],
  ["Moments", "生活瞬间", "일상의 순간", "Khoảnh khắc", "日常のひとこま"],
  ["Scroll story", "滚动故事", "스크롤 스토리", "Câu chuyện cuộn", "スクロールストーリー"],
  ["Illustrative portrait", "示意肖像画", "일러스트 초상화", "Chân dung minh họa", "イメージ用の肖像画"],
  ["Illustrative video", "示意视频", "연출 영상", "Video minh họa", "イメージ映像"],
  ["Illustrative scene", "示意场景", "연출 장면", "Cảnh minh họa", "イメージシーン"],
  ["Pause videos", "暂停视频", "영상 일시정지", "Tạm dừng video", "動画を一時停止"],
  ["Play videos", "播放视频", "영상 재생", "Phát video", "動画を再生"],
  [
    "Scroll to read each story",
    "向下滚动，逐一阅读每个故事",
    "스크롤하며 이야기를 하나씩 읽어 보세요",
    "Cuộn xuống để đọc từng câu chuyện",
    "スクロールして、ひとつずつ読んでみてください",
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
console.log("Updated " + entries.length + " customer-story strings in five languages.");
