'''
    A Redis wrapper module
    Tok - 01/05/2016
'''

import redis
import sys
import re
import datetime


class Myredis:

    def __init__(self):

        try:
            self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
        except:
            print('I am unable to connect to Redis, make sure it is running on port 6370.')
            sys.exit(-1)

    def getcategory(self, category, attr=''):

        key = self.__gen_key(category)
        if attr:
            return self.redis.hget(key, attr)
        else:
            return self.redis.hgetall(key)

    def addcategory(self, category):

        data = {}
        key = self.__gen_key(category)
        data['category'] = category
        data['datetime'] = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
        data['is_done'] = False
        self.redis.hmset(key, data)

    def isNewCategory(self, category):
        key = self.__gen_key(category)
        r = self.redis.hgetall(key)
        return False if len(r) else True

    def getNextCategory(self):

        next_catetory = ''

        keys = self.redis.keys(pattern='category:*')
        for key in keys:
            category_is_done = self.redis.hget(key, 'is_done')

            if category_is_done.decode("utf-8") == 'False':
                next_catetory = self.redis.hget(key, 'category')
                self.redis.hset(key, 'is_done', True)
                break

        return next_catetory

    def __gen_key(self, category):
        regex = re.compile('[^a-zA-Z0-9]')
        s = regex.sub('', category)
        return 'category:' + str(s)
