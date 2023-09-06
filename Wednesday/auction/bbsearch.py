import random, copy, heapq

import generate as gen
import regtrees as rtr
import auction as auc
import experiment as exr

random.seed()

def greedy(ordered, remain):
    if remain == []:
        return ordered
    
    max_item = -1
    max_value = -1
        
    for i in set(remain):
        new_remain = list(remain)
        new_remain.remove(i)
        for it in range(25):
            random.shuffle(new_remain)
            value = sum(rtr.evaluateOrder(ordered + [i] + new_remain))
            if value > max_value:
                max_value = value
                max_item = i

    new_remain = list(remain)
    new_remain.remove(max_item)
    return greedy(ordered + [max_item], new_remain)

def bestFirst(items):
    search_space = []
    visited = dict()
    heapq.heappush(search_space, (0,[]))

    best_solution = -1
    max_value = -1
    counter = 0

    while len(search_space) > 0 and counter < 2500:
        (value, ordered) = heapq.heappop(search_space)
        value = -value
        remain = list(items)
        for i in ordered:
            remain.remove(i)

        #print list(ordered + remain)
        
        counter = counter + 1

        if value > max_value:
            max_value = value
            best_solution = list(ordered + remain)
            #print best_solution, max_value

        for i in set(remain):
            new_ordered = ordered + [i]
            new_remain = list(remain)
            new_remain.remove(i)
            value = 0
            for it in range(10):
                random.shuffle(new_remain)
                value = max(value,sum(rtr.evaluateOrder(new_ordered + new_remain)))

            visit = ""
            for it in gen._ITEMS_:
                visit = visit + str(new_ordered.count(it)) + it
            if not visit in visited:
                heapq.heappush(search_space,(-value,new_ordered))
                visited[visit] = sum(rtr.evaluateOrder(new_ordered))
            else:
                value_pre = sum(rtr.evaluateOrder(new_ordered))
                if value_pre > visited[visit]:
                    heapq.heappush(search_space,(-value,new_ordered))
                    visited[visit] = value_pre

    return best_solution

def bestRandom(items):
    max_value = -1
    max_order = -1
    for i in range(2500):
        random.shuffle(items)
        value = sum(rtr.evaluateOrder(items))
        if value > max_value:
            max_value = value
            max_order = list(items)
    return max_order

def bestRandomAuction(agents, items):
    max_value = -1
    max_order = -1
    sumvalues = 0
    for i in range(1000):
        random.shuffle(items)
        values = auc.runAuction(list(items),copy.deepcopy(agents))
        value = sum(values)
        sumvalues = sumvalues + value
        if value > max_value:
            max_value = value
            max_order = list(items)
    return max_order, sumvalues / 1000

def bestfirst_experiment(num_auctions):
    agents = gen.generate_sensible_agents()
    exr.runAuctions(agents,num_auctions)
    rtr.learnTrees()

    for r in range(50):
        items = gen.create_items()
        active_agents = gen.select_agents(agents)

        for a in active_agents:
            print zip(a.wants,a.wantvalues), a.budget

        solution = sorted(items)
        values = auc.runAuction(solution, copy.deepcopy(active_agents))
        print "Least valuable first:"
        print zip(values,[round(e) for e in rtr.evaluateOrder(solution)])
        print solution
        print sum(values), round(sum(rtr.evaluateOrder(solution)))

        solution.reverse()
        values = auc.runAuction(solution, copy.deepcopy(active_agents))
        print "Most valuable first:"
        print zip(values,[round(e) for e in rtr.evaluateOrder(solution)])
        print solution
        print sum(values), round(sum(rtr.evaluateOrder(solution)))

        solution = bestRandom(items)
        values = auc.runAuction(solution, copy.deepcopy(active_agents))
        print "Best random:"
        print zip(values,[round(e) for e in rtr.evaluateOrder(solution)])
        print solution
        print sum(values), round(sum(rtr.evaluateOrder(solution)))

        solution = greedy([], sorted(items))
        values = auc.runAuction(solution, copy.deepcopy(active_agents))
        print "Greedy:"
        print zip(values,[round(e) for e in rtr.evaluateOrder(solution)])
        print solution
        print sum(values), round(sum(rtr.evaluateOrder(solution)))

        solution = bestFirst(solution)
        values = auc.runAuction(solution, copy.deepcopy(active_agents))
        print "Best first:"
        print zip(values,[round(e) for e in rtr.evaluateOrder(solution)])
        print solution
        print sum(values), round(sum(rtr.evaluateOrder(solution)))

        solution, average = bestRandomAuction(copy.deepcopy(active_agents), items)
        values = auc.runAuction(solution, copy.deepcopy(active_agents))
        print "Best random auction:"
        print zip(values,[round(e) for e in rtr.evaluateOrder(solution)])
        print solution
        print sum(values), round(sum(rtr.evaluateOrder(solution)))

        print "Random average:", round(average)

bestfirst_experiment(250)

