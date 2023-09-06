import random, copy

import generate as gen
import regtrees as rtr
import auction as auc

import pickle
import csv
import sys

random.seed()

def runAuctions(agents, rounds):
    #rtr.emptyData()
    auctions = []
    for ROUND in range(rounds):
        items = gen.create_items()
        random.shuffle(items)
        active_agents = gen.select_agents(agents)
        result = auc.runAuction(items, active_agents)
        print(list(zip(items,result)))
        auctions += [[items,result]]
        #rtr.addRows(items, result)
    return auctions

def bestRandomAuction(agents, items):
    max_value = -1
    max_order = -1
    for i in range(250):
        random.shuffle(items)
        values = runAuction(deepcopy(agents),copy(items))
        value = sum(values)
        if value > max_value:
            max_value = value
            max_order = list(items)
    return max_order

def learning_experiment(num_auctions):
    agents = gen.generate_sensible_agents()
    runAuctions(agents,num_auctions)
    rtr.learnTrees()

    for ROUND in range(10):
        items = gen.create_items()
        random.shuffle(items)
        active_agents = gen.select_agents(agents)
        values = auc.runAuction(items, active_agents)
        exp_values = rtr.evaluateOrder(items)

def find_path(tree, i):
    if i == 0:
        return ""
    for j in range(len(tree.children_left)):
        if tree.children_left[j] == i:
            return find_path(tree,j) + " " + str(j) + "(+)"
    for j in range(len(tree.children_right)):
        if tree.children_right[j] == i:
            return find_path(tree,j) + " " + str(j) + "(-)"

if sys.argv[1] == "test":
    agent_file = open("agent.pickle", "rb")
    agents = pickle.load(agent_file)
    items_file = open("items.pickle", "rb")
    items = pickle.load(items_file)
    
    active_agents = gen.select_agents(agents)
    result = auc.runAuction(items, active_agents)
    print(str(result) + " " + str(sum(result)))
    
    print("\n\nRANDOM ORDERINGS:")

    for ROUND in range(20):
        random.shuffle(items)
        active_agents = gen.select_agents(agents)
        result = auc.runAuction(items, active_agents)
        print(str(items))
        print(str(result) + " " + str(sum(result)))

else:
    agents = gen.generate_sensible_agents()
    LIST = runAuctions(agents,250)
    auction_file = open("auction.pickle", "wb")
    pickle.dump(LIST, auction_file)
    agent_file = open("agent.pickle", "wb")
    pickle.dump(agents, agent_file)
