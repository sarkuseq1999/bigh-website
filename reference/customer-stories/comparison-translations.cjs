const fs=require('node:fs');
const entries=[
  [
    "Choose a design",
    "选择设计",
    "디자인 선택",
    "Chọn thiết kế",
    "デザインを選ぶ"
  ],
  [
    "Testimonial design choices",
    "评价区设计选项",
    "후기 디자인 선택",
    "Các mẫu thiết kế lời nhận xét",
    "体験談のデザイン案"
  ],
  [
    "Daybook",
    "日常手记",
    "일상 노트",
    "Nhật ký",
    "日々のノート"
  ],
  [
    "Story Wall",
    "故事墙",
    "이야기 벽",
    "Góc chuyện kể",
    "ストーリーウォール"
  ],
  [
    "Spotlight",
    "聚光时刻",
    "스포트라이트",
    "Điểm nhấn",
    "スポットライト"
  ],
  [
    "Illustrative scenes. Sample stories for design review.",
    "场景仅为艺术示意。故事为设计评审示例。",
    "분위기 연출 이미지입니다. 디자인 검토용 예시 이야기입니다.",
    "Hình ảnh minh họa. Câu chuyện mẫu để xem xét thiết kế.",
    "イメージ画像。デザイン確認用のサンプルストーリーです。"
  ],
  [
    "All three sample stories are shown.",
    "已显示全部三个示例故事。",
    "세 가지 예시 이야기가 모두 표시됩니다.",
    "Đang hiển thị cả ba câu chuyện mẫu.",
    "3つのサンプルストーリーをすべて表示しています。"
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
console.log('Updated '+entries.length+' design comparison strings in five languages.');
