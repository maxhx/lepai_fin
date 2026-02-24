# -*- coding: utf-8 -*-

import json
import pandas as pd
from openpyxl import Workbook

# 假设 'orders.json' 是包含订单数据的 JSON 文件
json_file = '从浏览器复制出来拷贝到此.json'
excel_file = 'orders.xlsx'

# 读取 JSON 文件
with open(json_file, 'r',encoding='utf-8') as file:
    data = json.load(file)
    vData = data['rows']
# 将 JSON 数据转换为 DataFrame
df = pd.DataFrame(data['rows'])

# 假设每个订单的数据中包含 'Amount' 字段，我们要基于此字段计算总额
# 尝试将字符串列转换为数值类型，忽略错误
df['totalBaseAmount'] = pd.to_numeric(df['totalBaseAmount'], errors='coerce')
total_amount = df['totalBaseAmount'].sum()
print(f'输出的订单数量:{len(vData)}，订单金额总计:{total_amount}')

# 创建一个包含订单总额的新行
total_series = pd.Series({'OrderID': 'Total', 'Amount': total_amount})

# 将总额作为新行追加到 DataFrame 中
df = df._append(total_series, ignore_index=True)

# 将 DataFrame 写入 Excel 文件
# 使用 openpyxl 引擎来处理 xlsx 文件
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='Sheet1')
