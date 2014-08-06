# -*- coding:utf-8 -*-

import web
import json
import threading

from log import logger
from webglobal import Global
from dbase import SQLite

from querybill import QueryBill
from applybill import ApplyBill
from querystatus import QueryStatus
from rechange import Rechange
from rechangepost import RechangePost
from checkthread import CheckThread
from addbreach import AddBreach


urls = (
    '/','index',
    '/rechange','Rechange',
    '/rechange/post', 'RechangePost',
    '/rechange/change', 'AddBreach'
)

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
        logger.info(u'入参:%s' %args)
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
        logger.info(u'出参：%s' %str(result))
        return json.dumps(result)


def func():
    app = web.application(urls, globals())
    app.run()

def func2():
    check = CheckThread()
    check.run()

if __name__ == '__main__':
    logger.info(u'-----------易生活mock系统启动-----------')
    # 初始化数据
    SQLite.init()
    app1 = threading.Thread(target=func)
    app2 = threading.Thread(target=func2)
    app1.start()
    app2.start()
