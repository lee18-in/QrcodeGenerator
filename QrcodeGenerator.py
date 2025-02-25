import re
import qrcode
import qrcode.image.svg
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

# 全域變數，用來保存「合法」狀態下的文字
old_text = ""

# 定義各選項
ERROR_LEVELS = {
    "L (7%)": qrcode.constants.ERROR_CORRECT_L,
    "M (15%)": qrcode.constants.ERROR_CORRECT_M,
    "Q (25%)": qrcode.constants.ERROR_CORRECT_Q,
    "H (30%)": qrcode.constants.ERROR_CORRECT_H,
}
SIZE_MULTIPLIERS = {"1X": 1, "2X": 2, "3X": 3, "4X": 4, "5X": 5}
FILL_COLORS = [
    "black", "blue", "red", "green",
    "purple", "orange", "brown", "magenta",
    "cyan", "navy", "maroon", "olive",
    "teal", "lime", "indigo", "gold"
]
BACK_COLORS = [
    "white", "yellow", "pink", "gray",
    "lightblue", "lightgreen", "lavender", "beige",
    "coral", "aqua", "silver", "mintcream",
    "ivory", "peachpuff", "plum", "khaki"
]
VERSION_OPTIONS = ["Auto"] + [str(i) for i in range(1, 41)]
BORDER_OPTIONS = [str(i) for i in range(1, 6)]

# 修改後的編碼模式：數字、官方 Alphanumeric、UTF-8、UTF16
ENCODING_OPTIONS = ["數字", "官方 Alphanumeric", "UTF-8", "UTF16"]

def create_color_menu(master, variable, options):
    menubutton = tk.Menubutton(master, textvariable=variable, relief="raised", width=10,
                               font=("Arial", 10, "bold"), bg="black", fg="white")
    menu = tk.Menu(menubutton, tearoff=0, font=("Arial", 10, "bold"), bg="black", fg="white")
    menubutton.config(menu=menu)
    for option in options:
        menu.add_command(label=option, command=lambda opt=option: variable.set(opt),
                         background="black", foreground="white", font=("Arial", 10, "bold"))
    return menubutton

def on_text_change(event=None):
    global old_text
    current_text = text_box.get("1.0", "end-1c")
    selected_encoding = encoding_mode_var.get()

    if selected_encoding == "數字":
        if re.search(r"[^\d]", current_text):
            messagebox.showwarning("警告", "數字模式僅允許輸入數字！")
            revert_text()
            return
        capacity_limit = 7089
        usage = len(current_text)
    elif selected_encoding == "官方 Alphanumeric":
        if re.search(r"[^0-9A-Z \$%\*\+\-\.\/:]", current_text):
            messagebox.showwarning("警告", "官方 Alphanumeric 模式僅允許 [0-9, A-Z, 空白, $, %, *, +, -, ., /, :]！")
            revert_text()
            return
        capacity_limit = 4296
        usage = len(current_text)
    elif selected_encoding == "UTF-8":
        capacity_limit = 2953
        usage = len(current_text.encode("utf-8"))
    elif selected_encoding == "UTF16":
        # UTF16 模式：假設每個字元以 16-bit 表示，容量上限為 23624/16 ≈ 1476
        capacity_limit = 23624 // 16
        usage = len(current_text)
    else:
        capacity_limit = 2953
        usage = len(current_text.encode("utf-8"))
    
    # DEBUG 輸出：印出當前模式、使用量及上限
    print(f"[DEBUG] 模式: {selected_encoding}, 使用量: {usage}, 上限: {capacity_limit}")

    if usage > capacity_limit:
        messagebox.showwarning("警告", f"輸入容量超過上限！（目前：{usage}，上限：{capacity_limit}）")
        revert_text()
        return
    else:
        old_text = current_text

    update_qr()

def revert_text():
    text_box.delete("1.0", tk.END)
    text_box.insert("1.0", old_text)

def update_qr():
    text = text_box.get("1.0", "end-1c").strip()
    global qr_image

    if not text:
        qr_preview_label.config(image='', text='')
        qr_preview_label.image = None
        qr_image = None
        resolution_label.config(text="目前容量: 0 解析度: N/A")
        return

    selected_encoding = encoding_mode_var.get()

    # 處理資料：對於 UTF16 模式，使用 UTF-16 BE 編碼
    if selected_encoding in ("數字", "官方 Alphanumeric", "UTF-8"):
        data_to_encode = text
    elif selected_encoding == "UTF16":
        data_to_encode = text.encode("utf-16-be")
    else:
        data_to_encode = text

    if selected_encoding == "數字":
        capacity_limit = 7089
        usage = len(text)
    elif selected_encoding == "官方 Alphanumeric":
        capacity_limit = 4296
        usage = len(text)
    elif selected_encoding == "UTF-8":
        capacity_limit = 2953
        usage = len(text.encode("utf-8"))
    elif selected_encoding == "UTF16":
        capacity_limit = 23624 // 16
        usage = len(text)
    else:
        capacity_limit = 2953
        usage = len(text.encode("utf-8"))

    level_str = error_var.get()
    error_correction = ERROR_LEVELS.get(level_str, qrcode.constants.ERROR_CORRECT_L)
    size_str = size_var.get()
    box_size = SIZE_MULTIPLIERS.get(size_str, 1)
    fill_color = fill_color_var.get()
    back_color = back_color_var.get()
    version_str = version_var.get()
    border_val = int(border_var.get())

    version_used = None
    qr = None

    if version_str == "Auto":
        for v in range(1, 41):
            qr = qrcode.QRCode(
                version=v,
                error_correction=error_correction,
                box_size=box_size,
                border=border_val,
            )
            qr.add_data(data_to_encode)
            try:
                qr.make(fit=True)
                version_used = qr.version
                break
            except Exception:
                continue
        else:
            messagebox.showerror("錯誤", "無法生成 QR Code，資料可能過多！")
            revert_text()
            return
        version_var.set(str(version_used))
    else:
        version_val = int(version_str)
        qr = qrcode.QRCode(
            version=version_val,
            error_correction=error_correction,
            box_size=box_size,
            border=border_val,
        )
        qr.add_data(data_to_encode)
        try:
            qr.make(fit=True)
            version_used = qr.version
        except Exception as e:
            answer = messagebox.askyesno("錯誤", f"生成 QR Code 失敗：{e}\n是否還原輸入內容？")
            if answer:
                revert_text()
            return

    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    if img.size[0] > 500 or img.size[1] > 500:
        img = img.resize((500, 500), Image.Resampling.LANCZOS)

    resolution_label.config(
        text=f"目前容量: {usage} / {capacity_limit}  ({selected_encoding} 模式)  解析度: {img.size[0]} x {img.size[1]}，版本: {version_used}"
    )
    qr_img = ImageTk.PhotoImage(img)
    qr_preview_label.config(image=qr_img, text="")
    qr_preview_label.image = qr_img
    qr_image = img

def save_qr():
    if qr_image is None:
        messagebox.showwarning("警告", "請先產生 QR Code！")
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG 檔案", "*.png"), ("所有檔案", "*.*")]
    )
    if file_path:
        qr_image.save(file_path)
        messagebox.showinfo("成功", f"QR Code 已儲存至 {file_path}")

def save_vector_qr():
    text = text_box.get("1.0", "end-1c").strip()
    if not text:
        messagebox.showwarning("警告", "請先輸入文字以產生 QR Code！")
        return
    level_str = error_var.get()
    error_correction = ERROR_LEVELS.get(level_str, qrcode.constants.ERROR_CORRECT_L)
    size_str = size_var.get()
    box_size = SIZE_MULTIPLIERS.get(size_str, 1)
    fill_color = fill_color_var.get()
    back_color = back_color_var.get()
    version_str = version_var.get()
    version_val = None if version_str == "Auto" else int(version_str)
    border_val = int(border_var.get())
    qr = qrcode.QRCode(
        version=version_val,
        error_correction=error_correction,
        box_size=box_size,
        border=border_val,
    )
    qr.add_data(text)
    qr.make(fit=True)
    factory = qrcode.image.svg.SvgImage
    img = qr.make_image(image_factory=factory, fill_color=fill_color, back_color=back_color)
    file_path = filedialog.asksaveasfilename(
        defaultextension=".svg",
        filetypes=[("SVG 檔案", "*.svg"), ("所有檔案", "*.*")]
    )
    if file_path:
        img.save(file_path)
        messagebox.showinfo("成功", f"QR Code 向量圖已儲存至 {file_path}")

# ---------------------------
# 建立主視窗
root = tk.Tk()
root.title("QR Code 產生器")
root.geometry("1000x500")

# 上方區域：選項與按鈕
top_frame = tk.Frame(root)
top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
top_frame.columnconfigure(0, weight=1)

options_frame = tk.Frame(top_frame)
options_frame.grid(row=0, column=0, sticky="w")

tk.Label(options_frame, text="編碼模式：").grid(row=0, column=0, padx=5, pady=2, sticky="e")
encoding_mode_var = tk.StringVar(root)
encoding_mode_var.set("數字")
encoding_menu = tk.OptionMenu(options_frame, encoding_mode_var, *ENCODING_OPTIONS)
encoding_menu.config(width=15)
encoding_menu.grid(row=0, column=1, padx=5, pady=2)

tk.Label(options_frame, text="錯誤修正：").grid(row=0, column=2, padx=5, pady=2, sticky="e")
error_var = tk.StringVar(root)
error_var.set("L (7%)")
error_menu = tk.OptionMenu(options_frame, error_var, *ERROR_LEVELS.keys())
error_menu.config(width=10)
error_menu.grid(row=0, column=3, padx=5, pady=2)

tk.Label(options_frame, text="大小倍率：").grid(row=0, column=4, padx=5, pady=2, sticky="e")
size_var = tk.StringVar(root)
size_var.set("5X")
size_menu = tk.OptionMenu(options_frame, size_var, *SIZE_MULTIPLIERS.keys())
size_menu.config(width=10)
size_menu.grid(row=0, column=5, padx=5, pady=2)

tk.Label(options_frame, text="填充顏色：").grid(row=1, column=0, padx=5, pady=2, sticky="e")
fill_color_var = tk.StringVar(root)
fill_color_var.set("black")
fill_color_menu = create_color_menu(options_frame, fill_color_var, FILL_COLORS)
fill_color_menu.grid(row=1, column=1, padx=5, pady=2)

tk.Label(options_frame, text="背景顏色：").grid(row=1, column=2, padx=5, pady=2, sticky="e")
back_color_var = tk.StringVar(root)
back_color_var.set("white")
back_color_menu = create_color_menu(options_frame, back_color_var, BACK_COLORS)
back_color_menu.grid(row=1, column=3, padx=5, pady=2)

tk.Label(options_frame, text="QR版本：").grid(row=2, column=0, padx=5, pady=2, sticky="e")
version_var = tk.StringVar(root)
version_var.set("Auto")
version_menu = tk.OptionMenu(options_frame, version_var, *VERSION_OPTIONS)
version_menu.config(width=10)
version_menu.grid(row=2, column=1, padx=5, pady=2)

tk.Label(options_frame, text="邊框寬度：").grid(row=2, column=2, padx=5, pady=2, sticky="e")
border_var = tk.StringVar(root)
border_var.set("1")
border_menu = tk.OptionMenu(options_frame, border_var, *BORDER_OPTIONS)
border_menu.config(width=10)
border_menu.grid(row=2, column=3, padx=5, pady=2)

for var in (encoding_mode_var, error_var, size_var, fill_color_var, back_color_var, version_var, border_var):
    var.trace_add("write", lambda *args: update_qr())

button_frame = tk.Frame(top_frame)
button_frame.grid(row=3, column=0, sticky="w", pady=5)
refresh_button = tk.Button(button_frame, text="立即刷新 QR Code", command=update_qr)
refresh_button.grid(row=0, column=0, padx=5)
save_button = tk.Button(button_frame, text="另存新檔", command=save_qr)
save_button.grid(row=0, column=1, padx=5)
vector_button = tk.Button(button_frame, text="另存向量圖", command=save_vector_qr)
vector_button.grid(row=0, column=2, padx=5)

resolution_label = tk.Label(button_frame, text="目前容量: 0 解析度: N/A", font=("Arial", 10, "bold"))
resolution_label.grid(row=0, column=3, padx=5)

main_frame = tk.Frame(root)
main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

input_frame = tk.Frame(main_frame, bg="lightgray")
input_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
main_frame.columnconfigure(0, weight=3)
main_frame.rowconfigure(0, weight=1)

scrollbar = tk.Scrollbar(input_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_box = tk.Text(input_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, bg="lightgray")
text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=text_box.yview)
text_box.insert("1.0", "0000")
text_box.bind("<KeyRelease>", on_text_change)

preview_frame = tk.Frame(main_frame)
preview_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
qr_preview_label = tk.Label(preview_frame, bg="white")
qr_preview_label.pack()

qr_image = None

update_qr()
root.mainloop()