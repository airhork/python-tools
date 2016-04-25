"""Calculate the new cost of the stock
   
"""
commission = 0.0004
taxRate = 0.001

stocks = {'sh601166':'XYYH','sh600993':'MYL','sh600050':'ZGLT','sh600572':'KEB'}
url = 'http://hq.sinajs.cn/list=' + ','.join(stocks.keys())

szstocks = {'s_sh000001':'Sh', 's_sz399001':'ShenZhen'}
sz_url = 'http://hq.sinajs.cn/list=' + ','.join(szstocks.keys())

init = False
from urllib import request
from com.airhork.tool import util

usingproxy=True

def getReq():
	global init

	if init:
		return 
	print('start setting the proxy! ')

	user = ''
	passwd = ''
	url = ''

	proxy_support =	request.ProxyHandler({'http':'http://%s:%s@%s' %(user,passwd,url)})
	passwdmgr= request.HTTPPasswordMgrWithDefaultRealm()
	passwdmgr.add_password(None,'hq.sinajs.cn','','')
	from ntlm import HTTPNtlmAuthHandler
	auth_NTLM = HTTPNtlmAuthHandler.ProxyNtlmAuthHandler(passwdmgr)
	proxy_auth_handler = request.ProxyBasicAuthHandler(passwdmgr)
	


	opener = request.build_opener(proxy_support)
	request.install_opener(opener)
	init = True

def fetchRequest():
	print('using proxy %s' %(str(usingproxy)))
	if usingproxy:
		getReq()
		



def fetch():
	"""
	handler = request.ProxyHandler({'http':'http://proxy.ict:8080'})
	proxy_auth = request.ProxyBasicAuthHandler()
	proxy_auth.add_password('aspac.local','proxy.ict:8080','axesr','maxzhang2')
	opener = request.build_opener(handler,proxy_auth)
	response = opener.open(url)
	"""
	util.logCurrenttime()
	fetchRequest()
	response = request.urlopen(url)
	content = response.read().decode('gbk')
	response.close()
	values = list(filter((lambda x : '=' in x),content.split(';')))
	dic = {}
	for item in values:
		value = item.split('=')
		left = value[0]
		left = left[(len(left) - 8):len(left)]
		right = value[1]
		right = right[1:len(right) - 1]
		dic[left] = right.split(',')

	response = request.urlopen(sz_url)
	content = response.read().decode('gbk')
	response.close()
	print(content)
	values = list(filter((lambda x : '=' in x),content.split(';')))
	for item in values:
		value = item.split('=')
		left = value[0]
		left = left[(len(left) - 10):len(left)]
		right = value[1]
		right = right[1:len(right) - 1]
		dic[left] = right.split(',')

	for k,v in dic.items():
		if k in szstocks.keys():
			print('for %s, current price is %s, and the rate is %2.3f' %(szstocks[k],v[1],float(v[3])))	
		else:
			rate =  (((float(v[3])-float(v[2]))/float(v[2])) * 100)
			print('for %s, current price is %s, and the rate is %2.3f' %(stocks[k],v[3],rate))	


def calNewCost(newcount, price):
	"""
	newcount -- the new countyou will buy
	price -- the new price you will buy
	"""
	return calNewCost1(current, newcount, price)


def calNewCost1(current, newCount, price):
	"""Calculate the new cost by the new transition.
		@current
			The sequcen for the parameter current is 
			currentPrice, count, earnning 
		@newCount
		@price
	"""
	currentPrice = current[0]
	count = current[1]
	earnning = current[2]

	commission = calculateCommission(price, newCount)
	cashFlow = ((newCount > 0) and newCount * price + commission) or -newCount * price - commission
	newEarnning = count * (price - currentPrice) + earnning - commission
	newValue = (newCount + count) * price
	if(count + newCount == 0):
		cost = 0
	else:
		cost = (newValue - newEarnning) / (count + newCount)
		
	print("-------------------------")
	if(newCount > 0):
		print("For this transition,you need ", cashFlow)
	else:
		print("For this transition, you will withdraw ", cashFlow)

	print("new Earnning ",newEarnning)
	print("the total value is ",newValue)
	print("the new cost will be " ,cost)
	print("-------------------------")
	return [price,newCount + count, newEarnning]

def calNewCost2(current, newCount, price):
	currentPrice = current.currentPrice 
	count = current.count
	lost = current.lost
	current = [currentPrice, count, lost]
	return calNewCost1(current, newcount, price)


def sell(price, newCount):
	cost = 35.31
	count = 200
	lost = 575
	newLost = (cost - price) * count + lost
	if(price >= cost):
		calculateRate(cost,price)
	print("new Lost ",newLost)
	newTotal = (count - newCount) * price + newLost
	print(newTotal/(count - newCount))

def calculateCommission(price, newCount):
	"""
	"""
	commission = ((newCount > 0) and calculateBuyCommission(price,newCount)) or calculateSellCommission(price,-newCount)
	return commission

def calculateSellCommission(price, count):
	"""
	Calculates the cost when selling the stock
	"""
	comm = price * count * commission 
	return (((comm > 5) and comm) or 5) + price * count * taxRate

def calculateBuyCommission(price, count):
	"""
	Calculates the cost when buying the stock
	"""
	comm = price * count * commission
	return (((comm > 5) and comm) or 5)
	

def calculateRate(value1, value2):
	result = (((value2-value1)/value1) * 100)
	print("the rate of the ",value1,value2," is %2.3f" %result,"%")
	return result
	

def listAll(start=35.31,end=38.5):
	while(start < end):
		sell(start,100)
		start += 0.1


class Current:
	pass

