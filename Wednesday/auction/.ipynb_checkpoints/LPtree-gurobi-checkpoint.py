import cplex

import generate as gen

from pulp import *

def listrange(nstart,nend):
    a = []
    for k in xrange(nstart,nend+1):
        a.append(str(k))
    return a

itemtype = ["A","B","C","D"]
items = listrange(1,12)
T = len(itemtype)
N = len(items)
nrItems = dict(zip(itemtype,[3,3,3,3]))

paths = dict()
leafs = dict()
decisions = dict()

M = 1000000
fmax = {}

def readdata():
    for t in itemtype:
        filein = open("tree"+t+".txt",'r')
        for line in filein:
            row = line.split()
            if "decision" in line:
                decisions[t+row[0]+":T"] = [int(row[4]), float(row[7])]
                decisions[t+row[0]+":F"] = [int(row[4]), float(row[7])]
            else:
                leafs[t+row[0]] = float(row[5])
                paths[t+row[0]] = [t+row[k].replace("(+)",":T").replace("(-)",":F") for k in xrange(9,len(row)-1)]

def featuremap():
    features = []
    values = []
    features.append("sumv")
    values.append(M)
    features.append("index")
    values.append(N)

    for t in gen._ITEMS_:
        features.append("sold")
        values.append(nrItems[t])
        features.append("remain")
        values.append(nrItems[t])
        for t2 in gen._ITEMS_:
            if t != t2:
                features.append("sold" + t + "g" + t2)
                values.append(1)
                features.append("remain" + t + "g" + t2)
                values.append(1)

    for t in gen._ITEMS_:
        features.append("sum" + t)
        values.append(M)
        features.append("index")
        values.append(M)
        # for now replace average by index

    return features, values

def lpdtree():
    prob = LpProblem("DTreeLP", LpMaximize)
    x = LpVariable.dicts("x",(items,itemtype),0,1,LpInteger)
    y = LpVariable.dicts("y",(items,decisions.keys()),0,1,LpInteger)
    z = LpVariable.dicts("z",(items,leafs.keys()),0,1,LpInteger)
    v = LpVariable.dicts("v",(items))
    feat = dict()
    features, maxvalues = featuremap()
    for f in features:
        feat[f] = LpVariable.dicts(f,(items,itemtype))

    prob += sum([v[i] for i in items]),""

    for t in itemtype:
        prob += lpSum([x[i][t] for i in items]) == nrItems[t],""

    for i in items:
        prob += lpSum([x[i][t] for t in itemtype]) == 1,""
        prob += lpSum([z[i][l] for l in leafs.keys()]) == 1,""

    for i in items:
        prob += v[i] == lpSum([leafs[l]*z[i][l] for l in leafs.keys()]),""

    #feature constraints
    for i in items:
        for t in itemtype:
            prob += feat["sumv"][i][t] == lpSum([v[j] for j in listrange(1,int(i)-1)]),""
            prob += feat["index"][i][t] == lpSum([lpSum([x[j][t] for j in listrange(1,int(i)-1)])] for t in itemtype),""

    for i in items:
        for t in itemtype:
            prob += feat["sold"][i][t] == lpSum([x[j][t] for j in listrange(1,int(i)-1)]),""
            prob += feat["remain"][i][t] == lpSum([x[j][t] for j in listrange(int(i)+1,N)]),""

    for i in items:
        for t in itemtype:
            for t1 in itemtype:
                for t2 in itemtype:
                    if t1 != t2:
                         prob += feat["sold" + t1 + "g" + t2][i][t] == int(feat["sold"][i][t] > feat["sold"][i][t]),""
                         prob += feat["remain" + t1 + "g" + t2][i][t] == int(feat["remain"][i][t] > feat["remain"][i][t]),""

    for i in items:
        for t in itemtype:
            for t1 in itemtype:
                prob += feat["sum" + t1][i][t] == lpSum([leafs[l]*z[i][l] for l in leafs.keys() if t in l]),""
                            
    for i in items:
        for l in leafs.keys():
            prob += z[i][l] <= 1.0/float(len(paths[l])+0.5)*(x[i][l[0]]+sum([y[i][d] for d in paths[l]])),""

    for i in items:
        for d in decisions.keys():
            if ":T" in d:
                _feature = feat[features[decisions[d][0]]][i][d[0]]
                _constant = float(decisions[d][1] - 0.1)
                prob += y[i][d] <= _feature/_constant,""
                if maxvalues[decisions[d][0]] < _constant + 0.1:
                    prob += y[i][d] == 0
                else:
                    denominator = maxvalues[decisions[d][0]] + 1 - _constant
                    prob += y[i][d] >= (_feature/denominator) - ((_constant)/denominator),""
            else:
                prob += y[i][d] == 1-y[i][d.replace(':F',':T')],""

    prob.writeLP("LPtree.lp")
    prob.solve(CPLEX())
    print "Status: ", LpStatus[prob.status]
    itemorder = []
    leaforder = []
    if 'Optimal' in LpStatus[prob.status]:
        for i in items:
            for t in itemtype:
                if value(x[i][t]) == 1:
                    itemorder.append(t)
        for i in items:
            for l in leafs.keys():
                if value(z[i][l]) == 1:
                    leaforder.append(round(leafs[l]))
        print itemorder
        print leaforder
        print "Objective = " + str(value(prob.objective))

readdata()
lpdtree()
