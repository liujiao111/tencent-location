from flask import Flask, request, render_template,session,url_for

import data
import json
import time
from werkzeug import secure_filename
from heatmap import get_map_data
import config
import poi
import os

from datetime import timedelta

from flask import Flask, render_template, send_from_directory, send_file,redirect

import user


app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)  # 设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 设置session的保存时间。


UPLOAD_FOLDER = '/upload'

ALLOWED_EXTENSIONS = set(['csv', 'xls', 'xlsx', 'txt'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.before_request
def print_request_info():
    path = str(request.path)
    print("请求地址：" + str(request.path))


    #static文件夹下的放行
    if path.startswith("/static"):
        print("success")
        return

    if path == "/doData":
        if not "username" in session:
            return render_template('login.html')
        else:
            print("已经登录")
    print("success")
    return
    '''
        if path == "/login" or path == "/toregister" or path == "/register" or path == "/":
        print("success")
        return
        '''



@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/tencent', methods=['GET'])
def tencent():
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


@app.route('/register', methods=['POST'])
def register():
    '''
    注册
    '''
    username = request.form.get("username")
    password = request.form.get('password')
    phone = request.form.get('phone')
    if phone == None or phone == "":
        phone = "111111"
    flag, message = user.adduser(username, password, phone)
    if flag:
        return render_template('login.html', username=username, password=password, tip='注册成功！')
    return render_template('register.html', username=username, password=password, message=message)

@app.route('/doData', methods=['POST'])
def load_tencent_location_data():
    '''
    腾讯位置大数据
    :return:
    '''
    max_lon = request.form.get('max_lon')
    min_lon = request.form.get('min_lon')
    max_lat = request.form.get('max_lat')
    min_lat = request.form.get('min_lat')

    username = session['username']
    print('登录用户：', username)

    #判断用户可用免费爬取额度
    tc_user = user.getUserByUsername(username)
    print('当前用户，已用次数， 最大可用次数:', username, tc_user[5], tc_user[3])

    if tc_user[5] > tc_user[3]:
        return render_template('index.html', message='您的可用免费额度已用完，请充值，充值联系qq：917961898!')

    print(max_lon, min_lon, max_lat, min_lat)
    if(max_lon is None or max_lon is ''):
        return render_template('index.html', message='请输入完整的范围经纬度!')
    if (min_lon is None or max_lon is ''):
        return render_template('index.html', message='请输入完整的范围经纬度!')
    if (max_lat is None or max_lon is ''):
        return render_template('index.html', message='请输入完整的范围经纬度!')
    if (min_lat is None or max_lon is ''):
        return render_template('index.html', message='请输入完整的范围经纬度!')

    try:
        config.max_lon = int(max_lon)
        config.min_lon = int(min_lon)
        config.max_lat = int(max_lat)
        config.min_lat = int(min_lat)
    except Exception as e:
        return render_template('index.html', message='请输入整数类型的经纬度')

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

    #增加用户使用的次数
    user.add_user_use_count(username, 1)

    return send_from_directory(directory=os.getcwd(), filename=file_name, as_attachment=True, mimetype='application/octet-stream')


'''
/heatmap热力图可视化
'''
@app.route('/heatmap', methods=['GET'])
def heatmap():
    return render_template('heatmap/heatmap.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print('=======================', request.args.get('type'))
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            basepath = os.path.abspath(os.getcwd())  # 当前文件所在工作目录
            file.save(os.path.join(basepath + "/upload", filename))
            if(request.args.get('type') == "heatmap") :
                mdata = get_map_data(basepath + "/upload" + "/" + filename)
            elif request.args.get('type') == "poi":
                mdata = poi.get_poi_map_data(basepath + "/upload" + "/" + filename)
            elif request.args.get('type') == "coord":
                t = {}
                t['filename'] =  "/upload" + "/" + filename
                return json.dumps(t, ensure_ascii=False)
                '''
                return send_from_directory(directory=os.getcwd(), filename=basepath + "/upload" + "/" + filename, as_attachment=True,
                                           mimetype='application/octet-stream')'''

            t = {}
            t['data'] = mdata
            #移除上传的文件
            os.remove(basepath + "/upload"+ "/" + filename)
            return json.dumps(t, ensure_ascii=False)


    return '''
       <!doctype html>
       <title>Upload new File</title>
       <h1>Upload new File</h1>
       <form action="" method=post enctype=multipart/form-data>
         <p><input type=file name=file>
            <input type=submit value=Upload>
       </form>
       '''
@app.route('/poi', methods=['GET'])
def to_poi_index():
    '''
    跳转到POI数据爬取页面
    :return:
    '''
    return render_template('poi/index.html')

@app.route('/poivisaul', methods=['GET'])
def to_poi_visual_page():
    '''
       跳转到POI数据可视化页面
       :return:
       '''
    return render_template('poi/visual.html')


# 获取POI数据
@app.route('/poidata', methods=['POST'])
def get_poi_data():
    city = request.form.get('city')
    area = request.form.get('area')
    keyword = request.form.get('keyword')
    coord = request.form.get('coord')
    key = request.form.get('key')
    if(city == None or city == ""):
        return render_template('poi/index.html', message="城市不能为空")
    if (keyword == None or keyword == ""):
        return render_template('poi/index.html', message="POI关键字不能为空")
    if (key == None or key == ""):
        return render_template('poi/index.html', message="密钥不能为空，如有需要请自行申请或者联系917961898获取")

    print(city, area, keyword, coord, key)
    filename = poi.get_data(city, area, keyword, coord, key)
    if filename == None:
        return render_template('poi/index.html', message="爬取失败")
    return send_from_directory(directory=os.getcwd(), filename=filename, as_attachment=True,
                               mimetype='application/octet-stream')



@app.route('/coordpage', methods=['GET'])
def to_coord_page():
    '''
       跳转到坐标转换页面
       :return:
       '''

    return render_template('coord/index.html')

@app.route('/download', methods=['GET'])
def download_file():
    '''
    下载文件
    :return:
    '''
    filename = request.args.get('filename')
    print(filename)
    return send_from_directory(directory=os.getcwd(), filename=filename, as_attachment=True,
                               mimetype='application/octet-stream')

if __name__ == '__main__':
    app.run(config.host, config.port)