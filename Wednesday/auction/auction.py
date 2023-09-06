
import random

def simulatingBid(agents, max_bid, item, remain):
    bid_value = max_bid
    first_bidder = -1
    first_bid = -1
    while bid_value >= 0:
        indexes = list(range(len(agents)))
        random.shuffle(indexes)
        for i in indexes:
            a = agents[i]
            if a.willBid(item, bid_value, remain):
                if first_bidder == -1 or first_bidder == i:
                    first_bidder = i
                    first_bid = bid_value
                else:
                    temp_agents = copy.deepcopy(active_agents)
                    temp_items  = copy.deepcopy(remain)
                
                    temp_agents[first_bidder].buy(item, first_bid)
                    runAuction(temp_items, temp_agents)
                    v1 = temp_agents[first_bidder].currentValue + temp_agents[first_bidder].budget
                    
                    temp_agents = copy.deepcopy(active_agents)
                    temp_items  = copy.deepcopy(remain)

                    temp_agents[i].buy(item, bid_value)
                    runAuction(temp_items, temp_agents)
                    v2 = temp_agents[first_bidder].currentValue + temp_agents[first_bidder].budget

                    if v1 >= v2:
                        return first_bidder, first_bid
                    else:
                        first_bidder = i
                        first_bid = bid_value                
        bid_value = bid_value - 1
    return first_bidder, first_bid

def secondpriceBid(agents, max_bid, item, remain):
    bid_value = max_bid
    first_bidder = -1
    first_bid = -1
    while bid_value >= 0:
        indexes = list(range(len(agents)))
        random.shuffle(indexes)
        for i in indexes:
            a = agents[i]
            if a.willBid(item, bid_value, remain):
                if first_bidder == -1 or first_bidder == i:
                    first_bidder = i
                    first_bid = bid_value
                else:
                    return first_bidder, first_bid
        bid_value = bid_value - 1
    return first_bidder, first_bid

def myopicBid(agents, max_bid, item, remain):
    bid_value = max_bid
    while bid_value >= 0:
        indexes = list(range(len(agents)))
        random.shuffle(indexes)
        for i in indexes:
            a = agents[i]
            if a.willBid(item, bid_value, remain):
                return i, bid_value
        bid_value = bid_value - 1
    return -1, -1

def runAuction(items, agents):
    values = []
    remain = list(items)
    while len(remain) > 0:
        item = remain.pop(0)
        agent, bid = myopicBid(agents, 200, item, remain)
        #agent, bid = secondprinceBid(agents, 200, item, remain)
        #agent, bid = simulatingBid(agents, 200, item, remain)

        agents[agent].buy(item, bid)  
        values.append(bid)
    return values
