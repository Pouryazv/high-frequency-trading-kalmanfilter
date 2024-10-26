import asyncio
import websockets
from datetime import timedelta
import time
import random
from enum import Enum

import http.client, urllib.parse
import hmac, hashlib
import json

Intervals = {
    "1s" : timedelta(seconds=1),
    "1m" : timedelta(minutes=1),
    "3m" : timedelta(minutes=3),
    "5m" : timedelta(minutes=5),
    "15m" : timedelta(minutes=15),
    "30m" : timedelta(minutes=30),
    "1h" : timedelta(hours=1),
    "2h" : timedelta(hours=2),
    "4h" : timedelta(hours=4),
    "6h" : timedelta(hours=6),
    "8h" : timedelta(hours=8),
    "12h" : timedelta(hours=12),
    "1d" : timedelta(days=1),
    "3d" : timedelta(days=3),
    "1w" : timedelta(days=7),
    "1M" : timedelta(days=30),
}

class OrderStatus(Enum):
    NEW = 1
    PARTIALLY_FILLED = 2
    FILLED = 3
    CANCELED = 4
    PENDING_CANCEL = 5
    REJECTED = 6
    EXPIRED = 7

class OrderType(Enum):
    LIMIT = 1
    MARKET = 2
    STOP_LOSS = 3
    STOP_LOSS_LIMIT = 4
    TAKE_PROFIT = 5
    TAKE_PROFIT_LIMIT = 6
    LIMIT_MAKER = 7

class OrderSide(Enum):
    BUY = 1
    SELL = 2

class Binance():

    def __init__(self, config, test=True):
        self.config = config

        if 'api' in self.config and 'apikey' in self.config['api'] and 'secretkey' in self.config['api']:
            self.apikey = self.config['api']['apikey']
            self.secretkey = self.config['api']['secretkey']
        self.test = test

    def _request(self, method, url, body=None, headers={}):
        conn = http.client.HTTPSConnection("api.binance.com")
        conn.request(method, url, body, headers=headers)
        r1 = conn.getresponse()
        data1 = r1.read()
        conn.close()
        
        data = json.loads(data1)

        return r1.status, data

    def exchangeinfo(self):
        return self._request('GET', '/api/v3/exchangeInfo')

    def getklines(self, symbol, interval, limit, start = None, end = None):
        url = "/api/v3/klines?symbol={}&interval={}&limit={}".format(symbol, interval, limit)
        if start != None:
            url += "&startTime={}".format(start)
        if end != None:
            url += "&endTime={}".format(end)
        return self._request('GET', url)


    def subscribe(self, handler, symbol = None, interval = None, listenkey = None):
        asyncio.get_event_loop().run_until_complete(self.ws(handler, symbol, interval, listenkey))

    def unsubscribe(self):
        asyncio.get_event_loop().stop()

    def timestamp(self):
        return int(time.time() * 1000)
