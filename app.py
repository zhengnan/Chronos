#!
import json
import os
from flask import Flask, url_for, render_template, request, redirect
from werkzeug.datastructures import ImmutableMultiDict
import datetime
import time

app = Flask(__name__)

TEST_DATA_PATH = './test_data/'

# route()方法用于设定路由；类似spring路由配置
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/brddetailp.html')
def brdp_detail():
    return render_brd_page('brddetailp.html')

@app.route('/brddetailn.html')
def brdn_detail():
    return render_brd_page('brddetailn.html')

@app.route('/brddetail-readonly.html')
def brd_detail_readonly():
    return render_brd_page('brddetail-readonly.html')

def render_brd_page(html_file):
    data = load_test_data()
    section1 = data.get('changeDesc')
    section2 = data.get('rate')
    rateTitle = data.get('rateTitle')
    section3 = data.get('profitability')
    section4 = data.get('etaTime')
    section5 = data.get('eta')
    section6 = data.get('profitability1')
    section7 = data.get('profitability2')

    approveItems = get_parsed_approver_items()

    return render_template(html_file, section1=section1, rateTitle=rateTitle, section2=section2, section3=section3
        , section4=section4, section5=section5, section6=section6, section7=section7
        , approveItems=approveItems)

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

@app.route('/metric.html')
def metric():
    return render_template('/metric.html')

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
    return render_timeline_page('timeline.html')

def render_timeline_page(html_file):
    data = load_test_data()
    date_1 = data.get('eta')[0][1].replace(" ","")
    date_2 = data.get('eta')[1][1].replace(" ","")
    date_3 = data.get('eta')[2][1].replace(" ","")
    date_4 = data.get('eta')[3][1].replace(" ","")

    return render_template(html_file
                           , date1=date_1
                           , date2=date_2
                           , date3=date_3
                           , date4=date_4
                           , remaindate1=cal_remain_days(date_1)
                           , remaindate2=cal_remain_days(date_2)
                           , remaindate3=cal_remain_days(date_3)
                           , remaindate4=cal_remain_days(date_4)
                           )


@app.route('/devtimeline.html')
def devtimeline():
    return render_timeline_page('devtimeline.html')

@app.route('/approve', methods=['POST', 'GET'])
def approve():
    approver = 'Zheng, Nan'
    approveStatus = request.args.get(approver)
    cssClass = 'status-approved' if (approveStatus == 'Approved') else 'status'
    statusObj = {'status': approveStatus, 'cssClass': cssClass}
    print('statusObj: ', statusObj)

    persistData = load_approve_data()
    persistData[approver] = statusObj
    dump_approve_data(persistData)
    return 'OK'

@app.route('/markdone-phase1', methods=['POST', 'GET'])
def markDonePhase1():
    return markOnePhaseDone('P1')

def markOnePhaseDone(phaseName):
    persistData = load_phase_data()
    persistData[phaseName] = 'Done'
    dump_phase_data(persistData)
    return 'OK'

@app.route('/markdone-phase2', methods=['POST', 'GET'])
def markDonePhase2():
    return markOnePhaseDone('P2')

@app.route('/markdone-phase3', methods=['POST', 'GET'])
def markDonePhase3():
    return markOnePhaseDone('P3')

@app.route('/markdone-phase4', methods=['POST', 'GET'])
def markDonePhase4():
    return markOnePhaseDone('P4')

@app.route('/start.html')
def start():
    return render_template('start.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

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

def load_approve_data():
    data = {}
    with open(os.path.join(TEST_DATA_PATH, 'Reviewers.json'), 'r') as f:
        # print('In load_approve_data(). f: ', f)
        data = json.load(f)
    return data

def dump_approve_data(data):
    with open(os.path.join(TEST_DATA_PATH, 'Reviewers.json'), 'w') as f:
        json.dump(data, f)

def load_phase_data():
    data = {}
    with open(os.path.join(TEST_DATA_PATH, 'Phases.json'), 'r') as f:
        data = json.load(f)
        # print("phase data: ", data)
    return data

def dump_phase_data(data):
    with open(os.path.join(TEST_DATA_PATH, 'Phases.json'), 'w') as f:
        print("phase data to write: ", data)
        json.dump(data, f)

def cal_remain_days(end_date):
    tmp1 = time.strptime(end_date, "%Y-%m-%d")
    end = datetime.datetime(tmp1[0], tmp1[1], tmp1[2])
    print(end-datetime.datetime.now())
    diff = int(str(end-datetime.datetime.now()).split(" ")[0])
    print(diff)
    if diff<15:
        return "Risk: Only remain " + str(end-datetime.datetime.now()).split(",")[0]
    else:
        return "Remain " + str(end-datetime.datetime.now()).split(",")[0]
    return str(end-datetime.datetime.now()).split(",")[0]

def get_parsed_approver_items():
    outputItems = list()

    approveData = load_approve_data()
    # print('in brdn_detail(). approveData: ', approveData)

    dataKeys = approveData.keys()
    # print('approveData.keys(): ', dataKeys)
    for oneKey in dataKeys:
        loadedItem = approveData[oneKey]
        outputItem = dict()
        outputItem['approver'] = oneKey
        outputItem['status'] = loadedItem['status']
        outputItem['cssClass'] = loadedItem['cssClass']
        outputItems.append(outputItem)

    return outputItems

if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # 默认值：host=127.0.0.1, port=5000, debug=false
    app.run(debug=True)
