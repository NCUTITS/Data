"""
求取30秒内排队长度
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
from collections import Counter

path = "rcu/"  #设置文件所在的路径
columns = ["开始时刻", "结束时刻", "排队长度"]      #定义 Excel 文件中表头的名称

for files in os.listdir(path):   #遍历文件夹中的每个文件
    file = path + files          #获取当前文件的完整路径

    with open(file, 'r') as f:   #打开当前文件并读取其内容
        lines = f.readlines()    #读取文件所有行
        # 数据拆分到list1
        # list1 = [[None] for _ in range(len(lines) * 30)] # 不用时注释掉以节省内存
        # 数据聚合到list2（交通量）、list3（平均速度）、list4（平均排队长度）
        list2 = []
        list3 = []
        list4 = []
        # 数据聚合-过程列表lst2（交通量）、lst3（平均速度）、list4（平均排队长度）
        lst2 = []
        lst3 = []
        lst4 = []
        # my_array = np.empty((0, 2), str)
        j = 0
        l = 0
        sec = 0
        sec1 = None
        for line in lines:   #循环对每行操作
            breakdown = list(filter(None, re.split(r'\s|}|\{|]|\[|,|"|:', line)))   #一行数据中的元素进行拆分
            rows = int(breakdown[7])     #获取一行中包含几个目标车辆
            for i in range(0, rows):
                if sec1 is None:
                    lst4.append(breakdown[i * 68 + 22])   #依次append  uuid
            if sec1 is not None:
                sec += int(breakdown[rows * 68 + 14]) - sec1  #求取时间差
            sec1 = int(breakdown[rows * 68 + 14])   #赋值最新时间
            if sec > 30000:  #如果时间差大于30秒
                for i in range(0, rows):
                    lst4.append(breakdown[i * 68 + 22])   #依次append  uuid
                counter = Counter(lst4)   #统计一个列表 lst4 中每个元素出现的次数
                num_duplicates = sum(count > 1 for count in counter.values())   #计算列表 counter.values() 中出现次数大于 1 的元素个数
                list4.append([sec1 - sec, sec1, num_duplicates])
                print(sec1 - sec, sec1, num_duplicates)
                sec = 0
                sec1 = None
                lst2 = []
                lst3 = []
                lst4 = []
        out = "rcu_wait_out/" + files.replace('.txt', '') + "_wait.xlsx"   #构造输出 Excel 文件的文件名
        print("开始写入", out)
        df = pd.DataFrame(list4, columns=columns)     #将处理后的数据转换为 pandas.DataFrame 格式
        df.to_excel(out, sheet_name='sheet1', engine='openpyxl')    #将 DataFrame 中的数据写入 Excel 文件
        print("写入完成")
