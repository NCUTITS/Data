"""
统计
"""
import os
import sys
import pandas as pd
import numpy as np
import string
import re
import openpyxl
import xlsxwriter
import itertools
"""
在这个表达式中，path 是一个字符串变量，表示数据包的路径，例如 "rcu_wait_out/"。首先，path.replace("rcu_", "")
表示将字符串中所有出现的 "rcu_" 替换为空字符串，得到 "wait_out/"。接着，replace("_out/", "") 表示将字符串中所有出现的
"_out/" 替换为空字符串，得到 "wait"，即为数据包的类型。
"""
# 初始化
path = "rcu_wait_out/"  # 取数据包（修改处）
type = path.replace("rcu_", "").replace("_out/", "")
columns = ["统计时刻", "2023/03/21/ 07:00:00-09:00:00", "2023/03/21/ 17:00:00-19:00:00",
           "2023/03/21/ 19:00:00-21:00:00", "2023/03/25/ 14:00:00-16:00:00"]   #定义 Excel 文件中表头的名称
list1 = [[i * 30, 0, 0, 0, 0] for i in range(235)]
count20230321070000 = 0  #初始化
count20230321170000 = 0
count20230321190000 = 0
count20230325140000 = 0

# 数据统计-输入
for files in os.listdir(path):  #遍历文件夹中的每个文件
    file = path + files         #获取当前文件的完整路径
    date = files.split("_")[2]  # 日期提取，提取文件名中的日期信息
    df = pd.read_excel(file)    #读取 Excel 文件为 DataFrame 对象
    if len(df.index) >= 235:  # 剔除失效文件
        if date == "20230321070000":   # 判断文件属于哪个时间段
            count20230321070000 += 1
            for i in range(0, 235):
                list1[i][1] += df.iloc[i, 3]     #获取 DataFrame 对象中第 i 行、第四列的元素的值。
        elif date == "20230321170000":
            count20230321170000 += 1
            for i in range(0, 235):
                list1[i][2] += df.iloc[i, 3]
        elif date == "20230321190000":
            count20230321190000 += 1
            for i in range(0, 235):
                list1[i][3] += df.iloc[i, 3]
        elif date == "20230325140000":
            count20230325140000 += 1
            for i in range(0, 235):
                list1[i][4] += df.iloc[i, 3]
# 统计各时间段文件数量
print(count20230321070000, count20230321170000, count20230321190000, count20230325140000)

# 数据修正-参数标定
if type == "flow":
    amendment = 120
elif type == "speed":
    amendment = 3.6
elif type == "wait":
    amendment = 1
# 均值、修正-输出
for i in range(0, 235):
    list1[i][1] /= count20230321070000 / amendment
    list1[i][2] /= count20230321170000 / amendment
    list1[i][3] /= count20230321190000 / amendment
    list1[i][4] /= count20230325140000 / amendment

# 写文件
print(type + ".xlsx")
df1 = pd.DataFrame(list1, columns=columns)    # 创建 DataFrame 对象
df1.to_excel(type + ".xlsx", engine='openpyxl')   # 将 DataFrame 对象写入Excel 文件
print("写入完成")
