from flask import Flask, request, render_template,session

import data

import time


import config

import os

from datetime import timedelta

from flask import Flask, render_template, send_from_directory, send_file,redirect

import user


app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)  # 设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 设置session的保存时间。

@app.before_request
def print_request_info():
    path = str(request.path)
    print("请求地址：" + str(request.path))
    print(session)

    if path == "/login" or path == "/toregister" or path == "/register":
        print("success")
        return

    if not "username" in session:
        return render_template('login.html')
    else:
        print("已经登录")

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


'''
登录
'''
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if user.checkUser(username, password):
        session['username'] = username
        return render_template('index.html')
    return render_template('login.html', message='用户名或密码错误，请联系917961898')

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@app.route('/toregister', methods=['GET'])
def toregister():
    return render_template('register.html')

'''
注册
'''
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get("username")
    password = request.form.get('password')
    user.adduser(username, password)
    return render_template('login.html', username=username, password=password, tip='注册成功！')

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


'''
/heatmap热力图可视化
'''
@app.route('/heatmap', methods=['GET'])
def heatmap():
    return render_template('heatmap/heatmap.html')



if __name__ == '__main__':
    app.run(config.host, config.port)