'''
    A general html parse module:

    method:
        - start ( parse 'web' )
        - personalcreations

    internal methods:

        - __getBSObj (generic url to python html obj)
        - __collect_product_links (collect product link via perdefined css class)
        - __split (hash map splitter helper)
        _ __collect_send_product_detail (general data collection)

    Tok - 30/04/2016
'''

import re
import requests
from itertools import *
from threading import Thread
from bs4 import BeautifulSoup as BS
from crawler.link import Link
from shared.mykafka import MyKafka
import urllib


class Parse(Link, MyKafka):

    config = {}

    def __init__(self, config={}):
        if 'url_list' not in config.keys():
            raise Exception('I will need a list of urls to work')

        self.link = Link()
        #self.kafka = MyKafka('NOTHS-crawler-topic')
        self.config['url_list'] = config['url_list']
        self.start()

    def start(self):

        # try:
            for url in self.config['url_list']:

                self.base_url = url
                bsojb = self.__getBSObj(url)
                if re.search(r'personalcreations', url):
                    self.personalcreations(bsojb)
                elif re.search(r'tierneyphotography', url):
                    self.tierneyphotography(bsojb)
                else:
                    print('still need method for', url)
        # except:
        #     print('Unable to open ', url)

    def personalcreations(self, bsOjb):

        category_links = self.link.find_with_class(bsOjb, 'dropDownNavLI ', 'li')

        threads = []

        for category_link in category_links:
            self.link.addLink(category_link, 'category_link')
            #start treads
            t = Thread(target=self.__collect_product_links, args=(category_link[1], 'name', 'div', category_link[0]))
            threads.append(t)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        product_threads = []
        for item in self.__split({i: self.link.linkList[i] for i in self.link.linkList}, 200):
            t = Thread(target=self.__collect_send_product_detail, args=(item,
                                                                        {'product': {'class': 'productTitle',
                                                                                     'tag': 'span'},
                                                                         'price':   {'class': 'mainPrice_MinSalePrice',
                                                                                     'alter_class': 'mainPrice_SalePrice',
                                                                                     'tag': 'span'
                                                                                     },
                                                                         'desc':    {'class': 'ProductInfoText',
                                                                                     'tag': 'div'
                                                                                    }
                                                                         })
                       )
            product_threads.append(t)

        for t in product_threads:
            t.start()

    def __getBSObj(self, url, retries=0):

        if retries >= 3: return

        try:

            rg = re.compile("^(http|www)")
            if rg.match(url):
                r = requests.get(url).text.encode('ascii', 'ignore')
            else:
                r = requests.get(self.base_url + url).text.encode('ascii', 'ignore')
            bsObj = BS(r, "html.parser")
            return bsObj
        except:
            print('getBSObj Err - retry:', url )
            retries += 1
            self.__getBSObj(url, retries)


    def __collect_product_links(self, link, class_, tag, product_category):

        print('starting thread ..', link)
        bsObj = self.__getBSObj(link)
        products_links = self.link.find_with_class(bsObj, class_, tag)
        for products_link in products_links:
            self.link.addLink(products_link, 'product_link', product_category)

    def __split(self, data, SIZE=10000):
        it = iter(data)
        for i in range(0, len(data), SIZE):
            yield {k: data[k] for k in islice(it, SIZE)}

    def __collect_send_product_detail(self, links, args):

        print('starting thread ..', links)

        for k, v in links.items():

            if v['group'] is 'product_link':

                bsObj = self.__getBSObj(v['link'])

                dlink = v['link'].replace(',', '')
                dgroup = v['group']
                dcategory = v['category'] if 'category' in v else ''

                #getprice
                for price in bsObj.find_all(args['price']['tag'], {'class': args['price']['class']}, 'visible'):
                    dprice = price.text.replace(',', '')

                if not dprice:
                    for price in bsObj.find_all(args['price']['tag'], {'class': args['price']['alter_class']}, 'visible'):
                        dprice = price.text.replace(',', '')

                #gettitle
                for product in bsObj.find_all(args['product']['tag'], {'class': args['product']['class']}, 'visible'):
                    dproduct = product.text.replace(',', '')
                #getdesc
                for desc in bsObj.find_all(args['desc']['tag'], {'class': args['desc']['class']}, 'visible'):
                    ddesc = desc.text.replace(',', '')

                data = ",".join([dgroup, dlink, dproduct, dprice, ddesc, dcategory.decode("utf-8")])
                self.kafka.send(data)

            elif v['group'] is 'category_link':

                dlink = v['link'].replace(',', '')
                dgroup = v['group']
                dtitle = v['title']
                data = ",".join([dgroup, dlink, dtitle.decode("utf-8")])
                self.kafka.send(data)


    def tierneyphotography(self, bsOjb):

        photo_links = self.link.find_with_class(bsOjb, 'block-link', False)

        for link in photo_links:
            #print(link[1])
            if re.search(r'cache', link[1]):
                full_link = 'http://www.tierneyphotography.co.uk/' + link[1]
                filename = full_link.split('/')[-1]
                urllib.urlretrieve(full_link, filename)

        pass