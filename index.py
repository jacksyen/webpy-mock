# -*- coding:utf-8 -*-

import os
import web
import json
import threading
import time
import random
import logging
from util import RandomUtil
from util import MD5Util
from util import DateUtil
from webglobal import Global
from dbase import SQLite

urls = (
    '/','index'
)

GLOBAL_ACCOUNT = [
    # 水费
    {'1000001': {'userCode': '1000001', 'username': u'东家', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市渝中区88号', 'memo': '缴费成功', 'money': 120.00, 'status': 'SUCCESS', 'applyResultCode': '0000000'},
     '1000002': {'userCode': '1000002', 'username': u'李嘉家', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市江北区999号', 'memo': '缴费失败', 'money': 20.00, 'status': 'FAIL', 'applyResultCode': '0000106'},
     '1000003': {'userCode': '1000002', 'username': u'李嘉家', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市江北区999号', 'memo': '缴费处理中', 'money': 10.90, 'status': 'HANGUP', 'applyResultCode': '0000107'},
     '1000004': {'userCode': '1000004', 'username': u'周博', 'success': 'true', 'queryResultCode': '0000121'},
     '1000005': {'userCode': '1000005', 'username': u'郑中', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市江北区999号', 'memo': '缴费处理中', 'money': 10.90, 'status': 'HANGUP', 'applyResultCode': '0000107', 'isHangup': True}
    },
    # 气费
    {'2000001': {'userCode': '2000001', 'username': u'么么', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市渝中区门店8号', 'memo': '缴费成功', 'money': 312.88, 'status': 'SUCCESS', 'applyResultCode': '0000000'},
     '2000002': {'userCode': '2000002', 'username': u'刘尼', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市江北区洋河北路10号', 'memo': '缴费失败', 'money': 39.09, 'status': 'FAIL', 'applyResultCode': '0000106'},
     '2000003': {'userCode': '2000003', 'username': u'哈格', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市九龙坡区12号', 'memo': '缴费处理中', 'money': 19.10, 'status': 'HANGUP', 'applyResultCode': '0000107'},
     '2000004': {'userCode': '2000004', 'username': u'张尼', 'success': 'true', 'queryResultCode': '0000121'}
    },
    # 电费
    {'3000001': {'userCode': '3000001', 'username': u'占方式', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市渝中区11号', 'memo': '缴费成功', 'money': 81.20, 'status': 'SUCCESS', 'applyResultCode': '0000000'},
     '3000002': {'userCode': '3000002', 'username': u'张三丰', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市江北区健康路121号', 'memo': '缴费失败', 'money': 9.02, 'status': 'FAIL', 'applyResultCode': '0000106'},
     '3000003': {'userCode': '3000003', 'username': u'杨富', 'success': 'true', 'queryResultCode': '0000000','address': u'重庆市渝中区龙组路89号', 'memo': '缴费处理中', 'money': 190.90, 'status': 'HANGUP', 'applyResultCode': '0000107'},
     '3000004': {'userCode': '3000004', 'username': u'王博', 'success': 'true', 'queryResultCode': '0000121'}
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

    def __init__(self):
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del(self):
        if self.conn:
            logging.info(u'销毁conn')
            SQLite.close(self.conn)

    def GET(self):
        return self.execute()

    def POST(self):
        return self.execute()

    def execute(self):
        args = web.input()
        logging.info(u'入参:%s', args)
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
        self.db.execute('SELECT balance FROM %s WHERE merchantkey = ? ORDER BY updatetime desc limit 1' %Global.GLOBAL_TABLE_BALANCE, (Global.GLOBAL_MERCHANTS.get('lencee'),))
        querybalance = self.db.fetchone()
        if not querybalance:
            # 商户预存款未找到
            pass
        balance = querybalance['balance']
        if resultInfo.get('status') == 'SUCCESS':
            orderStatus = 'SUCCESS'
            resultCode = '0000000'
            # 修改商户预存款
            balance = float(format(balance - float(args.get('paymentAmount')), '.2f'))
            self.db.execute('UPDATE %s SET balance = ?, updatetime = ? WHERE merchantkey = ?' %Global.GLOBAL_TABLE_BALANCE, (balance, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), Global.GLOBAL_MERCHANTS.get('lencee')))
            self.conn.commit()
        elif resultInfo.get('status') == 'FAIL':
            orderStatus = 'FAIL'
            resultCode = '0000106'
        elif resultInfo.get('status') == 'HANGUP':
            orderStatus = 'PROCESSING'
            resultCode = '0000107'

        self.db.execute('INSERT INTO easylife_payment_order(easylifeorderno, outbizno, status, paymenttype, usercode, resultcode, paymentamount, addtime, updatetime) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', (easyLifeOrderNo, args.get('outBizNo'), orderStatus, queryType, args.get('userCode'), resultCode, float(args.get('paymentAmount')), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
        self.conn.commit()
        result = {
            'success': 'T',
            'signType': 'MD5',
            'outBizNo': args.get('outBizNo'),
            'orderStatus': orderStatus,
            'orderNo': args.get('orderNo'),
            'easyLifeOrderNo': easyLifeOrderNo,
            'channelId': RandomUtil.random6Str(),
            'balance': balance,
            'resultCode': resultInfo.get('applyResultCode'),
            'paymentResultInfos': '%s' %paymentResultInfos
        }
        from operator import itemgetter
        import urllib
        sortList = sorted(result.iteritems(), key=lambda d:d[0])
        sign = '&'.join(['%s=%s' %(k,v) for k,v in sortList])
        sign += Global.GLOBAL_MERCHANTS.get('lencee')
        result['sign'] = MD5Util.md5(sign)

        r = json.dumps(result)
        logging.info(u'缴费返回:%s', r)
        return r

    '''
    查询缴费状态
    '''
    def queryStatus(self, args):
        self.db.execute('SELECT * FROM easylife_payment_order WHERE outbizno = ?', (args.get('outBizNo'),))
        requestinfo = self.db.fetchone()
        data = {
            'success': 'T',
            'signType': 'MD5',
            'channelId': RandomUtil.random6Str(),
            'orderNo': args.get('orderNo')
        }
        if requestinfo:
            data['resultCode'] = requestinfo['resultCode']
            data['status'] = requestinfo['status']
        else:
            data['resultCode'] = '0000110'
            data['resultMessage'] = u"数据未找到"
        sign = '%s= %s%s' %('data', json.dumps(data), Global.GLOBAL_MERCHANTS.get('lencee'))
        result = {
            'data': data,
            'sign': MD5Util.md5(sign)
        }
        r = json.dumps(result)
        logging.info(u'查询缴费状态返回:%s', r)
        return r

    '''
    查询欠费
    '''
    def queryBill(self, args):
        globals = {}
        queryType = args.get('queryType')
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
        result = self.queryHandle(args, globals)
        logging.info(u'查询欠费返回：%s', str(result))
        return result


    '''
    查询处理
    '''
    def queryHandle(self, args, globals):
        resultInfo = globals.get(args.get('userCode'))
        if resultInfo == None:
            resultCode = '0000120'
        else:
            resultCode = resultInfo.get('queryResultCode')
        data = {
            'resultCode': resultCode,
            'orderNo': args.get('orderNo'),
            'channelId': RandomUtil.random6Str(),
            'signType': 'MD5',
            'success': 'T'
        }
        if resultCode == '0000000':
            info = {
                'address': resultInfo.get('address'),
                'agencyCode': args.get('agencyCode'),
                'extendInfo': {},
                'items': [{'channelCode': RandomUtil.random9Str(), 'charge': '0.00', 'month': DateUtil.getDate(), 'payables': resultInfo.get('money'), 'type': args.get('queryType')}],
                'success': resultInfo.get('success'),
                'userCode': resultInfo.get('userCode'),
                'username': resultInfo.get('username')
            }
            data['info'] = info
            data['totalPayable'] = resultInfo.get('money')
        else:
            data['resultMessage'] = Global.GLOBAL_RESP_CODE.get(resultCode)
        sign = '%s= %s%s' %('data', json.dumps(data), Global.GLOBAL_MERCHANTS.get('lencee'))
        result = {
            'data': data,
            'sign': MD5Util.md5(sign)
        }
        return json.dumps(result)

class CheckThread(threading.Thread):

    def __init__(self):
        logging.info(u'线程启动')
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            logging.info(u'销毁conn')
            SQLite.close(self.conn)

    def execute(self):
        self.db.execute('SELECT * FROM easylife_payment_order WHERE status=?', ('PROCESSING',))
        procs = self.db.fetchall()
        account = {}
        for info in procs:
            if info['paymentType'] == '000010':
                #水费
                globals = GLOBAL_ACCOUNT[0]
            elif info['paymentType'] == '000020':
                # 气费
                globals = GLOBAL_ACCOUNT[1]
            elif info['paymentType'] == '000030':
                # 电费
                globals = GLOBAL_ACCOUNT[2]
            elif info['paymentType'] == '000040':
                # 手机充值
                globals = GLOBAL_ACCOUNT[3]

            account = globals.get(info['userCode'])
            if account.get('isHangup') == True:
                continue
            flagNum = 0
            if account.get('rechangeStatus'):
                if account.get('rechangeStatus') == 'SUCCESS':
                    flagNum = 1
                else:
                    flagNum = 2
            res = self.getresult(info['paymentAmount'], flagNum)
            self.db.execute('UPDATE easylife_payment_order SET status = ?, resultcode = ?, updatetime = ? WHERE easylifeorderno = ?', (res.get('status'), res.get('resultCode'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), info['easyLifeOrderNo']))
            self.conn.commit()
            logging.info(u'修改订单：%s状态为%s，剩余备付金：%s', info['easyLifeOrderNo'], res.get('status'), res.get('balance'))

    def run(self):
        while True:
            try:
                self.execute()
                #10秒后重新检测
                time.sleep(10)
            except KeyboardInterrupt:
                logging.error(u'用户打断')
                exit(-1)
            except Exception, err:
                logging.error(u'定时修改状态出现异常:%s.', err)
                exit(-1)


    def getresult(self, money, flagNum=0):
        result = {}
        if flagNum:
            num = flagNum
        else:
            num = random.randint(1,2)
        self.db.execute('SELECT balance FROM %s WHERE merchantkey = ? ORDER BY updatetime desc limit 1' %Global.GLOBAL_TABLE_BALANCE, (Global.GLOBAL_MERCHANTS.get('lencee'),))
        querybalance = self.db.fetchone()
        if not querybalance:
            # 商户预存款未找到
            pass
        balance = querybalance['balance']
        if num == 1:
            result['status'] = 'SUCCESS'
            result['resultCode'] = '0000000'
            balance = float(format(balance - float(money), '.2f'))
            self.db.execute('UPDATE %s SET balance = ?, updatetime = ? WHERE merchantkey = ?' %Global.GLOBAL_TABLE_BALANCE, (balance, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), Global.GLOBAL_MERCHANTS.get('lencee')))
            self.conn.commit()
        else:
            result['status'] = 'FAIL'
            result['resultCode'] = '0000106'
        result['balance'] = balance
        return result


def func():
    app = web.application(urls, globals())
    app.run()

def func2():
    check = CheckThread()
    check.run()

if __name__ == '__main__':
    path = "log"
    if not os.path.exists(path):
        os.mkdir(path)
    # 日志系统
    filePath = "%s/easylife" %(path)
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S'
                        )
    import logging.handlers
    filehandler = logging.handlers.TimedRotatingFileHandler(filePath, when='D', interval=1, backupCount=0)
    filehandler.suffix = '%Y-%m-%d.log'
    logger = logging.getLogger('')
    logger.addHandler(filehandler)

    logging.info(u'-----------易生活mock系统启动-----------')
    # 初始化数据
    SQLite.init()
    app1 = threading.Thread(target=func)
    app2 = threading.Thread(target=func2)
    app1.start()
    app2.start()
