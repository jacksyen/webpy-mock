# -*- coding:utf-8 -*-

import sqlite3 as db
from webglobal import Global

class SQLite:

    def init_table(self):
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS %s(easylifeorderno text, outbizno text, status text, paymenttype text, usercode text, resultcode text, paymentamount real)''' %(Global.GLOBAL_TABLE_PAYMENT))

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS %s(merchantkey text, balance real)''' %(Global.GLOBAL_TABLE_BALANCE))

        for mer in Global.GLOBAL_MERCHANTS:
            self.cursor.execute('INSERT INTO %s(merchantkey, balance) VALUES("%s", %.2f)' %(Global.GLOBAL_TABLE_BALANCE, Global.GLOBAL_MERCHANTS.get(mer), 10000))

    def __init__(self):
        conn = db.connect('easylife.db')
        conn.row_factory = db.Row
        self.cursor = conn.cursor()
        self.init_table()
        conn.commit()

    def close(self, conn):
        if conn:
            conn.close()
