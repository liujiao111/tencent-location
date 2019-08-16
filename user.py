import csv

user_csv_file = 'user.csv'

def checkUser(username, password):
    csv_file = csv.reader(open(user_csv_file, 'r'))
    for users in csv_file:
        csv_username = users[0]
        csv_password = users[1]
        if csv_username == username:
            if csv_password == password:
                return True
    return False

def adduser(username, password):
    fields = [username, password]
    with open(r''+user_csv_file+'', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

if __name__ == '__main__':
    adduser('admin', '123')
    csv_file = csv.reader(open(user_csv_file, 'r'))
    for users in csv_file:
        csv_username = users[0]
        csv_password = users[1]
        print(csv_username,csv_password)
