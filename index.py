# -*- coding:utf-8 -*-

import web
import json
import threading
import time
import random
from util import RandomUtil
from util import MD5Util
from util import DateUtil
from webglobal import Global

urls = (
    '/','index'
)
key='9a7520152a7a97cfc76c82454463a83c'

GLOBAL_ACCOUNT = [
    # 水费
    {'1000001': {'userCode': '1000001', 'username': u'东家', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市渝中区88号', 'memo': '缴费成功', 'money': 120.00, 'status': 'SUCCESS', 'applyResultCode': '0000000'},
     '1000002': {'userCode': '1000002', 'username': u'李嘉家', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市江北区999号', 'memo': '缴费失败', 'money': 20.00, 'status': 'FAIL', 'applyResultCode': '0000106'},
     '1000003': {'userCode': '1000002', 'username': u'李嘉家', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市江北区999号', 'memo': '缴费处理中', 'money': 10.90, 'status': 'HANGUP', 'applyResultCode': '0000107'}
    },
    # 气费
    {'2000001': {'userCode': '2000001', 'username': u'么么', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市渝中区门店8号', 'memo': '缴费成功', 'money': 312.88, 'status': 'SUCCESS', 'applyResultCode': '0000000'},
     '2000002': {'userCode': '2000002', 'username': u'刘尼', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市江北区洋河北路10号', 'memo': '缴费失败', 'money': 39.09, 'status': 'FAIL', 'applyResultCode': '0000106'},
     '2000003': {'userCode': '2000003', 'username': u'哈格', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市九龙坡区12号', 'memo': '缴费处理中', 'money': 19.10, 'status': 'HANGUP', 'applyResultCode': '0000107'}
    },
    # 电费
    {'3000001': {'userCode': '3000001', 'username': u'占方式', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市渝中区11号', 'memo': '缴费成功', 'money': 81.20, 'status': 'SUCCESS', 'applyResultCode': '0000000'},
     '3000002': {'userCode': '3000002', 'username': u'张三丰', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市江北区健康路121号', 'memo': '缴费失败', 'money': 9.02, 'status': 'FAIL', 'applyResultCode': '0000106'},
     '3000003': {'userCode': '3000003', 'username': u'杨富', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市渝中区龙组路89号', 'memo': '缴费处理中', 'money': 190.90, 'status': 'HANGUP', 'applyResultCode': '0000107'}
    },
    # 手机充值
    {
        '18523125117': {'userCode': '18523125117', 'status': 'SUCCESS', 'applyResultCode': '0000000'},
        '15123334382': {'userCode': '15123334382', 'status': 'FAIL', 'applyResultCode': '0000106'},
        '13811111111': {'userCode': '13811111111', 'status': 'HANGUP', 'applyResultCode': '0000107', 'rechangeStatus': 'FAIL'},
        '13822222222': {'userCode': '13822222222', 'status': 'HANGUP', 'applyResultCode': '0000107', 'rechangeStatus': 'SUCCESS'}
    }
]


class index:
    def GET(self):
        return self.execute()

    def POST(self):
        return self.execute()

    def execute(self):
        args = web.input()
        service = args.get('service')
        if service == 'queryBillPayableAmountV2':
            # 查询账单欠费
            return self.queryBill(args)
        elif service == 'applyBillPaymentV2':
            # 缴费
            return self.applyBill(args)
        elif service == 'queryOrderStatusV2':
            # 查询状态
            return self.queryStatus(args)
        return 'not support service'

    '''
    账单缴费
    '''
    def applyBill(self, args):
        Global.GLOBAL_BALANCE
        queryType = args.get('paymentType')
        globals = {}
        if queryType == '000010':
            # 水费
            globals = GLOBAL_ACCOUNT[0]
        elif queryType == '000020':
            # 气费
            globals = GLOBAL_ACCOUNT[1]
        elif queryType == '000030':
            # 电费
            globals = GLOBAL_ACCOUNT[2]
        elif queryType == '000040':
            # 手机充值
            globals = GLOBAL_ACCOUNT[3]

        resultInfo = globals.get(args.get('userCode'))
        if resultInfo == None:
            return None

        paymentResultInfos = [
            {
                'agencyCode': args.get('agencyCode'),
                'charge':'0.00',
                'itemNo':'',
                'itemOutSerialNo':'',
                'memo': resultInfo.get('memo'),
                'money': resultInfo.get('money'),
                'status': resultInfo.get('status'),
                'type': queryType,
                'userCode': args.get('userCode')
            }
        ]
        easyLifeOrderNo = RandomUtil.random32Str()
        request = {
            'easyLifeOrderNo': easyLifeOrderNo,
            'outBizNo': args.get('outBizNo'),
            'paymentType': queryType,
            'paymentAmount': float(args.get('paymentAmount')),
            'userCode': args.get('userCode')
        }
        if resultInfo.get('status') == 'SUCCESS':
            orderStatus = 'SUCCESS'
            resultCode = '0000000'
            Global.GLOBAL_BALANCE = Global.GLOBAL_BALANCE - float(args.get('paymentAmount'))
        elif resultInfo.get('status') == 'FAIL':
            orderStatus = 'FAIL'
            resultCode = '0000106'
        elif resultInfo.get('status') == 'HANGUP':
            orderStatus = 'PROCESSING'
            resultCode = '0000107'

        request['status'] = orderStatus
        request['resultCode'] = resultCode
        Global.GLOBAL_REQUEST[args.get('outBizNo')] = request

        result = {
            'success': 'T',
            'signType': 'MD5',
            'sign': '84142521f0c8d29ab4ecfcdc8a92d88a',
            'outBizNo': args.get('outBizNo'),
            'orderStatus': orderStatus,
            'orderNo': args.get('orderNo'),
            'easyLifeOrderNo': easyLifeOrderNo,
            'channelId': RandomUtil.random6Str(),
            'balance': Global.GLOBAL_BALANCE,
            'resultCode': resultInfo.get('applyResultCode'),
            'paymentResultInfos': paymentResultInfos
        }
        return json.dumps(result);

    '''
    查询缴费状态
    '''
    def queryStatus(self, args):

        print 'global request:%s' %Global.GLOBAL_REQUEST
        requestinfo = Global.GLOBAL_REQUEST.get(args.get('outBizNo'))
        if requestinfo == None:
            return None

        data = {
            'resultCode': requestinfo.get('resultCode'),
            'status': requestinfo.get('status'),
            'success': 'T',
            'resultMessage': '',
            'signType': 'MD5',
            'channelId': RandomUtil.random6Str(),
            'orderNo': args.get('orderNo')
        }
        result = {
            'sign': RandomUtil.random32Str(),
            'data': data
        }
        return json.dumps(result);

    '''
    查询欠费
    '''
    def queryBill(self, args):
        queryType = args.get('queryType')
        if queryType == '000010':
            # 水费
            globals = GLOBAL_ACCOUNT[0]
            return self.queryHandle(args, globals)
        elif queryType == '000020':
            # 气费
            globals = GLOBAL_ACCOUNT[1]
            return self.queryHandle(args, globals)
        elif queryType == '000030':
            # 电费
            globals = GLOBAL_ACCOUNT[2]
            return self.queryHandle(args, globals)


    '''
    查询处理
    '''
    def queryHandle(self, args, globals):
        resultInfo = globals.get(args.get('userCode'))
        if resultInfo == None:
            return None
        print resultInfo
        info = {
            'address': resultInfo.get('address'),
            'agencyCode': args.get('agencyCode'),
            'extendInfo': {},
            'items': [{'channelCode': RandomUtil.random9Str(), 'charge': '0.00', 'month': DateUtil.getDate(), 'payables': resultInfo.get('money'), 'type': args.get('queryType')}],
            'success': resultInfo.get('success'),
            'userCode': resultInfo.get('userCode'),
            'username': resultInfo.get('username')
        }
        data = {
            'resultCode': resultInfo.get('queryResultCode'),
            'totalPayable': resultInfo.get('money'),
            'info': info,
            'orderNo': args.get('orderNo'),
            'channelId': '312312312432',
            'signType': 'MD5',
            'success': 'T'
        }
        result = {
            'data': data,
            'sign': RandomUtil.random32Str()
        }
        return json.dumps(result);

class CheckThread(threading.Thread):

    def __init__(self):
        print u'线程启动'

    def run(self):
        while True:
            for request in Global.GLOBAL_REQUEST:
                info = Global.GLOBAL_REQUEST.get(request)
                if info.get('status') == 'PROCESSING':
                    globals = {}
                    if info.get('paymentType') == '000010':
                        #水费
                        globals = GLOBAL_ACCOUNT[0]
                    elif info.get('paymentType') == '000020':
                        # 气费
                        globals = GLOBAL_ACCOUNT[1]
                    elif info.get('paymentType') == '000030':
                        # 电费
                        globals = GLOBAL_ACCOUNT[2]
                    elif info.get('paymentType') == '000040':
                        # 手机充值
                        globals = GLOBAL_ACCOUNT[3]
                    account = globals.get(info.get('userCode'))
                    flagNum = 0
                    if account.get('rechangeStatus'):
                        if account.get('rechangeStatus') == 'SUCCESS':
                            flagNum = 1
                    res = self.getresult(info.get('paymentAmount'), flagNum)
                    info['status'] = res.get('status')
                    info['resultCode'] = res.get('resultCode')
                    print u'修改订单：%s状态为%s，剩余备付金：%s' %(info.get('easyLifeOrderNo'), info.get('status'), Global.GLOBAL_BALANCE)
                    Global.GLOBAL_REQUEST[request] = info
            #10秒后重新检测
            time.sleep(10)

    def getresult(self, money, flagNum=0):
        Global.GLOBAL_BALANCE
        result = {}
        if flagNum:
            num = flagNum
        else:
            num = random.randint(1,2)
        if num == 1:
            result['status'] = 'SUCCESS'
            result['resultCode'] = '0000000'
            Global.GLOBAL_BALANCE = Global.GLOBAL_BALANCE - money
        else:
            result['status'] = 'FAIL'
            result['resultCode'] = '0000106'
        return result


def func():
    app = web.application(urls, globals())
    app.run()

def func2():
    check = CheckThread()
    check.run()

if __name__ == '__main__':
    app1 = threading.Thread(target=func)
    app2 = threading.Thread(target=func2)
    app1.start()
    app2.start()
