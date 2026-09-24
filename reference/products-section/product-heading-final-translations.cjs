const fs=require('node:fs');
const entries=[
  [
    "Explore our products.",
    "探索我们的产品。",
    "BiGH 제품을 만나보세요.",
    "Khám phá sản phẩm của chúng tôi.",
    "製品を見つける。"
  ],
  [
    "Find your starting point.",
    "找到你的健康起点。",
    "나에게 맞는 시작을 찾아보세요.",
    "Tìm điểm khởi đầu của bạn.",
    "あなたの一歩を、ここから。"
  ],
  [
    "Discover the science, ingredients, and purpose behind each BiGH product.",
    "了解每一款BiGH产品背后的科学、成分与初衷。",
    "각 BiGH 제품에 담긴 과학, 성분, 그리고 개발 목적을 알아보세요.",
    "Tìm hiểu khoa học, thành phần và mục đích đằng sau mỗi sản phẩm BiGH.",
    "BiGHの各製品に込めた科学、成分、そして想いをご紹介します。"
  ],
  [
    "Mitochondrial health",
    "线粒体健康",
    "미토콘드리아 건강",
    "Sức khỏe ty thể",
    "ミトコンドリアの健康"
  ],
  [
    "Mental energy",
    "脑力活力",
    "정신적 에너지",
    "Năng lượng tinh thần",
    "頭の活力"
  ],
  [
    "Brazilian green propolis, shaped by local plants and the bees that gather their resins.",
    "巴西绿蜂胶，源于当地植物与采集其树脂的蜜蜂。",
    "현지 식물과 그 수지를 모으는 꿀벌이 만들어 낸 브라질산 그린 프로폴리스.",
    "Keo ong xanh Brazil, kết tinh từ thực vật địa phương và những chú ong thu gom nhựa cây.",
    "ブラジルの植物と、その樹脂を集めるミツバチが生み出すグリーンプロポリス。"
  ],
  [
    "Its characteristic compounds include artepillin C—one reason researchers study Brazilian green propolis for its antioxidant properties.",
    "其特有成分包括阿特匹林C，这也是研究人员关注巴西绿蜂胶抗氧化特性的原因之一。",
    "특징적인 성분에는 아르테필린 C가 포함되어 있습니다. 연구자들이 브라질산 그린 프로폴리스의 항산화 특성에 주목하는 이유 중 하나입니다.",
    "Các hợp chất đặc trưng bao gồm artepillin C—một lý do khiến các nhà nghiên cứu quan tâm đến đặc tính chống oxy hóa của keo ong xanh Brazil.",
    "特徴的な成分の一つがアルテピリンC。ブラジル産グリーンプロポリスの抗酸化特性が研究される理由の一つです。"
  ],
  [
    "Minas Gerais, Brazil",
    "巴西米纳斯吉拉斯州",
    "브라질 미나스제라이스",
    "Minas Gerais, Brazil",
    "ブラジル・ミナスジェライス州"
  ],
  [
    "Distinctive plant compounds",
    "特色植物成分",
    "특징적인 식물 성분",
    "Hợp chất thực vật đặc trưng",
    "特徴的な植物成分"
  ],
  [
    "Free-radical defenses",
    "自由基防御",
    "활성산소 방어",
    "Bảo vệ trước gốc tự do",
    "フリーラジカルへの防御"
  ],
  [
    "Turmeric’s active compound, delivered as Longvida® curcumin with a specialized system designed to improve absorption.",
    "以Longvida®姜黄素呈现姜黄的活性成分，采用专门设计的递送系统，旨在提升吸收。",
    "강황의 활성 성분을 Longvida® 커큐민으로 담아, 흡수 개선을 위해 설계된 특수 전달 시스템으로 제공합니다.",
    "Hoạt chất của nghệ dưới dạng curcumin Longvida®, với hệ thống dẫn truyền chuyên biệt được thiết kế để cải thiện khả năng hấp thu.",
    "ウコンの活性成分をLongvida®クルクミンとして配合。吸収の向上を目指した独自のデリバリーシステムを採用しています。"
  ],
  [
    "Longvida® was developed with neuroscientists at the University of California, Los Angeles.",
    "Longvida®由研究团队与加州大学洛杉矶分校的神经科学家合作开发。",
    "Longvida®는 캘리포니아 대학교 로스앤젤레스의 신경과학자들과 함께 개발되었습니다.",
    "Longvida® được phát triển cùng các nhà khoa học thần kinh tại Đại học California, Los Angeles.",
    "Longvida®は、カリフォルニア大学ロサンゼルス校の神経科学者と共同で開発されました。"
  ],
  [
    "Longvida® curcumin",
    "Longvida®姜黄素",
    "Longvida® 커큐민",
    "Curcumin Longvida®",
    "Longvida®クルクミン"
  ],
  [
    "Advanced delivery",
    "先进递送技术",
    "첨단 전달 기술",
    "Dẫn truyền tiên tiến",
    "先進のデリバリー技術"
  ],
  [
    "A cellular approach to everyday stress, bringing nutrients involved in cellular energy and antioxidant defenses into one formula.",
    "从细胞层面关注日常压力，将参与细胞能量代谢与抗氧化防御的营养素融于一款配方。",
    "일상의 스트레스를 세포 관점에서 바라보며, 세포 에너지와 항산화 방어에 관여하는 영양소를 하나의 포뮬러에 담았습니다.",
    "Tiếp cận căng thẳng hằng ngày từ góc độ tế bào, kết hợp các dưỡng chất tham gia vào năng lượng tế bào và hệ thống phòng vệ chống oxy hóa trong một công thức.",
    "日々のストレスを細胞の視点から考え、細胞のエネルギーと抗酸化防御に関わる栄養素を一つのフォーミュラにまとめました。"
  ],
  [
    "Developed by Dr. Jian Kang Liu and Dr. Iris Wang, drawing on their research into stress and cellular health.",
    "由Jian Kang Liu博士与Iris Wang博士共同开发，融入他们对压力与细胞健康的研究。",
    "Jian Kang Liu 박사와 Iris Wang 박사가 스트레스와 세포 건강에 관한 연구를 바탕으로 개발했습니다.",
    "Được phát triển bởi Tiến sĩ Jian Kang Liu và Tiến sĩ Iris Wang, dựa trên nghiên cứu của họ về căng thẳng và sức khỏe tế bào.",
    "ストレスと細胞の健康に関する研究をもとに、Jian Kang Liu博士とIris Wang博士が開発しました。"
  ],
  [
    "Cellular energy",
    "细胞能量",
    "세포 에너지",
    "Năng lượng tế bào",
    "細胞のエネルギー"
  ],
  [
    "Everyday stress",
    "日常压力",
    "일상의 스트레스",
    "Căng thẳng hằng ngày",
    "日々のストレス"
  ]
];
const keyFile='src/i18n/copy-keys.json';
const keys=JSON.parse(fs.readFileSync(keyFile,'utf8'));
const locales=['en','cns','kr','vn','jp'];
const catalogs=locales.map(l=>JSON.parse(fs.readFileSync('messages/'+l+'.json','utf8')));
let next=Math.max(...Object.values(keys).map(k=>Number(k.slice(1))))+1;
for(const row of entries) {
 const key=keys[row[0]]??'m'+next++;
 keys[row[0]]=key;
 row.forEach((v,i)=>{catalogs[i].Copy[key]=v;});
}
fs.writeFileSync(keyFile,JSON.stringify(keys,null,2)+'\n');
locales.forEach((l,i)=>fs.writeFileSync('messages/'+l+'.json',JSON.stringify(catalogs[i],null,2)+'\n'));
console.log('Updated '+entries.length+' strings in all five languages.');

