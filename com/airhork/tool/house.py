"""
handles the rate in the house buying
"""


import math
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - -  %(asctime)s %(message)s', datefmt = '[%d/%b/%Y %H:%M:%S]')

interest=0.049
ginterest = 0.0325

maxium=1820


rate_per_month = lambda x : x / 12

cal = lambda x,y,z : (x * y * math.pow((1 + y),z)) / (math.pow((1 + y),z) - 1)

def full(base,year,gjj = 50,rate = 1):
	result1 = payment(base, year,rate)
	result2 = gongjijin(gjj * 10000,30, rate)
	result = result1 + result2
	logging.info('you have to pay %6.2f per month for all' % (result))
	# logging.info('minus gongjijin, you have to pay %6.2f' % (result - maxium))
	

def payment(base,year,rate = 1):
	base *= 10000
	months = year * 12
	real_interest = rate_per_month(interest) * rate
	result = cal(base, real_interest, months)
	logging.info('you have to pay %6.2f per month for commerical' % (result))
	return result


def gongjijin(base, year, rate = 1):
	months = year * 12
	#real_interest = rate_per_month(ginterest) * rate
	real_interest = rate_per_month(ginterest) 
	result = cal(base, real_interest, months)
	logging.info('you have to pay %6.2f per month for gongjijin' % (result))
	return result
	




 
  
  
