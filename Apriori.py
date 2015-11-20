#_*_ coding: utf-8 _*_
 
from functools import reduce
from operator import and_
from itertools import combinations

filePath = 'dat.txt'
MINSUPPORT = 0.15      # 支持度阀值
MINCONFIDENCE = 0.7    # 置信度阀值

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
        count = len(list(filter(tmpTransaction, self.allTransaction)))
        return float(count)/float(len(self.allTransaction))

    def start(self, minSupport=0.1, minConfidence=0.5):

        # 筛选出来所有大于等于支持度阀值的商品，即选出一维最大项目数
        itemCombSupports = list(filter(lambda freqpair: freqpair[1]>=minSupport,
                                  map(lambda item: (frozenset([item]), self.getSupport(item)), self.itemSet)))
        currentLset = set(map(lambda freqpair: freqpair[0], itemCombSupports))
        k = 2
        while len(currentLset)>0:
            # 组合出所有的k维项目
            currentCset = set([i.union(j) for i in currentLset for j in currentLset if len(i.union(j))==k])
            # 筛选出所有大于等于支持度阀值的商品，即选出k维最大项目数
            currentItemCombSupports = list(filter(lambda freqpair: freqpair[1]>=minSupport,
                                             map(lambda item: (item, self.getSupport(item)), currentCset)))
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
a.start(minSupport = MINSUPPORT,  minConfidence = MINCONFIDENCE)
for i in a.associationRules:
    l = list(i[0])
    print('如果你买了 %s 那么你买有  %d%% 的概率会买 %s' % (','.join(l), float(i[2])*100, ''.join(list(i[1]))))
