## 导入需要的库
##
import pandas as pd
import json
import matplotlib.pyplot as plt
import time
import csv
import matplotlib

## 创建空列表以存储数据
vehiclelist = []
traffic_flow = []

## 打开并读取所需处理的文件
with open('traffic_indicators_CS_0143_NG_NB1520309188_NB1520309188_20230321170000_20230321190000.txt', 'r', encoding='utf-8') as file:
    ## 遍历文件的每一行
    for line in file:
        ## 将每一行解析为JSON并存到vehiclelist中
        data = json.loads(line)
        vehiclelist.append(data)

## 创建一个空的DataFrame以存储处理后的数据
df = pd.DataFrame()
## 遍历vehiclelist中的每个车辆
for vehiclelistitem in vehiclelist:
    ## 提取时间戳并将其转化
    timestamp = vehiclelistitem['timeSec']
    date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
    timeType = vehiclelistitem['timeType']
    roadId = vehiclelistitem['roadId']
    
    ## 遍历每个车辆数据中的每个分支
    for branchitem in vehiclelistitem['laneData']['branchDataList']:
        branchId = branchitem['branchId']
        
        ## 遍历每个分支数据中的每个车道
        for laneData_item in branchitem['laneData']:
            laneTurnType = laneData_item['laneTurnType']
            laneId = laneData_item['laneId']
            laneOccupationRatio = laneData_item['laneOccupationRatio']
            
            ## 遍历每个车道数据中的每个流量数据
            for flow in laneData_item['flowData']:
                queueCount = flow['queueCount']
                queueLength = flow['queueLength']
                greenTime = flow['greenTime']
                trafficFlow = flow['trafficFlow']
                wastTime = flow['wastTime']
                trafficNumber = flow['trafficNumber']
                flowType = flow['flowType']
                
                ## 创建包含流量数据的字典并存到traffic_flow列表中
                flow_dict = {'timeSec': timestamp, 'date_time': date_time, 'timeType': timeType, 'roadId': roadId,
                             'laneTurnType': laneTurnType, 'laneId': laneId, 'laneOccupationRatio': laneOccupationRatio,
                             'queueCount': queueCount, 'queueLength': queueLength, 'greenTime': greenTime,
                             'trafficFlow': trafficFlow, 'wastTime': wastTime, 'trafficNumber': trafficNumber,
                             'flowType': flowType}
                traffic_flow.append(flow_dict)

## 将traffic_flow列表拼接成一个DataFrame
df = pd.concat([df, pd.DataFrame(traffic_flow)])

## 将结果输出为.csv文件
df.to_csv("traffic_indicators_CS_0143_NG_NB1520309188_NB1520309188_20230321170000_20230321190000.csv", index=False)
#df.to_excel("traffic_indicators_CS_0143_NG_NB1520309188_NB1520309188_20230321170000_20230321190000.xlsx", index=False)
##打开处理结果进行可视化操作
df  = pd.read_csv('1traffic_indicators_CS_0143_NG_NB1520309188_NB1520309188_20230321170000_20230321190000.csv',
                  parse_dates=['date_time'],dtype={'timesce':'datetime64[ns]'})
## 以时间轴
df  = df.set_index('date_time')
##1绘制排队车辆数随时间变化图
plt.plot(df.index,df['queueCount'])
##设置x轴的格式
plt.xlabel('date_time')
plt.xticks(rotation=45,ha='right')
##设置y轴的标签
plt.ylabel('queueCount')
#显示图形
plt.show()
##2绘制折线图
plt.plot(df.index,df['queueLength'])
##设置x轴的格式
plt.xlabel('date_time')
plt.xticks(rotation=45,ha='right')
##设置y轴的标签
plt.ylabel('queueLength')
#显示图形
plt.show()

##3绘制绿灯时间随时间变化图
plt.plot(df.index,df['greenTime'])
##设置x轴的格式
plt.xlabel('date_time')
plt.xticks(rotation=45,ha='right')
##设置y轴的标签
plt.ylabel('greenTime')
#显示图形
plt.show()
##4绘制交通流量随时间变化图
plt.plot(df.index,df['trafficFlow'])
##设置x轴的格式
plt.xlabel('date_time')
plt.xticks(rotation=45,ha='right')
##设置y轴的标签
plt.ylabel('trafficFlow')
#显示图形
plt.show()
##5绘制交通数量随时间变化图
plt.plot(df.index,df['trafficNumber'])
##设置x轴的格式
plt.xlabel('date_time')
plt.xticks(rotation=45,ha='right')
##设置y轴的标签
plt.ylabel('trafficNumber')
#显示图形
plt.show()
##6绘制延误时间随时间变化图
plt.plot(df.index,df['wastTime'])
##设置x轴的格式
plt.xlabel('date_time')
plt.xticks(rotation=45,ha='right')
##设置y轴的标签
plt.ylabel('wastTime')
#显示图形
plt.show()