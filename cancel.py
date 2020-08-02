#!/home/bot/martingale/coinbase/bin/python3
import ccxt
import json
import math
import time
import datetime
from functions import ini
from functions import amtsold
from functions import buyprice
from functions import cancelbuyorders
#print(ccxt.exchanges)


coinbase = ccxt.coinbaseprime({
        'password': 'xxxxxxxxxxx',
        'secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx==',
        'apiKey': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
})

coinbase.cancelAllOrders('DASH/USD')
