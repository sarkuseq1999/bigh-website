const fs = require('node:fs');
const entries = [
  ['Good science.', '好科学。', '좋은 과학.', 'Khoa học vững vàng.', '確かな科学を。'],
  ['For real life.', '融入每一天。', '우리의 일상으로.', 'Cho cuộc sống mỗi ngày.', '毎日の暮らしに。'],
  ['Cellular health is our starting point. Explore NuriCell and four distinctive formulas for everyday wellbeing.', '从细胞健康出发，探索NuriCell及另外四款各具特色的配方，关注日常健康。', '세포 건강에서 시작합니다. 일상의 건강을 위한 NuriCell과 네 가지 개성 있는 포뮬러를 만나보세요.', 'Sức khỏe tế bào là điểm khởi đầu. Khám phá NuriCell cùng bốn công thức riêng biệt hướng đến sức khỏe mỗi ngày.', '私たちの出発点は、細胞の健康。NuriCellと、毎日の健やかさを考えた4つの個性あるフォーミュラをご紹介します。'],
  ['Small beginnings.', '从微小开始。', '작은 시작.', 'Khởi đầu từ điều nhỏ.', '小さな始まりから。'],
  ['Fuller lives.', '让生活更丰盛。', '더 풍성한 삶.', 'Sống trọn vẹn hơn.', 'より豊かな毎日へ。'],
  ['A world of care, starting with your cells. Find your place in the BiGH family of formulas.', '从细胞开始，关爱生活的每一面。在BiGH配方家族中，发现适合你的选择。', '세포에서 시작되는 다양한 건강 관리. BiGH 포뮬러 제품군에서 나에게 맞는 선택을 찾아보세요.', 'Chăm sóc bản thân, bắt đầu từ tế bào. Tìm lựa chọn dành cho bạn trong gia đình công thức BiGH.', '細胞から始まる、さまざまなケア。BiGHのフォーミュラから、あなたに合う一品を見つけてください。'],
  ['Your daily dose', '为每一天', '매일 만나는', 'Mỗi ngày một chút', '毎日にひとさじの'],
  ['of possibility.', '添一份可能。', '새로운 가능성.', 'khả năng mới.', '可能性を。'],
  ['Meet NuriCell and the formulas alongside it. Different stories. A shared curiosity for better living.', '认识NuriCell和它的配方伙伴。不同的故事，共同探索更好的生活。', 'NuriCell과 함께하는 포뮬러들을 만나보세요. 서로 다른 이야기, 더 나은 삶을 향한 같은 호기심.', 'Làm quen với NuriCell và các công thức đồng hành. Mỗi sản phẩm một câu chuyện, cùng khám phá cuộc sống tốt hơn.', 'NuriCellと、その仲間たち。それぞれのストーリーに共通するのは、よりよい暮らしへの探究心です。'],
  ['Bold', '鲜明', '선명한', 'Mạnh mẽ', '力強く'],
  ['Elegant', '雅致', '우아한', 'Thanh lịch', '優雅に'],
  ['Expressive', '灵动', '표현력 있는', 'Sáng tạo', '表情豊かに'],
  ['Compare product headings', '比较产品区标题设计', '제품 섹션 제목 비교', 'So sánh tiêu đề phần sản phẩm', '商品セクションの見出しを比較'],
  ['Heading options', '标题方案', '제목 디자인', 'Mẫu tiêu đề', '見出しのデザイン'],
  ['Heading option {number}: {name}', '标题方案{number}：{name}', '제목 디자인 {number}: {name}', 'Mẫu tiêu đề {number}: {name}', '見出し案{number}：{name}'],
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
console.log(`Updated ${entries.length} heading strings in all ${locales.length} catalogs.`);
