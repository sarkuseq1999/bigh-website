const fs = require('node:fs');
const entries = [
  ["Previous product", "上一款产品", "이전 제품", "Sản phẩm trước", "前の商品"],
  ["Next product", "下一款产品", "다음 제품", "Sản phẩm tiếp theo", "次の商品"],
  ["Cellular health & mental energy", "细胞健康与脑力活力", "세포 건강과 정신적 에너지", "Sức khỏe tế bào & năng lượng tinh thần", "細胞の健康と頭の活力"],
  ["From Minas Gerais, Brazil", "源自巴西米纳斯吉拉斯州", "브라질 미나스제라이스산", "Từ Minas Gerais, Brazil", "ブラジル・ミナスジェライス州産"],
  ["Plant-based antioxidants", "植物源抗氧化成分", "식물 유래 항산화 성분", "Chất chống oxy hóa từ thực vật", "植物由来の抗酸化成分"],
  ["Advanced curcumin", "进阶姜黄素配方", "차별화된 커큐민", "Curcumin tiên tiến", "進化したクルクミン"],
  ["A cellular approach to everyday stress", "从细胞层面关注日常压力", "일상의 스트레스를 세포 관점에서", "Tiếp cận căng thẳng hằng ngày từ tế bào", "日々のストレスを細胞の視点から"],
  ["Bees produce this green propolis from local plant resins. Its characteristic compounds include artepillin C—one reason researchers study Brazilian green propolis for its antioxidant properties.", "蜜蜂采集当地植物树脂，酿成这种绿蜂胶。其特色成分包括阿特匹林C，这也是研究人员关注巴西绿蜂胶抗氧化特性的原因之一。", "벌이 현지 식물의 수지를 모아 만드는 그린 프로폴리스입니다. 특징적인 성분 중 하나인 아르테필린 C는 연구자들이 브라질산 그린 프로폴리스의 항산화 특성에 주목하는 이유 중 하나입니다.", "Ong tạo ra loại keo ong xanh này từ nhựa thực vật địa phương. Một trong những hợp chất đặc trưng là artepillin C — lý do các nhà nghiên cứu quan tâm đến đặc tính chống oxy hóa của keo ong xanh Brazil.", "ミツバチが現地の植物の樹脂からつくるグリーンプロポリス。特徴的な成分にはアルテピリンCが含まれ、ブラジル産グリーンプロポリスの抗酸化特性が研究される理由の一つとなっています。"],
  ["A diverse blend of concentrated plant extracts, bringing together antioxidant compounds from grape seeds, pine bark, and other botanical sources.", "融合多种浓缩植物提取物，汇集葡萄籽、松树皮等植物中的抗氧化成分。", "포도씨, 소나무 껍질을 비롯한 여러 식물에서 얻은 항산화 성분을 담은 농축 식물 추출물 블렌드입니다.", "Sự kết hợp đa dạng các chiết xuất thực vật cô đặc, quy tụ hợp chất chống oxy hóa từ hạt nho, vỏ thông và các nguồn thực vật khác.", "ブドウ種子や松樹皮など、さまざまな植物由来の抗酸化成分を集めた濃縮植物エキスのブレンドです。"],
  ["Designed to support your cells’ natural defenses against free radicals—unstable molecules that can damage cells.", "旨在支持细胞对抗自由基的天然防御能力。自由基是不稳定的分子，可能损伤细胞。", "세포를 손상시킬 수 있는 불안정한 분자인 활성산소 라디칼에 맞서는 세포의 자연적인 방어 체계를 지원하도록 설계되었습니다.", "Được thiết kế để hỗ trợ khả năng bảo vệ tự nhiên của tế bào trước gốc tự do — những phân tử không ổn định có thể gây tổn thương tế bào.", "細胞にダメージを与えることがある不安定な分子、フリーラジカル。それに対する細胞本来の防御機能を支えることを目指した配合です。"],
  ["Featuring Longvida® curcumin, developed with neuroscientists at the University of California, Los Angeles. Its specialized delivery system is designed to improve how your body absorbs turmeric’s active compound.", "采用与加州大学洛杉矶分校神经科学家共同开发的Longvida®姜黄素。其专门的递送系统旨在改善人体对姜黄活性成分的吸收。", "캘리포니아 대학교 로스앤젤레스의 신경과학자들과 함께 개발한 Longvida® 커큐민을 담았습니다. 특수 전달 시스템은 강황의 활성 성분이 체내에 더 잘 흡수되도록 설계되었습니다.", "Chứa curcumin Longvida®, được phát triển cùng các nhà khoa học thần kinh tại Đại học California, Los Angeles. Hệ thống dẫn truyền chuyên biệt được thiết kế để cải thiện khả năng hấp thu hoạt chất của nghệ trong cơ thể.", "カリフォルニア大学ロサンゼルス校の神経科学者と共同開発されたLongvida®クルクミンを配合。独自の送達システムは、ウコンの活性成分を体内でより吸収しやすくするために設計されています。"],
  ["Developed by Dr. Jian Kang Liu and Dr. Iris Wang, bringing their research on stress and cellular health into a formula designed for life’s demanding days.", "由Jian Kang Liu博士与Iris Wang博士共同开发，将他们对压力和细胞健康的研究融入配方，为忙碌而充满挑战的日常而设计。", "Jian Kang Liu 박사와 Iris Wang 박사가 스트레스와 세포 건강에 관한 연구를 바탕으로 바쁜 일상을 위해 개발한 포뮬러입니다.", "Được phát triển bởi Tiến sĩ Jian Kang Liu và Tiến sĩ Iris Wang, đưa nghiên cứu về căng thẳng và sức khỏe tế bào vào công thức dành cho những ngày nhiều áp lực.", "Jian Kang Liu博士とIris Wang博士が開発。ストレスと細胞の健康に関する研究を、忙しく負担の多い毎日のためのフォーミュラに生かしています。"],
  ["Nature Calm brings together nutrients involved in cellular energy and antioxidant defenses, with everyday stress in mind.", "Nature Calm着眼于日常压力，汇集参与细胞能量代谢与抗氧化防御的营养成分。", "Nature Calm은 일상의 스트레스를 고려하여 세포 에너지와 항산화 방어에 관여하는 영양소를 함께 담았습니다.", "Nature Calm kết hợp các dưỡng chất tham gia vào quá trình tạo năng lượng tế bào và bảo vệ chống oxy hóa, hướng đến những căng thẳng thường ngày.", "Nature Calmは日々のストレスを考え、細胞のエネルギーや抗酸化防御に関わる栄養成分を組み合わせています。"],
  ["Led by NuriCell. Discover the story behind every formula.", "以NuriCell为主角，探索每款配方背后的故事。", "NuriCell을 중심으로, 각 포뮬러에 담긴 이야기를 만나보세요.", "NuriCell dẫn đầu. Khám phá câu chuyện đằng sau từng công thức.", "主役はNuriCell。それぞれのフォーミュラに込められたストーリーへ。"],
  ["Select a bottle to explore", "点击产品，了解更多", "제품을 선택해 자세히 알아보세요", "Chọn một sản phẩm để khám phá", "ボトルを選んで詳しく見る"],
  ["Exploring {name}", "正在了解{name}", "{name} 살펴보기", "Đang khám phá {name}", "{name}をご紹介"],
];
const keyFile = 'src/i18n/copy-keys.json';
const keys = JSON.parse(fs.readFileSync(keyFile, 'utf8'));
const locales = ['en', 'cns', 'kr', 'vn', 'jp'];
const catalogs = locales.map(locale => JSON.parse(fs.readFileSync(`messages/${locale}.json`, 'utf8')));
let next = Math.max(...Object.values(keys).map(key => Number(key.slice(1)))) + 1;
for (const row of entries) {
  const key = keys[row[0]] ?? `m${next++}`;
  keys[row[0]] = key;
  row.forEach((value, index) => { catalogs[index].Copy[key] = value; });
}
fs.writeFileSync(keyFile, JSON.stringify(keys, null, 2) + '\n');
locales.forEach((locale, index) => fs.writeFileSync(`messages/${locale}.json`, JSON.stringify(catalogs[index], null, 2) + '\n'));
console.log(`Updated ${entries.length} lineup strings in all ${locales.length} catalogs.`);
