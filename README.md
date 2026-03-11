# 💡 創作者策略助手

這是一個以 OpenAI 驅動的 Streamlit 應用，專門用於創作者策略規劃。

## 功能

- **Quick Planner**：產生 IG Bio 與 4 週 MVP 內容策略。
- **輸出模式**：
  - **Standard**：完整且較詳細的策略輸出。
  - **Low-token**：精簡高密度輸出。
  - **SKIPE**：固定區塊格式輸出（Intent Lock → IA → Deliverable）。
- **漏斗框架選擇**：
  - `Problem → Compare → Decision → Action`
  - `SEOULMATE 31 強化版`
- **URL 參考欄位**：可貼上「參考 URL」與「URL 重點摘錄」，若只貼 URL 未提供摘錄，系統會提示改以待確認事項輸出，避免臆測。
- **自我檢查面板**：快速檢查重複、格式一致性、訊號密度與雜訊。
- **結果暫存**：重新整理後仍可下載上一份結果並檢視自檢。
- **Chat**：自由對話模式。

## 額外檔案

- `URL_CONTEXT_TEMPLATE.md`：URL 資訊整理模板（先讀來源，再貼重點進 App）。
- `SEOULMATE_FUNNEL_BLUEPRINT.md`：Problem→Compare→Decision→Action 強化版網站漏斗藍圖。

## 本機執行

1. 安裝相依套件

```bash
pip install -r requirements.txt
```

2. 啟動應用

```bash
streamlit run streamlit_app.py
```

3. 開啟終端機顯示的本機網址，輸入你的 OpenAI API 金鑰。
