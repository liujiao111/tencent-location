import pymysql

import config

import uuid

def get_connect():
    return pymysql.connect(host=config.db_host, user =config.db_username, password =config.db_password, database =config.db_database, charset ="utf8", port = config.db_port)


def checkUser(username, password):
    conn = get_connect()
    cursor = conn.cursor()
    sql = "select * from ct_user where username = %s"
    res = cursor.execute(sql, [username])

    one_data = cursor.fetchone()
    if one_data == None:
        return False
    if one_data[1] == username and one_data[2] == password:
        return True
    cursor.close()
    conn.close()

    return False



def getUserByUsername(username):
    '''
    根据用户名查询用户
    :param csv_username:
    :return:
    '''
    conn = get_connect()
    cursor = conn.cursor()
    sql = "select * from ct_user where username = %s"
    res = cursor.execute(sql, [username])

    one_data = cursor.fetchone()
    if one_data == None:
        return None
    cursor.close()
    conn.close()
    return one_data


def adduser(username, password, phone):
    '''
        新增用户
        :param username:
        :param password:
        :param phone:
        :return:
        '''
    tc_user = getUserByUsername(username)
    if tc_user is not None:
        return False, "注册失败,用户名已存在"


    conn = get_connect()
    cursor = conn.cursor()
    id = str(uuid.uuid1())
    sql = "insert into ct_user(id, username, password, phone, max_use_count) values(%s, %s, %s, %s, %s)"
    res = 0
    try:
        res = cursor.execute(sql, [id, username, password, phone, 0])
        print(res)
        conn.commit()
    except Exception:
        conn.rollback()
    cursor.close()
    conn.close()
    return True, "注册成功"


def add_user_use_count(username, count):
    '''
    增加用户使用额度
    :param username:
    :return:
    '''
    tc_user = getUserByUsername(username)
    if tc_user is None:
        return

    conn = get_connect()
    cursor = conn.cursor()

    org_count = getUserByUsername(username)[5]
    target_count = org_count + count
    sql = "update ct_user set used_count = %s where username= %s"

    res = cursor.execute(sql, [target_count, username])

    conn.commit()
    cursor.close()
    conn.close()
    return res
    

if __name__ == '__main__':
    '''
    adduser('admin', '123')
    csv_file = csv.reader(open(user_csv_file, 'r'))
    for users in csv_file:
        csv_username = users[0]
        csv_password = users[1]
        print(csv_username,csv_password)
        '''
    #print(getUserByUsername('gg'))

    #print(checkUser('admin', "sfs"))

    #print(add_user_use_count('admin', 1))

    print(adduser('admin222', 'ww', '24252'))