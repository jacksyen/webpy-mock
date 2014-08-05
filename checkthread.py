# -*- coding:utf-8 -*-
# checkthread.py ---
#
# Filename: checkthread.py
# Description:
# Author:
# Maintainer:
# Created: 周二 八月  5 12:47:52 2014 (+0800)
# Version:
# Package-Requires: ()
# Last-Updated:
#           By:
#     Update #: 10
# URL:
# Doc URL:
# Keywords:
# Compatibility:
#
#

# Commentary:
#
#
#
#

# Change Log:
#
#
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.
#
#
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

# Code:
class CheckThread(threading.Thread):

    def __init__(self):
        logger.log().info(u'线程启动')
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            logger.log().info(u'销毁conn')
            SQLite.close(self.conn)

    def execute(self):
        self.db.execute('SELECT * FROM easylife_payment_order WHERE status=? AND iskeephangup=?', ('PROCESSING', 0))
        procs = self.db.fetchall()
        account = {}
        for info in procs:
            self.db.execute('SELECT * FROM %s WHERE usercode = ?' %Global.GLOBAL_TABLE_PAYMENT_USER, (info['usercode'],))
            account = self.db.fetchone()
            flagNum = 0
            if account['rechangeStatus']:
                if account['rechangeStatus'] == 'SUCCESS':
                    flagNum = 1
                else:
                    flagNum = 2
            res = self.getresult(info['paymentAmount'], flagNum)
            self.db.execute('UPDATE easylife_payment_order SET status = ?, resultcode = ?, updatetime = ? WHERE easylifeorderno = ?', (res.get('status'), res.get('resultCode'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), info['easyLifeOrderNo']))
            self.conn.commit()
            logger.log().info(u'修改订单：%s状态为%s，剩余备付金：%s', info['easyLifeOrderNo'], res.get('status'), res.get('balance'))

    def run(self):
        while True:
            try:
                self.execute()
                #10秒后重新检测
                time.sleep(10)
            except KeyboardInterrupt:
                logger.log().error(u'用户打断')
                exit(-1)
            except Exception, err:
                logger.log().error(u'定时修改状态出现异常:%s.', err)
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


#
# checkthread.py ends here
