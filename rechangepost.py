# -*- coding:utf-8 -*-
# rechangepost.py ---
#
# Filename: rechangepost.py
# Description:
# Author:
# Maintainer:
# Created: 周二 八月  5 12:46:47 2014 (+0800)
# Version:
# Package-Requires: ()
# Last-Updated:
#           By:
#     Update #: 14
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
class RechangePost:

    def __init__(self):
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            logger.info(u'销毁conn')
            SQLite.close(self.conn)

    def POST(self):
        args = web.input()
        logger.info(u'入参:%s' %args)
        amount = args.get('amount')
        result = {}
        if not amount or len(amount) == 0:
            result['status'] = 'FAIL'
            return
        try:
            addbalance = float(amount)
            if addbalance <=0:
                result['status'] = 'FAIL'
                return
            self.db.execute('SELECT balance FROM %s WHERE merchantkey = ? ORDER BY updatetime desc limit 1' %Global.GLOBAL_TABLE_BALANCE, (Global.GLOBAL_MERCHANTS.get('lencee'),))
            querybalance = self.db.fetchone()
            balance = querybalance['balance']
            balance = float(format(balance + addbalance, '.2f'))
            self.db.execute('UPDATE %s SET balance = ?, updatetime = ? WHERE merchantkey = ?' %Global.GLOBAL_TABLE_BALANCE, (balance, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), Global.GLOBAL_MERCHANTS.get('lencee')))
            self.conn.commit()
            result['status'] = 'SUCCESS'
            result['balance'] = balance
        except Exception, err:
            result['status'] = 'ABNORMAL'
            logger.error(u'增加商户预存款异常：%s' %err)
        r = json.dumps(result)
        logger.info(u'增加商户预存款返回:%s' %r)
        return r

#
# rechangepost.py ends here
