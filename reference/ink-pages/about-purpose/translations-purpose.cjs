// Adds the description of the About page's new purpose painting (November 10, 2026: the oak on a
// sunny afternoon, Mo picked A) to the five catalogs. DRAFT translation, not native-reviewed, in
// the manner of the old oak's description (m900, which stays in the catalogs, unused). Keys start
// at m1230, a range of its own, so a session adding keys at the same time cannot collide. A string
// that already has a key keeps it and its translations, so re-running is safe. hken.json stays {}
// (/hken redirects to /cns).
// Run from the repo root:
//   node reference/ink-pages/about-purpose/translations-purpose.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  [
    "A valley oak on a sunny afternoon, painted in watercolour: a child on its rope swing, a grandmother pushing, a dog watching, a picnic in the grass; under the ground, gold leaf lies among its roots",
    "水彩绘制的一棵大橡树，阳光明媚的午后：孩子坐在秋千上，祖母在身后轻推，小狗在一旁看着，草地上摆着野餐；地面之下，金箔静静躺在树根之间。",
    "수채화로 그린 화창한 오후의 커다란 참나무. 그네를 타는 아이와 뒤에서 밀어 주는 할머니, 지켜보는 강아지, 풀밭 위의 소풍 자리. 땅 아래 뿌리 사이에는 금박이 놓여 있다.",
    "Cây sồi lớn trong một buổi chiều nắng, vẽ bằng màu nước: em bé trên chiếc xích đu, người bà đứng sau đẩy, chú chó ngồi nhìn, bữa dã ngoại trên cỏ; dưới mặt đất, một mảng vàng lá nằm giữa những rễ cây.",
    "水彩で描いた、晴れた午後の大きなオークの木。ぶらんこに乗る子ども、後ろから押すおばあさん、見守る犬、草の上のピクニック。地面の下、根のあいだに金箔がある。",
  ],
];
const path = "src/i18n/copy-keys.json";
const keys = JSON.parse(fs.readFileSync(path, "utf8"));
const locales = ["en", "cns", "kr", "vn", "jp"];
const catalogs = locales.map((l) => JSON.parse(fs.readFileSync("messages/" + l + ".json", "utf8")));
const used = new Set(Object.values(keys));
let next = 1230;
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
