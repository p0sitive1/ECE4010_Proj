import torch
import random
import numpy as np


def str_to_function(expr):
    return lambda x: eval(expr)


class MyError(Exception):
    def __init__(self, message):
        self.message = message


def generate_random_function():
    # 随机选择一种基本函数（可以根据需要添加其他基本函数）
    basic_functions = ["x"]
    func = random.choice(basic_functions)

    a = random.uniform(-5, -3)
    a = -3
    b = random.uniform(20, 30)
    b = 20

    final = str(a) + "*" + func + "+" + str(b)

    return final


class Goods:
    def __init__(self, functionListForCustomers, price=-1):
        self.functionListForCustomers = functionListForCustomers
        if price == -1:
            self.price = random.randint(10, 20)
        else:
            self.price = price
        self.sales = -1
        self.TR = -1
        self.lower_bound = np.random.uniform(low=0, high=5, size=10)

    def set_price(self, price):
        self.price = price

    def compute_quantity(self, customerID, price=-1):
        if price < 0:
            price = self.price
        resultFunction = str_to_function(self.functionListForCustomers[customerID])
        return resultFunction(price)

    def compute_sales(self, price=-1):
        temp = 0
        if price < 0:
            price = self.price
        for i in range(len(self.functionListForCustomers)):
            if price > self.lower_bound[i]:
                temp += self.compute_quantity(i, price)
        self.sales = temp
        if self.sales <= 0:
            self.sales = 0
        return self.sales * price

    def compute_ALL(self, price=-1):
        if price < 0:
            price = self.price
        self.TR = self.compute_sales(price)
        return self.TR


class SupermarketEnv:
    def __init__(self):
        self.goodsList = []
        self.revenueList = []

    def create_goods(self, customerNumber):
        functionListForGoods = []
        for i in range(customerNumber):
            functionListForGoods.append(generate_random_function())
        return Goods(functionListForGoods)

    def create_goods_list(self, goodsNumber, customerNumber):
        for i in range(goodsNumber):
            self.goodsList.append(self.create_goods(customerNumber))

    def compute_revenue_list(self, priceList):
        if len(priceList) != len(self.goodsList):
            raise MyError("The length of priceList is not equals to goodsList length")
        self.revenueList = []
        for i in range(len(self.goodsList)):
            self.revenueList.append(self.goodsList[i].compute_ALL(priceList[i]))

    def compute_TR(self):
        return sum(self.revenueList)