# -*- coding:utf-8 -*-

import sqlite3 as db
from webglobal import Global
from util import DateUtil

class SQLite:

    @staticmethod
    def init():
        conn = SQLite.conn()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS %s(easylifeorderno text, outbizno text, status text, paymenttype text, usercode text, resultcode text, paymentamount real, iskeephangup integer, addtime datetime, updatetime datetime)''' %(Global.GLOBAL_TABLE_PAYMENT))

        cursor.execute('''CREATE TABLE IF NOT EXISTS %s(merchantkey text, balance real, addtime datetime, updatetime datetime)''' %(Global.GLOBAL_TABLE_BALANCE))

        for mer in Global.GLOBAL_MERCHANTS:
            cursor.execute('SELECT * FROM %s WHERE merchantkey = ?' %Global.GLOBAL_TABLE_BALANCE, (Global.GLOBAL_MERCHANTS.get(mer),))
            if cursor.fetchone():
                continue
            cursor.execute('INSERT INTO %s(merchantkey, balance, addtime, updatetime) VALUES("%s", %.2f, "%s", "%s")' %(Global.GLOBAL_TABLE_BALANCE, Global.GLOBAL_MERCHANTS.get(mer), 10000, DateUtil.getDate(format='%Y-%m-%d %H:%M:%S'), DateUtil.getDate(format='%Y-%m-%d %H:%M:%S')))
        conn.commit()
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
