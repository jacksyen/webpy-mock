# -*- coding:utf-8 -*-

import sqlite3 as db

class SQLite:

    def init_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS easylife_payment_order(easylifeorderno text, outbizno text, status text, paymenttype text, usercode text, resultcode text, paymentamount real)''')

    def __init__(self):
        conn = db.connect('easylife.db')
        conn.row_factory = db.Row
        self.cursor = conn.cursor()
        self.init_table()
        conn.commit()

    def close(self, conn):
        if conn:
            conn.close()
