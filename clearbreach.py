# -*- coding:utf-8 -*-
# clearbreach.py ---
#
# Filename: clearbreach.py
# Description:
# Author:
# Maintainer:
# Created: 周四 八月  7 17:51:18 2014 (+0800)
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
import web
import json
from log import logger
from util import DateUtil
from webglobal import Global
from dbase import SQLite

# Code:
class ClearBreach:

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
        result = {}
        try:
            self.db.execute('UPDATE %s SET breach = ?, updatetime = ? WHERE usercode = ?' %Global.GLOBAL_TABLE_PAYMENT_USER, ('0.0', DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), userCode))
            self.conn.commit()
            result['status'] = 'SUCCESS'
            result['breach'] = '0.0'
            result['msg'] = '修改成功'
        except Exception, e:
            logger.error(u'清空滞纳金失败')
            result['msg'] = u'修改失败'
        r = json.dumps(result)
        logger.info(u'清空滞纳金返回:%s' %r)
        return r
#
# clearbreach.py ends here
