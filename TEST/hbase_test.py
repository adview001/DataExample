'''
    Test pack for hbase Module
'''
# content of link_test.py
import pytest
import sys
import happybase
sys.path.insert(0, r'../')
from shared.myhbase import Myhbase

connection = happybase.Connection('localhost')
connection.open()

try:
        connection.create_table(
            'crawler_test',
            {
                'group': dict(),
                'category': dict(),
                'product': dict(),
                'link': dict(),
            }
        )

        connection.create_table(
            'trend_test',
            {
                'group': dict(),
                'category': dict(),
                'city': dict(),
                'stats': dict(),
            }
        )
except:
    pass

crawler_test_conn = connection.table('crawler_test')
trend_test_conn = connection.table('trend_test')

crawler_test_conn.put('mycategorymyproduct', {
                                                'group:name': 'product_link',
                                                'category:name': 'mycategory',
                                                'product:name': 'myproduct',
                                                'product:price': '$9.99',
                                                'product:desc': 'I am a product description 1',
                                                'link:url': 'http://productlink1.com',
                                                })

crawler_test_conn.put('mycategorymyproduct2', {
                                                'group:name': 'product_link',
                                                'category:name': 'mycategory',
                                                'product:name': 'myproduct2',
                                                'product:price': '$10.99',
                                                'product:desc': 'I am a product description 2',
                                                'link:url': 'http://productlink2.com',
                                                })

crawler_test_conn.put('mycategory2myproduct1', {
                                                'group:name': 'product_link',
                                                'category:name': 'mycategory2',
                                                'product:name': 'myproduct1',
                                                'product:price': '$5.99',
                                                'product:desc': 'I am a product description 3',
                                                'link:url': 'http://productlink3.com',
                                                })

trend_test_conn.put('mycategoryinterests2016-03-012016-03-31', {
                                                'group:name': 'interests',
                                                'category:name': 'mycategory',
                                                'stats:from': '2016-03-01',
                                                'stats:to': '2016-03-31',
                                                'stats:value': '10'
                                                })

trend_test_conn.put('mycategoryinterests2016-04-012016-05-01', {
                                                'group:name': 'interests',
                                                'category:name': 'mycategory',
                                                'stats:from': '2016-04-01',
                                                'stats:to': '2016-05-01',
                                                'stats:value': '20'
                                                })




hb_cralwer_test = Myhbase('crawler_test')

def test_save_cawler_rec():

    new_data = ",".join(['product_link', 'http://newadd.com', 'product1', '$10', 'Im a new product desc from test', 'testcategory'])
    hb_cralwer_test.save_crawler([0,new_data])

    row = crawler_test_conn.row('testcategoryproduct1')
    assert row['product:name'] == 'product1'
    assert row['product:desc'] == 'Im a new product desc from test'
    assert row['category:name'] == 'testcategory'


crawler_test_conn
