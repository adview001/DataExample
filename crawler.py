'''
    initialize Crawler module
    Tok - 30/04/2016
'''

from crawler.prase import Parse
from shared.proxy import Proxy

class Crawler(Proxy):

    config = {'proxy': False }

    def __init__(self, config={}):

        # initialise config for spider
        for keys, value in config.items():
            self.config[keys] = value
        # initialise proxy if true
        if self.config['proxy'] is True:
            Proxy()

    def start(self):
        Parse(self.config)

c = Crawler({'proxy': True, 'url_list': ['http://www.tierneyphotography.co.uk/clients/sheffield-town-hall-wedding-dana-danny/pw/town1']})
c.start()