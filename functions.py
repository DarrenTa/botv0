#!/home/user/venv/bin/python3
import ccxt
import json
import math
import time

#print(ccxt.exchanges)

coinbase = ccxt.coinbaseprime({
	'password': 'xxxxxxxxxxx',
	'secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx==',
	'apiKey': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
})



#function ini will place the inital sell orders.
#input is the minimum price that the bot will sell at.
#baseamount is the minimim sell order amount
#the balance must be 32x this base amount in order for
#the bot to work as intended
#The gapsize is the percentage that the next ask will be above the previous ask.
#For example, a gapsize of 0.07 will put the next ask 7% higher.

def ini(minprice,gapsize):
	balances = coinbase.fetch_balance()
	#print(balances['DASH'])
	#Amount of USD that lowest ask is placed above the last price
	backoffmarket = 0.40
	amtratios = [0.25, 0.5, 0.25, 0.33333334,0.44444445,0.59259262, 0.79012349, 1.05349799, 1.40466398, 1.8728853, 2.49718038, 3.32957383, 4.43943175, 5.91924232, 7.89232306, 10.52309739, 14.03079649, 18.70772862, 24.94363812, 33.25818411]
	freeDASH = balances['DASH']['free']
	Dreserve = 0.02*(freeDASH-115)
	dashatrisk = freeDASH - max(0.02*(freeDASH-115),0.001)
	baseamount = math.floor(10**8*dashatrisk/sum(amtratios))/10**8
	amounts = []
	for i in range(0,len(amtratios)):
		amounts.append(math.floor(1000*baseamount*amtratios[i])/1000)
	lastmarketprice = coinbase.fetchTicker('DASH/USD')['last']
	#print(amounts)
	baseprice = max(minprice,lastmarketprice+backoffmarket)
	multfactor = 1 + gapsize
	#priceratios=[1, 1.02, 1.025, 1.03, 1.035, 1.04, 1.045, 1.05, 1.055, 1.06, 1.065, 1.07, 1.075, 1.08, 1.085, 1.09, 1.095, 1.1]
	priceratios=[1.0,1.0+2*gapsize,1.0+4*gapsize]
	for k in range(0,17):
		priceratios.append(1+(k+6)*gapsize)
	#print("priceratios:",priceratios)
	#print("amtratios:",amtratios)
	#print("length",len(priceratios)," and ",len(amtratios))
	prices = []
	for k in range (0,len(amtratios)):
		prices.append(math.floor(1000*baseprice*priceratios[k])/1000)
	#print(sum(amounts))
	for i in range (0,len(amtratios)):
		print("sell ",amounts[i]," at ",prices[i])
		coinbase.createLimitSellOrder('DASH/USD',amounts[i],prices[i])
		time.sleep(.28)
	data = open("selldata.py","w")
	data.write("prices = "+str(prices)+"\n")
	data.write("amounts = "+str(amounts)+"\n")
	data.close()
	statefile = open("state.py","w")
	statefile.write("state='sp'\n")
	statefile.close()



def amtsold(amounts,prices):
	orders = coinbase.fetchOrders('DASH/USD')
	zero = 0.0
	onorder=[]
	soldamount=[]
	for i in range(0,len(amounts)):
		onorder.append(zero)
		soldamount.append(zero)
	for order in orders:
		for i in range(0,len(amounts)):
			if prices[i] == order['price'] and order['side']=="sell":
				onorder[i]=onorder[i]+order['remaining']
	for i in range(0,len(amounts)):
		soldamount[i]=amounts[i]-onorder[i]
	return math.floor(1000*sum(soldamount))/1000

def buyprice(amounts,prices,desiredgain):
	orders = coinbase.fetchOrders('DASH/USD')
	zero = 0.0
	onorder=[]
	soldamount=[]
	usdsoldamount=[]
	for i in range(0,len(amounts)):
		onorder.append(zero)
		soldamount.append(zero)
		usdsoldamount.append(zero)
	for order in orders:
		for i in range(0,len(amounts)):
			if prices[i] == order['price'] and order['side']=="sell":
				onorder[i]=onorder[i]+order['remaining']
	for i in range(0,len(amounts)):
		soldamount[i]=amounts[i]-onorder[i]
		usdsoldamount[i]=(amounts[i]-onorder[i])*prices[i]
	return math.floor(100*(1-desiredgain)*sum(usdsoldamount)/sum(soldamount))/100


def cancelbuyorders():
	orders = coinbase.fetchOpenOrders('DASH/USD')
	for order in orders:
		if order['side']=='buy':
			coinbase.cancelOrder(order['id'])
	return 0.0
