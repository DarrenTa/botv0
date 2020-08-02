#!/home/user/venv/bin/python3
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



balances = coinbase.fetch_balance()

print("DASH:",balances['DASH'])
print("USD: ",balances['USD'])
print("last:",coinbase.fetchTicker('DASH/USD')['last'])

orders = coinbase.fetchOpenOrders('DASH/USD')

for order in orders:
	print("Order to ",order['side'],order['remaining'],"DASH for",order['price'],"USD.")
