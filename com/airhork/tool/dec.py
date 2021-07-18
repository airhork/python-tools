"""
handles the rate in the house buying
"""


import math
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - -  %(asctime)s %(message)s', datefmt = '[%d/%b/%Y %H:%M:%S]')

class Budget:
	pass


class PolicyValue:
    pass

inp = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
	
diff =  lambda x,y : x - y if y > 0 else 0

reduction = lambda x,y,z : x - y -z


maxAgaR = 28017
maxHouse = 3922

p2020Jul = PolicyValue()
p2020Jul.maxAgaR = 28017
p2020Jul.maxHouse = 3922

p2020Jan = PolicyValue()
p2020Jan.maxAgaR = 24633
p2020Jan.maxHouse = 3448

p2021Jul = PolicyValue()
p2021Jul.maxAgaR = 31014
p2021Jul.maxHouse = 4342


basicDic2020 = {'Jan': p2020Jan, 'Jul':p2020Jul}

# basicDic2021 = {'Jan' : p2020Jul}
basicDic2021 = {'Jan' : p2020Jul, 'Jul': p2021Jul}

basicDicMap = {2020 : basicDic2020, 2021 : basicDic2021}




def taxC(value, rate, adj):
	return (value - 5000) * rate - adj

def getTax(value, rate, adj):
        return value * rate - adj

def annualTaxC(base):
	devide = base / 12
	if devide < 3000:
		return base - base * 0.03
	elif devide < 12000:
		return base - base * 0.1 + 210
	elif devide < 25000:
		return base - base * 0.2 + 1410
	elif devide < 35000:
		return base - base * 0.25 + 2660
	elif devide < 55000:
		return base - base * 0.3 + 4410
	elif devide < 80000:
		return base - base * 0.35 + 7160
	else:
		return base - base * 0.45 + 15160

def hayRate(hay) :
        if hay <= 18:
                return 0.1
        elif hay < 21:
                return 0.15
        elif hay < 24:
                return 0.25
        else:
                return 0.4

def getBase(base, maxAgaR, maxHouse) :
        agel = lambda x : min(x,maxAgaR) * 0.08
        house = lambda x : maxHouse / 2 if x * 0.14 > maxHouse else x * 0.07
        job = lambda x : min(x, maxAgaR) * 0.005
        med = lambda x : min(x, maxAgaR) * 0.02

        arrs = { 'age pay' : agel , 'house pay' : house, 'jobless pay' : job , 'mdeical care' : med}

        print('For your input salary  %s, with agaR %s and houseValue %s' %(base, maxAgaR,maxHouse))

        sum = 0
        for item, fun in arrs.items():
                value = fun(base)
                sum += value
                print(' spend %s for %s ' %(item, value))

        beforeTax = base - sum
        return beforeTax
        
        

def cal(base, increase = 1, bonusRate = 0.1, year=2020, comp = 5000):
        
        beforeTax = 0

        ref = 0
        rate = 0
        adj = 0

        result = {}
        bonusBase = base
        i = 1
        taxSum = 0
        totalSalary =0
        paidTax = 0
        lastMaxAgaR = 0
        lastMaxHouse = 0
        

        for item in inp:

                if i == 4 and increase != 1:
                        base = base * increase
                        if item in basicDic:
                            lastMaxAgaR = basicDic[item].maxAgaR
                            lastMaxHouse = basicDic[item].maxHouse
                        beforeTax = getBase(base, lastMaxAgaR, lastMaxHouse)
                        print('before tax %s' %(beforeTax))
                        ref = reduction(beforeTax, 5000, comp)
                
                basicDic = basicDicMap[year]


                if item in basicDic: 
                    lastMaxAgaR = basicDic[item].maxAgaR
                    lastMaxHouse = basicDic[item].maxHouse

                    beforeTax = getBase(base, lastMaxAgaR, lastMaxHouse)
                    print('before tax %s' %(beforeTax))
                    ref = reduction(beforeTax, 5000, comp)

                totalSalary += base


                
                rate = 0
                adj = 0
                taxSum += ref
                if taxSum < 36000:
                        rate  = 0.03
                        adj = 0
                elif taxSum < 144000:
                        rate = 0.1
                        adj = 2520
                elif taxSum < 300000:
                        rate = 0.2
                        adj = 16920
                elif taxSum < 420000:
                        rate = 0.25
                        adj = 31920
                elif taxSum < 660000:
                        rate = 0.3
                        adj = 52920
                elif taxSum < 960000:
                        rate = 0.35
                        adj = 85920
                else:
                        rate = 0.45
                        adj = 181920

                pretax = getTax(taxSum, rate, adj)
                tax = pretax - paidTax
                paidTax += tax

                salary = beforeTax - tax
                result[item] = salary
                i += 1

                handSum = sum(list(result.values()))
                        
                
                print('for the month %s, tax %.2f, salary %.2f ' %(item, tax, salary))
                

        bonus = bonusBase * 12 *  bonusRate
        bonusTax = annualTaxC(bonus)
        print('total base salary %.2f, total package %.2f with bonus %.2f ' %(totalSalary, totalSalary + bonus, bonus))
        print('You after tax base is %.2f' %(handSum))
        print('You after tax bonus is %.2f' %(bonusTax))
        print('Apr total income is %.2f' %(result['Apr'] + bonusTax))
        print('You after tax total package is %.2f' %(handSum + bonusTax))




def calculate(base, bonusRate = 1, hay = 17):

	agel = lambda x : min(x,maxAgaR) * 0.08 

	house = lambda x : maxHouse / 2 if x * 0.14 > maxHouse else x * 0.07

	job = lambda x : min(x, maxAgaR) * 0.005

	med = lambda x : min(x, maxAgaR) * 0.02



	arrs = { 'age pay' : agel , 'house pay' : house, 'jobless pay' : job , 'mdeical care' : med}

	print('For your input salary  %s' %(base))

	sum = 0
	for item, fun in arrs.items():
		value = fun(base)
		sum += value
		print(' spend %s for %s ' %(item, value))

	beforeTax = base - sum

	print('before tax %s' %(beforeTax))

	rate = 0
	adj = 0

	ref = beforeTax - 5000

	if ref < 3000 :
		rate = 0.03
		adj = 0
	elif ref < 12000:
		rate = 0.1
		adj = 210
	elif ref < 25000:
		rate = 0.2
		adj = 1410
	elif ref < 35000 :
		rate = 0.25
		adj = 2660
	elif ref < 55000 :
		rate = 0.3
		adj = 4410
	elif ref < 80000:
		rate = 0.35
		adj = 7160
	else:
		rate =  0.45
		adj = 15160

	tax = taxC(beforeTax, rate, adj)

	print('You anual salary (before tax) is %.2f' %(base * 12 * (1 + 0.1 * bonusRate)))
	print('You anual bonous is (before tax) is %.2f' %(base * 12 * hayRate(hay) * bonusRate))
	print('You anual bonous is (after tax) is %.2f' %(annualTaxC(base * 12 * hayRate(hay) * bonusRate)))
	print('You tax to pay is %.2f' %(tax))
	print('You after tax salary is %.2f' %(beforeTax - tax))





def show():

	strp = lambda x : 'c%s' %str(x)

	values = {}
	with open('d:/dec.txt') as content:	
		for line in content.readlines():
			ba = line.split(':')
			budget = Budget()
			budget.budget = int(ba[1])
			budget.pre= int(ba[2])
			budget.real= int(ba[3])
			budget.option = ba[4] if len(ba) == 5 else ''
			values[ba[0]] = budget
	
	dsum = 0
	
	ssum = sum([x.real for x in values.values()])
	tsum = sum([x.budget for x in values.values()])
	psum = sum([x.pre for x in values.values()])
	msum = sum([x.budget for x in values.values() if x.option == ''])
	dsum = sum([diff(x.budget,x.real) for x in values.values()])
	
	display(values)
	
	print('total bugdge is %s' %(tsum))
	print('total diff bugdge is %s' %(dsum))
	print('You already spent %s' %(ssum + psum))
	print('The actually expense might is %s' %(tsum - dsum))
	print('Your mandatory expense might is %s' %(msum))
	print('Your still need %s' %(tsum - dsum - ssum - psum))

def display(values):
	print('------------------------------')
	print('Item	Budget	Pre	Real	Diff')
	for i in range(1,len(values) + 1):
		value = 'c' + str(i)
		budget = values[value]
		print('%s	%s	%s	%s	%5.2f' %(value,budget.budget,budget.pre,budget.real,diff(budget.budget,budget.real)))
	print('-------------------------------')
		




 
  
  
