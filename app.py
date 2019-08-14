from flask import Flask, request, render_template

import data

import time


import config

import os

from flask import Flask, render_template, send_from_directory, send_file

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')



@app.route('/doData', methods=['POST'])
def signin():
    max_lon = request.form.get('max_lon')
    min_lon = request.form.get('min_lon')
    max_lat = request.form.get('max_lat')
    min_lat = request.form.get('min_lat')

    print(max_lon, min_lon, max_lat, min_lat)
    if(max_lon is None or max_lon is ''):
        return render_template('result.html', message='请输入完整的范围经纬度!')
    if (min_lon is None or max_lon is ''):
        return render_template('result.html', message='请输入完整的范围经纬度!')
    if (max_lat is None or max_lon is ''):
        return render_template('result.html', message='请输入完整的范围经纬度!')
    if (min_lat is None or max_lon is ''):
        return render_template('result.html', message='请输入完整的范围经纬度!')

    try:
        config.max_lon = int(max_lon)
        config.min_lon = int(min_lon)
        config.max_lat = int(max_lat)
        config.min_lat = int(min_lat)
    except Exception as e:
        return render_template('result.html', message='请输入整数类型的经纬度')

    print("爬取开始")


    flag = True
    now_time_str = str(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())))
    file_name = "TecentData-" + now_time_str + ".csv"
    while (flag):  # 一直循环吧，相信我，不到一小时你电脑硬盘就要炸，大概速度是一分钟一百兆数据就可以爬下来
        for i in range(4):
            try:
                data.get_TecentData(4, i, file_name)  # 主要是循环count，来获取四个链接里的数据
            except Exception as e:
                return render_template('result.html', message='爬取失败，请联系管理员')
        flag = False
    print('运行成功')

    return send_from_directory(directory=os.getcwd(), filename=file_name, as_attachment=True, mimetype='application/octet-stream')

if __name__ == '__main__':
    app.run()