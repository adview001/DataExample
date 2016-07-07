'''
    A Google Trend module
    Tok - 01/05/2016
'''

from pytrends.pyGTrends import pyGTrends
from shared.proxy import Proxy
import sys
from random import randint
import time
import re

#nothsproject@gmail.com

class Gtrend():

    def __init__(self):
        # connect to Google
        try:
            self.google_username = "testingnoths@gmail.com"
            self.google_password = "1234qwer1234"
            self.connector = pyGTrends(self.google_username, self.google_password)
            time.sleep(randint(5, 10))
        except:
            print('I am unable to connect to google trends.')
            sys.exit(-1)

    def get_report(self, search):
        time.sleep(randint(5, 15))
        self.connector.request_report(keywords=search, geo='GB-ENG')
        time.sleep(randint(5, 15))
        data = self.connector.get_data()
        return data

    def pack_gdata(self, gdata, keyword):

        cdata = []

        if gdata:
            arr = gdata.splitlines()
            section = False

            interest_section_rx = re.compile("^Interest over time")
            city_section_rx = re.compile("^Top cities")
            topsearch_section_rx = re.compile("^Top searches")

            for line in arr:
                print(line)
                if interest_section_rx.match(line):
                    section = 'interest_section'
                elif city_section_rx.match(line):
                    section = 'city_section'
                elif topsearch_section_rx.match(line):
                    break

                if section is not False and section == 'interest_section':
                    l = re.compile(r'(\d{4}-\d{2}-\d{2}) \- (\d{4}-\d{2}-\d{2}),(\d+)').match(line)
                    if line is not '' and l is not None:
                        cdata.append([keyword, 'interests', l.group(1), l.group(2), l.group(3)])

                if section is not False and section == 'city_section':
                    l = re.compile(r'^(.+),(\d+)$').match(line)
                    if line is not '' and l is not None:
                        cdata.append([keyword, 'city', l.group(1), l.group(2)])

        return cdata

