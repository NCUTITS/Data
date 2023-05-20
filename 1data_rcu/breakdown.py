"""
功能：拆分文件每行的元素并生成Excel文档
"""
import re
import os
import xlsxwriter
path = "rcu/"        #设置文件所在的路径
columns = ["deviceType", "dataVersion", "rcuId", "targetsNum", "deviceId", "speedNorth",   #定义Excel文件中的列名
           "locEast",
           "accelVert", "latitude", "type", "uuid", "lenplateNo", "speed", "plateColor", "len",
           "eleConfidence",
           "accelVertConfidence", "height", "longitude", "elevation", "locNorth", "heading",
           "plateNo",
           "plateType",
           "objColor", "posConfidence", "laneId", "speedEastConfidence", "histLocNum",
           "speedEast",
           "trackedTimes",
           "filterInfoType", "objId", "width", "spdConfidence", "speedNorthConfidence",
           "headConfidence",
           "predLocNum", "status", "channelId", "timestamp"]

for files in os.listdir(path): #遍历指定目录下的所有文件
    file = path + files        #拼接文件名和路径
    out = "rcu_out/" + files.replace('.txt', '') + ".xlsx"  #定义输出Excel文件名
    with open(file, 'r') as f:  #打开输入文件并读取数据
        lines = f.readlines()  #读取所有行
        list1 = []
        j = 0
        sum_line = 0
        for line in lines:     #循环对每行操作
            breakdown = list(filter(None, re.split(r'\s|}|\{|]|\[|,|"|:', line))) #一行数据中的元素进行拆分
            rows = line.count("status")       #计算每行数据中包含多少个"status"字段，也就是一行有几个目标
            for i in range(0, rows):
                list1.append([breakdown[1], breakdown[3], breakdown[5], breakdown[7], breakdown[9],      #将提取后的数据添加到列表中
                              breakdown[i * 68 + 12], breakdown[i * 68 + 14], breakdown[i * 68 + 16],
                              breakdown[i * 68 + 18], breakdown[i * 68 + 20], breakdown[i * 68 + 22],
                              breakdown[i * 68 + 24], breakdown[i * 68 + 26], breakdown[i * 68 + 28],
                              breakdown[i * 68 + 30], breakdown[i * 68 + 32], breakdown[i * 68 + 34],
                              breakdown[i * 68 + 36], breakdown[i * 68 + 38], breakdown[i * 68 + 40],
                              breakdown[i * 68 + 42], breakdown[i * 68 + 44], breakdown[i * 68 + 46],
                              breakdown[i * 68 + 48], breakdown[i * 68 + 50], breakdown[i * 68 + 52],
                              breakdown[i * 68 + 54], breakdown[i * 68 + 56], breakdown[i * 68 + 58],
                              breakdown[i * 68 + 60], breakdown[i * 68 + 62], breakdown[i * 68 + 64],
                              breakdown[i * 68 + 66], breakdown[i * 68 + 68], breakdown[i * 68 + 70],
                              breakdown[i * 68 + 72], breakdown[i * 68 + 74], breakdown[i * 68 + 76],
                              breakdown[i * 68 + 78], breakdown[rows * 68 + 12], breakdown[rows * 68 + 14]])
                sum_line += 1
                print(sum_line)

        print("开始写入", out)
        workbook = xlsxwriter.Workbook(out)    #创建一个输出Excel文件
        for i in range(0, len(list1), 1000000):   #对 list1 进行分块，每块的大小为 1000000 个元素。
            worksheet = workbook.add_worksheet('sheet{}'.format(i / 1000000 + 1))     #为每个分块创建一个 Excel 工作表，工作表名称为 'sheet1'、'sheet2'、'sheet3‘
            for row_num, row_data in enumerate(list1[i:i + 1000000]):#遍历当前分块中的每一行数据
                row_data_str = list(map(str, row_data))  #将行数据中的每个元素都转换为字符串，存储在列表 row_data_str 中
                worksheet.write_row(row_num, 0, row_data_str)  #将当前行的数据写入 Excel 工作表中。
        workbook.close() #完成数据写入后，关闭 Excel 文件
        print("写入完成")


