import os
import json
import tkinter as tk
from utils import process
from tkinter import filedialog


# 打开文件夹对话框并返回路径
def select_folder(entry: tk.Entry):
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry.delete(0, tk.END)  # 清空当前文本
        entry.insert(0, folder_path)  # 插入新的文件夹路径


def select_file(entry: tk.Entry):
    file_path = filedialog.askopenfilename()
    if file_path:
        entry.delete(0, tk.END)  # 清空当前文本
        entry.insert(0, file_path)  # 插入新的文件路径


# 创建GUI
def create_gui():
    root = tk.Tk()
    root.title("Wallpaper Engine 壁纸提取器")

    # 设置窗口大小和居中显示
    window_width = 600
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    # 居中显示文字
    title_label = tk.Label(
        root, text="Wallpaper Engine 壁纸提取器", font=("Arial", 16, "bold")
    )
    title_label.grid(row=1, column=0, columnspan=3, pady=10)

    # 输入框和按钮
    tk.Label(root, text="创意工坊路径:").grid(row=2, column=0, padx=10, pady=10)
    origin_path_entry = tk.Entry(root, width=50)
    origin_path_entry.grid(row=2, column=1, padx=10, pady=10)
    tk.Button(root, text="选择", command=lambda: select_folder(origin_path_entry)).grid(
        row=2, column=2
    )

    tk.Label(root, text="提取路径:").grid(row=3, column=0, padx=10, pady=10)
    output_path_entry = tk.Entry(root, width=50)
    output_path_entry.grid(row=3, column=1, padx=10, pady=10)
    tk.Button(root, text="选择", command=lambda: select_folder(output_path_entry)).grid(
        row=3, column=2
    )

    tk.Label(root, text="RePKG.exe 路径:").grid(row=4, column=0, padx=10, pady=10)
    execute_path_entry = tk.Entry(root, width=50)
    execute_path_entry.grid(row=4, column=1, padx=10, pady=10)
    tk.Button(root, text="选择", command=lambda: select_file(execute_path_entry)).grid(
        row=4, column=2
    )

    # 并行数滑块
    tk.Label(root, text="并行数量:").grid(row=5, column=0, padx=10, pady=10)
    parallel_num_slider = tk.Scale(
        root, from_=1, to=os.cpu_count(), orient=tk.HORIZONTAL
    )
    parallel_num_slider.set(os.cpu_count())
    parallel_num_slider.grid(row=5, column=1, padx=10, pady=10)

    # 用于显示状态的Label
    status_label = tk.Label(root, text="", font=("Arial", 12, "italic"), fg="blue")
    status_label.grid(row=6, column=0, columnspan=3, pady=20)

    # 运行按钮
    def run_process():
        origin_path = origin_path_entry.get()
        output_base = output_path_entry.get()
        execute_path = execute_path_entry.get()
        parallel_num = int(parallel_num_slider.get())

        target_ids = os.listdir(origin_path)
        failed = []
        processed_list = []
        origin_metadata = []
        if os.path.exists(os.path.join(output_base, "metadata.json")):
            with open(
                os.path.join(output_base, "metadata.json"), "r", encoding="utf-8"
            ) as f:
                origin_metadata = json.load(f)
                assert isinstance(origin_metadata, list), "metadata.json 格式错误"
                processed_list.extend(item["ID"] for item in origin_metadata)

        target_ids = list(set(target_ids) - set(processed_list))

        metadata, failed = process(
            origin_path, target_ids, output_base, parallel_num, execute_path
        )

        with open(
            os.path.join(output_base, "metadata.json"), "w", encoding="utf-8"
        ) as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)

        if len(failed) != 0:
            with open(
                os.path.join(output_base, "failed.json"), "w", encoding="utf-8"
            ) as f:
                json.dump(failed, f, ensure_ascii=False, indent=4)
        status_label.config(text="运行完成", fg="green")

    tk.Button(root, text="提取", command=run_process).grid(
        row=6, column=1, padx=10, pady=20
    )

    root.mainloop()


if __name__ == "__main__":
    create_gui()
