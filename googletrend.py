'''
    initialize Google Trend report data
    Tok - 01/05/2016

    data send:
    iphone,interests,2016-04-17,2016-04-23,34
    iphone,interests,2016-04-24,2016-04-30,34
    iphone,city,Nazeing,100
    iphone,city,Leicester,79
'''

import time
from shared.myredis import Myredis
from trends.gtrend import Gtrend
from random import randint
from shared.mykafka import MyKafka



class GoogleTrend(Myredis, Gtrend, MyKafka):

    def __init__(self):
        self.redis = Myredis()
        self.gtrend = Gtrend()
        self.kafka = MyKafka('NOTHS-trends-topic')

    def start(self):

        while True:
            time.sleep(randint(60, 90))
            print('starting google trend ...')
            category = self.redis.getNextCategory()
            if category:
                print('reporting on :', category)
                gdata = self.gtrend.get_report(category)
                cdata = self.pack_gdata(gdata, category.decode("utf-8") )

                for data in cdata:
                    list_ = ",".join(data)
                    self.kafka.send(list_)
                print('end')

gt = GoogleTrend()
gt.start()

