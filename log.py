# -*- coding:utf-8 -*-
import os
import logging
import logging.handlers


'''
日志记录
'''
class logger():

    def __init__(self):
        pass

    @staticmethod
    def log():
        path = "log"
        if not os.path.exists(path):
            os.mkdir(path)
        # 日志系统
        #filePath = "%s/%s.log" %(path, time.strftime("%Y-%m-%d",time.localtime()))
        filePath = '%s/easylife' %path

        logging.basicConfig(level=logging.INFO)
        filehandler = logging.handlers.TimedRotatingFileHandler(filePath, when='d', interval=1, backupCount=0)
        filehandler.suffix = '%Y-%m-%d.log'
        filehandler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S'))
        logging.getLogger('').addHandler(filehandler)
        return logging
