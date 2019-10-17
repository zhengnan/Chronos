#!
import json
import os
from flask import Flask, url_for, render_template, request, redirect
from werkzeug.datastructures import ImmutableMultiDict
import datetime
import time

app = Flask(__name__)

#TEST_DATA_PATH = '/Users/nanzhen/workspace/Chronos/test_data/'
TEST_DATA_PATH = '/Users/jzzhangz/Documents/workspace/Chronos/test_data/'

# route()方法用于设定路由；类似spring路由配置
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/brddetailp.html')
def brdp_detail():
    data = load_test_data()
    section1 = data.get('changeDesc')
    section2 = data.get('rate')
    rateTitle = data.get('rateTitle')
    section3 = data.get('profitability')
    section4 = data.get('eta')
    section5 = data.get('profitability1')
    section6 = data.get('profitability2')
    section7 = data.get('etaTime')
    return render_template('brddetailp.html', section1=section1, rateTitle=rateTitle, section2=section2, section3=section3, section4=section4,section5=section5,section6=section6,section7=section7)

@app.route('/brddetailn.html')
def brdn_detail():
    data = load_test_data()
    section1 = data.get('changeDesc')
    section2 = data.get('rate')
    section3 = data.get('profitability')
    section4 = data.get('eta')
    return render_template('brddetailn.html', section1=section1, section2=section2, section3=section3, section4=section4)

@app.route('/hello', methods=['POST', 'GET'])
def hello():
    para = request.args.get('section1')
    return render_template('timeline.html')

@app.route('/modify.html')
def modify():
    datakey_data = ['123', '321']
    return render_template('/modify.html', fee_type_data='123', datakey_data=datakey_data)

@app.route('/comments', methods=['POST', 'GET'])
def comments():
    print(request.args)
    return 'OK'

@app.route('/input.html')
def input():
    return render_template('/input.html')

@app.route('/first', methods=['POST', 'GET'])
def first():
    process_first(request.args.to_dict())
    return 'OK'

@app.route('/update.html')
def update():
    data = load_test_data()
    rate = data.get('rate')
    rateTitle = data.get('rateTitle')
    feeType = data.get('feeType')
    datakey = data.get('datakey')
    datakeyall = data.get('datakeyall')
    changeDesc = data.get('changeDesc')
    profitability = data.get('profitability')
    eta = data.get('eta')
    etaTime = data.get('etaTime')
    profitability = data.get('profitability')
    profitability1 = data.get('profitability1')
    profitability2 = data.get('profitability2')
    return render_template('/update.html', eta=eta, rate=rate, rateTitle=rateTitle, feeType=feeType, datakey=datakey, datakeyall=datakeyall, changeDesc=changeDesc, profitability=profitability, profitability1=profitability, profitability2=profitability2,etaTime=etaTime)


@app.route('/timeline.html')
def timeline():
    data = load_test_data()
    date_1 = data.get('eta').split("\"}")[0][-11:].replace(" ","")
    date_2 = data.get('eta').split("\"}")[1][-11:].replace(" ","")
    date_3 = data.get('eta').split("\"}")[2][-11:].replace(" ","")
    date_4 = data.get('eta').split("\"}")[3][-11:].replace(" ","")

    return render_template('timeline.html'
                           , date1=date_1
                           , date2=date_2
                           , date3=date_3
                           , date4=date_4
                           , remaindate1=cal_remain_days(date_1)
                           , remaindate2=cal_remain_days(date_2)
                           , remaindate3=cal_remain_days(date_3)
                           , remaindate4=cal_remain_days(date_4)
                           )

def process_first(origin):
    keys = origin.keys()
    l = list(keys)
    data = eval(l[0])
    dump_test_data(data)

def load_test_data():
    data = {}
    with open(os.path.join(TEST_DATA_PATH, 'TestCase.json'), 'r') as f:
        data = json.load(f)
    return data

def dump_test_data(data):
    with open(os.path.join(TEST_DATA_PATH, 'TestCase.json'), 'w') as f:
        json.dump(data, f)

def cal_remain_days(end_date):
    tmp1 = time.strptime(end_date, "%Y-%m-%d")
    end = datetime.datetime(tmp1[0], tmp1[1], tmp1[2])
    print(end-datetime.datetime.now())
    return str(end-datetime.datetime.now()).split(",")[0]


if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host=127.0.0.1, port=5000, debug=false
    app.run(debug=True)
