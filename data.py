# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 00:45:20 2018
@author: Liuj
"""
import requests
import json
import pandas as pd
import time
import config


def get_TecentData(count=4, rank=0, file_name = 'TencentDat.csv'):  # 先默认为从rank从0开始
    url = 'https://xingyun.map.qq.com/api/getXingyunPoints'
    locs = ''
    paload = {'count': count, 'rank': rank}
    response = requests.post(url, data=json.dumps(paload))
    datas = response.text
    dictdatas = json.loads(datas)  # dumps是将dict转化成str格式，loads是将str转化成dict格式
    time = dictdatas["time"]  # 有了dict格式就可以根据关键字提取数据了，先提取时间
    print(time)
    locs = dictdatas["locs"]  # 再提取locs（这个需要进一步分析提取出经纬度和定位次数）
    locss = locs.split(",")
    # newloc=[locss[i:i+3] for i in range(0,len(locss),3)]
    temp = []  # 搞一个容器
    for i in range(int(len(locss) / 3)):
        lat = locss[0 + 3 * i]  # 得到纬度
        lon = locss[1 + 3 * i]  # 得到经度
        count = locss[2 + 3 * i]
        
        if(config.min_lat<int(lat)<config.max_lat and  config.min_lon<int(lon)<config.max_lon):
            temp.append([time, int(lat) / 100, int(lon) / 100, count])  # 容器追加四个字段的数据：时间，纬度，经度和定位次数

    result = pd.DataFrame(temp)  # 用到神器pandas，真好用
    result.dropna()  # 去掉脏数据，相当于数据过滤了
    result.columns = ['time', 'lat', 'lon', 'count']
    print(file_name)
    result.to_csv(file_name, mode='a', index=False)  # model="a",a的意思就是append，可以把得到的数据一直往TecentData.txt中追加

