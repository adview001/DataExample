'''
    A Hbase wrapper module
    Tok - 02/05/2016
'''
import sys
import happybase

class Myhbase:

    def __init__(self, table='test'):
        try:
            connection = happybase.Connection('localhost')
            self.table = connection.table(table)
        except:
            print('I can not connect to hbase.')
            sys.exit(-1)

    def save_crawler(self, rec):

        print(rec)
        x = rec[1].split(',')
        print('add rec to hbase ...')
        if str(x[0]) == 'product_link':
            key = str(x[5]) + str(x[2])
            self.table.put(key, {'group:name': str(x[0]),
                                 'category:name': str(x[5]),
                                 'product:name': str(x[2]),
                                 'product:price': str(x[3]),
                                 'product:desc': str(x[4]),
                                 'link:url': str(x[1])
                                })

        elif str(x[0]) == 'category_link':

            key = 'category' + str(x[2])
            self.table.put(key, {'group:name': str(x[0]),
                                 'category:name': str(x[2]),
                                 'link:url': str(x[1])
                                })


    def save_trend(self, rec):

        x = rec[1].split(',')
        print('add rec to hbase ...')
        if str(x[1]) == 'interests':
            key = str(x[0]) + 'interests' + str(x[2]) + str(x[3])
            self.table.put(key, {'group:name': str(x[1]),
                                 'category:name': str(x[0]),
                                 'stats:from': str(x[2]),
                                 'stats:to': str(x[3]),
                                 'stats:value': str(x[4])
                                 })
        elif str(x[1]) == 'city':
            key = str(x[0]) + 'city' + str(x[2])
            self.table.put(key, {'group:name': str(x[1]),
                                 'category:name': str(x[0]),
                                 'city:name': str(x[2]),
                                 'stats:value': str(x[3])
                                 })

    def getAllproducts(self):
        for key, data in self.table.scan():
            return (key, data)

    def getAllcategories(self):
        categoryname = set()
        for key, data in self.table.scan():
            categoryname.add(data['category:name'])
        return categoryname

    def getCategoryProducts(self, category):
        catprod = []
        for key, data in self.table.scan(row_prefix=category,):
            catprod.append(data)
        return catprod
