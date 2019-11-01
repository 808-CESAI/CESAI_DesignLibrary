from flask import Flask, render_template, redirect, jsonify, send_file,request
import os
from flask_sqlalchemy import  SQLAlchemy
import datetime
import hashlib
import mymodels
import time


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="*******************************"

app.config['SQLALCHEMY_COMMIT-TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

@app.route('/hello/',methods=['POST'])
def hello():
    a = datetime.datetime.now()

    n = mymodels.UserTable.query.filter_by(user_name='aaa').first()
    print(n.password)
    m=mymodels.UserTable.query.all()
    b = datetime.datetime.now()
    print(b - a)
    return str(mymodels.UserTable.query.all()[0].password)

@app.route('/img/',methods=['POST'])
def img():
    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'./scr_file')
    filename ='1.jpg'  # Content-Type: image/png
    file = os.path.join(filepath, filename)

    a = datetime.datetime.now()
    print(mymodels.UserTable.query.all())
    b = datetime.datetime.now()
    print(b - a)

    return send_file(file)


# 通过用户id获取所有绘画
@app.route('/GetDraw/',methods=['POST'])
def GetDraw():
    a = datetime.datetime.now()
    UserId = request.form['UserId']#获取用户id参数
    draw = mymodels.DrawTable.query.filter_by(user_id=UserId).all()#通过用户id查找绘画
    data = {}#返回的json
    if len(draw) == 0:
        data['code'] = '404'
        data['msg'] = 'FAIL'
    else:
        data['code'] = '200'
        data['msg'] = 'SUCCESS'
        img = {}
        lists = []
        for num in range(0,len(draw)):
            id=str(draw[num].id)
            url=str(draw[num].image)
            i={}
            i['id'] = id
            i['url'] = url
            lists.append(i)

        img['lists'] = lists
        data['data'] = img
    b = datetime.datetime.now()
    print(b - a)
    return jsonify(data)

# 登陆
@app.route('/login/',methods=['POST'])
def login():
    a = datetime.datetime.now()
    username = request.form['username']
    password = request.form['password']
    paw = hashlib.md5(password.encode('utf-8'))#MD5加密
    user = mymodels.UserTable.query.filter_by(user_name=username).first()#通过用户名查找用户
    data = {}
    if user == None:
        data['code'] = '406'
        data['msg'] = 'user does not exist'
    else:
        if paw.hexdigest() == user.password:
            data['code'] = '200'
            data['msg'] = 'SUCCESS'
            data['data'] = {'id':user.id,'name':username}
        else:
            data['code'] = '406'
            data['msg'] = 'Password mismatch'

    print(paw.hexdigest())
    b = datetime.datetime.now()
    print(b - a)
    return jsonify(data)

# 注册
@app.route('/signin/',methods=['POST'])
def signin():
    a = datetime.datetime.now()
    username = request.form['username']
    password = request.form['password']
    tel = request.form['tel']
    mail = request.form['mail']
    if tel == '':
        tel = None;
    if mail == '':
        mail = None;

    paw = hashlib.md5(password.encode('utf-8'))#MD5加密
    user = mymodels.UserTable.query.filter_by(user_name=username).first()#通过用户名查找用户
    data = {}
    if user != None:#用户已存在
        data['code'] = '406'
        data['msg'] = 'User already exists'
    else:
       createtime = datetime.datetime.now()
       NewUser = mymodels.UserTable(user_name=username,password=paw.hexdigest(),tel=tel,mail=mail,create_time=createtime)
       db.session.add(NewUser)
       db.session.flush()#提交记录
       id = NewUser.id#获得id
       db.session.commit()#插入记录
       data['code'] = '200'
       data['msg'] = 'SUCCESS'
       data['data'] = {'id': NewUser.id, 'name': username}
    print(paw.hexdigest())
    b = datetime.datetime.now()
    print(b - a)
    return jsonify(data)


if __name__=='__main__':
    app.run(host='0.0.0.0')




