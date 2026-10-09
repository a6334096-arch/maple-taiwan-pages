# 楓景｜台灣賞楓與秋色查詢

公開網站：https://maple-taiwan-responsive.a6334096.chatgpt.site

手機與電腦皆可使用。現有 29 處具官方賞楓或秋色介紹的景點，依景點本身的可核對資料篩選。支援名稱搜尋（台／臺皆可）、
地區與縣市篩選、月份參考、收藏、縮放與密集景點群組。
台灣海岸線採 Natural Earth，景點使用官方經緯度；步道圖示為入口代表點。

一般賞楓月份與有日期的楓況公告分開顯示。季節參考不代表目前已轉紅；
缺少可靠官方觀測時顯示「尚無資料」。主地圖以賞楓為主，純銀杏或山毛櫸秋色景點移出。

## GitHub 自動備份設定（已備妥，上傳後才啟用）

1. 將本專案內容（包含 `.github/workflows/sync-maple-data.yml`）放到 GitHub
   儲存庫的**預設分支**；不要只上傳 ZIP 檔，也不要漏掉 `.github` 資料夾。
2. 在儲存庫 **Settings → Actions → General** 允許 Actions 執行，並在
   **Workflow permissions** 選擇 **Read and write permissions**。
   若組織政策或受保護分支禁止機器人直接提交，須由管理者允許此備份流程寫入。
3. 開啟 **Actions → 同步台灣賞楓資料 → Run workflow**，手動執行一次。
   確認成功後，在 `data/current/` 查看三個 JSON 檔及提交歷史。
4. 之後依排程每天台灣時間約 **08:30** 同步，**10:30** 再補同步一次。
   實際執行可能延後；GitHub 公開儲存庫 60 天沒有活動時可能停用排程，
   可在 Actions 重新啟用。這些設定尚未在使用者 GitHub 帳戶中啟用。

流程使用 GitHub 自帶的 `GITHUB_TOKEN` 提交同一儲存庫，不需要新增 PAT、
網站更新金鑰或私人更新入口憑證。只讀取網站公開 JSON，不會修改網站楓況。
網站每天上午 08:00（台灣時間）由既有獨立排程查核官方來源；GitHub 流程
將當時可讀取的網站資料備份到版本紀錄。它不會自行查核官方來源，
也不把舊資料、查核日期或備份時間當作今天的觀測。

若網站查核未完成，GitHub 仍備份當時的最近資料，保留來源與原有日期。
下載失敗、內容不是 JSON、儲存失敗或缺少景點資料時，流程失敗而不提交；
三份資料全部驗證完成後才寫入。沒有內容變化時不新增提交。

| 檔案 | 用途 |
| --- | --- |
| `data/current/places.json` | 網站最新景點目錄與地理座標 |
| `data/current/seasons.json` | 最新一般賞楓月份、官方來源與季節查核紀錄 |
| `data/current/foliage.json` | 官方有日期的楓況紀錄，以及楓況查核紀錄 |
| `web/places.json`、`web/seasons.json` | 網站原始目錄與季節初始資料 |
| `.github/workflows/sync-maple-data.yml` | GitHub 排程／手動同步設定 |
| `scripts/sync-github-data.py` | 公開 JSON 下載、驗證及備份 |

網站程式碼修改後仍需重新部署；GitHub 備份不會把程式碼自動部署回網站。
`data/current/` 是資料快照，`web/` 是網站原始檔，兩者用途不同。

## 本機使用

僅預覽介面可用 `python -m http.server 8000 --directory web`；即時楓況端點
與自動更新儲存功能由部署後的 Worker 提供，本機靜態預覽不含這些端點。

手動備份（Python 3.10 以上，無額外套件）：

```bash
python scripts/sync-github-data.py
```

重新產生地理 SVG：`python scripts/generate-map.py`。
建置 Worker：`node scripts/generate-worker.mjs`、`bash scripts/build.sh`。
驗證部署產物：`node scripts/validate-artifact.mjs`。

海岸線與官方座標來源見 `data/MAP-SOURCES.md`。

GitHub 官方說明：[排程與手動執行](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)。

## 歷年賞楓時間參考

2026-10-07 補充 13 處景點季節資料，其中 12 處新增明確月份，另 1 處為開始月份參考。目前 29 處中有 21 處具可用月份範圍。資料使用官方景點介紹、官方季節攻略、大學季節年表與已標示年度的過往官方刊載紀錄。較早期的年表、單一年度案例、區域遊程及特定步道範圍均在 note 說明，不視為逐年保證或實際楓況。尚無明確證據的景點維持月份待確認。

部署更新會將較新的研究資料套用至較舊的缺月分紀錄；較新的自動查核與所有實際楓況紀錄保留。GitHub 既有同步工作會下載更新後的公開 seasons.json 到 data/current；它不會自動同步此網站的原始碼修改。

## 景點樹種與歷年照片

每個景點資訊欄均含樹種與歷年影像欄位。來源與授權記錄見 `data/PHOTO-SOURCES.md`、`web/places.json`。資料待補時不推測品種或以其他景點代替；歷年影像不代表最新楓況。新增照片與樹種需人工查核，不會由既有楓況同步程序自動新增。

### 選擇性地名底圖

道路底圖使用 OpenFreeMap 向量圖（MapLibre GL JS），載入前移除所有 symbol 圖層，地名由已收錄且符合篩選的景點資料建立。縣市有景點即可顯示，不要求已有近期轉紅紀錄；放大後显示獨立景點名稱並避開重疊。道路底圖以原有台灣海岸線裁切，外站或 WebGL 無法使用時回到簡約底圖。

## 主題收錄審查

2026-10-07 移除 7 處缺乏可核對景點特定賞楓／秋色介紹的項目，詳見 `data/THEME-REVIEW.md`。單純出現在廣泛主題列表、適合登山或觀景，不作為收錄依據。沒有近期楓況不代表與主題無關；已核實的秋色樹種景點仍保留。更新端點僅接受目前目錄，已移除的項目不會因舊儲存資料重新出現。
