# -*- coding: utf-8 -*-

import json
import pandas as pd
import os
from openpyxl import Workbook

# 检查JSON文件是否存在
json_file = '从浏览器复制出来拷贝到此.json'
excel_file = 'orders.xlsx'

# 构建完整的文件路径
script_dir = os.path.dirname(__file__)  # 获取当前脚本所在的目录
json_path = os.path.join(script_dir, json_file)

if not os.path.exists(json_path):
    print(f"错误: 找不到文件 '{json_file}'")
    print("请确保JSON文件存在于当前目录中")
    exit(1)

# 读取 JSON 文件
try:
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        vData = data['rows']
except FileNotFoundError:
    print(f"错误: 找不到文件 '{json_file}'")
    exit(1)
except json.JSONDecodeError:
    print(f"错误: '{json_file}' 不是有效的JSON文件")
    exit(1)
except KeyError:
    print(f"错误: JSON文件中没有找到 'rows' 键")
    exit(1)

# 将 JSON 数据转换为 DataFrame
df = pd.DataFrame(data['rows'])

# 假设每个订单的数据中包含 'Amount' 字段，我们要基于此字段计算总额
# 尝试将字符串列转换为数值类型，忽略错误
if 'totalBaseAmount' in df.columns:
    df['totalBaseAmount'] = pd.to_numeric(df['totalBaseAmount'], errors='coerce')
    total_amount = df['totalBaseAmount'].sum()
    print(f'输出的订单数量:{len(vData)}，订单金额总计:{total_amount}')
else:
    print("警告: DataFrame中没有找到 'totalBaseAmount' 列")
    total_amount = 0

# 创建一个包含订单总额的新行
# 根据实际的列名创建总计行
total_row = {}
for col in df.columns:
    if col == 'totalBaseAmount':
        total_row[col] = total_amount
    elif col == df.columns[0]:  # 使用第一列存储'Total'标识
        total_row[col] = 'Total'
    else:
        total_row[col] = ''  # 其他列留空

# 将总额作为新行追加到 DataFrame 中
df = pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)

# 将 DataFrame 写入 Excel 文件
# 使用 openpyxl 引擎来处理 xlsx 文件
with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='Sheet1')

print(f"Excel文件已成功生成: {excel_file}")
