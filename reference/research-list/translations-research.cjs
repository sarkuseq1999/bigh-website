// Adds the research list strings (September 24, 2026: 32 new references, three filters, show
// more) to the five catalogs. Draft translations for review by a native speaker. Entries that
// already had keys (the first four references) are not touched.
// Run from the repo root: node reference/research-list/translations-research.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  // Filters and the show-more control
  ["Ingredients", "成分", "성분", "Thành phần", "成分"],
  ["Guides", "科普指南", "안내 자료", "Hướng dẫn", "ガイド"],
  ["Show all sources", "显示全部资料", "모든 자료 보기", "Xem tất cả nguồn", "すべての資料を表示"],
  ["Show fewer", "收起", "접기", "Thu gọn", "表示を減らす"],
  // Kickers
  ["Review · Antioxidants", "综述 · 抗氧化物质", "리뷰 · 항산화 물질", "Tổng quan · Chất chống oxy hóa", "総説 · 抗酸化物質"],
  ["Review · Exercise", "综述 · 运动", "리뷰 · 운동", "Tổng quan · Vận động", "総説 · 運動"],
  ["Review · Brain aging", "综述 · 大脑老化", "리뷰 · 뇌의 노화", "Tổng quan · Lão hóa não", "総説 · 脳の老化"],
  ["Review · Stress", "综述 · 压力", "리뷰 · 스트레스", "Tổng quan · Căng thẳng", "総説 · ストレス"],
  ["Review · Mitochondria", "综述 · 线粒体", "리뷰 · 미토콘드리아", "Tổng quan · Ty thể", "総説 · ミトコンドリア"],
  ["Review · Brain energy", "综述 · 大脑能量", "리뷰 · 뇌의 에너지", "Tổng quan · Năng lượng của não", "総説 · 脳のエネルギー"],
  ["Cochrane review · Antioxidant supplements", "Cochrane 系统综述 · 抗氧化补充剂", "코크란 리뷰 · 항산화 보충제", "Tổng quan Cochrane · Thực phẩm bổ sung chống oxy hóa", "コクランレビュー · 抗酸化サプリメント"],
  ["Classic paper · Free radicals", "经典论文 · 自由基", "고전 논문 · 자유 라디칼", "Bài báo kinh điển · Gốc tự do", "古典的論文 · フリーラジカル"],
  ["Animal study · NuriCell ingredients", "动物研究 · NuriCell 成分", "동물 연구 · NuriCell 성분", "Nghiên cứu trên động vật · Thành phần NuriCell", "動物研究 · NuriCell の成分"],
  ["Review · NuriCell ingredients", "综述 · NuriCell 成分", "리뷰 · NuriCell 성분", "Tổng quan · Thành phần NuriCell", "総説 · NuriCell の成分"],
  ["Review of trials · NuriCell ingredients", "试验综述 · NuriCell 成分", "임상시험 리뷰 · NuriCell 성분", "Tổng quan các thử nghiệm · Thành phần NuriCell", "試験の総説 · NuriCell の成分"],
  ["Pooled trials in patients · NuriCell ingredients", "患者试验汇总 · NuriCell 成分", "환자 대상 시험 통합 분석 · NuriCell 성분", "Gộp các thử nghiệm trên bệnh nhân · Thành phần NuriCell", "患者対象試験の統合解析 · NuriCell の成分"],
  ["Cochrane review · NuriCell ingredients", "Cochrane 系统综述 · NuriCell 成分", "코크란 리뷰 · NuriCell 성분", "Tổng quan Cochrane · Thành phần NuriCell", "コクランレビュー · NuriCell の成分"],
  ["Human trial · Turmerific ingredient", "人体试验 · Turmerific 成分", "인체 시험 · Turmerific 성분", "Thử nghiệm trên người · Thành phần Turmerific", "ヒト試験 · Turmerific の成分"],
  ["Human trial · Curcumin", "人体试验 · 姜黄素", "인체 시험 · 커큐민", "Thử nghiệm trên người · Curcumin", "ヒト試験 · クルクミン"],
  ["Review · Curcumin", "综述 · 姜黄素", "리뷰 · 커큐민", "Tổng quan · Curcumin", "総説 · クルクミン"],
  ["Pooled trials · Advanced OPC ingredient", "试验汇总 · Advanced OPC 成分", "시험 통합 분석 · Advanced OPC 성분", "Gộp các thử nghiệm · Thành phần Advanced OPC", "試験の統合解析 · Advanced OPC の成分"],
  ["Human trial · Advanced OPC ingredient", "人体试验 · Advanced OPC 成分", "인체 시험 · Advanced OPC 성분", "Thử nghiệm trên người · Thành phần Advanced OPC", "ヒト試験 · Advanced OPC の成分"],
  ["Review · Green propolis", "综述 · 绿蜂胶", "리뷰 · 그린 프로폴리스", "Tổng quan · Keo ong xanh", "総説 · グリーンプロポリス"],
  ["Review · Propolis", "综述 · 蜂胶", "리뷰 · 프로폴리스", "Tổng quan · Keo ong", "総説 · プロポリス"],
  ["Review · Nature Calm ingredient", "综述 · Nature Calm 成分", "리뷰 · Nature Calm 성분", "Tổng quan · Thành phần Nature Calm", "総説 · Nature Calm の成分"],
  ["Human trial · Nature Calm ingredient", "人体试验 · Nature Calm 成分", "인체 시험 · Nature Calm 성분", "Thử nghiệm trên người · Thành phần Nature Calm", "ヒト試験 · Nature Calm の成分"],
  ["Healthy aging", "健康老龄化", "건강한 노화", "Lão hóa khỏe mạnh", "健やかな加齢"],
  ["Brain health", "大脑健康", "뇌 건강", "Sức khỏe não bộ", "脳の健康"],
  ["Supplements", "膳食补充剂", "보충제", "Thực phẩm bổ sung", "サプリメント"],
  ["Ingredient explained", "成分解读", "성분 설명", "Giải thích thành phần", "成分の解説"],
  // Science · titles and texts
  ["Antioxidants: how they really work", "抗氧化物质究竟如何起作用", "항산화 물질은 실제로 어떻게 작용할까", "Chất chống oxy hóa thực sự hoạt động thế nào", "抗酸化物質は実際どう働くのか"],
  [
    "Barry Halliwell reviews how antioxidants act in the body and where the evidence is weaker than the marketing. Free radicals also do useful jobs, and more antioxidant is not automatically better.",
    "Barry Halliwell 综述了抗氧化物质在体内的作用方式，以及哪些地方的证据比宣传要弱。自由基也有有用的功能，抗氧化物质并非越多越好。",
    "Barry Halliwell이 항산화 물질이 몸에서 어떻게 작용하는지, 그리고 어디에서 근거가 광고보다 약한지 정리했습니다. 자유 라디칼도 유용한 역할을 하며, 항산화 물질이 많다고 반드시 좋은 것은 아닙니다.",
    "Barry Halliwell tổng quan cách chất chống oxy hóa hoạt động trong cơ thể và những chỗ bằng chứng yếu hơn lời quảng cáo. Gốc tự do cũng đảm nhận những việc hữu ích, và nhiều chất chống oxy hóa hơn không tự động tốt hơn.",
    "Barry Halliwell が、抗酸化物質が体内でどう働くか、そして根拠が宣伝ほど強くない点を総説しています。フリーラジカルにも有用な役割があり、抗酸化物質は多ければよいわけではありません。",
  ],
  ["Exercise keeps mitochondria healthy", "运动让线粒体保持健康", "운동이 미토콘드리아를 건강하게 지킨다", "Vận động giữ cho ty thể khỏe mạnh", "運動がミトコンドリアを健康に保つ"],
  [
    "A review of how physical activity builds and maintains healthy mitochondria in muscle. Movement remains the best-supported way to care for them.",
    "这篇综述介绍了身体活动如何在肌肉中建立并维持健康的线粒体。运动仍然是证据最充分的线粒体保养方式。",
    "신체 활동이 근육 속 미토콘드리아를 어떻게 만들고 건강하게 유지하는지 정리한 리뷰입니다. 움직임은 여전히 미토콘드리아를 돌보는 가장 근거가 탄탄한 방법입니다.",
    "Tổng quan về cách hoạt động thể chất xây dựng và duy trì ty thể khỏe mạnh trong cơ bắp. Vận động vẫn là cách chăm sóc ty thể có bằng chứng vững nhất.",
    "身体活動が筋肉の中で健康なミトコンドリアをつくり、保つ仕組みの総説です。運動は今も、ミトコンドリアを守る最も根拠のある方法です。",
  ],
  ["How the brain ages", "大脑如何老化", "뇌는 어떻게 늙어갈까", "Não bộ lão hóa như thế nào", "脳はどのように老いるのか"],
  [
    "Mattson and Arumugam describe the hallmarks of brain aging, including changes in energy metabolism and mitochondria. A map of the biology, not a treatment guide.",
    "Mattson 与 Arumugam 描述了大脑老化的标志，包括能量代谢和线粒体的变化。这是一张生物学地图，不是治疗指南。",
    "Mattson과 Arumugam이 에너지 대사와 미토콘드리아의 변화를 포함한 뇌 노화의 특징들을 설명합니다. 생물학의 지도이지 치료 안내서가 아닙니다.",
    "Mattson và Arumugam mô tả các dấu hiệu đặc trưng của lão hóa não, gồm những thay đổi trong chuyển hóa năng lượng và ty thể. Một bản đồ sinh học, không phải hướng dẫn điều trị.",
    "Mattson と Arumugam が、エネルギー代謝やミトコンドリアの変化を含む脳の老化の特徴を説明しています。生物学の地図であり、治療の手引きではありません。",
  ],
  ["Stress and your mitochondria", "压力与你的线粒体", "스트레스와 당신의 미토콘드리아", "Căng thẳng và ty thể của bạn", "ストレスとあなたのミトコンドリア"],
  [
    "Picard and McEwen propose a framework for how psychological stress affects mitochondria, drawn mostly from animal and cell studies. An idea being tested, not a settled fact.",
    "Picard 与 McEwen 提出了一个关于心理压力如何影响线粒体的框架，主要基于动物和细胞研究。这是一个仍在验证中的想法，不是定论。",
    "Picard와 McEwen이 주로 동물 및 세포 연구를 바탕으로 심리적 스트레스가 미토콘드리아에 미치는 영향에 대한 틀을 제안합니다. 검증 중인 가설이지 확정된 사실이 아닙니다.",
    "Picard và McEwen đề xuất một khung lý thuyết về cách căng thẳng tâm lý ảnh hưởng đến ty thể, chủ yếu dựa trên nghiên cứu trên động vật và tế bào. Một ý tưởng đang được kiểm chứng, chưa phải sự thật đã xác lập.",
    "Picard と McEwen が、主に動物・細胞研究をもとに、心理的ストレスがミトコンドリアに与える影響の枠組みを提案しています。検証中の考えであり、確定した事実ではありません。",
  ],
  ["Why mitochondria matter in aging", "线粒体为何在老化中如此重要", "노화에서 미토콘드리아가 중요한 이유", "Vì sao ty thể quan trọng trong lão hóa", "老化においてミトコンドリアが重要な理由"],
  [
    "Sun, Youle and Finkel review the evidence that mitochondrial decline is part of how cells age, and the open questions. Mechanisms, not a product claim.",
    "Sun、Youle 与 Finkel 综述了线粒体衰退是细胞老化一部分的证据，以及尚未解决的问题。讲的是机制，不是产品功效。",
    "Sun, Youle, Finkel이 미토콘드리아의 쇠퇴가 세포 노화의 일부라는 근거와 아직 남은 질문들을 정리합니다. 작용 원리에 관한 것이지 제품 효능 주장이 아닙니다.",
    "Sun, Youle và Finkel tổng quan bằng chứng cho thấy sự suy giảm của ty thể là một phần của quá trình lão hóa tế bào, cùng những câu hỏi còn bỏ ngỏ. Cơ chế, không phải tuyên bố về sản phẩm.",
    "Sun、Youle、Finkel が、ミトコンドリアの衰えが細胞の老化の一部であるという根拠と、未解決の問いを総説しています。仕組みの話であり、製品の効能ではありません。",
  ],
  ["How the brain uses energy", "大脑如何使用能量", "뇌는 에너지를 어떻게 쓸까", "Não bộ dùng năng lượng như thế nào", "脳はエネルギーをどう使うのか"],
  [
    "Magistretti and Allaman explain how brain cells produce and share energy. Background on why mental energy is, at bottom, a cellular question.",
    "Magistretti 与 Allaman 解释了脑细胞如何产生和分享能量。这是理解“精神能量归根结底是细胞问题”的背景知识。",
    "Magistretti와 Allaman이 뇌세포가 에너지를 만들고 나누는 방식을 설명합니다. 정신적 에너지가 결국 세포의 문제인 이유를 이해하는 배경 지식입니다.",
    "Magistretti và Allaman giải thích cách tế bào não tạo ra và chia sẻ năng lượng. Kiến thức nền về lý do năng lượng tinh thần, xét đến cùng, là câu chuyện của tế bào.",
    "Magistretti と Allaman が、脳細胞がエネルギーをつくり分け合う仕組みを説明しています。「メンタルのエネルギー」が結局は細胞の問題である理由の背景知識です。",
  ],
  ["Antioxidant pills and living longer", "抗氧化补充剂与长寿", "항산화 보충제와 더 오래 사는 것", "Viên chống oxy hóa và sống lâu hơn", "抗酸化サプリと長生き"],
  [
    "A review of 78 trials found no evidence that antioxidant supplements help people live longer, and a possible harm from beta-carotene and vitamin E at high doses. Balance for the whole topic.",
    "一项汇总 78 项试验的综述没有发现抗氧化补充剂能帮助人们更长寿的证据，而高剂量的 β-胡萝卜素和维生素 E 可能有害。这是整个话题的平衡视角。",
    "78건의 시험을 종합한 리뷰에서 항산화 보충제가 수명을 늘린다는 근거는 발견되지 않았고, 고용량 베타카로틴과 비타민 E는 오히려 해로울 가능성이 있었습니다. 이 주제 전체의 균형을 위한 자료입니다.",
    "Một tổng quan 78 thử nghiệm không tìm thấy bằng chứng rằng thực phẩm bổ sung chống oxy hóa giúp sống lâu hơn, và beta-carotene cùng vitamin E liều cao có thể gây hại. Góc nhìn cân bằng cho cả chủ đề.",
    "78 件の試験を検討したレビューでは、抗酸化サプリが長生きに役立つという根拠は見つからず、高用量のβカロテンとビタミンEには害の可能性が示されました。このテーマ全体のバランスを取る資料です。",
  ],
  ["Where the free-radical idea came from", "自由基理论从何而来", "자유 라디칼 이론은 어디서 시작됐나", "Ý tưởng về gốc tự do bắt nguồn từ đâu", "フリーラジカル説はどこから来たのか"],
  [
    "Denham Harman's original proposal that free radicals drive aging. Parts of the theory have since been revised, but it started the field.",
    "Denham Harman 最初提出自由基推动老化的观点。这一理论的部分内容后来已被修正，但它开创了这个领域。",
    "자유 라디칼이 노화를 이끈다는 Denham Harman의 최초 제안입니다. 이론의 일부는 이후 수정되었지만, 이 분야를 연 논문입니다.",
    "Đề xuất ban đầu của Denham Harman rằng gốc tự do thúc đẩy lão hóa. Một phần lý thuyết đã được điều chỉnh, nhưng chính nó đã mở ra lĩnh vực này.",
    "フリーラジカルが老化を進めるという Denham Harman の最初の提案です。理論の一部はその後修正されましたが、この分野の出発点となりました。",
  ],
  // Ingredients · NuriCell
  ["A companion study of the same two nutrients", "同样两种营养素的配套研究", "같은 두 영양소를 다룬 자매 연구", "Nghiên cứu song hành về cùng hai dưỡng chất", "同じ2つの栄養素の姉妹研究"],
  [
    "Hagen and colleagues, in a companion paper to the Liu study, tested acetyl-L-carnitine and lipoic acid in aging animals and measured metabolic function and oxidative stress. An animal study, not a human trial.",
    "Hagen 及同事在与 Liu 研究配套的论文中，在老龄动物中测试了乙酰左旋肉碱和硫辛酸，并测量代谢功能和氧化应激。这是动物研究，不是人体试验。",
    "Hagen과 동료들은 Liu 연구의 자매 논문에서 노화한 동물에서 아세틸-L-카르니틴과 리포산을 시험하고 대사 기능과 산화 스트레스를 측정했습니다. 동물 연구이며, 인체 시험이 아닙니다.",
    "Hagen và cộng sự, trong bài báo song hành với nghiên cứu của Liu, thử nghiệm acetyl-L-carnitine và acid lipoic trên động vật lớn tuổi rồi đo chức năng chuyển hóa và stress oxy hóa. Một nghiên cứu trên động vật, không phải thử nghiệm trên người.",
    "Hagen らは Liu 研究の姉妹論文で、老齢の動物でアセチル-L-カルニチンとリポ酸を試験し、代謝機能と酸化ストレスを測定しました。動物研究であり、ヒト試験ではありません。",
  ],
  ["Dr. Liu on lipoic acid and the aging brain", "刘博士谈硫辛酸与老化的大脑", "리우 박사가 말하는 리포산과 노화하는 뇌", "Tiến sĩ Liu về acid lipoic và bộ não lão hóa", "劉博士が語るリポ酸と老化する脳"],
  [
    "An overview by Dr. Jiankang Liu of how alpha-lipoic acid may support aging mitochondria and memory in animal studies. Written by our scientist; mostly animal work.",
    "刘健康博士综述了 α-硫辛酸在动物研究中如何可能支持老化的线粒体和记忆。由我们的科学家撰写，主要基于动物研究。",
    "리우 젠캉 박사가 알파리포산이 동물 연구에서 노화하는 미토콘드리아와 기억을 어떻게 도울 수 있는지 정리한 개관입니다. 우리 과학자가 썼으며, 대부분 동물 연구입니다.",
    "Tổng quan của Tiến sĩ Jiankang Liu về cách acid alpha-lipoic có thể hỗ trợ ty thể lão hóa và trí nhớ trong các nghiên cứu trên động vật. Do nhà khoa học của chúng tôi viết; chủ yếu là nghiên cứu trên động vật.",
    "劉健康博士による、αリポ酸が動物研究で老化するミトコンドリアと記憶をどう支えうるかの概説です。当社の科学者によるもので、主に動物研究です。",
  ],
  ["Creatine and thinking in healthy adults", "肌酸与健康成年人的思维能力", "크레아틴과 건강한 성인의 사고력", "Creatine và khả năng tư duy ở người trưởng thành khỏe mạnh", "クレアチンと健康な成人の思考力"],
  [
    "A systematic review of six small trials found creatine may help short-term memory and reasoning in healthy people, with mixed results elsewhere. Small studies; more work needed.",
    "一项系统综述汇总了六项小型试验，发现肌酸可能有助于健康人的短期记忆和推理能力，其他方面结果不一。研究规模小，仍需更多研究。",
    "6건의 소규모 시험을 종합한 체계적 리뷰에서 크레아틴이 건강한 사람의 단기 기억과 추론에 도움이 될 수 있고, 다른 영역은 결과가 엇갈렸습니다. 소규모 연구이며 더 많은 연구가 필요합니다.",
    "Một tổng quan hệ thống sáu thử nghiệm nhỏ cho thấy creatine có thể giúp trí nhớ ngắn hạn và khả năng suy luận ở người khỏe mạnh, các kết quả khác chưa thống nhất. Nghiên cứu nhỏ; cần thêm bằng chứng.",
    "6 件の小規模試験の系統的レビューで、クレアチンは健康な人の短期記憶と推論を助ける可能性があり、他の面では結果がまちまちでした。小規模な研究であり、さらなる検証が必要です。",
  ],
  ["Lipoic acid as a supplement", "作为补充剂的硫辛酸", "보충제로서의 리포산", "Acid lipoic dưới dạng thực phẩm bổ sung", "サプリメントとしてのリポ酸"],
  [
    "Shay and colleagues review what lipoic acid does in the body and what supplement studies suggest. Mechanisms are clearer than human benefits.",
    "Shay 及同事综述了硫辛酸在体内的作用以及补充剂研究的提示。其作用机制比对人的益处更清楚。",
    "Shay와 동료들이 리포산이 몸에서 하는 일과 보충제 연구가 시사하는 바를 정리합니다. 작용 원리는 사람에서의 이점보다 더 분명합니다.",
    "Shay và cộng sự tổng quan acid lipoic làm gì trong cơ thể và các nghiên cứu về bổ sung gợi ý điều gì. Cơ chế rõ hơn lợi ích trên người.",
    "Shay らが、リポ酸が体内で果たす働きとサプリ研究の示唆を総説しています。仕組みは、人での効果よりも明確です。",
  ],
  ["Acetyl-L-carnitine in mild memory problems", "乙酰左旋肉碱与轻度记忆问题", "가벼운 기억 문제와 아세틸-L-카르니틴", "Acetyl-L-carnitine ở người có vấn đề trí nhớ nhẹ", "軽い記憶の問題とアセチル-L-カルニチン"],
  [
    "A meta-analysis of trials in people with mild cognitive impairment or mild Alzheimer's disease reported a benefit over placebo. Patients, not healthy adults; older trials.",
    "一项荟萃分析汇总了轻度认知障碍或轻度阿尔茨海默病患者的试验，报告其效果优于安慰剂。对象是患者而非健康成年人，且试验年代较早。",
    "경도인지장애 또는 경증 알츠하이머병 환자 대상 시험들을 종합한 메타분석에서 위약보다 나은 효과가 보고되었습니다. 건강한 성인이 아닌 환자이며, 오래된 시험들입니다.",
    "Một phân tích gộp các thử nghiệm ở người suy giảm nhận thức nhẹ hoặc Alzheimer nhẹ báo cáo lợi ích so với giả dược. Bệnh nhân, không phải người trưởng thành khỏe mạnh; các thử nghiệm đã cũ.",
    "軽度認知障害または軽度アルツハイマー病の患者を対象とした試験のメタ解析で、プラセボを上回る効果が報告されました。健康な成人ではなく患者であり、古い試験です。",
  ],
  ["Acetyl-L-carnitine for dementia", "乙酰左旋肉碱与痴呆症", "치매와 아세틸-L-카르니틴", "Acetyl-L-carnitine cho chứng sa sút trí tuệ", "認知症とアセチル-L-カルニチン"],
  [
    "A Cochrane review found no clear evidence of benefit in dementia. Shown beside the pooled trials above so both readings are visible.",
    "一项 Cochrane 系统综述没有发现其对痴呆症有明确益处的证据。与上面的试验汇总并列展示，让两种解读都能看到。",
    "코크란 리뷰에서는 치매에 대한 분명한 이점의 근거를 찾지 못했습니다. 위의 통합 분석과 나란히 두어 두 가지 해석을 모두 볼 수 있게 했습니다.",
    "Một tổng quan Cochrane không tìm thấy bằng chứng rõ ràng về lợi ích trong sa sút trí tuệ. Đặt cạnh phân tích gộp ở trên để cả hai cách đọc đều được thấy.",
    "コクランレビューでは、認知症に対する明確な効果の根拠は見つかりませんでした。上の統合解析と並べて示し、両方の読み方が見えるようにしています。",
  ],
  // Ingredients · Turmerific
  ["Longvida curcumin in healthy older adults", "Longvida 姜黄素与健康老年人", "건강한 노년층과 Longvida 커큐민", "Curcumin Longvida ở người lớn tuổi khỏe mạnh", "健康な高齢者と Longvida クルクミン"],
  [
    "Cox and colleagues gave 60 healthy adults aged 60 to 85 the Longvida curcumin preparation for four weeks and reported changes in attention, working memory and mood. The same preparation Turmerific uses; a small, short study.",
    "Cox 及同事让 60 名 60 至 85 岁的健康成年人服用 Longvida 姜黄素制剂四周，报告了注意力、工作记忆和情绪的变化。这正是 Turmerific 所用的制剂；研究规模小、时间短。",
    "Cox와 동료들은 60~85세 건강한 성인 60명에게 Longvida 커큐민 제제를 4주간 주고 주의력, 작업 기억, 기분의 변화를 보고했습니다. Turmerific이 쓰는 것과 같은 제제이며, 작고 짧은 연구입니다.",
    "Cox và cộng sự cho 60 người trưởng thành khỏe mạnh từ 60 đến 85 tuổi dùng chế phẩm curcumin Longvida trong bốn tuần và báo cáo thay đổi về sự chú ý, trí nhớ làm việc và tâm trạng. Cùng chế phẩm Turmerific sử dụng; một nghiên cứu nhỏ và ngắn.",
    "Cox らは 60〜85 歳の健康な成人 60 人に Longvida クルクミン製剤を 4 週間与え、注意力・作業記憶・気分の変化を報告しました。Turmerific が使うのと同じ製剤で、小規模かつ短期の研究です。",
  ],
  ["A curcumin form and memory", "一种姜黄素制剂与记忆", "한 커큐민 제제와 기억력", "Một dạng curcumin và trí nhớ", "あるクルクミン製剤と記憶"],
  [
    "Small and colleagues followed 40 adults without dementia for 18 months on a different curcumin preparation, Theracurmin, and reported memory changes. Another preparation, a small group.",
    "Small 及同事让 40 名无痴呆的成年人服用另一种姜黄素制剂 Theracurmin 并随访 18 个月，报告了记忆变化。制剂不同，样本量小。",
    "Small과 동료들은 치매가 없는 성인 40명에게 다른 커큐민 제제인 Theracurmin을 18개월간 주고 기억력 변화를 보고했습니다. 다른 제제이며, 작은 집단입니다.",
    "Small và cộng sự theo dõi 40 người trưởng thành không sa sút trí tuệ trong 18 tháng với một chế phẩm curcumin khác, Theracurmin, và báo cáo thay đổi về trí nhớ. Chế phẩm khác, nhóm nhỏ.",
    "Small らは認知症のない成人 40 人に別のクルクミン製剤 Theracurmin を 18 か月間与え、記憶の変化を報告しました。別の製剤で、小さな集団です。",
  ],
  ["Curcumin's chemistry problem", "姜黄素的化学难题", "커큐민의 화학적 난제", "Vấn đề hóa học của curcumin", "クルクミンの化学的な問題"],
  [
    "Nelson and colleagues explain why curcumin is poorly absorbed and why many laboratory results have not held up. A skeptical review, included on purpose.",
    "Nelson 及同事解释了姜黄素为何难以吸收，以及为何许多实验室结果未能经受验证。这是一篇持怀疑态度的综述，我们特意收录。",
    "Nelson과 동료들이 커큐민이 잘 흡수되지 않는 이유와 많은 실험실 결과가 재현되지 않은 이유를 설명합니다. 회의적인 리뷰이며, 일부러 실었습니다.",
    "Nelson và cộng sự giải thích vì sao curcumin hấp thu kém và vì sao nhiều kết quả trong phòng thí nghiệm không đứng vững. Một tổng quan hoài nghi, được đưa vào có chủ đích.",
    "Nelson らが、クルクミンが吸収されにくい理由と、多くの実験室での結果が再現されなかった理由を説明しています。懐疑的な総説で、あえて掲載しています。",
  ],
  // Ingredients · Advanced OPC Formula
  ["Grape seed extract and blood pressure", "葡萄籽提取物与血压", "포도씨 추출물과 혈압", "Chiết xuất hạt nho và huyết áp", "ブドウ種子エキスと血圧"],
  [
    "A meta-analysis of nine trials found a modest drop in systolic blood pressure and heart rate with grape seed extract, and no change in cholesterol. Modest effects in short trials.",
    "一项汇总九项试验的荟萃分析发现，葡萄籽提取物使收缩压和心率略有下降，胆固醇没有变化。短期试验中的效果有限。",
    "9건의 시험을 종합한 메타분석에서 포도씨 추출물이 수축기 혈압과 심박수를 약간 낮췄고, 콜레스테롤에는 변화가 없었습니다. 짧은 시험에서의 작은 효과입니다.",
    "Một phân tích gộp chín thử nghiệm cho thấy chiết xuất hạt nho làm giảm nhẹ huyết áp tâm thu và nhịp tim, không thay đổi cholesterol. Hiệu quả khiêm tốn trong các thử nghiệm ngắn.",
    "9 件の試験のメタ解析で、ブドウ種子エキスにより収縮期血圧と心拍数がわずかに下がり、コレステロールは変わりませんでした。短期試験でのささやかな効果です。",
  ],
  ["Pine bark extract: a trial that found nothing", "松树皮提取物：一项没有发现效果的试验", "소나무 껍질 추출물: 효과를 찾지 못한 시험", "Chiết xuất vỏ thông: một thử nghiệm không thấy tác dụng", "松樹皮エキス：効果が見られなかった試験"],
  [
    "A 12-week trial of pine bark extract in 130 adults found no effect on blood pressure, cholesterol or other heart-risk markers. A null result, shown because honesty matters.",
    "一项对 130 名成年人进行的 12 周松树皮提取物试验，没有发现其对血压、胆固醇或其他心脏风险指标有影响。这是一个阴性结果，出于诚实我们予以展示。",
    "성인 130명을 대상으로 한 12주간의 소나무 껍질 추출물 시험에서 혈압, 콜레스테롤, 기타 심장 위험 지표에 효과가 없었습니다. 정직함이 중요하기에 보여 드리는 무효 결과입니다.",
    "Một thử nghiệm 12 tuần với chiết xuất vỏ thông trên 130 người trưởng thành không thấy tác dụng lên huyết áp, cholesterol hay các chỉ số nguy cơ tim mạch khác. Một kết quả âm tính, được đưa ra vì sự trung thực.",
    "成人 130 人を対象にした 12 週間の松樹皮エキス試験では、血圧、コレステロール、その他の心血管リスク指標に効果は見られませんでした。誠実さのために示す、効果なしの結果です。",
  ],
  // Ingredients · Green Bee Propolis
  ["Artepillin C, the key compound in green propolis", "Artepillin C：绿蜂胶的关键成分", "그린 프로폴리스의 핵심 성분 아르테필린 C", "Artepillin C, hợp chất chính trong keo ong xanh", "グリーンプロポリスの主要成分アルテピリン C"],
  [
    "A review of the chemistry, absorption and laboratory findings for artepillin C, the compound Brazilian green propolis is known for. Mostly laboratory studies; few human trials.",
    "这篇综述介绍了巴西绿蜂胶的标志性成分 artepillin C 的化学性质、吸收情况和实验室研究结果。主要是实验室研究，人体试验很少。",
    "브라질 그린 프로폴리스로 잘 알려진 성분 아르테필린 C의 화학적 성질, 흡수, 실험실 연구 결과를 정리한 리뷰입니다. 대부분 실험실 연구이며 인체 시험은 적습니다.",
    "Tổng quan về hóa học, khả năng hấp thu và các phát hiện trong phòng thí nghiệm của artepillin C, hợp chất làm nên tên tuổi keo ong xanh Brazil. Chủ yếu là nghiên cứu trong phòng thí nghiệm; ít thử nghiệm trên người.",
    "ブラジル産グリーンプロポリスで知られる成分アルテピリン C の化学、吸収、実験室での知見の総説です。主に実験室研究で、ヒト試験は少数です。",
  ],
  ["What has been tested about propolis", "蜂胶已被验证过什么", "프로폴리스에 대해 무엇이 검증되었나", "Keo ong đã được kiểm chứng những gì", "プロポリスについて検証されてきたこと"],
  [
    "A review of experimental studies on propolis from different regions. Composition varies with the plants bees visit, so results do not transfer between products.",
    "这篇综述汇总了不同地区蜂胶的实验研究。蜂胶成分随蜜蜂采集的植物而异，因此结果不能在不同产品之间套用。",
    "여러 지역 프로폴리스에 대한 실험 연구를 정리한 리뷰입니다. 성분은 벌이 찾는 식물에 따라 달라지므로, 결과가 제품 간에 그대로 옮겨지지 않습니다.",
    "Tổng quan các nghiên cứu thực nghiệm về keo ong từ nhiều vùng khác nhau. Thành phần thay đổi theo loài cây ong ghé thăm, nên kết quả không chuyển từ sản phẩm này sang sản phẩm khác.",
    "各地域のプロポリスに関する実験研究の総説です。成分はミツバチが訪れる植物によって変わるため、結果は製品間でそのまま当てはまりません。",
  ],
  // Ingredients · Nature Calm
  ["CoQ10 in aging", "辅酶 Q10 与老化", "노화와 코엔자임 Q10", "CoQ10 trong lão hóa", "老化とコエンザイム Q10"],
  [
    "A review of coenzyme Q10's role in cellular energy and what supplement trials in aging and disease have shown. Mixed trial results.",
    "这篇综述介绍了辅酶 Q10 在细胞能量中的作用，以及在老化和疾病方面补充剂试验的结果。试验结果不一。",
    "코엔자임 Q10이 세포 에너지에서 하는 역할과, 노화 및 질병에서의 보충제 시험 결과를 정리한 리뷰입니다. 시험 결과는 엇갈립니다.",
    "Tổng quan về vai trò của coenzyme Q10 trong năng lượng tế bào và kết quả các thử nghiệm bổ sung trong lão hóa và bệnh tật. Kết quả thử nghiệm chưa thống nhất.",
    "コエンザイム Q10 の細胞エネルギーでの役割と、老化や疾患におけるサプリ試験の結果の総説です。試験結果はまちまちです。",
  ],
  ["L-theanine and everyday stress", "L-茶氨酸与日常压力", "L-테아닌과 일상의 스트레스", "L-theanine và căng thẳng hằng ngày", "L-テアニンと日常のストレス"],
  [
    "Thirty healthy adults took L-theanine for four weeks and reported fewer stress-related symptoms than on placebo. Small and short; healthy volunteers.",
    "30 名健康成年人服用 L-茶氨酸四周，报告的压力相关症状少于服用安慰剂时。研究规模小、时间短，对象为健康志愿者。",
    "건강한 성인 30명이 L-테아닌을 4주간 복용하고 위약 때보다 스트레스 관련 증상이 적었다고 보고했습니다. 작고 짧은 연구이며, 건강한 자원자 대상입니다.",
    "Ba mươi người trưởng thành khỏe mạnh dùng L-theanine trong bốn tuần và báo cáo ít triệu chứng liên quan đến căng thẳng hơn so với giả dược. Nhỏ và ngắn; tình nguyện viên khỏe mạnh.",
    "健康な成人 30 人が L-テアニンを 4 週間摂取し、プラセボ時よりストレス関連症状が少なかったと報告しました。小規模かつ短期で、健康なボランティアが対象です。",
  ],
  ["Phosphatidylserine and memory complaints", "磷脂酰丝氨酸与记忆困扰", "포스파티딜세린과 기억력 고민", "Phosphatidylserine và than phiền về trí nhớ", "ホスファチジルセリンと記憶の悩み"],
  [
    "Seventy-eight older Japanese adults with memory complaints took soybean phosphatidylserine for six months; those with lower scores at the start improved more. One trial, one group.",
    "78 名有记忆困扰的日本老年人服用大豆磷脂酰丝氨酸六个月；起始分数较低者改善更明显。仅一项试验、一个人群。",
    "기억력 고민이 있는 일본 노인 78명이 대두 포스파티딜세린을 6개월간 복용했고, 시작 점수가 낮았던 사람들이 더 많이 나아졌습니다. 시험 하나, 집단 하나입니다.",
    "Bảy mươi tám người cao tuổi Nhật Bản có than phiền về trí nhớ dùng phosphatidylserine từ đậu nành trong sáu tháng; những người có điểm thấp lúc đầu cải thiện nhiều hơn. Một thử nghiệm, một nhóm.",
    "記憶の悩みを持つ日本の高齢者 78 人が大豆由来ホスファチジルセリンを 6 か月摂取し、開始時の点数が低かった人ほど改善しました。1 つの試験、1 つの集団です。",
  ],
  // Guides
  ["What do we know about healthy aging?", "关于健康老龄化，我们知道什么？", "건강한 노화에 대해 무엇을 알고 있을까?", "Chúng ta biết gì về lão hóa khỏe mạnh?", "健やかな加齢について何がわかっているか"],
  [
    "The National Institute on Aging sums up what research says about staying healthy as we age: movement, food, sleep, connection, and what remains uncertain.",
    "美国国家老龄化研究所总结了关于健康老龄化的研究结论：运动、饮食、睡眠、人际联系，以及仍不确定的部分。",
    "미국 국립노화연구소가 나이 들어도 건강을 지키는 것에 대해 연구가 말해 주는 것들을 정리합니다: 움직임, 음식, 수면, 사람과의 연결, 그리고 아직 불확실한 것들.",
    "Viện Quốc gia về Lão hóa Hoa Kỳ tóm tắt những gì nghiên cứu nói về việc giữ sức khỏe khi già đi: vận động, ăn uống, giấc ngủ, kết nối, và những điều còn chưa chắc chắn.",
    "米国国立加齢研究所が、年齢を重ねても健康でいることについて研究が示すことをまとめています：運動、食事、睡眠、人とのつながり、そしてまだ不確かなこと。",
  ],
  ["Cognitive health and older adults", "认知健康与老年人", "인지 건강과 노년층", "Sức khỏe nhận thức và người cao tuổi", "認知の健康と高齢者"],
  [
    "The National Institute on Aging on what helps keep thinking skills as we age, and which claims are not backed by evidence.",
    "美国国家老龄化研究所介绍了随着年龄增长如何保持思维能力，以及哪些说法缺乏证据支持。",
    "미국 국립노화연구소가 나이 들며 사고력을 지키는 데 도움이 되는 것과, 근거가 없는 주장들을 설명합니다.",
    "Viện Quốc gia về Lão hóa Hoa Kỳ về những gì giúp giữ khả năng tư duy khi già đi, và những tuyên bố nào không có bằng chứng.",
    "米国国立加齢研究所による、加齢とともに思考力を保つのに役立つことと、根拠のない主張についての解説です。",
  ],
  ["Dietary supplements: what you need to know", "膳食补充剂：你需要知道的事", "보충제: 알아 두어야 할 것", "Thực phẩm bổ sung: những điều bạn cần biết", "サプリメント：知っておきたいこと"],
  [
    "The Office of Dietary Supplements explains how supplements are regulated, how to read a label, and the questions to ask before taking one.",
    "美国膳食补充剂办公室解释了补充剂如何受到监管、如何阅读标签，以及服用前应当问的问题。",
    "미국 국립보건원 보충제사무국이 보충제가 어떻게 규제되는지, 라벨을 어떻게 읽는지, 복용 전에 무엇을 물어야 하는지 설명합니다.",
    "Văn phòng Thực phẩm bổ sung Hoa Kỳ giải thích thực phẩm bổ sung được quản lý ra sao, cách đọc nhãn, và những câu hỏi cần đặt ra trước khi dùng.",
    "米国栄養補助食品局が、サプリメントがどう規制されているか、ラベルの読み方、摂取前に確認すべき質問を説明しています。",
  ],
  ["Turmeric", "姜黄", "강황", "Nghệ", "ウコン"],
  [
    "What is known about turmeric and curcumin, how well they are absorbed, and safety notes, from the National Center for Complementary and Integrative Health.",
    "美国国家补充与整合健康中心介绍了关于姜黄和姜黄素的已知信息、吸收情况以及安全注意事项。",
    "미국 국립보완통합건강센터가 강황과 커큐민에 대해 알려진 것, 흡수 정도, 안전 관련 유의점을 설명합니다.",
    "Những gì đã biết về nghệ và curcumin, khả năng hấp thu và lưu ý an toàn, từ Trung tâm Quốc gia về Sức khỏe Bổ sung và Tích hợp Hoa Kỳ.",
    "米国国立補完統合衛生センターによる、ウコンとクルクミンについてわかっていること、吸収の程度、安全性の注意点です。",
  ],
  ["Grape seed extract", "葡萄籽提取物", "포도씨 추출물", "Chiết xuất hạt nho", "ブドウ種子エキス"],
  [
    "A plain summary of the research on grape seed extract and its safety.",
    "关于葡萄籽提取物研究及其安全性的通俗概述。",
    "포도씨 추출물 연구와 안전성에 대한 쉬운 요약입니다.",
    "Tóm tắt dễ hiểu về nghiên cứu chiết xuất hạt nho và tính an toàn của nó.",
    "ブドウ種子エキスの研究と安全性についてのわかりやすいまとめです。",
  ],
  ["Choline", "胆碱", "콜린", "Choline", "コリン"],
  [
    "A consumer fact sheet on choline: what it does, how much people need, and food sources.",
    "面向消费者的胆碱资料：它的作用、人体需要量以及食物来源。",
    "소비자를 위한 콜린 자료: 하는 일, 필요한 양, 음식 급원.",
    "Tờ thông tin cho người tiêu dùng về choline: tác dụng, lượng cần thiết và nguồn thực phẩm.",
    "コリンについての消費者向け資料：働き、必要量、食品からの摂取源。",
  ],
  ["Carnitine", "肉碱", "카르니틴", "Carnitine", "カルニチン"],
  [
    "A fact sheet for health professionals on carnitine, including acetyl-L-carnitine, and what studies have looked at.",
    "面向专业人士的肉碱资料，包括乙酰左旋肉碱，以及相关研究考察过的内容。",
    "아세틸-L-카르니틴을 포함한 카르니틴에 대한 전문가용 자료와 연구들이 살펴본 내용입니다.",
    "Tờ thông tin dành cho chuyên gia y tế về carnitine, gồm acetyl-L-carnitine, và những gì các nghiên cứu đã xem xét.",
    "アセチル-L-カルニチンを含むカルニチンについての専門家向け資料と、研究が調べてきた内容です。",
  ],
  ["Antioxidants", "抗氧化物质", "항산화 물질", "Chất chống oxy hóa", "抗酸化物質"],
  [
    "The National Library of Medicine's plain introduction to antioxidants and free radicals.",
    "美国国家医学图书馆对抗氧化物质和自由基的通俗介绍。",
    "미국 국립의학도서관의 항산화 물질과 자유 라디칼에 대한 쉬운 소개입니다.",
    "Giới thiệu dễ hiểu của Thư viện Y khoa Quốc gia Hoa Kỳ về chất chống oxy hóa và gốc tự do.",
    "米国国立医学図書館による、抗酸化物質とフリーラジカルのわかりやすい入門です。",
  ],
];
const path = "src/i18n/copy-keys.json";
const keys = JSON.parse(fs.readFileSync(path, "utf8"));
const locales = ["en", "cns", "kr", "vn", "jp"];
const catalogs = locales.map((l) => JSON.parse(fs.readFileSync("messages/" + l + ".json", "utf8")));
let next = Math.max(...Object.values(keys).map((k) => Number(k.slice(1)))) + 1;
let added = 0;
for (const row of entries) {
  if (row.length !== 5) throw new Error("Row needs five languages: " + row[0]);
  if (keys[row[0]]) continue; // never overwrite an existing translation
  const key = "m" + next++;
  keys[row[0]] = key;
  row.forEach((value, i) => {
    catalogs[i].Copy[key] = value;
  });
  added += 1;
}
fs.writeFileSync(path, JSON.stringify(keys, null, 2) + "\n");
locales.forEach((l, i) => fs.writeFileSync("messages/" + l + ".json", JSON.stringify(catalogs[i], null, 2) + "\n"));
console.log("Added " + added + " research list strings in five languages; next id m" + next);
