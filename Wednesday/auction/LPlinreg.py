import cplex
from pulp import *

def listrange(nstart,nend):
    a = []
    for k in xrange(nstart,nend+1):
        a.append(str(k))
    return a

itemtype = ["A","B","C","D"]
items = listrange(1,40)
T = len(itemtype)
N = len(items)
nrItems = dict(zip(itemtype,[10,10,10,10]))

cBefore = dict(zip(itemtype,[0.5,0.3,0.2,0.1]))
cAfter = dict(zip(itemtype,[0.5,0.3,0.2,0.1]))
cSumBids = dict(zip(itemtype,[0.5,0.3,0.2,0.1]))

M = 1000000

def lplinreg():
    prob = LpProblem("LinRegLP", LpMaximize)
    x = LpVariable.dicts("x",(items,itemtype),0,1,LpInteger)
    before = LpVariable.dicts("before",(items,itemtype))
    after = LpVariable.dicts("after",(items,itemtype))
    sumBids = LpVariable.dicts("sumBids",(items,itemtype))
    xbe = LpVariable.dicts("xbe",(items,itemtype),0)
    xaf = LpVariable.dicts("xaf",(items,itemtype),0)
    xsb = LpVariable.dicts("xsb",(items,itemtype),0)


    prob += sum([sum([cBefore[t]*xbe[i][t] + cAfter[t]*xaf[i][t] + cSumBids[t]*xsb[i][t] for i in items]) for t in itemtype]),""
    
    for i in items:
        prob += lpSum([x[i][t] for t in itemtype]) == 1,""
    for t in itemtype:
        prob += lpSum([x[i][t] for i in items]) == nrItems[t],""

    for t in itemtype:
        for i in items:
            prob += before[i][t] == lpSum([x[j][t] for j in listrange(1,int(i)-1)])
            prob += after[i][t] == lpSum([x[j][t] for j in listrange(int(i)+1,N)]),""
            prob += sumBids[i][t] == lpSum([cSumBids[t] * xsb[j][t] for j in listrange(1,int(i)-1)]),""
            
            prob += xbe[i][t] <= M*x[i][t],""
            prob += xbe[i][t] <= before[i][t],""
            prob += xbe[i][t] >= before[i][t] - M*(1-x[i][t]),""
            
            prob += xaf[i][t] <= M*x[i][t],""
            prob += xaf[i][t] <= after[i][t],""
            prob += xaf[i][t] >= after[i][t] - M*(1-x[i][t]),""
            
            prob += xsb[i][t] <= M*x[i][t],""
            prob += xsb[i][t] <= sumBids[i][t],""
            prob += xsb[i][t] >= sumBids[i][t] - M*(1-x[i][t]),""

    prob.writeLP("LPlinreg.lp")
    prob.solve(CPLEX())
    print "Status: ", LpStatus[prob.status]
    out = open('linregsolution.txt','w')
    out.write("  ")
    for t in itemtype:
        out.write("  %(type)1s " % {"type": t})
    out.write("\n")
    for i in items:
        out.write("%(item)2s" % {"item": i})
        for t in itemtype:
            out.write("  %(val)1.0f " % {"val": value(x[i][t])})
        out.write("\n")
    out.write("\nObjective = " + str(value(prob.objective)))
    out.close()

lplinreg()

    
