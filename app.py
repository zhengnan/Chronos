#!
import json
import os
from flask import Flask, url_for, render_template, request, redirect
from werkzeug.datastructures import ImmutableMultiDict

app = Flask(__name__)

TEST_DATA_PATH = '/Users/nanzhen/workspace/Chronos/test_data/'

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

@app.route('/timeline.html')
def timeline():
    return render_template('timeline.html')

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
    rate = [["true","true","1"],["true","false","2"],["false","true","3"],["false","false","4"]]
    rateTitle = ["sortable","panEU","rate"]
    feeType = '321'
    datakey = ['123', '321']
    datakeyall = ['123', '321']
    changeDesc = 'dsa'
    profitability = '32132'
    etaTime = '2019-10-19'
    eta= [["Validation Reguriment"," 2019-10-20 "],["Development"," 2019-10-23 "],["Test"," 2019-10-27 "],["Deployment"," 2019-10-30 "]]
    return render_template('/update.html', eta=eta, rate=rate, rateTitle=rateTitle, feeType=feeType, datakey=datakey, datakeyall=datakeyall, changeDesc=changeDesc, profitability=profitability, etaTime=etaTime)

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

if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host=127.0.0.1, port=5000, debug=false
    app.run(debug=True)
