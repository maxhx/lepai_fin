import json 
from openpyxl import Workbook

# 创建一个新的工作簿
wb = Workbook()

# 选择默认工作表
ws = wb.active

# 打开JSON文件并读取数据
with open('从浏览器复制出来拷贝到此.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    vData = data['data']
    for row in vData:
        # print(row['orderId']+'\t'+row['totalBaseAmount'])
        ws.append([row['orderId'],row['totalBaseAmount']])
# 保存工作簿
wb.save('output.xlsx')    
