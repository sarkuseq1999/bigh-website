const fs = require('node:fs');
const entries = [
  ['Signature', '经典', '시그니처', 'Dấu ấn', 'シグネチャー'],
  ['Spotlight', '聚光', '스포트라이트', 'Tâm điểm', 'スポットライト'],
  ['Portrait', '雅框', '포트레이트', 'Chân dung', 'ポートレート'],
  ['More life.', '让生活更丰盛。', '더 풍성한 삶.', 'Sống trọn vẹn hơn.', 'もっと豊かに。'],
  ['In every day.', '从每一天开始。', '매일의 순간에.', 'Trong từng ngày.', '一日、一日を。'],
  ['Your next chapter', '人生的新篇章', '당신의 다음 장은', 'Chương mới của bạn', 'あなたの次の章は'],
  ['starts within.', '从内在开始。', '내면에서 시작됩니다.', 'bắt đầu từ bên trong.', '内側から始まる。'],
  ['The art of living.', '生活的艺术。', '삶의 예술.', 'Nghệ thuật sống.', '暮らしを彩るアート。'],
  ['The science within.', '源于内在的科学。', '그 안의 과학.', 'Khoa học từ bên trong.', 'その内側に、科学。'],
  ['Start with NuriCell, BiGH’s flagship for cellular health and mental energy. Then explore the formulas that complete the collection.', '从BiGH专注细胞健康与脑力活力的旗舰配方NuriCell开始，再探索系列中的其他特色配方。', '세포 건강과 정신적 에너지에 집중한 BiGH의 대표 포뮬러, NuriCell에서 시작하세요. 이어서 제품군을 완성하는 다른 포뮬러들도 만나보세요.', 'Bắt đầu với NuriCell, công thức chủ lực của BiGH dành cho sức khỏe tế bào và năng lượng tinh thần. Sau đó khám phá những công thức làm nên bộ sưu tập.', 'まずは、細胞の健康と頭の活力に着目したBiGHの主力フォーミュラ、NuriCellから。そして、コレクションを彩るほかのフォーミュラへ。'],
  ['Meet NuriCell, our flagship formula focused on your cells’ tiny power plants. Discover the rest of the BiGH family alongside it.', '认识NuriCell——我们的旗舰配方，专注细胞中的微小能量工厂。同时探索BiGH家族中的其他产品。', '세포 속 작은 발전소에 주목한 대표 포뮬러, NuriCell을 만나보세요. 함께하는 BiGH의 다른 제품들도 살펴보세요.', 'Làm quen với NuriCell, công thức chủ lực tập trung vào những nhà máy năng lượng nhỏ bé trong tế bào. Khám phá các thành viên khác của gia đình BiGH bên cạnh sản phẩm này.', '細胞の中の小さな発電所に着目した主力フォーミュラ、NuriCell。BiGHファミリーのほかの商品も、あわせてご紹介します。'],
  ['NuriCell brings our focus on cellular health into one signature formula, developed by Dr. Jian Kang Liu and Dr. Iris Wang.', 'NuriCell将我们对细胞健康的专注融入一款代表性配方，由Jian Kang Liu博士与Iris Wang博士共同开发。', 'Jian Kang Liu 박사와 Iris Wang 박사가 개발한 NuriCell은 세포 건강에 대한 우리의 관심을 하나의 시그니처 포뮬러에 담았습니다.', 'NuriCell kết tinh định hướng về sức khỏe tế bào trong một công thức đặc trưng, được phát triển bởi Tiến sĩ Jian Kang Liu và Tiến sĩ Iris Wang.', 'Jian Kang Liu博士とIris Wang博士が開発したNuriCell。細胞の健康への私たちの想いを、一つの代表的なフォーミュラに込めています。'],
  ['BiGH’s flagship formula', 'BiGH旗舰配方', 'BiGH의 대표 포뮬러', 'Công thức chủ lực của BiGH', 'BiGHの主力フォーミュラ'],
  ['Compare elegant designs', '比较雅致设计', '우아한 디자인 비교', 'So sánh thiết kế thanh lịch', 'エレガントなデザインを比較'],
  ['Elegant designs', '雅致设计', '우아한 디자인', 'Thiết kế thanh lịch', 'エレガントなデザイン'],
  ['Elegant design {number}: {name}', '雅致设计{number}：{name}', '우아한 디자인 {number}: {name}', 'Thiết kế thanh lịch {number}: {name}', 'エレガントなデザイン{number}：{name}'],
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
console.log(`Updated ${entries.length} elegant-design strings in all ${locales.length} catalogs.`);
