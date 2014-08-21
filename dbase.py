# -*- coding:utf-8 -*-

import sqlite3 as db
from webglobal import Global
from util import DateUtil
from util import RandomUtil

class SQLite:

    @staticmethod
    def init():
        conn = SQLite.conn()
        conn.text_factory = str
        cursor = conn.cursor()
        # 创建缴费信息表
        cursor.execute('''CREATE TABLE IF NOT EXISTS %s(easylifeorderno text, outbizno text, status text, paymenttype text, usercode text, resultcode text, paymentamount real, iskeephangup integer, addtime datetime, updatetime datetime)''' %(Global.GLOBAL_TABLE_PAYMENT))
        # 创建商户预存款表
        cursor.execute('''CREATE TABLE IF NOT EXISTS %s(merchantkey text, balance real, addtime datetime, updatetime datetime)''' %(Global.GLOBAL_TABLE_BALANCE))
        # 创建缴费用户信息表
        cursor.execute('''CREATE TABLE IF NOT EXISTS %s(usercode text, username text, querystatus text, queryresultcode text, address text, memo text, paymentmoney real, count real, price real, flag INTEGER, paymentstatus text, paymenttype text, paymentresultcode text, ishangup int, rechangestatus text, breach text, addtime datetime, updatetime datetime)''' %(Global.GLOBAL_TABLE_PAYMENT_USER))
        # 创建用户欠费信息表
        cursor.execute('''CREATE TABLE IF NOT EXISTS %s(itemno text, usercode text, count real, startcount real, endcount real, price real, breach text, itemmoney real, month text, addtime datetime, updatetime datetime)''' %Global.GLOBAL_TABLE_USER_ARREARS)

        for mer in Global.GLOBAL_MERCHANTS:
            cursor.execute('SELECT * FROM %s WHERE merchantkey = ?' %Global.GLOBAL_TABLE_BALANCE, (Global.GLOBAL_MERCHANTS.get(mer),))
            if cursor.fetchone():
                continue
            cursor.execute('INSERT INTO %s(merchantkey, balance, addtime, updatetime) VALUES("%s", %.2f, "%s", "%s")' %(Global.GLOBAL_TABLE_BALANCE, Global.GLOBAL_MERCHANTS.get(mer), 10000, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))

        cursor.execute('SELECT * FROM %s' %(Global.GLOBAL_TABLE_PAYMENT_USER))
        if not cursor.fetchone():
            for user in Global.GLOBAL_ACCOUNT:
                # 设置用户缴费后是否没有欠费信息标识
                flag = 0
                if user.get('flag'):
                    flag = 1

                # 添加用户数据
                userCode = user.get('userCode')
                cursor.execute('INSERT INTO %s(usercode, username, querystatus, queryresultcode, address, memo, flag, paymentstatus, paymenttype, paymentresultcode, ishangup, rechangestatus, addtime, updatetime) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)' %Global.GLOBAL_TABLE_PAYMENT_USER, (userCode, user.get('userName'), user.get('queryStatus'), user.get('queryResultCode'), user.get('address'), user.get('memo'), flag, user.get('paymentStatus'), user.get('paymentType'), user.get('paymentResultCode'), user.get('isHangup'), user.get('rechangeStatus'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
                conn.commit()

                # 增加用户欠费信息
                userArrears = Global.GLOBAL_ACCOUNT_ARREARS.get(userCode)
                index = 0
                if userArrears:
                    for arrear in userArrears:
                        itemMoney = float(format((arrear.get('count') * arrear.get('price')), '.2f'))
                        cursor.execute('INSERT INTO easylife_user_arrears(itemno, usercode, count, startcount, endcount, price, breach, itemmoney, month, addtime, updatetime) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)' %Global.GLOBAL_ACCOUNT_ARREARS, (RandomUtil.random20Str(), userCode, arrear.get('count'), arrear.get('startCount'), (arrear.get('count') + arrear.get('startCount')), arrear.get('price'), str(arrear.get('breach')), itemMoney, DateUtil.getCutDate(month=index), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
                        conn.commit()
                        index = index + 1

        SQLite.close(conn)


    @staticmethod
    def conn():
        conn = db.connect('easylife.db')
        conn.row_factory = db.Row
        return conn

    @staticmethod
    def close(conn):
        if conn:
            conn.close()
