import pandas as pd
import numpy as np

import csv


def get_map_data(filepath):
    #filepath = "C:\\Users\\hgvgh\\Desktop\\tencent-location\\upload\\TecentData-2019-08-17-21-44-25.csv"
    csv_data = pd.read_csv(filepath, usecols=['lon', 'lat', 'count'])
    with open(filepath, 'r') as f:
        reader = csv.reader(f)

        res = []
        ls = []
        i = 0
        for da in reader:
            if i == 0:
                i = i + 1
                continue
            lon = da[2]
            lat = da[1]
            count = da[3]
            data = {"elevation": count, "coord": [lon, lat]}
            ls.append(data)
            i = i + 1
        res.append(ls)

        return res

    ''' 
    print(type(csv_data))
    res = []
    ls = []
    for one in csv_data:
        lon = csv_data['lon']
        lat = csv_data['lat']
        count = csv_data['count']
        print(lon)
        data = {"elevation": count.replace("\n", ""), "coord" : [lon.replace("\n", ""), lat.replace("\n", "")]}
        ls.append(data)
    res.append(ls)
    '''

    return ""


