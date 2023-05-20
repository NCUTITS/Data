"""
统计30秒内的车辆数
"""
import os
import pandas as pd
import re


path = "已完成/" #设置文件夹路径
columns = ["开始时刻", "结束时刻", "交通量"]  #定义 Excel 文件中表头的名称

for files in os.listdir(path):  #遍历文件夹中的每个文件
    file = path + files   #获取当前文件的完整路径

    with open(file, 'r') as f:  #打开当前文件并读取其内容
        lines = f.readlines()   #读取文件所有行
        # 数据拆分到list1
        # list1 = [[None] for _ in range(len(lines) * 30)]
        # 数据聚合到list2（交通量）、list3（排队长度）
        list2 = []
        lst2 = []
        # my_array = np.empty((0, 2), str)
        j = 0
        l = 0
        sec = 0
        sec1 = None
        for line in lines:   #循环对每行操作
            breakdown = list(filter(None, re.split(r'\s|}|\{|]|\[|,|"|:', line)))  #一行数据中的元素进行拆分
            rows = int(breakdown[7])  #获取一行中包含几个目标车辆
            for i in range(0, rows):
                lst2.append(breakdown[i * 68 + 46]) #依次append
            if sec1 is not None:
                sec += int(breakdown[rows * 68 + 14]) - sec1  #求取时间差
            sec1 = int(breakdown[rows * 68 + 14])  #赋值最新时间
            if sec > 30000:   #如果时间差大于30秒
                list2.append([sec1 - sec, sec1, len(set(lst2))])  #append 开始时刻、结束时刻、交通量
                print(sec1 - sec, sec1, len(set(lst2)))  #print 开始时刻、结束时刻、交通量
                sec = 0
                sec1 = None
                lst2 = []
        out = "rcu_flow_out/" + files.replace('.txt', '') + "_flow.xlsx"   #构造输出 Excel 文件的文件名
        print("开始写入", out)
        df = pd.DataFrame(list2, columns=columns)     #将处理后的数据转换为 pandas.DataFrame 格式
        df.to_excel(out, sheet_name='sheet1', engine='openpyxl')     #将 DataFrame 中的数据写入 Excel 文件
        print("写入完成")
