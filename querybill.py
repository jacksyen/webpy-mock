# -*- coding:utf-8 -*-
# querybill.py ---
#
# Filename: querybill.py
# Description:
# Author:
# Maintainer:
# Created: 周二 八月  5 12:12:38 2014 (+0800)
# Version:
# Package-Requires: ()
# Last-Updated:
#           By:
#     Update #: 31
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
class QueryBill:

    def __init__(self):
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            SQLite.close(self.conn)

        '''
    查询欠费
    '''
    def queryBill(self, args):
        self.db.execute('SELECT * FROM %s WHERE usercode = ?' %Global.GLOBAL_TABLE_PAYMENT_USER, (args.get('userCode'), ))
        globals = self.db.fetchone()
        if globals == None:
            resultCode = '0000120'
        else:
            resultCode = globals['queryresultcode']
        # 如果查询结果等于0000205，直接return
        if resultCode =='0000205':
            return None
        data = {
            'resultCode': resultCode,
            'orderNo': args.get('orderNo'),
            'channelId': RandomUtil.random6Str(),
            'signType': 'MD5',
            'success': 'T'
        }
        if resultCode == '0000000':
            info = {
                'address': globals['address'],
                'agencyCode': args.get('agencyCode'),
                'extendInfo': {},
                'items': [{'channelCode': RandomUtil.random9Str(), 'charge': '0.00', 'month': DateUtil.getDate(), 'payables': globals['paymentmoney'], 'type': args.get('queryType')}],
                'success': globals['querystatus'],
                'userCode': globals['usercode'],
                'username': globals['username']
            }
            data['info'] = info
            data['totalPayable'] = globals['paymentmoney']
        else:
            data['resultMessage'] = Global.GLOBAL_RESP_CODE.get(resultCode)
        sign = '%s= %s%s' %('data', json.dumps(data), Global.GLOBAL_MERCHANTS.get('lencee'))
        result = {
            'data': data,
            'sign': MD5Util.md5(sign)
        }
        return result

#
# querybill.py ends here
