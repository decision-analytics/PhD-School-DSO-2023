import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import random, copy, numpy
from sklearn.tree import DecisionTreeRegressor
import generate as gen

import pickle

DATASETS = dict()
TARGETS = dict()
REGRESSORS = []
TREES = dict()

def save_all():
    LIST = []
    LIST.append(DATASETS)
    LIST.append(TARGETS)
    LIST.append(TREES)
    rtr_file = open("rtr.pickle", "wb")
    pickle.dump(LIST, rtr_file)

def load_all():
    rtr_file = open("rtr.pickle", "rb")

    LIST = pickle.load(rtr_file)
    print(LIST)
    DATASETS = LIST[0]
    print(DATASETS)
    TARGETS = LIST[1]
    print(TARGETS)
    TREES = LIST[2]
    print(TREES)

def emptyData():
    global DATASETS, TARGETS, TREES
    DATASETS = dict()
    TARGETS = dict()
    TREES = dict()
    for t in gen._ITEMS_:
        DATASETS[t] = []
        TARGETS[t] = []
        TREES[t] = DecisionTreeRegressor(min_samples_leaf=10)

def createRow(item, sold, remain, bids):
    newrow = []

    newrow = newrow + [sum(bids)]
    newrow = newrow + [len(sold)]

    for t in gen._ITEMS_:
        newrow = newrow + [sold.count(t)]
        newrow = newrow + [remain.count(t)]
        #for t2 in gen._ITEMS_:
        #    if t != t2:
        #        newrow = newrow + [sold.count(t) > sold.count(t2)]
        #        newrow = newrow + [remain.count(t) > remain.count(t2)]

    sumbids = dict()
    for t in gen._ITEMS_:
        sumbids[t] = 0.0
    for i in range(len(sold)):
        sumbids[sold[i]] = sumbids[sold[i]] + bids[i]
    for t in gen._ITEMS_:
        newrow = newrow + [sumbids[t]]
        #if sold.count(t) > 0:
        #    newrow = newrow + [sumbids[t] / sold.count(t)]
        #else:
        #    newrow = newrow + [0]

    return newrow

def addRow(bid, item, sold, remain, bids):
    global DATASETS, TARGETS, TREES
    TARGETS[item] = TARGETS[item] + [bid]
    DATASETS[item] = DATASETS[item] + [createRow(item, sold, remain, bids)]

def addRows(items, bids):
    remain = list(items)
    done_bids = []
    sold = []
    while len(remain) != 0:
        item = remain.pop(0)
        bid = bids.pop(0)

        addRow(bid, item, sold, remain, done_bids)

        sold = sold + [item]
        done_bids = done_bids + [bid]

def learnTrees():
    global DATASETS, TARGETS, TREES
    for t in gen._ITEMS_:
        TREES[t].fit(DATASETS[t],TARGETS[t])

def evaluateOrder(order):
    values = []
    sold = []
    remain = list(order)
    while remain != []:
        item = remain.pop(0)
        row = createRow(item, sold, remain, values)
        values = values + [TREES[item].predict(row)]
        sold = sold + [item]
    return values    
