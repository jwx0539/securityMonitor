import re
import time
from flask import Flask
from flask import request
from flask import render_template
from connect_db import enqury_data

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    na_db = enqury_data()
    now_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    data_len = {'cve_len':na_db.cvedatas.count(),
    'wechat_len':na_db.wechatdatas.count(),
    'deepweb_len':na_db.deepwebdatas.count(),
    'anquanke_len':na_db.anquankedatas.count(),
    'seebug_len':na_db.seebugdatas.count(),
    }
    today_len = {
    'cve_today':na_db.cvedatas.find({'time':re.compile(now_time)}).count(),
    'wechat_today':na_db.wechatdatas.find({'time':re.compile(now_time)}).count(),
    'deepweb_today':na_db.deepwebdatas.find({'time':re.compile(now_time)}).count(),
    'anquanke_today':na_db.anquankedatas.find({'time':re.compile(now_time)}).count(),
    'seebug_today':na_db.seebugdatas.find({'time':re.compile(now_time)}).count(),
    }
    return render_template('home.html',data_len=data_len,today_len=today_len)

@app.route('/wechat', methods=['GET'])
def wechat():
    ress = []
    all_ress = []
    now_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    na_db = enqury_data()
    collections = na_db.wechatdatas
    for res in collections.find().sort('time',-1):
        ress.append(res)
    for i in collections.find().sort('time',-1):
        all_ress.append(i)
    return render_template('wechat.html',ress=ress,all_ress=all_ress)

@app.route('/deepweb', methods=['GET'])
def deepweb():
    deepdatas = []
    all_deepdatas = []
    now_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    na_db = enqury_data()
    collections = na_db.deepwebdatas
    for res in collections.find({'time':re.compile(now_time)}).sort('time',-1):
        deepdatas.append(res)
    for i in collections.find().sort('time',-1):
        all_deepdatas.append(i)
    return render_template('deepweb.html',deepdatas=deepdatas,all_deepdatas=all_deepdatas)

@app.route('/spider', methods=['GET'])
def spider():
    datas = []
    all_datas = []
    now_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    na_db = enqury_data()
    #print(now_time)
    collections = na_db.cvedatas
    for res in collections.find({'time':re.compile(now_time)}).sort('time',-1):
        datas.append(res)
    for i in collections.find().sort('time',-1):
        all_datas.append(i)
    return render_template('spider.html',datas=datas,all_datas=all_datas)


@app.route('/anquanke', methods=['GET'])
def anquanke():
    responses = []
    all_responses = []
    now_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    na_db = enqury_data()
    collections = na_db.anquankedatas
    for res in collections.find({'time':re.compile(now_time)}).sort('time',-1):
        responses.append(res)
    for i in collections.find().sort('time',-1):
        all_responses.append(i)
    return render_template('anquanke.html',responses=responses,all_responses=all_responses)

@app.route('/seebug', methods=['GET'])
def seebug():
    seebugs = []
    all_seebugs = []
    now_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    na_db = enqury_data()
    collections = na_db.seebugdatas
    for res in collections.find({'time':re.compile(now_time)}).sort('time',-1):
        seebugs.append(res)
    for i in collections.find().sort('time',-1):
        all_seebugs.append(i)
    return render_template('seebug.html',seebugs=seebugs,all_seebugs=all_seebugs)

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        wordlists = []
        content = request.form['content']
        na_db = enqury_data()
        collections = [na_db.cvedatas,na_db.wechatdatas,na_db.deepdatas,na_db.anquankedatas,na_db.seebugdatas]
        for collection in collections:
            for res in collection.find({'content':re.compile(content,re.IGNORECASE)}).sort('time',-1):
                wordlists.append(res)
        #print(wordlists)
        return render_template('result.html',wordlists=wordlists)
    else:
        return render_template('search.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')
    


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)