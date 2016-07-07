'''
    A Kafka module sending data to Kafka

    via topic 'NOTHS-crawler-topic' data structure:
    datagroup, url, product title, price, product decs

    eg:
    product_link,http://www.website.com/product/leathe...,Leather Tote,$195.00,Sometimes you need to carry t...

    Tok - 30/04/2016
'''

from kafka import KafkaProducer
from kafka.common import KafkaError
import sys

class MyKafka:
    def __init__(self, topic):

        try:
            self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
        except KafkaError as e:
            print('I am unable to connect to Kafka - make sure its running on port 9092.', e)
            sys.exit(-1)

        if not topic:
            raise Exception('I need a kafka topic.')

        self.topic = topic

    def send(self, data):

        future = self.producer.send(self.topic, bytes(data, 'utf-8'))
        try:
            record_metadata = future.get(timeout=10)
        except KafkaError:
            # Decide what to do if produce request failed...
            print('Kafka Err', record_metadata)
        else:
            print('Writing to Kafka pipe')
            # print(record_metadata.topic)
            # print(record_metadata.partition)
            # print(record_metadata.offset)
