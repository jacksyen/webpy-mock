# -*- coding:utf-8 -*-
# addbreach.py ---
#
# Filename: addbreach.py
# Description:
# Author:
# Maintainer:
# Created: 周二 八月  5 16:49:30 2014 (+0800)
# Version:
# Package-Requires: ()
# Last-Updated:
#           By:
#     Update #: 24
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
import web
import json
from log import logger
from util import DateUtil
from webglobal import Global
from dbase import SQLite

# Code:
class AddBreach:

    def __init__(self):
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            SQLite.close(self.conn)

    def POST(self):
        args = web.input()
        logger.info(u'入参:%s' %args)
        userCode = args.get('usercode')
        # 查询用户欠费信息
        self.db.execute('SELECT sum(itemmoney) paymentmoney, sum(breach) breach, itemno FROM %s WHERE usercode =?' %Global.GLOBAL_TABLE_USER_ARREARS, (userCode,))
        info = self.db.fetchone()
        result = {}
        if not info:
            result['msg'] = u'缴费用户信息未找到'
            r = json.dumps(result)
            logger.info(u'修改金额返回:%s' %r)
            return r
        try:
            amount = info['paymentmoney']
            balance = float(format(amount + 1.50, '.2f'))
            breach = str(format(float(info['breach']) + 1.5, '.2f'))
            self.db.execute('UPDATE %s SET paymentmoney = ?, breach = ?, updatetime = ? WHERE usercode = ?' %Global.GLOBAL_TABLE_PAYMENT_USER, (balance, breach, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), userCode))
            self.conn.commit()
            result['status'] = 'SUCCESS'
            result['balance'] = balance
            result['breach'] = breach
            result['msg'] = '修改成功'
        except Exception, e:
            logger.error(u'增加滞纳金失败')
            result['msg'] = u'修改失败'
        r = json.dumps(result)
        logger.info(u'修改金额返回:%s' %r)
        return r
#
# addbreach.py ends here
