# QrcodeGenerator
這是一個使用 Python (Tkinter + Segno) 開發的進階 QR Code 產生器。具備即時預覽、自訂顏色、動態 UI 排版及多項專家級參數設定功能。

## 功能特色
* **即時動態預覽**: 輸入文字當下即可即時生成 QR Code 並在右側進行預覽，預覽圖會根據視窗縮放自動調整大小。
* **自訂外觀與顏色**: 支援靈活調整「填充」與「背景」顏色，並在下拉選單中智慧呈現顏色的高對比視覺效果。
* **進階參數設定**: 
  * 容錯等級 (L, M, Q, H)
  * 編碼版本 (Auto, 1~40)
  * 區塊大小、邊框寬度及遮罩圖案調整
  * 強制指定編碼模式 (Auto, Numeric, Alphanumeric, Byte)
  * 支援強制加入 UTF-8 ECI 標頭，提升特殊字元或多國語系的相容性
* **智能錯誤提示**: 若輸入的資料量超出 QR Code 物理極限容量，會自動給予友善的中文除錯建議。
* **多種格式輸出**: 支援將生成的 QR Code 以高畫質儲存為 PNG、SVG 及 GIF 等檔案格式。

## 環境架設與執行

1. 建立虛擬環境 (Virtual Environment)
   ```bash
   python -m venv venv
   ```
2. 啟動虛擬環境
   * Windows:
     ```bash
     venv\Scripts\activate
     ```
   * macOS / Linux:
     ```bash
     source venv/bin/activate
     ```
3. 安裝依賴套件 (本專案核心依賴 `segno` 及圖片處理函式庫 `Pillow`)
   ```bash
   pip install segno Pillow qrcode[pil]
   ```
4. 執行應用程式
   ```bash
   python QrcodeGenerator.py
   ```

## 授權條款 (License)

MIT License

Copyright (c) 2026 lee18.in

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
