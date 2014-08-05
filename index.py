# -*- coding:utf-8 -*-

import os
import web
import json
import threading
import time
import random
from log import logger
from util import RandomUtil
from util import MD5Util
from util import DateUtil
from webglobal import Global
from dbase import SQLite
from querybill import QueryBill
from applybill import ApplyBill
from querystatus import QueryStatus
from rechange import Rechange
from rechangepost import RechangePost
from checkthread import CheckThread

urls = (
    '/','index',
    '/rechange','Rechange',
    '/rechange/post', 'RechangePost',
    '/rechange/change', 'change'
    
)

class change:

    def __init__(self):
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            SQLite.close(self.conn)

    def POST(self):
        args = web.input()
        logger.log().info(u'入参:%s', args)
        userCode = args.get('usercode')
        self.db.execute('SELECT * FROM %s WHERE usercode =?' %Global.GLOBAL_TABLE_PAYMENT_USER, (userCode,))
        info = self.db.fetchone()
        if not info:
            pass
        amount = info['paymentmoney']
        balance = float(format(amount + 1.50, '.2f'))
        self.db.execute('UPDATE %s SET paymentmoney = ?, updatetime = ? WHERE usercode = ?' %Global.GLOBAL_TABLE_PAYMENT_USER, (balance, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), userCode))
        self.conn.commit()
        result = {}
        result['status'] = 'SUCCESS'
        result['balance'] = balance
        r = json.dumps(result)
        logger.log().info(u'修改金额返回:%s', r)
        return r

class index:

    def __init__(self):
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            SQLite.close(self.conn)

    def GET(self):
        return self.execute()

    def POST(self):
        return self.execute()

    def execute(self):
        args = web.input()
        logger.log().info(u'入参:%s', args)
        service = args.get('service')
        result = {}
        if service == 'queryBillPayableAmountV2':
            # 查询账单欠费
            query = QueryBill()
            result = query.queryBill(args)
        elif service == 'applyBillPaymentV2':
            # 缴费
            bill = ApplyBill()
            result = bill.applyBill(args)
        elif service == 'queryOrderStatusV2':
            # 查询状态
            status = QueryStatus()
            result = status.queryStatus(args)
        logger.log().info(u'出参：%s', str(result))
        return json.dumps(result)


def func():
    app = web.application(urls, globals())
    app.run()

def func2():
    check = CheckThread()
    check.run()

if __name__ == '__main__':
    logger.log().info(u'-----------易生活mock系统启动-----------')
    # 初始化数据
    SQLite.init()
    app1 = threading.Thread(target=func)
    app2 = threading.Thread(target=func2)
    app1.start()
    app2.start()
