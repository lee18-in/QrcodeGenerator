import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import segno
from PIL import Image, ImageTk
import io
from typing import Any

class QRCodeGeneratorApp:
    FILL_COLORS = [
        "black", "blue", "red", "green", "purple", "orange", "brown", "magenta",
        "cyan", "navy", "maroon", "olive", "teal", "lime", "indigo", "gold"
    ]
    BACK_COLORS = [
        "white", "yellow", "pink", "gray", "lightblue", "lightgreen", "lavender",
        "beige", "coral", "aqua", "silver", "mintcream", "ivory", "peachpuff",
        "plum", "khaki", "transparent"
    ]

    def __init__(self, master):
        self.master = master
        self.master.title("QR Code 產生器 (整合進化版)")
        self.master.geometry("1200x600")    #   初始尺寸設定為 1200x600，確保有足夠空間展示所有功能與預覽
        self.master.minsize(600, 400)       #   最小尺寸設定為 600x400，確保預覽區仍有足夠空間展示 QR Code
        self.master.maxsize(1200, 600)       #   最大尺寸設定為 1200x600，確保在大螢幕上也能有良好的展示效果

        self.qr_obj = None
        self.current_img = None

        self._setup_variables()
        self._create_widgets()
        self._bind_events()

        self.text_box.insert("1.0", "MIT License Copyright (c) 2026 lee18.in")
        self.update_qr()

    def _setup_variables(self):
        # 基本與外觀
        self.error_level_var = tk.StringVar(value="L (7%)")
        self.save_format_var = tk.StringVar(value="PNG")
        self.fill_color_var = tk.StringVar(self.master, value="black")
        self.back_color_var = tk.StringVar(self.master, value="white")

        # 進階參數
        self.version_var = tk.StringVar(value="Auto")
        self.mask_var = tk.StringVar(value="Auto")
        self.box_size_var = tk.StringVar(value="10")
        self.border_var = tk.StringVar(value="4")

        # 專家模式
        self.mode_var = tk.StringVar(value="Auto")
        self.eci_var = tk.BooleanVar(value=False)

    def _create_widgets(self):
        # 主容器
        main_container = ttk.Frame(self.master, padding=10)
        main_container.pack(fill=tk.BOTH, expand=True)

        # 使用 grid 佈局取代 pack，以更精確地控制縮放行為
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)  # 左欄 (文字輸入) 會隨視窗縮放
        main_container.grid_columnconfigure(1, weight=0)  # 右欄 (設定與預覽) 保持固定寬度

        # --- 左側：輸入與設定 ---
        left_frame = ttk.Frame(main_container)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.text_box = tk.Text(left_frame, width=40, undo=True)
        self.text_box.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # --- 右側：預覽與資訊 ---
        right_frame = ttk.Frame(main_container, width=380) # 固定寬度
        right_frame.grid(row=0, column=1, sticky="ns")
        right_frame.grid_propagate(False) # 確保寬度固定，不受視窗拉扯影響

        # 設定區塊擺在上
        settings_frame = ttk.Frame(right_frame, padding=5)
        settings_frame.pack(fill=tk.X, side=tk.TOP, pady=0)
        self._build_settings(settings_frame)

        ttk.Separator(right_frame, orient="horizontal").pack(fill=tk.X, pady=5, padx=5)

        # 顯示尺寸與資訊的區塊
        info_frame = ttk.Frame(right_frame, padding=5)
        info_frame.pack(fill=tk.X, side=tk.TOP, pady=0)

        self.info_label = ttk.Label(info_frame, text="等待生成...", justify=tk.LEFT, anchor="nw", font=("Arial", 10))
        self.info_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 將「格式」與「儲存」按鈕整合在 DATA 右側的區塊中
        action_frame = ttk.Frame(info_frame)
        action_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))

        fmt_frame = ttk.Frame(action_frame)
        fmt_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        ttk.Label(fmt_frame, text="格式:").pack(side=tk.LEFT)
        ttk.Combobox(fmt_frame, textvariable=self.save_format_var, values=["PNG", "SVG", "GIF"], state="readonly", width=4).pack(side=tk.RIGHT, fill=tk.X, expand=True)

        save_btn = ttk.Button(action_frame, text="💾 儲存...", command=self.save_qr)
        save_btn.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        ttk.Separator(right_frame, orient="horizontal").pack(fill=tk.X, pady=5, padx=5)

        preview_frame = ttk.Frame(right_frame, relief="sunken")
        preview_frame.pack(fill=tk.BOTH, expand=True)
        preview_frame.pack_propagate(False) # 確保預覽框可隨視窗縮小，不被圖片強制撐大

        self.preview_label = tk.Label(preview_frame, text="預覽區", bg="gray20", fg="white")
        self.preview_label.pack(fill=tk.BOTH, expand=True)

    def _build_settings(self, parent):
        for i in (1, 3, 5):
            parent.columnconfigure(i, weight=1)

        #     請依照此區備註調整 ui 版面設計，確保所有功能都能清晰呈現且易於使用。
        #  ======================[ 1200px  ]===============
        #  =[ 浮動px ]=|==[ 380px 固定寬度 ]=================
        #  text       |容錯   填充    版本     
        #  text       |區塊   背景    遮罩    
        #  text       |邊框   模式    ECI標頭
        #  text       |==========================
        #  text       |『～～大空格～～ why？』                  Totel Window Height=???px
        #  text       | DATA           |    格式  
        #  text       | DATA           |  [ SAVE ]   
        #  text       | DATA           |  [ SAVE ]   
        #  text       |========================== 
        #  text       | QR Code 預覽區 (動態縮放填滿右側框架)
        #  ================================================

        
        # --- 第一行 ---
        ttk.Label(parent, text="容錯:").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Combobox(parent, textvariable=self.error_level_var, values=["L (7%)", "M (15%)", "Q (25%)", "H (30%)"], state="readonly", width=2).grid(row=0, column=1, sticky="ew", padx=(0, 5))

        ttk.Label(parent, text="填充:").grid(row=0, column=2, sticky="w")
        self.fill_cb = ttk.Combobox(parent, textvariable=self.fill_color_var, values=self.FILL_COLORS, state="readonly", width=7)
        self.fill_cb.configure(postcommand=lambda: self._colorize_dropdown(self.fill_cb, self.FILL_COLORS))
        self.fill_cb.grid(row=0, column=3, sticky="ew", padx=(0, 5))
        self.fill_cb.configure(style="Fill.TCombobox")

        ttk.Label(parent, text="版本:").grid(row=0, column=4, sticky="w")
        ttk.Combobox(parent, textvariable=self.version_var, values=["Auto"] + [str(i) for i in range(1, 41)], state="readonly", width=2).grid(row=0, column=5, sticky="ew")

        # --- 第二行 ---
        ttk.Label(parent, text="區塊:").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Combobox(parent, textvariable=self.box_size_var, values=[str(i) for i in range(1, 31)], width=2).grid(row=1, column=1, sticky="ew", padx=(0, 5))

        ttk.Label(parent, text="背景:").grid(row=1, column=2, sticky="w")
        self.back_cb = ttk.Combobox(parent, textvariable=self.back_color_var, values=self.BACK_COLORS, state="readonly", width=7)
        self.back_cb.configure(postcommand=lambda: self._colorize_dropdown(self.back_cb, self.BACK_COLORS))
        self.back_cb.grid(row=1, column=3, sticky="ew", padx=(0, 5))
        self.back_cb.configure(style="Back.TCombobox")

        ttk.Label(parent, text="遮罩:").grid(row=1, column=4, sticky="w")
        ttk.Combobox(parent, textvariable=self.mask_var, values=["Auto"] + [str(i) for i in range(8)], state="readonly", width=2).grid(row=1, column=5, sticky="ew")

        # --- 第三行 ---
        ttk.Label(parent, text="邊框:").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Combobox(parent, textvariable=self.border_var, values=[str(i) for i in range(0, 11)], state="readonly", width=2).grid(row=2, column=1, sticky="ew", padx=(0, 5))

        ttk.Label(parent, text="模式:").grid(row=2, column=2, sticky="w")
        ttk.Combobox(parent, textvariable=self.mode_var, values=["Auto", "Numeric", "Alphanumeric", "Byte"], state="readonly", width=6).grid(row=2, column=3, sticky="ew", padx=(0, 5))

        ttk.Checkbutton(parent, text="ECI標頭", variable=self.eci_var).grid(row=2, column=4, columnspan=2, sticky="w")

    def _bind_events(self):
        self.text_box.bind("<KeyRelease>", self.on_text_change)
        self.preview_label.bind("<Configure>", self._resize_preview)
        variables = [
            self.error_level_var, self.fill_color_var, self.back_color_var,
            self.box_size_var, self.border_var, self.version_var, self.mask_var,
            self.mode_var, self.eci_var
        ]
        for var in variables:
            var.trace_add("write", self.update_qr)

    def _colorize_dropdown(self, cb, colors):
        def apply_colors():
            try:
                # 取得 Combobox 內建的 popdown listbox (負責顯示下拉清單的底層元件)
                popdown = self.master.tk.call('ttk::combobox::PopdownWindow', cb)
                listbox = f"{popdown}.f.l"
                for i, color in enumerate(colors):
                    bg = color if color != "transparent" else "white"
                    try:
                        r, g, b = self.master.winfo_rgb(bg)
                        luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 256
                        fg = "white" if luminance < 128 else "black"
                    except tk.TclError:
                        fg = "black"
                    # 設定 listbox 內各個選項的背景色與文字顏色
                    self.master.tk.call(listbox, 'itemconfigure', i, '-background', bg, '-foreground', fg)
            except Exception:
                pass
        # 利用 after 延遲 10 毫秒，確保下拉選單先完成預設的資料更新與展開動作後再上色
        self.master.after(10, apply_colors)

    def on_text_change(self, event=None):
        self.update_qr()
        
    def _update_color_styles(self):
        if not hasattr(self, 'fill_cb') or not hasattr(self, 'back_cb'):
            return

        def get_fg(color):
            if color == "transparent": return "black"
            try:
                # 取得 RGB 數值 (0~65535)，並換算為亮度
                r, g, b = self.master.winfo_rgb(color)
                luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 256
                return "white" if luminance < 128 else "black"
            except tk.TclError:
                return "black"

        # 填充顏色的 Style
        fill_color = self.fill_color_var.get()
        fill_bg = fill_color if fill_color != "transparent" else "white"
        fill_fg = get_fg(fill_bg)

        # 背景顏色的 Style
        back_color = self.back_color_var.get()
        back_bg = back_color if back_color != "transparent" else "white"
        back_fg = get_fg(back_bg)

        style = ttk.Style()
        style.map("Fill.TCombobox", fieldbackground=[("readonly", fill_bg)], selectbackground=[("readonly", fill_bg)], selectforeground=[("readonly", fill_fg)])
        style.configure("Fill.TCombobox", foreground=fill_fg)

        style.map("Back.TCombobox", fieldbackground=[("readonly", back_bg)], selectbackground=[("readonly", back_bg)], selectforeground=[("readonly", back_fg)])
        style.configure("Back.TCombobox", foreground=back_fg)

    def update_qr(self, *args):
        self._update_color_styles()
        text = self.text_box.get("1.0", tk.END).strip()
        if not text:
            self.preview_label.config(image='', text="請輸入文字以產生 QR Code...")
            self.preview_label.image = None  # type: ignore
            self.info_label.config(text="狀態: 等待輸入內容...")
            self.qr_obj = None
            return

        try:
            # 1. 收集並準備參數
            err = self.error_level_var.get().split()[0].lower()
            ver = self.version_var.get()
            mask = self.mask_var.get()
            mode = self.mode_var.get()
            
            kwargs: dict[str, Any] = {'error': err}
            if ver != "Auto": kwargs['version'] = int(ver)
            if mask != "Auto": kwargs['mask'] = int(mask)
            if mode != "Auto": kwargs['mode'] = mode.lower()
            if self.eci_var.get(): kwargs['eci'] = True

            # 2. 生成核心 QR 物件 (segno 會自動尋找能容納內容的「最小版本」)
            self.qr_obj = segno.make(text, **kwargs)

            # 3. 準備繪圖參數
            scale = int(self.box_size_var.get() or 10)
            border = int(self.border_var.get() or 4)
            fill = self.fill_color_var.get()
            back = self.back_color_var.get()
            light_color = None if back.lower() == "transparent" else back

            # 4. 輸出到記憶體以供預覽
            out = io.BytesIO()
            self.qr_obj.save(out, kind='png', scale=scale, border=border, dark=fill, light=light_color)
            out.seek(0)
            img = Image.open(out)

            # 5. 更新解析度與尺寸資訊面板
            actual_w, actual_h = img.size
            mat_w, mat_h = self.qr_obj.symbol_size(border=0)
            qr_version_name = self.qr_obj.designator

            info_text = (
                f"最低需求版本: {qr_version_name} (模塊矩陣: {mat_w} x {mat_h})\n"
                f"最終圖片尺寸: {actual_w} x {actual_h} px  (含邊框計算)\n"
                f"編碼模式: {self.qr_obj.mode} | 資料長度: {len(text)}/2953 字元"
            )
            self.info_label.config(text=info_text, foreground="blue")

            # 6. 保存原始圖片，並呼叫縮放方法來動態填滿 UI 框架
            self.current_img = img.copy()
            self._resize_preview()

        except Exception as e:
            self.qr_obj = None
            self.current_img = None
            error_msg = str(e)
            
            # 針對常見的容量或編碼錯誤給予白話文提示
            if "Data too large" in error_msg:
                input_bytes = len(text.encode('utf-8'))
                error_msg = (
                    f"資料量過大！\n\n"
                    f"📊 目前輸入量: {len(text)} 字元 (約 {input_bytes} Bytes)\n"
                    f"📏 絕對物理極限: 2,953 Bytes (最低容錯 L、最大版本 40 下)\n\n"
                    f"您輸入的資料已超過目前設定的「容錯等級」或「版本」極限。\n\n"
                    f"💡 解決方式：\n"
                    f"1. 將「容錯」調低 (例如 L)\n"
                    f"2. 確認「版本」設為 Auto\n"
                    f"3. 減少您要產生的文字量"
                )
            elif "mode" in error_msg.lower() or "alphanumeric" in error_msg.lower():
                error_msg = "編碼模式衝突！\n\n強制指定的「模式」無法支援您輸入的字元。\n(例如 Alphanumeric 不支援小寫英文)\n\n💡 解決方式：將「模式」設為 Auto"
                
            self.info_label.config(text=f"狀態: 生成失敗", foreground="red")
            self.preview_label.config(image='', text=f"❌ 無法產生 QR Code:\n\n{error_msg}")

    def _resize_preview(self, event=None):
        if not getattr(self, 'current_img', None):
            return

        # 取得預覽區目前的寬高
        w = self.preview_label.winfo_width()
        h = self.preview_label.winfo_height()

        if w < 10 or h < 10:
            return

        # 複製原圖並縮放到目前的框架大小 (保持等比例縮放，填滿最大可用空間)
        preview_img = self.current_img.copy()
        preview_img.thumbnail((w, h), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(preview_img.convert("RGBA"))
        self.preview_label.config(image=photo, text="")
        self.preview_label.image = photo  # type: ignore

    def save_qr(self):
        if not self.qr_obj:
            messagebox.showwarning("警告", "請先產生 QR Code！")
            return

        fmt = self.save_format_var.get().lower()
        filetypes = [(f"{fmt.upper()} 檔案", f"*.{fmt}"), ("所有檔案", "*.*")]
        filepath = filedialog.asksaveasfilename(defaultextension=f".{fmt}", filetypes=filetypes)
        
        if filepath:
            scale = int(self.box_size_var.get() or 10)
            border = int(self.border_var.get() or 4)
            fill = self.fill_color_var.get()
            back = self.back_color_var.get()
            light_color = None if back.lower() == "transparent" else back

            save_kwargs = {'kind': fmt, 'dark': fill, 'light': light_color, 'border': border}
            if fmt != 'svg':
                save_kwargs['scale'] = scale

            try:
                self.qr_obj.save(filepath, **save_kwargs)
                messagebox.showinfo("成功", f"QR Code 已儲存至:\n{filepath}")
            except Exception as e:
                messagebox.showerror("錯誤", f"儲存失敗:\n{e}")

def main():
    root = tk.Tk()
    # 嘗試套用更美觀的主題
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    
    app = QRCodeGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()