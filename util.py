# -*- coding:utf-8 -*-
import hashlib
import random
import time
import uuid

'''
MD5帮助类
'''
class MD5Util:

    @staticmethod
    def md5(param):
        md = hashlib.md5()
        md.update(param)
        return md.hexdigest()


'''
随机数帮助类
'''
class RandomUtil:

    @staticmethod
    def random16Str():
        num = random.randint(10,99)
        result = '%.4f%d' %(time.time(), num)
        result = result.replace('.','')
        return result

    @staticmethod
    def random32Str():
        return uuid.uuid1().hex

'''
class JSONUtil:

    @staticmethod
    def toJson(json_str):
        try:
            return json.loads(json_str)
        except e:
            return None

'''
