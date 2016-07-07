from shared.myhbase import Myhbase
import re
import collections
import hashlib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
# %pylab inline
import matplotlib.pyplot as plt

class Analyseresult(Myhbase):

    def __init__(self):
        pass

    def start(self):

        while True:

            print('Commands: "show": display all category, "linear <category name>": display linear graph, "exit": exit programme, "coef": Show trening again product stats')
            the_input = raw_input('Enter input:')

            if the_input == 'exit':
                break
            elif the_input == 'show':

                the_input = raw_input('Enter 1 for products, 2 for categories:')

                hb = Myhbase('crawler')

                if the_input == '1':
                    print(hb.getAllproducts())
                elif the_input == '2':
                    print(hb.getAllcategories())

            elif re.compile(r'^linear\s.+$').match(the_input):
                category = re.compile(r'^linear\s(.+)$').match(the_input)
                if category is not None:
                    self.lineargraph(category.group(1))
            elif the_input == 'coef':
                self.coef()


    def lineargraph(self, category):

        if category is not '':
            try:

                hb = Myhbase('trend')

                X = []
                Y = []
                i = 1
                rowkey = category + 'interests'
                print(rowkey)

                for key, data in hb.table.scan(row_prefix=rowkey, ):
                    X.append([i])
                    v = int(data['stats:value'])
                    Y.append([v])
                    i += 1

                if X:
                    mdl = LinearRegression().fit(X, Y)
                    m = mdl.coef_[0]
                    b = mdl.intercept_
                    plt.scatter(X, Y, color='blue')

                    x_len = len(X)
                    plt.plot([0, x_len], [b, m * x_len + b], 'r')
                    plt.title(category, fontsize=20)
                    plt.xlabel('Time (Weeks)', fontsize=15)
                    plt.ylabel('Trending', fontsize=15)
                    plt.show()
                else:
                    print('not enough data for category', category)
            except:
                print('opss something is wrong.')


    def coef(self):

        hb_crawler = Myhbase('crawler')
        hb_trend = Myhbase('trend')
        data_hash = collections.defaultdict(dict)

        categories = hb_crawler.getAllcategories()

        for category in categories:
            print(category)

            #find coffient
            X = []
            Y = []
            i = 1
            rowkey = category + 'interests'
            print(rowkey)

            for key, data in hb_trend.table.scan(row_prefix=rowkey, ):
                X.append([i])
                v = int(data['stats:value'])
                Y.append([v])
                i += 1

            if X:

                mdl = LinearRegression().fit(X, Y)
                m = mdl.coef_[0]
                data_hash[category]['coef'] = m

                min_price = None
                max_price = None
                mean_price = 0
                total_price = 0

                products_in_category = hb_crawler.getCategoryProducts(category)
                for item in products_in_category:
                    if item['product:price']:

                        item_price = item['product:price']
                        regex = re.compile('[^0-9\.]')
                        item_price = regex.sub('', item_price)
                        item_price = float(item_price)

                        total_price += item_price

                        if item_price < min_price or min_price is None:
                            min_price = item_price

                        if item_price > max_price or max_price is None:
                            max_price = item_price

                        data_hash[category]['min_price'] = min_price
                        data_hash[category]['max_price'] = max_price
                        data_hash[category]['total_price'] = total_price
                        data_hash[category]['mean_price'] = total_price / len(products_in_category)
                        data_hash[category]['range_price'] = max_price - min_price
                        data_hash[category]['total_item'] = len(products_in_category)



        print(data_hash)
        x = []
        y = []
        z = []
        for key, item in data_hash.iteritems():

            x.append(item['mean_price'])
            y.append(item['coef'][0])
            z.append(item['total_item'])

        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        colors = np.random.rand( len(x) )
        area = np.pi * z
        plt.scatter(x, y, s=area, c=colors, alpha=0.5)
        plt.title('Product range, price and trending coefficient', fontsize=20)
        plt.xlabel('Averge Price', fontsize=15)
        plt.ylabel('Trend Coefficient', fontsize=15)
        plt.show()


    def test(self):

        N = 50
        x = np.random.rand(N)
        print(x)
        y = np.random.rand(N)
        print(y)
        colors = np.random.rand(N)
        area = np.pi * (15 * np.random.rand(N)) ** 2  # 0 to 15 point radiuses

        plt.scatter(x, y, s=area, c=colors, alpha=0.5)
        plt.show()


a = Analyseresult()
a.start()





