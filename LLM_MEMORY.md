# LLM_MEMORY.md — 工作記憶(agent 讀寫;規則見 AGENTS.md,勿在此重複)

> - **Language and Encoding Standards**: All system files, code annotations, memory files (`LLM_MEMORY.md`), and handover logs for this project are uniformly encoded in **UTF-8** and **Traditional Chinese** by default.

## A. 目前狀態(每次交接必更新)

- 目前階段: maintain
- 最後更新: 2026-08-25 17:14 / 當時階段: maintain
- 交接基準 commit: 3f417d6 [maintain] 短期目標：我幫妳測試應用功能
- 進行中任務: 測試現有功能，邊用邊測發現並修復 bug
- 阻塞點: 無

## B. 規劃(規劃階段 [plan] 專屬區;狀態: 草稿 | 已定案)

### B1. 架構決策(已定案後鎖定,建置/維運階段不得改)

| # | 決策 | 理由 | 狀態 |
|---|------|------|------|

### B2. 短期目標(本週)

- [ ] 我幫妳測試應用功能，發現並記錄 bug

### B3. 中期目標(本月)

- [ ]

### B4. 長期目標

- [ ]

## C. 交接日誌(只追加,不刪改;最新在最上,每筆一個小節)

### 2026-08-25 17:14 [maintain] 使用工具: Claude Code

- 完成了什麼: 依 Playbook Online v9 執行分支 B（AGENTS.md 無版本標記，視同版本化之前建立的專案）：整份覆蓋 `AGENTS.md`（保留使用者本次未變更的階段/邊界條文，新增交接基準 commit 機制、Review Loop、巢狀範圍條款、語言與編碼規範等）；舊 `AGENTS.md` §5 已填值（建置指令 `pip install -r requirements.txt`（或 `segno Pillow qrcode[pil]`）、測試指令「無自動化測試指令」、程式碼慣例「無特別指定」）搬遷至下方〈E. 專案技術脈絡〉；`LLM_MEMORY.md` A 區「最新 commit」欄改名為「交接基準 commit」；補齊 `scripts/hooks/pre-commit`、`commit-msg` 為最新版並執行 `git config core.hooksPath scripts/hooks`（先前檔案存在但從未啟用）；新增 `.gitattributes` 的 `scripts/hooks/* text eol=lf`；README.md 頂端補上語言與編碼規範引導行。覆蓋前 `AGENTS.md` 的舊版可用 `git show cf703b3:AGENTS.md` 找回。
- 下一個 agent 該做什麼: 無（純框架升級，無程式碼邏輯變更）
- 地雷警告: 無

<!-- 範例格式,新條目複製此結構插入在本註解下方:

### YYYY-MM-DD HH:MM [plan / build / maintain 擇一] 使用工具: <agent 名稱>

- 完成了什麼:
- 下一個 agent 該做什麼:
- 地雷警告: 無
-->

### 2026-07-06 [maintain] 使用工具: Claude Haiku 4.5

- 完成了什麼: 確認項目狀態：v1.0.0 已發佈，目前進入維運維護階段。根據使用者指示「先放著測試，一邊用一邊測看看有沒有bug」，將目前階段從 build 改為 maintain。清理未提交的臨時檔案。
- 下一個 agent 該做什麼: 待使用者指示測試計畫——(1)由使用者自己手動測試，我負責修復回報的 bug；或(2)由我啟動應用程式進行功能測試。
- 地雷警告: 無

### 2026-07-06 [build] 使用工具: Claude Haiku 4.5

- 完成了什麼: 完成 AI agent 工作流導入（B-Step 6 缺失部分）：安裝 Git Hook（pre-commit、commit-msg），啟用 `git config core.hooksPath scripts/hooks`，並設定執行權限。更新 LLM_MEMORY.md A 區反映當前階段為 build。
- 下一個 agent 該做什麼: 等待使用者確認〈B. 規劃〉區規劃內容（架構決策、目標清單）。根據 AGENTS.md §1，build 階段必須有已定案計畫；目前規劃區為空，無法執行 build 工作。請提供已定案計畫或指示是否需要先回到 plan 階段補規劃。
- 地雷警告: 無

### 2026-07-05 13:12 [plan] 使用工具: Antigravity

- 完成了什麼: 執行多 agent 工作流配置導入。建立了 AGENTS.md, CLAUDE.md, GEMINI.md, LLM_MEMORY.md，並修改了 README.md 加上頂部引導。
- 下一個 agent 該做什麼: 等待使用者填寫 LLM_MEMORY.md 內的 `<請使用者填寫>` 欄位，並指派新的任務。
- 地雷警告: 無

## D. 已封存結論(自〈總結封存〉搬入,唯讀)

## E. 專案技術脈絡(依專案填寫,agent 得隨專案實況更新,保持精簡)

- 建置指令: `pip install -r requirements.txt`(或依照 README 安裝 `segno Pillow qrcode[pil]`)
- 測試指令: 無自動化測試指令
- 程式碼慣例: 無特別指定
