// Adds the Science page's round 3 strings (November 4, 2026) to the five catalogs. DRAFT
// translation, not native-reviewed: the site's understated voice, no new claims. Keys start at
// m1100, a range of its own, so a session adding keys after m965 at the same time cannot collide
// (re-running is safe: a string that already has a key keeps it). hken.json stays {} (/hken
// redirects to /cns). Dr. Liu is named as the catalogs already name him (m055): 刘健康博士 in
// Chinese, "Tiến sĩ Jiankang Liu" in Vietnamese, "Dr. Jiankang Liu" in Japanese and Korean.
// Mitochondria and free radicals as the catalogs already say them (线粒体 / 미토콘드리아 / ty thể /
// ミトコンドリア; 自由基 / 자유 라디칼 / gốc tự do / フリーラジカル). "What are mitochondria?" already
// has its key. Dr. Liu's path (Berkeley, Salzburg, Today) stays English in every language, as its
// stops always were.
// Run from the repo root:
//   node reference/ink-pages/science/translations-science-round3.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  [
    "Our science starts in the cell.",
    "我们的科学，从细胞开始。",
    "우리의 과학은 세포에서 시작합니다.",
    "Khoa học của chúng tôi bắt đầu từ tế bào.",
    "私たちのサイエンスは、細胞から始まります。",
  ],
  [
    "How do your cells make energy? And what changes as we age? Dr.\u00a0Jiankang Liu has spent decades studying both.",
    "你的细胞如何产生能量？随着年龄增长，又会发生哪些变化？刘健康博士数十年来一直研究这两个问题。",
    "세포는 어떻게 에너지를 만들까요? 그리고 나이가 들면 무엇이 달라질까요? Dr.\u00a0Jiankang Liu는 수십 년 동안 이 두 가지를 연구해 왔습니다.",
    "Tế bào của bạn tạo ra năng lượng như thế nào? Và điều gì thay đổi khi chúng ta già đi? Tiến sĩ Jiankang Liu đã dành hàng chục năm nghiên cứu cả hai câu hỏi này.",
    "細胞はどのようにエネルギーをつくるのでしょう？そして、年齢とともに何が変わるのでしょう？Dr.\u00a0Jiankang Liu は、この二つを何十年も研究してきました。",
  ],
  [
    "A brass microscope, a notebook and poppies on a desk by an open window over golden California hills, painted in ink and watercolour",
    "水墨淡彩画：开着的窗边，书桌上放着黄铜显微镜、笔记本和罂粟花，窗外是金色的加州山丘",
    "수묵 담채화: 열린 창가 책상 위의 황동 현미경, 공책, 양귀비. 창밖으로 금빛 캘리포니아 언덕이 보입니다",
    "Tranh mực và màu nước: kính hiển vi bằng đồng, cuốn sổ và hoa anh túc trên bàn cạnh cửa sổ mở, nhìn ra những ngọn đồi vàng California",
    "水墨淡彩画：開いた窓辺の机に真鍮の顕微鏡、ノート、ポピー。窓の外には金色のカリフォルニアの丘",
  ],
  [
    "Why start with the cell?",
    "为什么从细胞开始？",
    "왜 세포에서 시작할까요?",
    "Vì sao bắt đầu từ tế bào?",
    "なぜ細胞から始めるのか？",
  ],
  [
    "Everything you do, from a clear thought to a long walk, runs on energy your cells make. You have about 37 trillion of them, and each one makes its own.",
    "你做的每一件事，从清晰地思考到长距离散步，都依靠细胞产生的能量。你大约有37万亿个细胞，每一个都自己产生能量。",
    "맑은 생각부터 긴 산책까지, 우리가 하는 모든 일은 세포가 만드는 에너지로 움직입니다. 우리 몸에는 약 37조 개의 세포가 있고, 세포마다 스스로 에너지를 만듭니다.",
    "Mọi việc bạn làm, từ một suy nghĩ minh mẫn đến một cuộc đi bộ dài, đều nhờ năng lượng do tế bào tạo ra. Bạn có khoảng 37 nghìn tỷ tế bào, và mỗi tế bào tự tạo năng lượng cho mình.",
    "はっきり考えることから長い散歩まで、私たちのすることはすべて、細胞がつくるエネルギーで動いています。体には約37兆個の細胞があり、一つひとつが自分でエネルギーをつくっています。",
  ],
  [
    "Inside your cells, mitochondria turn food into energy.",
    "在细胞里，线粒体把食物转化为能量。",
    "세포 속 미토콘드리아는 음식을 에너지로 바꿉니다.",
    "Bên trong tế bào, ty thể biến thức ăn thành năng lượng.",
    "細胞の中では、ミトコンドリアが食べ物をエネルギーに変えています。",
  ],
  [
    "Making energy also makes free radicals, which your cells keep in check.",
    "产生能量的同时也会产生自由基，而细胞会把它们控制在一定范围内。",
    "에너지를 만들 때 자유 라디칼도 생기는데, 세포는 이를 적절히 억제합니다.",
    "Khi tạo năng lượng, tế bào cũng sinh ra gốc tự do, và tế bào giữ chúng trong tầm kiểm soát.",
    "エネルギーをつくるとフリーラジカルもでき、細胞はそれを抑えています。",
  ],
  [
    "What are free radicals?",
    "什么是自由基？",
    "자유 라디칼이란 무엇일까요?",
    "Gốc tự do là gì?",
    "フリーラジカルとは？",
  ],
  [
    "With age, mitochondria tend to work less well: one of the hallmarks of aging.",
    "随着年龄增长，线粒体往往不如从前那样运作良好，这是衰老的特征之一。",
    "나이가 들면 미토콘드리아는 예전만큼 잘 일하지 못하는 경향이 있습니다. 이는 노화의 특징 중 하나입니다.",
    "Theo tuổi tác, ty thể thường hoạt động kém đi: một trong những dấu hiệu đặc trưng của lão hóa.",
    "年齢とともに、ミトコンドリアの働きは衰えがちです。これは老化の特徴の一つです。",
  ],
  [
    "How do cells age?",
    "细胞如何衰老？",
    "세포는 어떻게 노화할까요?",
    "Tế bào lão hóa như thế nào?",
    "細胞はどう老化する？",
  ],
  [
    "Cell count: Bianconi and colleagues, Annals of Human Biology, 2013.",
    "细胞数量：Bianconi 等，Annals of Human Biology，2013年。",
    "세포 수: Bianconi 외, Annals of Human Biology, 2013.",
    "Số lượng tế bào: Bianconi và cộng sự, Annals of Human Biology, 2013.",
    "細胞の数：Bianconi ほか、Annals of Human Biology、2013年。",
  ],
  [
    "Like a town at dusk: every house lights its own lamp, as every cell makes its own energy.",
    "就像黄昏时的小镇：每户人家点亮自己的灯，正如每个细胞产生自己的能量。",
    "해 질 녘의 마을처럼, 집집마다 스스로 등불을 켜듯 세포마다 스스로 에너지를 만듭니다.",
    "Như một thị trấn lúc hoàng hôn: mỗi ngôi nhà tự thắp đèn của mình, như mỗi tế bào tự tạo năng lượng của mình.",
    "夕暮れの町のように。どの家も自分の明かりをともし、どの細胞も自分のエネルギーをつくっています。",
  ],
  [
    "San Francisco’s Victorian houses on a hill at dusk, their windows lighting up, painted in ink and watercolour",
    "水墨淡彩画：黄昏时旧金山山坡上的维多利亚式房屋，窗户一扇扇亮起",
    "수묵 담채화: 해 질 녘 언덕 위 샌프란시스코의 빅토리아풍 집들, 창문에 하나둘 불이 켜집니다",
    "Tranh mực và màu nước: những ngôi nhà kiểu Victoria trên đồi San Francisco lúc hoàng hôn, các ô cửa sổ lần lượt sáng đèn",
    "水墨淡彩画：夕暮れの丘に並ぶサンフランシスコのヴィクトリア様式の家々、窓に明かりがともっていく",
  ],
  [
    "Every formula has a scientist behind it.",
    "每一款配方背后，都有一位科学家。",
    "모든 포뮬러 뒤에는 과학자가 있습니다.",
    "Mỗi công thức đều có một nhà khoa học đứng sau.",
    "どのフォーミュラにも、その背後に科学者がいます。",
  ],
  [
    "Read the research yourself.",
    "亲自读一读这些研究。",
    "연구를 직접 읽어 보세요.",
    "Hãy tự đọc các nghiên cứu.",
    "研究をご自身で読んでみてください。",
  ],
  [
    "Three studies to start with, and every source we cite. For each one we say what it shows, and what it does not.",
    "先从三项研究读起，也可以查看我们引用的全部来源。每一项，我们都说明它能说明什么，以及不能说明什么。",
    "먼저 읽어 볼 세 가지 연구와 우리가 인용하는 모든 자료입니다. 각 자료가 무엇을 보여 주고 무엇을 보여 주지 않는지 함께 설명합니다.",
    "Ba nghiên cứu để bắt đầu, cùng mọi nguồn chúng tôi trích dẫn. Với mỗi nguồn, chúng tôi nói rõ điều nó cho thấy và điều nó không cho thấy.",
    "まず読みたい三つの研究と、私たちが引用するすべての資料です。それぞれについて、何を示し、何を示さないのかをお伝えします。",
  ],
  [
    "Old bound journals along a library table, three laid open in front, painted in ink and watercolour",
    "水墨淡彩画：图书馆长桌上排列着装订的旧期刊，前面摊开着三本",
    "수묵 담채화: 도서관 탁자 위에 늘어선 오래된 제본 학술지, 앞에 세 권이 펼쳐져 있습니다",
    "Tranh mực và màu nước: những tập tạp chí khoa học đóng bìa cũ trên bàn thư viện, ba cuốn mở ra phía trước",
    "水墨淡彩画：図書館の机に並ぶ製本された古い学術誌。手前に三冊が開かれています",
  ],
  [
    "Two enamel camp mugs on a redwood picnic table in a California park, painted in ink and watercolour",
    "水墨淡彩画：加州公园里红木野餐桌上的两只搪瓷露营杯",
    "수묵 담채화: 캘리포니아 공원의 레드우드 피크닉 테이블 위 법랑 캠핑 머그 두 개",
    "Tranh mực và màu nước: hai chiếc cốc men cắm trại trên bàn picnic gỗ đỏ trong một công viên California",
    "水墨淡彩画：カリフォルニアの公園のレッドウッドのピクニックテーブルに置かれた二つのホーローのキャンプマグ",
  ],
];
const path = "src/i18n/copy-keys.json";
const keys = JSON.parse(fs.readFileSync(path, "utf8"));
const locales = ["en", "cns", "kr", "vn", "jp"];
const catalogs = locales.map((l) => JSON.parse(fs.readFileSync("messages/" + l + ".json", "utf8")));
const used = new Set(Object.values(keys));
let next = 1100;
const added = [];
for (const row of entries) {
  let key = keys[row[0]];
  if (!key) {
    while (used.has("m" + next)) next++;
    key = "m" + next;
    used.add(key);
    keys[row[0]] = key;
  }
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
