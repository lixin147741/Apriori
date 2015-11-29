#_*_ coding: utf-8 _*_

import random

# 每个用户购买的商品在 MINPRODUCTCANBUY 到 MAXPRODUCTCANBUG之间
MINPRODUCTCANBUY = 1  # 用户最少购买的商品
MAXPRODUCTCANBUG = 10 # 用户最多购买的商品

# 购买记录一共多少条 
TOTALCOUNTITEMS = 10000

# 商品集，商品集的个数应该大于等于用户最多购买的数量
PRODUCTS = ['牛奶','香蕉','啤酒','尿不湿','袜子','洗发露','苹果','香皂','面包','剃须刀','饮料']


with open('dat.txt', 'w') as f:
	for i in range(TOTALCOUNTITEMS):
		tmpPro = random.sample(PRODUCTS, random.choice(range(10))+1)
		f.write(','.join(tmpPro)+'\n')
