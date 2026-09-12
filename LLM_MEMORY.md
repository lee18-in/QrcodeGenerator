# LLM_MEMORY.md — 工作記憶(agent 讀寫;規則見 AGENTS.md,勿在此重複)

> - **Language and Encoding Standards**: All system files, code annotations, memory files (`LLM_MEMORY.md`), and handover logs for this project are uniformly encoded in **UTF-8** and **Traditional Chinese** by default.

## A. 目前狀態(每次交接必更新)

- 目前階段: maintain
- 最後更新: 2026-09-12 10:46 / 當時階段: maintain
- 交接基準 commit: 0f1ccb4 [maintain] 升級 AI agent 工作流至 Playbook v9
- 進行中任務: 測試現有功能，邊用邊測發現並修復 bug
- 阻塞點: 2026-09-12 10:46 那筆（venv／bin 移出版控）待審閱，需新 session／新工具承接（§2.1 禁止左手審右手）

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

### 2026-09-12 10:46 [maintain] 使用工具: Claude Opus 5 (Cursor)

- 完成了什麼: 使用者要求把 GitHub 12 個 repo 同步到本機，比對時發現本 repo 有未提交的刪除與一個從未生效的 ignore 規則。依使用者裁示三項改動：①`.gitignore` 原內容僅一行 `"venv/"`（含雙引號），gitignore 不支援引號語法，該行**從未生效**，已改寫為 `venv*/`、`.venv*/` 並補建置產物規則（`bin/*.AppImage`、`bin/*.exe`、`build/`、`dist/`、`*.spec`）；②`git rm -r --cached venv` 將 1327 個 `venv/` 檔案（32.9 MB）移出索引，本機目錄保留不動；③提交使用者先前已在工作樹刪除的 `bin/QrcodeGenerator-x86_64.AppImage`（33.6 MB）與 `bin/QrcodeGenerator.exe`（19.9 MB）。使用者明示 push。
- 為何改: 版控中的 `venv/` 是在使用者另一台 Linux 機器建立的 Python 3.12.3 環境（`pyvenv.cfg` 的 command 寫死 `/mnt/1THDD256NVME/Archive/Documents/github/QrcodeGenerator/`），內含 8 個 `x86_64-linux-gnu` 的 `.so`，在使用者目前的 arm64 macOS 上無法運作，屬純死重量；起因即 ①的引號語法失效。移除環境目錄屬架構級決定，本 repo 在 maintain 階段（§1 禁止架構級變更），**依使用者 2026-09-12 10:45 明確裁示執行，階段不變更**。處理方式比照 VoltMatch 2026-07-29 對 `.venv2/` 的先例。
- 驗證紀錄: `git check-ignore -v venv` 在改寫前確認 `venv` **未**被忽略，證實舊規則失效。暫存區核對為 1329 筆 D（1327 屬 `venv/`、2 屬 `bin/`）+ 1 筆 M（`.gitignore`），無其他檔案誤納。`git ls-files` 比對確認新 ignore 規則除 `venv/` 與該 2 個 bin 檔外，未命中任何其他已版控檔案。`venv/` 目錄提交後仍存在於工作樹（`--cached` 只動索引）。pre-commit hook 反向測試：故意不含 `LLM_MEMORY.md` 送出，確實被擋下並回報正確訊息。無自動化測試指令可跑。
- 下一個 agent 該做什麼: 本次改動需要審閱: ①`venv*/` 這個 glob 是否過寬（結尾斜線只匹配目錄，但請確認專案無以 venv 開頭的目錄需納管）；②`*.spec` 是否會誤擋未來想版控的 PyInstaller spec 檔（本 repo 目前無任何 `.spec` 已版控）；③確認 `bin/` 兩個執行檔移除後，README 或說明文件是否還指向那兩個路徑（本次未檢查文件內引用）；④32.9 MB + 53.5 MB 仍留在 git 歷史中，只有未來 commit 不再帶它，如需真正瘦身要 rewrite history（屬架構級決定，須使用者裁示）。等待新 session/新工具審閱。
- 地雷警告: ①接手時 `core.hooksPath` 未設定（2026-08-25 那筆聲稱已執行 `git config core.hooksPath scripts/hooks`，但該設定屬本機層級、不隨 clone 帶過來），本次已於 10:39 對本機全部 12 個 repo 重新設定，hook 現已生效。②其他機器 pull 後本機的 `venv/` 目錄會被刪除；該環境本來就與本機平台不符，若在 Linux 機器上仍在使用需事先知悉。③本 repo 之 `venv/` 移除不影響 `requirements.txt`，重建環境見〈E. 專案技術脈絡〉。

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
