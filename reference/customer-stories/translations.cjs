const fs=require('node:fs');
const entries=[
  [
    "In their own words.",
    "听听他们怎么说。",
    "각자의 이야기.",
    "Qua lời kể của họ.",
    "それぞれの言葉で。"
  ],
  [
    "The routines, questions, and choices behind everyday wellbeing.",
    "日常健康背后的习惯、疑问与选择。",
    "일상의 건강을 둘러싼 습관, 질문, 그리고 선택.",
    "Những thói quen, câu hỏi và lựa chọn đằng sau sức khỏe mỗi ngày.",
    "日々の健やかさにつながる、習慣、疑問、そして選択。"
  ],
  [
    "Choose a sample story",
    "选择示例故事",
    "예시 이야기 선택",
    "Chọn câu chuyện mẫu",
    "サンプルストーリーを選ぶ"
  ],
  [
    "Morning routine",
    "晨间习惯",
    "아침 습관",
    "Thói quen buổi sáng",
    "朝の習慣"
  ],
  [
    "The science",
    "科学背景",
    "과학적 배경",
    "Cơ sở khoa học",
    "科学の背景"
  ],
  [
    "The source",
    "产品来源",
    "원료의 출처",
    "Nguồn gốc",
    "原料の産地"
  ],
  [
    "It fits into my mornings.",
    "它融入了我的早晨。",
    "아침 습관에 자연스럽게 더했어요.",
    "Dễ dàng thêm vào buổi sáng của tôi.",
    "朝の習慣に、自然になじみました。"
  ],
  [
    "Weekday mornings are hectic in our house. I keep NuriCell with my breakfast things so I remember it. I like a routine that feels easy to keep up with.",
    "我们家平日的早晨总是忙忙碌碌。我把NuriCell和早餐用品放在一起，这样就不会忘记。我喜欢这种容易坚持的日常习惯。",
    "평일 아침이면 우리 집은 늘 분주해요. 잊지 않으려고 NuriCell을 아침 식사 준비물 옆에 두고 있어요. 부담 없이 이어갈 수 있는 습관이 좋아요.",
    "Buổi sáng các ngày trong tuần ở nhà tôi khá bận rộn. Tôi để NuriCell cùng đồ ăn sáng để nhớ dùng. Tôi thích một thói quen dễ duy trì.",
    "平日の朝は、家の中がいつも慌ただしいんです。忘れないように、NuriCellを朝食の用意と一緒に置いています。無理なく続けられる習慣が気に入っています。"
  ],
  [
    "I read up on it first.",
    "我先做了些了解。",
    "먼저 꼼꼼히 알아봤어요.",
    "Tôi tìm hiểu kỹ trước.",
    "まず、よく調べました。"
  ],
  [
    "I don’t buy supplements on impulse. I read about NuriCell and looked into the scientists behind the formula before trying it. Knowing that background mattered to me.",
    "我不会冲动购买营养补充剂。试用之前，我阅读了NuriCell的资料，也了解了配方背后的科学家。对我来说，了解这些背景很重要。",
    "저는 영양제를 충동적으로 사지 않아요. NuriCell을 사용해 보기 전에 제품 정보를 읽고, 포뮬러를 만든 과학자들에 대해서도 알아봤어요. 그런 배경을 아는 것이 제게는 중요했어요.",
    "Tôi không mua thực phẩm bổ sung một cách bốc đồng. Trước khi dùng thử, tôi đọc về NuriCell và tìm hiểu các nhà khoa học đứng sau công thức. Hiểu được nền tảng đó rất quan trọng với tôi.",
    "サプリメントを衝動買いすることはありません。試す前にNuriCellについて読み、配合を手がけた科学者についても調べました。そうした背景を知ることが、私には大切でした。"
  ],
  [
    "The source mattered to me.",
    "我在意它的来源。",
    "어디에서 왔는지가 중요했어요.",
    "Nguồn gốc quan trọng với tôi.",
    "産地を知ることが大切でした。"
  ],
  [
    "I’d heard of propolis, but I didn’t know what made the green kind different. Reading about its source in Minas Gerais, Brazil, helped me understand what I was buying.",
    "我听说过蜂胶，但以前并不知道绿蜂胶有什么不同。读到它来自巴西米纳斯吉拉斯州后，我更了解自己购买的是什么。",
    "프로폴리스는 들어봤지만, 그린 프로폴리스가 무엇이 다른지는 몰랐어요. 브라질 미나스제라이스라는 산지에 대해 읽고 나서 제가 사는 제품을 더 잘 이해하게 됐어요.",
    "Tôi đã nghe nói đến keo ong, nhưng chưa biết keo ong xanh có gì khác biệt. Đọc về nguồn gốc ở Minas Gerais, Brazil giúp tôi hiểu rõ hơn sản phẩm mình mua.",
    "プロポリスは知っていましたが、グリーンプロポリスがどう違うのかは知りませんでした。ブラジルのミナスジェライス州という産地について読み、自分が何を買うのかを理解できました。"
  ],
  [
    "Design draft — all testimonials and reviewer names below are fictional samples.",
    "设计草稿——以下所有评价和评价者姓名均为虚构示例。",
    "디자인 초안 — 아래의 모든 후기와 작성자 이름은 가상의 예시입니다.",
    "Bản nháp thiết kế — tất cả lời nhận xét và tên người đánh giá bên dưới đều là ví dụ hư cấu.",
    "デザイン案 — 以下の体験談と投稿者名は、すべて架空のサンプルです。"
  ],
  [
    "Fictional sample",
    "虚构示例",
    "가상 예시",
    "Ví dụ hư cấu",
    "架空のサンプル"
  ],
  [
    "Illustrative reviewer",
    "虚构评价者",
    "가상의 작성자",
    "Người đánh giá hư cấu",
    "架空の投稿者"
  ],
  [
    "Previous sample story",
    "上一个示例故事",
    "이전 예시 이야기",
    "Câu chuyện mẫu trước",
    "前のサンプルストーリー"
  ],
  [
    "Next sample story",
    "下一个示例故事",
    "다음 예시 이야기",
    "Câu chuyện mẫu tiếp theo",
    "次のサンプルストーリー"
  ],
  [
    "A different perspective",
    "换个角度看看",
    "또 다른 관점",
    "Một góc nhìn khác",
    "別の視点から"
  ],
  [
    "Sample story {number} of {count}: {name}",
    "示例故事{number}/{count}：{name}",
    "예시 이야기 {number}/{count}: {name}",
    "Câu chuyện mẫu {number}/{count}: {name}",
    "サンプルストーリー {number}/{count}：{name}"
  ]
];
const path='src/i18n/copy-keys.json';
const keys=JSON.parse(fs.readFileSync(path,'utf8'));
const locales=['en','cns','kr','vn','jp'];
const catalogs=locales.map(l=>JSON.parse(fs.readFileSync('messages/'+l+'.json','utf8')));
let next=Math.max(...Object.values(keys).map(k=>Number(k.slice(1))))+1;
for(const row of entries){const key=keys[row[0]]??'m'+next++;keys[row[0]]=key;row.forEach((v,i)=>{catalogs[i].Copy[key]=v;});}
fs.writeFileSync(path,JSON.stringify(keys,null,2)+'\n');
locales.forEach((l,i)=>fs.writeFileSync('messages/'+l+'.json',JSON.stringify(catalogs[i],null,2)+'\n'));
console.log('Updated '+entries.length+' customer-story strings in five languages.');

