# -*- coding: utf-8 -*-

import json
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from openpyxl import Workbook

def select_json_file():
    # 打开文件选择对话框，选择 JSON 文件
    json_file_path = filedialog.askopenfilename(title="选择 JSON 文件", filetypes=[("JSON Files", "*.json")])
    if json_file_path:
        json_file_label.config(text=json_file_path)
        process_json_file(json_file_path)

def process_json_file(json_file):
    # 读取 JSON 文件
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            vData = data['data']

        # 将 JSON 数据转换为 DataFrame
        df = pd.DataFrame(vData)

        # 尝试将字符串列转换为数值类型，忽略错误
        df['totalBaseAmount'] = pd.to_numeric(df['totalBaseAmount'], errors='coerce')
        total_amount = df['totalBaseAmount'].sum()
        total_orders = len(vData)
        
        # 显示订单数量和总金额
        messagebox.showinfo("结果", f'输出的订单数量: {total_orders}，订单金额总计: {total_amount:.2f}')
        
        # 创建一个包含订单总额的新行
        total_series = pd.DataFrame({'totalBaseAmount': [total_amount]}, index=['Total'])

        # 使用 pd.concat 将总额作为新行添加到 DataFrame 中
        df = pd.concat([df, total_series])

        # 将 DataFrame 写入 Excel 文件
        excel_file = json_file.replace(".json", ".xlsx")
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        
        messagebox.showinfo("完成", f'数据已成功导出到 {excel_file} 文件。')

    except Exception as e:
        messagebox.showerror("出错", f"处理文件时发生错误: {e}")

# 创建 GUI 窗口
root = tk.Tk()
root.title("JSON 转 Excel 工具")

# 创建选择文件的按钮和标签
select_file_button = tk.Button(root, text="选择 JSON 文件", command=select_json_file)
select_file_button.pack(pady=20)

json_file_label = tk.Label(root, text="未选择文件")
json_file_label.pack(pady=20)

root.geometry("400x200")
root.mainloop()