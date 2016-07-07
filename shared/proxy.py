'''
    A proxy module connecting Tor via port 9150
    Tok - 30/04/2016
'''

import socket
import requests
import sys

from shared import socks


class Proxy:

    wmip = 'http://icanhazip.com'

    def __init__(self):
        print('initialize tor proxy....')

        try:
            socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
            socket.socket = socks.socksocket
            print('Using IP', requests.get(self.wmip).text)
        except:
            print('I am unable to connect to a proxy - make sure the proxy server is running on port 9150.')
            sys.exit(-1)



