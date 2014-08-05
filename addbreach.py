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
#     Update #: 3
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
        logger.log().info(u'入参:%s', args)
        userCode = args.get('usercode')
        self.db.execute('SELECT * FROM %s WHERE usercode =?' %Global.GLOBAL_TABLE_PAYMENT_USER, (userCode,))
        info = self.db.fetchone()
        if not info:
            pass
        amount = info['paymentmoney']
        balance = float(format(amount + 1.50, '.2f'))
        self.db.execute('UPDATE %s SET paymentmoney = ?, breach = ?, updatetime = ? WHERE usercode = ?' %Global.GLOBAL_TABLE_PAYMENT_USER, (balance, '1.50', DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), userCode))
        self.conn.commit()
        result = {}
        result['status'] = 'SUCCESS'
        result['balance'] = balance
        r = json.dumps(result)
        logger.log().info(u'修改金额返回:%s', r)
        return r
#
# addbreach.py ends here
