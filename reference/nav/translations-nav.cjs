// Adds the menu bar's (October 5, 2026) two new words to the five catalogs (m585, m586): the
// narrow window's menu button says "Menu", and "Close" while its sheet is open (its accessible
// names stay the existing "Open menu" / "Close menu"). DRAFT translations, not native-reviewed;
// they follow the catalogs' own "Open menu" / "Close menu" (m224, m225). hken.json stays {}
// (/hken redirects to /cns). Run once from the repo root (a key already present is reused):
//   node reference/nav/translations-nav.cjs
// Row order: [en, cns (Simplified Chinese), kr, vn, jp]
const fs = require("node:fs");
const entries = [
  ["Menu", "菜单", "메뉴", "Menu", "メニュー"],
  ["Close", "关闭", "닫기", "Đóng", "閉じる"],
];
const path = "src/i18n/copy-keys.json";
const keys = JSON.parse(fs.readFileSync(path, "utf8"));
const locales = ["en", "cns", "kr", "vn", "jp"];
const catalogs = locales.map((l) => JSON.parse(fs.readFileSync("messages/" + l + ".json", "utf8")));
let next = Math.max(...Object.values(keys).map((k) => Number(k.slice(1)))) + 1;
const added = [];
for (const row of entries) {
  const key = keys[row[0]] ?? "m" + next++;
  keys[row[0]] = key;
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
console.log("next id m" + next);
