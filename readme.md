# Apriori算法
### 介绍
- 该[关联规则](https://zh.wikipedia.org/wiki/%E5%85%B3%E8%81%94%E5%BC%8F%E8%A7%84%E5%88%99)在分类上属于单维，单层，布尔关联规则。
- `Apriori` 的核心是基于两阶段频集思想的递推算法
- `Apriori` 是一种最有影响的挖掘布尔关联规则的频繁集项的算法
- 所有支持度大于最小支持度项集称为频繁项集（简称`频集`）

### 基本思想 
- 简单统计所有含一个元素项目集出现的频数，并找出那些不小于最小支持度的项目集，即`一维最大项目数`
- 循环处理直到再没有最大项目集生成
- 循环过程是：在第`k`步中，根据第`k-1`步生成的`(k-1)`维最大项目集产生`k`维候选项目，然后对数据库进行搜索，得到候选项目集的项集支持度，与最小支持度进行比较，从而得到`k`维最大项目集

### 应用场景
关联规则一个经典的实例是[购物篮分析](http://baike.baidu.com/view/7357329.htm)(Market Basket Analysis)。超市对顾客的购买记录数据库进行关联规则挖掘，可以发现顾客的购买习惯，例如，购买产品X的同时也购买产品Y，于是，超市就可以调整货架的布局，比如将X产品和Y产品放在一起，增进销量。

### 算法特点
- 优点：简单、易理解、数据要求低
- 缺点：
	- 在每一步产生侯选项目集时循环产生的组合过多，没有排除不应该参与组合的元素;
	- 每次计算项集的支持度时，都对数据库D中的全部记录进行了一遍扫描比较，如果是一个大型的数据库的话，这种扫描比较会大大增加计算机系统的I/O开销。而这种代价是随着数据库的记录的增加呈现出几何级数的增加。
	
### 算法描述

	I = {I1,I2,I3...Im}是项的集合
	D = {t1,t2,t3...tn}是交易数据库
	其中每个t是I的真子集
	MinSupport是最小支持度
	
	begin
	// 找出频繁1项集
	P1 = find1Items()
	// 循环处理直到没有最大项集产生
	for(k = 2; P[k-1] != null;k++) {
		// 根据第k-1维的项目集生成k维项目集
		C[k] = apriori(P[k-1])
		for t in D {
			if t.contains(c[k]) {
				for c in C[k] {
					c.count++
				}
			}		
		}
		// 所有满足最小支持度的项目生成一个新的项集
		P[k] = c > MinSupport for c in C[k]
	
	}
### 算法实现
	#_*_ coding: utf-8 _*_

	from operator import and_
	from itertools import combinations

	filePath = '/Users/kee/Desktop/dat.txt'

	class AprioriAssociationRule:
    def __init__(self, inputfile):
        self.allTransaction = []
        self.itemSet = set([])
        with open(inputfile, 'r') as inf:
        
            for line in inf.readlines():
                elements = set(filter(lambda entry: len(entry)>0, line.strip().split(',')))
                if len(elements)>0:
                    self.allTransaction.append(elements)
                    for element in elements:
                        self.itemSet.add(element)
        self.toRetItems = {}
        self.associationRules = []

    # 获取一列商品的支持度
    def getSupport(self, itemList):
        if type(itemList) != frozenset:
            itemList = frozenset([itemList])
        tmpTransaction = lambda transaction: reduce(and_, [(item in transaction) for item in itemList])
        count = len(filter(tmpTransaction, self.allTransaction))
        return float(count)/float(len(self.allTransaction))

    def start(self, minSupport=0.15, minConfidence=0.6):

        # 筛选出来所有大于等于支持度阀值的商品，即选出一维最大项目数
        itemCombSupports = filter(lambda freqpair: freqpair[1]>=minSupport,
                                  map(lambda item: (frozenset([item]), self.getSupport(item)), self.itemSet))
        currentLset = set(map(lambda freqpair: freqpair[0], itemCombSupports))
        k = 2
        while len(currentLset)>0:
            # 组合出所有的k维项目
            currentCset = set([i.union(j) for i in currentLset for j in currentLset if len(i.union(j))==k])
            # 筛选出所有大于等于支持度阀值的商品，即选出k维最大项目数
            currentItemCombSupports = filter(lambda freqpair: freqpair[1]>=minSupport,
                                             map(lambda item: (item, self.getSupport(item)), currentCset))
            currentLset = set(map(lambda freqpair: freqpair[0], currentItemCombSupports))
            itemCombSupports.extend(currentItemCombSupports)
            k += 1
        # 把所有的满足支持度的组合保存起来
        for key, supportVal in itemCombSupports:
            self.toRetItems[key] = supportVal
 
        for key in self.toRetItems:
            # 对每一组满足支持度的组合再任意进行排列组合，任意一组的任意一个排列组合都会在toRetItems出现
            subsets = [frozenset(item) for k in range(1, len(key)) for item in combinations(key, k)]
            for subset in subsets:
                # 计算置信度并且把满足置信度的保留下来
                confidence = self.toRetItems[key] / self.toRetItems[subset]
                if confidence > minConfidence:
                    self.associationRules.append([subset, key-subset, confidence])


	a = AprioriAssociationRule(filePath)
	a.start()
	for i in a.associationRules:
   	 l = list(i[0])
   	 print('if you buy  %s ,then you have  %d%% 	persent to buy %s' % (l, float(i[2])*100, 	list(i[1])))
	print(a.toRetItems)
	
	
	


