#%%
import numpy as np
import matplotlib.pyplot as plt

#%%
def createCumlHappynessFunction(happy1, change12):
    h1 = happy1
    h2 = happy1 - change12
    b = - np.log(h2 / h1)
    a = h1 / np.exp(-b)
    def cumlHappynessFunction(x):
        return a * (1 - np.exp(-b*x)) / b
    return cumlHappynessFunction


#%%
def randomFromRange(a, b):
    r = np.random.rand()
    return a + r * (b - a)

def getMinKeyVal(dct):
    minVal = np.infty
    minKey = None
    for key in dct:
        val = dct[key]
        if val < minVal:
            minVal = val
            minKey = key
    return (minKey, minVal)


#%%
products = ['apple', 'banana', 'cd', 'doughnut']

class Person:
    def __init__(self, id):
        self.id = id
        self.money = 1000
        self.products = {
            p: int(randomFromRange(1, 100))
            for p in products
        }
        h1 = randomFromRange(2, 20)
        delta12 = randomFromRange(0.125, h1 / 2)
        self.happynessFunctions = {
            p: createCumlHappynessFunction(h1, delta12)
            for p in products
        }

    def calcHappyness(self):
        h = 0
        for p in products:
            n = self.products[p]
            h += self.happynessFunctions[p](n)
        return h

    def salesPrice(self, product):
        n = self.products[product]
        if n <= 0:
            return np.infty
        h0 = self.happynessFunctions[product](n)
        h1 = self.happynessFunctions[product](n-1)
        delta = h0 - h1
        return delta

    def buyPrice(self, product):
        n = self.products[product]
        h0 = self.happynessFunctions[product](n)
        h1 = self.happynessFunctions[product](n+1)
        delta = h1 - h0
        return delta
    
#%%
def getBestPriceForProduct(product, sellers):
    bestPrice = np.infty
    bestSeller = None
    for seller in sellers:
        price = seller.salesPrice(product)
        if price < bestPrice:
            bestPrice = price
            bestSeller = seller
    return (bestSeller, bestPrice)


def choseTrade(buyer, sellers):
    desires = {p: person.buyPrice(p) for p in products}
    prices = {p: getBestPriceForProduct(p, sellers) for p in products}
    costEffects = [(p, desires[p] / prices[p][1]) for p in products]
    costEffectsSorted = sorted(costEffects, key= lambda e: e[1])
    
    for costEffect in costEffectsSorted:
        product = costEffect[0]
        (seller, price) = prices[product]
        if price <= buyer.money:
            return (seller, product, price)
    
    return (None, None, None)


def trade(buyer, seller, product, price):
    buyer.money -= price
    seller.money += price
    buyer.products[product] += 1
    seller.products[product] -= 1


    
#%%
nrPeople = 100
nrSteps = 100

#%%
people = [Person(i) for i in range(nrPeople)]

log = []

order = list(range(nrPeople))
for t in range(nrSteps):
    np.random.shuffle(order)
    for i in order:
        person = people[i]
        sellers = [p for p in people if p != person]
        (seller, product, price) = choseTrade(person, sellers)
        if seller:
            trade(person, seller, product, price)
            log.append({ 'time': t, 'buyer': person.id, 'seller': seller.id, 'product': product, 'price': price})
    
    h = np.sum([p.calcHappyness() for p in people])
    print(f"{t} - {h}")









# %%
