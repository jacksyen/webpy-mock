# -*- coding:utf-8 -*-
# rechange.py ---
#
# Filename: rechange.py
# Description:
# Author:
# Maintainer:
# Created: 周二 八月  5 12:45:52 2014 (+0800)
# Version:
# Package-Requires: ()
# Last-Updated:
#           By:
#     Update #: 42
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
class Rechange:

    def __init__(self):
        self.render = web.template.render('templates', base='layout')
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            logger.info(u'销毁conn')
            SQLite.close(self.conn)

    def GET(self):
        self.db.execute('select balance from %s where merchantkey = ?' %Global.GLOBAL_TABLE_BALANCE, (Global.GLOBAL_MERCHANTS.get('lencee'),))
        querybalance = self.db.fetchone()
        balance = querybalance['balance']

        # 获取所有缴费用户
        self.db.execute('SELECT usercode, paymentmoney, breach, flag, paymenttype FROM %s WHERE paymentstatus = "SUCCESS" and paymenttype != "000040" ORDER BY paymenttype' %Global.GLOBAL_TABLE_PAYMENT_USER)
        infos = self.db.fetchall()
        newInfos = [dict(row) for row in infos]
        for info in newInfos:
            # 获取用户的欠费信息
            self.db.execute('SELECT sum(itemmoney) paymentmoney, sum(breach) breach from %s WHERE usercode = ?' %Global.GLOBAL_TABLE_USER_ARREARS, (info['usercode'],))
            arrear = self.db.fetchone()
            info['paymentmoney'] = arrear['paymentmoney']
            info['breach'] = arrear['breach']
        return self.render.rechange(balance, newInfos)
#
# rechange.py ends here
