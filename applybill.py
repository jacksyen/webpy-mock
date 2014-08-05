# -*- coding:utf-8 -*-
# applybill.py ---
#
# Filename: applybill.py
# Description:
# Author:
# Maintainer:
# Created: 周二 八月  5 12:32:14 2014 (+0800)
# Version:
# Package-Requires: ()
# Last-Updated:
#           By:
#     Update #: 36
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

from log import logger
from util import RandomUtil
from util import MD5Util
from util import DateUtil
from webglobal import Global
from dbase import SQLite

# Code:
class ApplyBill:

    def __init__(self):
        self.conn = SQLite.conn()
        self.db = self.conn.cursor()

    def __del__(self):
        if self.conn:
            SQLite.close(self.conn)

    '''
    账单缴费
    '''
    def applyBill(self, args):
        self.db.execute('SELECT * FROM %s WHERE usercode = ?' %Global.GLOBAL_TABLE_PAYMENT_USER, (args.get('userCode'),))
        resultInfo = self.db.fetchone()
        if resultInfo == None:
            return None
        paymentResultInfos = [
            {
                'agencyCode': args.get('agencyCode'),
                'charge':'0.0',
                'itemNo':'',
                'itemOutSerialNo':'',
                'memo': resultInfo['memo'],
                'money': resultInfo['paymentmoney'],
                'status': resultInfo['querystatus'],
                'type': resultInfo['paymentType'],
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
        if resultInfo['paymentstatus'] == 'SUCCESS':
            orderStatus = 'SUCCESS'
            resultCode = '0000000'
            # 修改商户预存款
            balance = float(format(balance - float(args.get('paymentAmount')), '.2f'))
            self.db.execute('UPDATE %s SET balance = ?, updatetime = ? WHERE merchantkey = ?' %Global.GLOBAL_TABLE_BALANCE, (balance, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), Global.GLOBAL_MERCHANTS.get('lencee')))
            self.conn.commit()
        elif resultInfo['paymentstatus'] == 'FAIL':
            orderStatus = 'FAIL'
            resultCode = resultInfo['paymentresultcode']
        elif resultInfo['paymentstatus'] == 'HANGUP':
            orderStatus = 'PROCESSING'
            resultCode = '0000107'

        # 是否保持挂起状态
        if resultInfo['ishangup']:
            iskeephangup = 1
        else:
            iskeephangup = 0
        self.db.execute('INSERT INTO easylife_payment_order(easylifeorderno, outbizno, status, paymenttype, usercode, resultcode, paymentamount, iskeephangup, addtime, updatetime) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (easyLifeOrderNo, args.get('outBizNo'), orderStatus, resultInfo['paymenttype'], args.get('userCode'), resultCode, float(args.get('paymentAmount')), iskeephangup, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
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
            'resultCode': resultInfo['paymentresultcode'],
            'paymentResultInfos': '%s' %paymentResultInfos
        }
        from operator import itemgetter
        import urllib
        sortList = sorted(result.iteritems(), key=lambda d:d[0])
        sign = '&'.join(['%s=%s' %(k,v) for k,v in sortList])
        sign += Global.GLOBAL_MERCHANTS.get('lencee')
        result['sign'] = MD5Util.md5(sign)
        return result
#
# applybill.py ends here
