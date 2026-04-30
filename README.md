# met_term

Meteorological term workspace.

## v1.0

首個可用版本，完成氣象術語站的基礎建置、字母分頁、搜尋效能優化，以及來源連結補強。

### 版本內容
- 建立 `met_term` GitHub Pages 網站
- 完成大量氣象術語的繁體中文翻譯與中文辭典式解釋
- 已整合目前站內術語資料（約 9431 筆）
- 建立字母分頁架構：首頁、全部頁、各字母頁
- 加入搜尋、分頁、字母導覽
- 針對大資料量做前端載入優化
- 為詞條補上可點擊的「參考來源」連結，並以新分頁開啟
- 固定網站視覺風格與標題設定

### 網站特色
- **首頁入口化**：不預載全量資料，降低初始載入壓力
- **字母頁載入**：按字母讀取對應 JSON，提高大資料量下的可用性
- **全站總表**：保留 `all.html` 供完整檢索
- **繁體中文呈現**：以科技文青溫暖風格建構氣象辭典網站

### 連結
- GitHub Pages 首頁：<https://tdd-ceo-claw.github.io/met_term/>
- GitHub Pages 全部頁：<https://tdd-ceo-claw.github.io/met_term/all.html>
- GitHub Release：<https://github.com/tdd-ceo-claw/met_term/releases/tag/v1.0>
