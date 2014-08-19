# -*- coding:utf-8 -*-
# querystatus.py ---
#
# Filename: querystatus.py
# Description:
# Author:
# Maintainer:
# Created: 周二 八月  5 12:40:09 2014 (+0800)
# Version:
# Package-Requires: ()
# Last-Updated:
#           By:
#     Update #: 28
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


import json

from log import logger
from util import RandomUtil
from util import MD5Util
from util import DateUtil
from webglobal import Global
from dbase import SQLite

# Code:
class QueryStatus:

    def __init__(self):
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            SQLite.close(self.conn)

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
            'orderNo': args.get('orderNo'),
            'info': []
        }
        try:
            if requestinfo:
                self.db.execute('SELECT * FROM %s WHERE usercode = ?' %Global.GLOBAL_TABLE_PAYMENT_USER, (requestinfo['usercode'], ))
                userinfo = self.db.fetchone()
                data['resultCode'] = requestinfo['resultcode']
                data['status'] = requestinfo['status']
                data['info'].append({'startCount': 200, 'endCount': userinfo['count'] + 200})
            else:
                data['resultCode'] = '0000110'
                data['resultMessage'] = u"数据未找到"
        except Exception, e:
            logger.error(e)
        sign = '%s= %s%s' %('data', json.dumps(data, ensure_ascii=False), Global.GLOBAL_MERCHANTS.get('lencee'))
        result = {
            'data': data,
            'sign': MD5Util.md5(sign)
        }
        return result

#
# querystatus.py ends here
