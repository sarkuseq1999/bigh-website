// Adds NuriCell chapter 5's new strings (Dr. Liu in the view west, Mo picked A2, October 26, 2026)
// to the five catalogs. DRAFT translation, not native-reviewed: the site's understated voice, no new
// claims; Dr. Liu named as the catalogs already name him (刘博士 / Liu 박사 / Tiến sĩ Liu / Liu 博士
// in sentences; the Latin name in the description, as m-key "A portrait painting of Dr. Jiankang
// Liu..."), the nutrients and Berkeley as in the Science page's entries. Only these rows: running
// translations-nuricell.cjs again would rewrite its older rows. Run from the repo root:
//   node reference/ink-pages/nuricell/translations-liu-berkeley.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  [
    "At UC Berkeley, he studied two of NuriCell’s nutrients together.",
    "在加州大学伯克利分校，他把 NuriCell 中的两种营养素放在一起研究。",
    "캘리포니아대학교 버클리에서 그는 NuriCell의 두 가지 영양소를 함께 연구했습니다.",
    "Tại Đại học California, Berkeley, ông nghiên cứu cùng lúc hai dưỡng chất có trong NuriCell.",
    "カリフォルニア大学バークレー校で、彼は NuriCell の2つの栄養素を組み合わせて研究しました。",
  ],
  [
    "His study from Bruce Ames’s laboratory, published in 2002, gave acetyl-L-carnitine and alpha-lipoic acid to older animals. Both are in NuriCell, which he formulated.",
    "他在布鲁斯·艾姆斯（Bruce Ames）实验室完成的研究于2002年发表，让老龄动物摄入乙酰左旋肉碱和α-硫辛酸。这两种成分都在他配制的 NuriCell 中。",
    "브루스 에임스(Bruce Ames) 연구실에서 나와 2002년에 발표된 그의 연구는 나이 든 동물에게 아세틸 L-카르니틴과 알파리포산을 먹였습니다. 둘 다 그가 만든 NuriCell에 들어 있습니다.",
    "Nghiên cứu của ông tại phòng thí nghiệm của Bruce Ames, công bố năm 2002, cho động vật lớn tuổi dùng acetyl-L-carnitine và axit alpha-lipoic. Cả hai đều có trong NuriCell, công thức do ông xây dựng.",
    "ブルース・エイムズ（Bruce Ames）の研究室から2002年に発表された彼の研究では、老齢の動物にアセチルL-カルニチンとα-リポ酸を与えました。どちらも彼が処方した NuriCell に含まれています。",
  ],
  [
    "An animal study, not a test of NuriCell.",
    "这是一项动物研究，并非对 NuriCell 的测试。",
    "동물 연구이며, NuriCell을 시험한 것이 아닙니다.",
    "Đây là nghiên cứu trên động vật, không phải thử nghiệm NuriCell.",
    "動物を対象とした研究で、NuriCell を試験したものではありません。",
  ],
  [
    "A portrait painting of Dr. Jiankang Liu on a hill above San Francisco Bay, the Golden Gate in the fog, painted in ink and colour",
    "刘健康博士站在旧金山湾上方山坡上的肖像画，远处金门大桥隐没在雾中，以水墨设色绘成。",
    "샌프란시스코만이 내려다보이는 언덕 위의 Dr. Jiankang Liu와 안개 속 금문교를 먹과 채색으로 그린 초상화.",
    "Tranh chân dung Dr. Jiankang Liu trên ngọn đồi nhìn xuống vịnh San Francisco, cầu Cổng Vàng trong sương, vẽ bằng mực và màu.",
    "サンフランシスコ湾を見下ろす丘に立つ Dr. Jiankang Liu と、霧の中のゴールデンゲートブリッジを墨と彩色で描いた肖像画。",
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
