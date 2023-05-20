import json
import pandas as pd
import datetime

# 将JSON文件转换为Python对象
file = open("data1\spat_291_20230321170000_20230321190000.json", 'r', encoding='utf-8')
data_list = []
for line in file.readlines():
    data_dic = json.loads(line)  # 将JSON文件转换为Python对象
    data_list.append(data_dic)  # 写入列表

# 获取数据对象中的全部键结构
def get_keys(data, keys = []):
    if isinstance(data, dict):
        for k, v in data.items():
            new_keys = keys + [k]
            yield from get_keys(v, new_keys)
    elif isinstance(data, list):
        for i, v in enumerate(data):
            new_keys = keys + [i]
            yield from get_keys(v, new_keys)
    else:
        yield keys

all_keys = list(get_keys(data_dic))
for keys in all_keys:
    print(keys)

# 获取数据对象中的全部键结构与对应值
def print_keys(data, level=0):
    # 如果data是字典类型，则遍历所有键值对
    if isinstance(data, dict):
        for key, value in data.items():
            # 计算当前键的级别并输出缩进
            # print('  ' * level + key)仅获取键名
            current = '  ' * level
            print(f'{current}{key}:{value}')  # 获取键名与对应值
            # 递归遍历值中的键
            print_keys(value, level + 1)
    # 如果data是列表类型，则遍历所有元素
    elif isinstance(data, list):
        for item in data:
            # 递归遍历列表元素中的键
            print_keys(item, level + 1)
print_keys(data_dic)

# 将数据读到Pandas中
data1 = []
data2 = []
df1 = pd.DataFrame()
df2 = pd.DataFrame()
for data_list_item in data_list:
    # sendDataType = data_list_item['sendDataType']
    # message = data_list_item['message']
    # beforeKafkaTime = data_list_item['beforeKafkaTime']
    for data_item in data_list_item['message']:
        # data = data_item['data']
        # regionId = data_item['regionId']
        for intersections_item in data_item['data']:
            # intersections = intersections_item['intersections']
            # msgType = intersections_item['msgType']
            # msgCnt = intersections_item['msgCnt']
            # uuid = intersections_item['uuid']
            # timestamp = intersections_item['timestamp']
            for phases_item in intersections_item['intersections']:
                # phases = phases_item['phases']
                # intersectionTimestamp = phases_item['intersectionTimestamp']
                # regionId = phases_item['regionId']
                # nodeId = phases_item['nodeId']
                # status = phases_item['status']
                for phaseStates_item in phases_item['phases']:
                    # phaseStates = phaseStates_item['phaseStates']  # 相位状态
                    phaseId = phaseStates_item['phaseId']  # 相位ID
                    for para_item in phaseStates_item['phaseStates']:
                        nextStartUTCTime = para_item['nextStartUTCTime']  # 下一次相位启动的UTC时间
                        nextStartlocTime = datetime.datetime.fromtimestamp(nextStartUTCTime // 1000)  # 下一次相位启动的北京时间
                        light = para_item['light']  # 当前相位的信号灯状态
                        nextEndUTCTime = para_item['nextEndUTCTime']  # 下一次相位结束的UTC时间
                        nextEndlocTime = datetime.datetime.fromtimestamp(nextEndUTCTime // 1000)  # 下一次相位结束的北京时间
                        likelyEndTime = para_item['likelyEndTime']  # 当前相位可能结束的时间
                        likelyEndUTCTime = para_item['likelyEndUTCTime']  # 当前相位可能结束的UTC时间
                        likelyEndlocTime = datetime.datetime.fromtimestamp(likelyEndUTCTime // 1000)  # 当前相位可能结束的北京时间
                        nextDuration = para_item['nextDuration']  # 下一相位的持续时间
                        startTime = para_item['startTime']  # 当前相位开始的时间
                        startUTCTime = para_item['startUTCTime']  # 当前相位开始的UTC时间
                        startlocTime = datetime.datetime.fromtimestamp(startUTCTime // 1000)  # 当前相位开始的北京时间
                        duration = (para_item['nextStartUTCTime'] - para_item['startUTCTime']) / 1000  # 当前相位持续的时间
                        data1_dic = {'phaseId': phaseId, 'light': light, 'startlocTime': startlocTime, 'startUTCTime': startUTCTime,
                                      'duration': duration, 'startTime': startTime, 'likelyEndTime': likelyEndTime,
                                     'nextStartUTCTime': nextStartUTCTime, 'nextStartlocTime': nextStartlocTime,
                                     'likelyEndUTCTime': likelyEndUTCTime, 'likelyEndlocTime': likelyEndlocTime,
                                      'nextEndUTCTime': nextEndUTCTime, 'nextEndlocTime': nextEndlocTime, 'nextDuration': nextDuration, }
                        data1.append(data1_dic)

df1 = pd.concat([df1, pd.DataFrame(data1)])
df1.to_csv("spat_291_20230321170000_20230321190000_deal.csv", index=False)


