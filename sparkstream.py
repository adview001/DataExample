'''
    A Spark Stream module store data to hbase/redis
    useage: spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.5.0 sparkstream.py localhost:2181 NOTHS-trends-topic trend
    sparkstream.py <zk> <topic> <hbtable>
    Tok - 02/05/2016
'''

from __future__ import print_function

print("Load Spark streaming libraries... ")
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtil
import sys
from shared.myredis import Myredis
from shared.myhbase import Myhbase

class Sparksteam(Myredis, Myhbase):

    def __init__(self, zkQuorum, topic, hbtable):
        self.zkQuorum = zkQuorum
        self.topic = topic
        self.hbase = Myhbase(hbtable)
        self.redis = Myredis()

    def start(self):

        sc = SparkContext(appName="PythonStreamingNOTHS")
        ssc = StreamingContext(sc, 10)

        kvs = KafkaUtils.createStream(ssc, self.zkQuorum, "spark-streaming-consumer", {self.topic: 1})
        print('******* Event received in window: ', kvs.pprint())

        if topic == 'NOTHS-crawler-topic':
            kvs.foreachRDD(self.save_crawler_hbase)
        elif topic == 'NOTHS-trends-topic':
            kvs.foreachRDD(self.save_trends_hbase)

        ssc.start()
        ssc.awaitTermination()

    def save_trends_hbase(self, time, rdd):

        try:
            recs = rdd.collect()
            if recs:
                for rec in recs:
                    self.hbase.save_trend(rec)
        except:
            print('HBase update Err.')


    def save_crawler_hbase(self, time, rdd):

        try:
            recs = rdd.collect()
            if recs:
                for rec in recs:
                    self.hbase.save_crawler(rec)

                    x = rec[1].split(',')
                    if str(x[0]) == 'category_link':
                        if self.redis.isNewCategory(str(x[2])):
                            self.redis.addcategory(str(x[2]))
        except:
            print('HBase update Err.')

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: sparkstream.py <zk> <topic> <hbtable>", file=sys.stderr)
        exit(-1)

    zkQuorum, topic, hbtable = sys.argv[1:]
    ss = Sparksteam(zkQuorum, topic, hbtable)
    ss.start()
