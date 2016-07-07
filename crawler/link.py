'''
    A general link parser module:

    method:
        - find link with tag, class
        - add link

    Tok - 30/04/2016
'''
import hashlib
import collections
import threading

class Link:

    def __init__(self):
        self.linkList = collections.defaultdict(dict)
        self.linkList_lock = threading.Lock()

    def find_with_class(self, bsOjb, class_, tag):
        url_list = []

        try:
            if tag:
                for catagoryli in bsOjb.find_all(tag, {'class': class_}, 'visible'):
                    for a in catagoryli.find_all('a', href=True):
                        url_list.append([a.text.encode('ascii', 'ignore'),
                                         a.get('href')])
            else:
                for a in bsOjb.find_all('a', {'class': class_}, 'visible'):
                    url_list.append([a.text.encode('ascii', 'ignore'),
                         a.get('href')])


        except:
            print('failed to parse link', a)

        return url_list

    def addLink(self, link, group, catgeory=''):

        link_key = hashlib.md5(link[1].encode('utf-8')).hexdigest()

        if link_key not in self.linkList:

                self.linkList_lock.acquire()
                self.linkList[link_key]['group'] = group
                self.linkList[link_key]['title'] = link[0]
                self.linkList[link_key]['link'] = link[1]
                self.linkList[link_key]['category'] = catgeory

                self.linkList_lock.release()