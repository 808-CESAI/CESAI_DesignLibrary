# coding: utf-8

from flask import Flask, render_template, redirect, jsonify, send_file,request
import os
from flask_sqlalchemy import  SQLAlchemy
import datetime
import hashlib
import mymodels



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="**********************"

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


# 登陆
@app.route('/login/',methods=['POST'])
def login():
    a = datetime.datetime.now()
    username = request.form['username']
    password = request.form['password']
    paw = hashlib.md5(password.encode('utf-8'))#MD5加密
    user = mymodels.UserTable.query.filter_by(user_name=username).first()#通过用户名查找用户、
    print(user)
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
       db.close_all_sessions
       data['code'] = '200'
       data['msg'] = 'SUCCESS'
       data['data'] = {'id': NewUser.id, 'name': username}
    print(paw.hexdigest())
    b = datetime.datetime.now()
    print(b - a)
    return jsonify(data)


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


# 获取所有故事
@app.route('/GetStory/',methods=['POST'])
def GetStory():
    a = datetime.datetime.now()
    storys = mymodels.StoryTable.query.all()#获取所有故事
    data = {}  # 返回的json
    if len(storys) == 0:
        data['code'] = '404'
        data['msg'] = 'FAIL'
    else:
        data['code'] = '200'
        data['msg'] = 'SUCCESS'
        datas = {}
        lists = []
        for num in range(0,len(storys)):
            id = str(storys[num].id)
            title = str(storys[num].title)
            author = str(storys[num].author)
            img = str(storys[num].picture)
            story = {}
            story['id'] =id
            story['title'] = title
            story['author'] = author
            story['img'] = img
            lists.append(story)

        datas['lists'] = lists
        data['data'] = datas

    b = datetime.datetime.now()
    print(b - a)
    return jsonify(data)


# 获取所有儿歌
@app.route('/GetSong/',methods=['POST'])
def GetSong():
    a = datetime.datetime.now()
    songs = mymodels.SongTable.query.all()#获取所有儿歌
    data = {}  # 返回的json
    if len(songs) == 0:
        data['code'] = '404'
        data['msg'] = 'FAIL'
    else:
        data['code'] = '200'
        data['msg'] = 'SUCCESS'
        datas = {}
        lists = []
        for num in range(0,len(songs)):
            id = str(songs[num].id)
            title = str(songs[num].title)
            img = str(songs[num].picture)
            singer = str(songs[num].singer)
            song = {}
            song['id'] =id
            song['title'] = title
            song['img'] = img
            song['singer'] = singer
            lists.append(song)

        datas['lists'] = lists
        data['data'] = datas

    b = datetime.datetime.now()
    print(b - a)
    return jsonify(data)


# 通过故事id获取配音
@app.route('/GetRecording/',methods=['POST'])
def GetRecording():
    a = datetime.datetime.now()
    StoryId = request.form['StoryId']  # 获取故事id参数
    recordings = mymodels.RecordingTable.query.filter_by(story_id=StoryId).all()#通过故事id查找配音
    data = {}  # 返回的json
    if len(recordings) == 0:
        data['code'] = '404'
        data['msg'] = 'FAIL'
    else:
        data['code'] = '200'
        data['msg'] = 'SUCCESS'
        datas = {}
        lists = []
        for num in range(0, len(recordings)):
            id = str(recordings[num].id)
            user_id = str(recordings[num].user_id)
            story_id = str(recordings[num].story_id)
            recording = str(recordings[num].recording)
            title = str(recordings[num].title)
            i = {}
            i['id'] = id
            i['user_id'] = user_id
            i['story_id'] = story_id
            i['recording'] = recording
            i['title'] = title
            lists.append(i)

        datas['lists'] = lists
        data['data'] = datas
    b = datetime.datetime.now()
    print(b - a)
    return jsonify(data)


# 获取所有合集
@app.route('/GetCollection/',methods=['POST'])
def GetCollection():
    a = datetime.datetime.now()
    collections = mymodels.CollectionTabe.query.all() # 获取所有合集
    data = {}  # 返回的json
    if len(collections) == 0:
        data['code'] = '404'
        data['msg'] = 'FAIL'
    else:
        data['code'] = '200'
        data['msg'] = 'SUCCESS'
        datas = {}
        lists = []
        for num in range(0, len(collections)):
            id = str(collections[num].id)
            title = str(collections[num].title)
            img = str(collections[num].picture)
            collection = {}
            collection['id'] = id
            collection['title'] = title
            collection['img'] = img
            lists.append(collection)

        datas['lists'] = lists
        data['data'] = datas
    b = datetime.datetime.now()
    print(b - a)
    return jsonify(data)

# 通过合集id获取动画
@app.route('/GetCartoon/',methods=['POST'])
def GetCartoon():
    a = datetime.datetime.now()
    CollectionId = request.form['CollectionId']  # 获取合集id参数
    cartoons = mymodels.CartoonTable.query.filter_by(collection_id=CollectionId).all()#通过合集id查找动画
    data = {}  # 返回的json
    if len(cartoons) == 0:
        data['code'] = '404'
        data['msg'] = 'FAIL'
    else:
        data['code'] = '200'
        data['msg'] = 'SUCCESS'
        datas = {}
        lists = []
        for num in range(0, len(cartoons)):
            id = str(cartoons[num].id)
            cartoon = str(cartoons[num].cartoon)
            title = str(cartoons[num].title)
            img = str(cartoons[num].picture)

            i = {}
            i['id'] = id
            i['cartoon'] = cartoon
            i['title'] = title
            i['img'] = img
            lists.append(i)

        datas['lists'] = lists
        data['data'] = datas
    b = datetime.datetime.now()
    print(b - a)
    return jsonify(data)


if __name__=='__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)




