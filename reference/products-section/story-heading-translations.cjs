const fs = require('node:fs');
const entries = [
  [
    "Cells",
    "细胞",
    "세포",
    "Tế bào",
    "細胞"
  ],
  [
    "Life",
    "生活",
    "일상",
    "Cuộc sống",
    "暮らし"
  ],
  [
    "Small cells.",
    "微小的细胞，",
    "작은 세포에서,",
    "Tế bào nhỏ.",
    "小さな細胞から。"
  ],
  [
    "Big possibilities.",
    "无限的可能。",
    "더 큰 가능성으로.",
    "Khả năng lớn.",
    "大きな可能性へ。"
  ],
  [
    "Good health starts small. Meet NuriCell, our flagship for cellular health and mental energy, and explore four more formulas with distinctive stories in science and nature.",
    "健康始于微小之处。认识我们的旗舰配方NuriCell，专注细胞健康与脑力活力，再探索另外四款融合科学与自然、各有特色的配方。",
    "건강은 작은 곳에서 시작됩니다. 세포 건강과 정신적 에너지에 주목한 대표 포뮬러 NuriCell, 그리고 과학과 자연의 특별한 이야기를 담은 네 가지 포뮬러를 만나보세요.",
    "Sức khỏe bắt đầu từ những điều nhỏ bé. Làm quen với NuriCell, công thức chủ lực dành cho sức khỏe tế bào và năng lượng tinh thần, cùng bốn công thức mang những câu chuyện riêng về khoa học và thiên nhiên.",
    "健康は、小さなところから。細胞の健康と頭の活力に着目した主力フォーミュラNuriCellと、科学と自然の物語を持つ4つのフォーミュラをご紹介します。"
  ],
  [
    "Your life is full.",
    "生活如此丰富，",
    "소중한 것으로 가득한 삶,",
    "Cuộc sống đầy ý nghĩa.",
    "充実した毎日を、"
  ],
  [
    "Keep it that way.",
    "让精彩继续。",
    "오래도록 함께하세요.",
    "Hãy giữ trọn vẹn.",
    "これからも。"
  ],
  [
    "From NuriCell’s focus on cellular health and mental energy to plant-based antioxidant support, explore five formulas made for everyday wellbeing.",
    "从NuriCell关注的细胞健康与脑力活力，到植物来源的抗氧化支持，探索五款为日常健康而设计的配方。",
    "세포 건강과 정신적 에너지에 주목한 NuriCell부터 식물성 항산화 성분까지, 일상의 건강을 위한 다섯 가지 포뮬러를 살펴보세요.",
    "Từ sức khỏe tế bào và năng lượng tinh thần mà NuriCell hướng đến, đến khả năng hỗ trợ chống oxy hóa từ thực vật, hãy khám phá năm công thức dành cho sức khỏe mỗi ngày.",
    "細胞の健康と頭の活力に着目したNuriCellから、植物由来の抗酸化サポートまで。毎日の健やかさを考えた5つのフォーミュラをご覧ください。"
  ],
  [
    "The science runs deep.",
    "深耕科学，",
    "깊이 있는 과학,",
    "Khoa học đi sâu.",
    "科学を深める。"
  ],
  [
    "The purpose is you.",
    "只为你的健康。",
    "그 중심에는 당신이 있습니다.",
    "Vì chính bạn.",
    "その先に、あなた。"
  ],
  [
    "Our flagship NuriCell was formulated by Dr. Jian Kang Liu and Dr. Iris Wang. Discover it alongside four distinctive formulas, united by BiGH’s focus on everyday wellbeing.",
    "我们的旗舰NuriCell由Jian Kang Liu博士与Iris Wang博士共同研发。与另外四款特色配方一起，呈现BiGH对日常健康的共同关注。",
    "대표 제품 NuriCell은 Jian Kang Liu 박사와 Iris Wang 박사가 공동 개발했습니다. 일상의 건강을 생각하는 BiGH의 네 가지 특별한 포뮬러도 함께 만나보세요.",
    "NuriCell, công thức chủ lực của chúng tôi, được xây dựng bởi Tiến sĩ Jian Kang Liu và Tiến sĩ Iris Wang. Khám phá sản phẩm cùng bốn công thức đặc trưng, cùng chung định hướng của BiGH về sức khỏe mỗi ngày.",
    "主力製品NuriCellは、Jian Kang Liu博士とIris Wang博士が共同開発しました。日々の健やかさを見つめるBiGHの4つの個性あるフォーミュラとともに、ご紹介します。"
  ],
  [
    "Compare headline options",
    "比较标题方案",
    "헤드라인 옵션 비교",
    "So sánh tiêu đề",
    "見出し案を比較"
  ],
  [
    "Headline options",
    "标题方案",
    "헤드라인 옵션",
    "Các tiêu đề",
    "見出し案"
  ],
  [
    "Headline option {number}: {name}",
    "标题方案{number}：{name}",
    "헤드라인 옵션 {number}: {name}",
    "Tiêu đề {number}: {name}",
    "見出し案{number}：{name}"
  ]
];
const keyFile = 'src/i18n/copy-keys.json';
const keys = JSON.parse(fs.readFileSync(keyFile, 'utf8'));
const locales = ['en','cns','kr','vn','jp'];
const catalogs = locales.map(locale => JSON.parse(fs.readFileSync('messages/'+locale+'.json','utf8')));
let next = Math.max(...Object.values(keys).map(key => Number(key.slice(1)))) + 1;
for (const row of entries) {
  const key = keys[row[0]] ?? 'm'+next++;
  keys[row[0]] = key;
  row.forEach((value,index) => { catalogs[index].Copy[key] = value; });
}
fs.writeFileSync(keyFile, JSON.stringify(keys,null,2)+'\n');
locales.forEach((locale,index) => fs.writeFileSync('messages/'+locale+'.json', JSON.stringify(catalogs[index],null,2)+'\n'));
console.log('Updated '+entries.length+' strings in all '+locales.length+' languages.');

