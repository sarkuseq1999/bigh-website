// Adds the September 24 "Make sense of the science." strings to the five catalogs.
// The section's headline, introduction, article titles, previews and button are Mo's accepted
// English copy (September 21); the translations and the design-specific lines are drafts.
// Run from the repo root: node reference/science-section/translations.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  ["Make sense of the science.", "读懂科学。", "과학, 쉽게 이해하기.", "Hiểu khoa học thật dễ dàng.", "科学を、わかりやすく。"],
  [
    "Explore cellular health, mental energy, and healthy aging—with explanations that make the science easier to understand.",
    "探索细胞健康、脑力活力与健康老龄化——用通俗的解释，让科学更容易理解。",
    "세포 건강, 정신적 활력, 건강한 노화를 살펴보세요. 과학을 더 쉽게 이해할 수 있도록 풀어서 설명합니다.",
    "Khám phá sức khỏe tế bào, năng lượng tinh thần và lão hóa khỏe mạnh — với những lời giải thích giúp khoa học trở nên dễ hiểu hơn.",
    "細胞の健康、思考の活力、健やかな加齢について。科学をもっとわかりやすくする解説とともにご紹介します。",
  ],
  ["Explore the science", "探索科学", "과학 살펴보기", "Khám phá khoa học", "科学を探る"],
  [
    "What are mitochondria—and why do they matter?",
    "什么是线粒体？它们为什么重要？",
    "미토콘드리아란 무엇이며, 왜 중요할까요?",
    "Ty thể là gì — và vì sao chúng quan trọng?",
    "ミトコンドリアとは？なぜ大切なの？",
  ],
  [
    "A simple guide to your cells’ tiny power plants, their role in everyday energy, and what mitochondrial health means.",
    "简单了解细胞里的小小发电厂：它们在日常能量中的作用，以及线粒体健康的含义。",
    "세포 속 작은 발전소를 쉽게 안내합니다. 일상의 에너지에서 하는 역할과 미토콘드리아 건강의 의미를 알아봅니다.",
    "Hướng dẫn đơn giản về những nhà máy điện tí hon trong tế bào, vai trò của chúng đối với năng lượng hằng ngày và ý nghĩa của sức khỏe ty thể.",
    "細胞の中の小さな発電所をやさしく解説。毎日のエネルギーでの役割と、ミトコンドリアの健康が意味することを紹介します。",
  ],
  [
    "What are free radicals—and how do antioxidants help?",
    "什么是自由基？抗氧化剂如何发挥作用？",
    "자유 라디칼이란 무엇이며, 항산화제는 어떻게 도울까요?",
    "Gốc tự do là gì — và chất chống oxy hóa giúp ích như thế nào?",
    "フリーラジカルとは？抗酸化物質はどう役立つの？",
  ],
  [
    "A simple explanation of free radicals, the damage they can cause, and your cells’ natural defenses.",
    "简单解释自由基、它们可能造成的损伤，以及细胞的天然防御。",
    "자유 라디칼과 그로 인한 손상, 그리고 세포가 스스로를 지키는 방어 체계를 쉽게 설명합니다.",
    "Giải thích đơn giản về gốc tự do, những tổn thương chúng có thể gây ra và hệ phòng vệ tự nhiên của tế bào.",
    "フリーラジカルと、それが引き起こしうるダメージ、そして細胞にもともと備わる防御の仕組みをやさしく解説します。",
  ],
  [
    "What happens to your cells as you age?",
    "随着年龄增长，细胞会发生什么变化？",
    "나이가 들면 세포에는 어떤 변화가 생길까요?",
    "Điều gì xảy ra với tế bào khi bạn có tuổi?",
    "年齢とともに、細胞には何が起こるの？",
  ],
  [
    "A closer look at how cells change over time and what researchers are learning about healthy aging.",
    "深入了解细胞如何随时间变化，以及研究人员对健康老龄化的新认识。",
    "세포가 시간에 따라 어떻게 변하는지, 연구자들이 건강한 노화에 대해 새롭게 알아가는 내용을 자세히 살펴봅니다.",
    "Tìm hiểu kỹ hơn cách tế bào thay đổi theo thời gian và những gì các nhà nghiên cứu đang khám phá về lão hóa khỏe mạnh.",
    "細胞が時間とともにどう変わるのか、そして健やかな加齢について研究者が明らかにしつつあることを詳しく見ていきます。",
  ],
  ["Read a quick explainer", "阅读简短解说", "짧은 설명 읽기", "Đọc phần giải thích ngắn", "かんたんな解説を読む"],
  [
    "Science section design choices",
    "科学板块设计选项",
    "과학 섹션 디자인 선택",
    "Lựa chọn thiết kế phần khoa học",
    "科学セクションのデザイン選択",
  ],
  ["Kitchen science", "厨房里的科学", "부엌 속 과학", "Khoa học trong bếp", "キッチンの科学"],
  ["Myth or fact", "是事实还是误区", "사실일까, 오해일까", "Lầm tưởng hay sự thật", "誤解？事実？"],
  ["Chat", "聊天", "채팅", "Trò chuyện", "チャット"],
  [
    "Cells need power, like a bulb. Mitochondria help make it.",
    "细胞和灯泡一样需要能量。线粒体帮助产生能量。",
    "전구처럼 세포에도 에너지가 필요합니다. 미토콘드리아가 그 에너지를 만드는 것을 돕습니다.",
    "Như bóng đèn, tế bào cũng cần năng lượng. Ty thể giúp tạo ra năng lượng đó.",
    "電球と同じように、細胞にもエネルギーが必要です。それをつくる手助けをするのがミトコンドリアです。",
  ],
  [
    "Air browns a cut apple. Lemon juice slows it down. Cells have defenses, too.",
    "切开的苹果在空气中会变褐，柠檬汁能减缓这个过程。细胞也有自己的防御。",
    "자른 사과는 공기에 닿으면 갈색으로 변합니다. 레몬즙은 이를 늦춰 줍니다. 세포에도 방어 체계가 있습니다.",
    "Táo cắt ra để ngoài không khí sẽ bị thâm. Nước chanh làm chậm quá trình này. Tế bào cũng có cơ chế phòng vệ.",
    "切ったりんごは空気にふれると茶色くなります。レモン汁はそれをゆるやかにします。細胞にも守る仕組みがあります。",
  ],
  [
    "A tree adds a ring each year. Cells change with time, too.",
    "树木每年增加一圈年轮。细胞也会随时间变化。",
    "나무는 해마다 나이테를 하나씩 더합니다. 세포도 시간이 흐르며 변합니다.",
    "Mỗi năm cây thêm một vòng gỗ. Tế bào cũng thay đổi theo thời gian.",
    "木は一年ごとに年輪を一つ重ねます。細胞も時間とともに変わっていきます。",
  ],
  ["Air only", "只接触空气", "공기만", "Chỉ để ngoài không khí", "空気だけ"],
  ["With lemon juice", "加了柠檬汁", "레몬즙을 뿌린 것", "Có nước chanh", "レモン汁あり"],
  [
    "Myth or fact? Tap your answer to flip the card.",
    "是事实还是误区？点选答案，翻开卡片。",
    "사실일까요, 오해일까요? 답을 누르면 카드가 뒤집힙니다.",
    "Lầm tưởng hay sự thật? Chạm vào câu trả lời để lật thẻ.",
    "事実？それとも誤解？答えをタップしてカードをめくりましょう。",
  ],
  [
    "Mitochondria are found in most of your cells.",
    "你身体的大多数细胞里都有线粒体。",
    "미토콘드리아는 우리 몸 대부분의 세포에 있습니다.",
    "Hầu hết các tế bào của bạn đều có ty thể.",
    "ミトコンドリアは、体のほとんどの細胞にある。",
  ],
  [
    "More antioxidants always mean better health.",
    "抗氧化剂越多，就一定越健康。",
    "항산화제는 많을수록 무조건 건강에 좋습니다.",
    "Càng nhiều chất chống oxy hóa thì càng tốt cho sức khỏe.",
    "抗酸化物質は、多ければ多いほど健康によい。",
  ],
  [
    "Healthy aging comes down to one thing.",
    "健康老龄化只取决于一件事。",
    "건강한 노화는 단 한 가지로 결정됩니다.",
    "Lão hóa khỏe mạnh chỉ phụ thuộc vào một điều duy nhất.",
    "健やかな加齢は、たった一つのことで決まる。",
  ],
  ["Myth", "误区", "오해", "Lầm tưởng", "誤解"],
  ["Fact", "事实", "사실", "Sự thật", "事実"],
  ["Myth.", "误区。", "오해입니다.", "Lầm tưởng.", "誤解です。"],
  ["Fact.", "事实。", "사실입니다.", "Sự thật.", "事実です。"],
  ["You got it.", "答对了。", "정답입니다.", "Bạn đã đúng.", "正解です。"],
  ["Not quite.", "不太对。", "아쉽네요.", "Chưa đúng lắm.", "ちょっと違います。"],
  [
    "You got {score} of 3 right.",
    "3 题中你答对了 {score} 题。",
    "3문제 중 {score}문제를 맞혔습니다.",
    "Bạn trả lời đúng {score}/3 câu.",
    "3問中 {score}問 正解しました。",
  ],
  [
    "Answer all three to see your score.",
    "答完三题即可查看得分。",
    "세 문제를 모두 풀면 점수를 볼 수 있습니다.",
    "Trả lời cả ba câu để xem điểm của bạn.",
    "3問すべて答えると、結果が表示されます。",
  ],
  ["Play again", "再玩一次", "다시 하기", "Chơi lại", "もう一度"],
  ["Show all answers", "显示全部答案", "정답 모두 보기", "Xem tất cả đáp án", "すべての答えを見る"],
  ["Tap a question.", "点选一个问题。", "질문을 눌러 보세요.", "Chạm vào một câu hỏi.", "質問をタップしてください。"],
  [
    "Answers in plain words",
    "用浅显的话回答",
    "쉬운 말로 답해 드립니다",
    "Trả lời bằng lời lẽ dễ hiểu",
    "やさしい言葉でお答えします",
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
console.log("Updated " + entries.length + " science-section strings in five languages.");
