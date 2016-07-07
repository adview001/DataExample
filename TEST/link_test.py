'''
    Test pack for Link Module
'''
# content of link_test.py
import pytest
import sys
sys.path.insert(0, r'../')
from crawler.link import Link
from bs4 import BeautifulSoup as BS

link = Link()


def test_link_instance():
    isinstance(link, int)


def test_link_list():
     assert link.linkList == {}


def test_parse_link():
    html = __get_html()
    bsObj = BS(html, "html.parser")
    assert len(link.find_with_class(bsObj, 'link', 'li')) == 3

def test_add_link():

    link1 = ['link1 title', 'http://somelinke1.com']
    link2 = ['link2 title', 'http://somelinke2.com']
    link3 = ['link3 title', 'http://somelinke1.com']

    link.addLink(link1, 'link_group')
    assert len(link.linkList) == 1

    link.addLink(link2, 'link_group')
    assert len(link.linkList) == 2

    # repeated url address will be ingored
    link.addLink(link3, 'link_group')
    assert len(link.linkList) == 2

def __get_html():
    return "<html><header></header><body><li class='link'><a href='http://link1.com'>link1</a></li><li class='link'><a href='http://link2.com'>link2</a></li><li class='link'><a href='http://link3.com'>link3</a></li></body></html>"
