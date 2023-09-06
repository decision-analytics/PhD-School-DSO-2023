import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import random, copy
random.seed()

class agent(object):
    def __init__(self, b):
        self.budget = b
        self.bought = []
        self.wants = []
        self.wantvalues = []
        self.currentValue = 0
        self.bidprobability = 2.0
        self.storedValues = dict()
     
    def getMaxGreedy(self, copy):
        max = 0
        while len(copy) > 0:
            best_index = -1
            for index in range(len(self.wants)):
                want = self.wants[index]
                value = self.wantvalues[index]
                if best_index == -1 or self.wantvalues[best_index] < value:
                    if all(f in copy for f in want):
                        best_index = index
            if best_index == -1:
                break
            for f in self.wants[best_index]:
                copy.remove(f)
            max = max + self.wantvalues[best_index]
        return max

    def getMax(self, copy):
        return self.getMaxGreedy(copy)
        max = 0
        for index in range(len(self.wants)):
            want = self.wants[index]
            value = self.wantvalues[index]
            if all(f in copy for f in want):
                for f in want:
                    copy.remove(f)
                next_value = self.getMax(copy)
                if(max < value + next_value):
                    max = value + next_value
                copy.extend(want)
        return max

    def getValue(self, flower):
        copy = list(self.bought)
        copy.append(flower)
        if not flower in self.storedValues:
            self.storedValues[flower] = self.getMax(copy) - self.currentValue
        return self.storedValues[flower]
    
    def addWant(self, flowers, value):
        self.wants.append(flowers)
        self.wantvalues.append(value)

    def willBid(self, flower, bid, remain):
        if random.random() > self.bidprobability:
            return False
        if bid > self.budget:
            return False
        if [flower] not in self.wants:
            return False
        
        value = self.getValue(flower)
        if value >= bid:
            return True
        return False
    
    def buy(self, flower, bid):
        self.bought.append(flower)
        self.currentValue = self.getMax(list(self.bought))
        self.budget = self.budget - bid
        self.storedValues = dict()
