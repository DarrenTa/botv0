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




minprice = 70.7
#baseamount = 1.0
baseamount = 0.374
gapsize = 0.005
#desired gain amount needs to be a number more than .01 if your account does not have a trading balance.
#as the coinbase fee goes down with trading, this amount can be lowered.
desiredgain = 0.02
USDreserve=59

exec(open("./state.py").read())
exec(open("./selldata.py").read())
exec(open("./buydata.py").read())

print(datetime.datetime.now(),state)

if state=='wait':
	ini(minprice,gapsize)
elif state=='sp':
	x = amtsold(amounts,prices)
	#print("amtsold:",x)
	if x >= 0.01:
		y = buyprice(amounts,prices,desiredgain)
		balances = coinbase.fetch_balance()
		USDfree = math.floor(100*balances['USD']['free'])/100
		buyamount=math.floor(0.9945*1000*(USDfree-USDreserve)/y)/1000
		#print(balances)
		print("Place buy order for ",buyamount,"Dash at",y,"USD")
		coinbase.createLimitBuyOrder('DASH/USD',buyamount,y)
		buyfile = open("buydata.py","w")
		buyfile.write("oldsoldamount = "+str(x)+"\n")
		buyfile.write("oldbuyprice = "+str(y)+"\n")
		buyfile.close()
		statefile = open("state.py","w")
		statefile.write("state='bp'\n")
		statefile.close()
elif state=='bp':
	balances = coinbase.fetch_balance()
	if balances['USD']['used']< 0.20 and amtsold(amounts,prices) <= (oldsoldamount + 0.001):
		print("No USD to buy with going to go to wait stage")
		time.sleep(3)
		coinbase.cancelAllOrders('DASH/USD')
		time.sleep(3)
		coinbase.cancelAllOrders('DASH/USD')
		time.sleep(2)
		coinbase.cancelAllOrders('DASH/USD')
		orders = coinbase.fetchOpenOrders('DASH/USD')
		print(orders)
		statefile = open("state.py","w")
		statefile.write("state='wait'\n")
		statefile.close()
	elif amtsold(amounts,prices) > (oldsoldamount + 0.001):
		cancelbuyorders()
		time.sleep(2)
		y = buyprice(amounts,prices,desiredgain)
		x = amtsold(amounts,prices)
		USDfree = math.floor(100*balances['USD']['total'])/100
		buyamount=math.floor(0.9945*1000*(USDfree-USDreserve)/y)/1000
		print("Place buy order for ",buyamount,"Dash at",y,"USD")
		coinbase.createLimitBuyOrder('DASH/USD',buyamount,y)
		buyfile = open("buydata.py","w")
		buyfile.write("oldsoldamount = "+str(x)+"\n")
		buyfile.write("oldbuyprice = "+str(y)+"\n")
		buyfile.close()
	else:
		print("No adjustments to buy order made.")
elif state=='stop':
	print('State is stop, nothing done')
