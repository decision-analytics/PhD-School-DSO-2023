import random, copy, itertools, collections

from agent import *
from auction import *

random.seed()

_NUM_AGENTS_          = 5
_NUM_PARTICIPANTS_    = 5

_MIN_BUDGET_          = 40
_MAX_BUDGET_          = 200
_MIN_ITEMS_           = 1
_MAX_ITEMS_           = 3
_ITEMS_               = ["A","B","C","D"]
_NUM_ITEMS_           = len(_ITEMS_)
_ITEM_SUBSETS_        = list()
_ITEM_SUBSETS_.extend(itertools.combinations(_ITEMS_,2))
#_ITEM_SUBSETS_.extend(itertools.combinations(_ITEMS_,3))

_PRICE_RANGE_          = [0.75,1.5]

average_price          = dict(zip(_ITEMS_,[10,15,20,30]))
item_popularity        = dict(zip(_ITEMS_,[random.randint(1,10),random.randint(1,10),random.randint(1,10),random.randint(1,10)]))
item_sparsity          = dict(zip(_ITEMS_,[random.randint(1,10),random.randint(1,10),random.randint(1,10),random.randint(1,10)]))
subset_complementarity = dict(zip(_ITEM_SUBSETS_,[random.choice([1.1,1.4,1.7,2.0]) for i in _ITEM_SUBSETS_]))
subset_probability     = dict(zip(_ITEM_SUBSETS_,[random.choice([0.2,0.4,0.6,0.8]) for i in _ITEM_SUBSETS_]))

_MIN_ITEMS_PER_AUCTION_ = 10
_MAX_ITEMS_PER_AUCTION_ = 30

def reset():
    global average_price, item_popularity, item_sparsity, subset_complementarity, subset_probability

    average_price          = dict(zip(_ITEMS_,[random.randint(5,15),random.randint(10,20),random.randint(20,30),random.randint(30,50)]))
    item_popularity        = dict(zip(_ITEMS_,[random.randint(1,10),random.randint(1,10),random.randint(1,10),random.randint(1,10)]))
    item_sparsity          = dict(zip(_ITEMS_,[random.randint(1,10),random.randint(1,10),random.randint(1,10),random.randint(1,10)]))
    subset_complementarity = dict(zip(_ITEM_SUBSETS_,[random.choice([1.1,1.4,1.7,2.0]) for i in _ITEM_SUBSETS_]))
    subset_probability     = dict(zip(_ITEM_SUBSETS_,[random.choice([0.2,0.4,0.6,0.8]) for i in _ITEM_SUBSETS_]))

def select(popularity):
    total_popularity = sum([popularity[it] for it in popularity.keys()])
    rand = random.uniform(0,total_popularity)
    sump = 0
    for key in popularity.keys():
        sump = sump + popularity[key]
        if sump >= rand:
            return key
    return popularity.keys()[-1]

def create_items():
    items = []
    num = random.randint(_MIN_ITEMS_PER_AUCTION_,_MAX_ITEMS_PER_AUCTION_)
    for i in range(num):
        items.extend([select(item_sparsity)])
    random.shuffle(items)
    return items

def select_agents(agents):
    active_agents = copy.deepcopy(agents)
    random.shuffle(active_agents)
    return active_agents[0:_NUM_PARTICIPANTS_]

def create_agents():
    reset()
    agents = []
    for i in range(int(round(_NUM_AGENTS_))):
        a = agent(random.randint(_MIN_BUDGET_,_MAX_BUDGET_))
        num = random.randint(_MIN_ITEMS_,_MAX_ITEMS_)
        wanted = list()
        values = list()
        j = 0
        while j < num:
            chosen = select(item_popularity)
            if not chosen in wanted:
                mod = random.uniform(_PRICE_RANGE_[0],_PRICE_RANGE_[1])
                values.append(round(average_price[chosen] * mod))
                wanted.append(chosen)
                j = j + 1

        for j in range(num):
            a.addWant(list(wanted[j]),values[j])

        possible_subsets = list()
    #    for j in range(num-1):
    #        possible_subsets.extend(itertools.combinations(wanted,j+2))
        possible_subsets.extend(itertools.combinations(wanted,2))

        for s in possible_subsets:
            s = tuple(sorted(s))
            prob = random.random()
            if prob < subset_probability[s]:
                a.addWant(list(s), round(subset_complementarity[s] * sum([values[wanted.index(it)] for it in s])))

        #a.budget = a.budget + max(a.wantvalues)

        agents.append(a)

    return agents

def test(it, agents):
    items = list(it)
    random.shuffle(items)
    result = runAuction(items, copy.deepcopy(agents))
    #print sum(result), " = ", zip(items, result)
    return sum(result)

def agent_string(agents):
    string = ""    
    for a in agents:
       string = string + str(list(zip(a.wants,a.wantvalues))) + str(a.budget) + "\n"
    return string

def result_string(results):
    l = len(results)
    string = str(results[0]) + " " + \
             str(results[int(float(l)*0.05)]) + " " + \
             str(results[int(float(l)*0.25)]) + " " + \
             str(results[int(float(l)*0.5)]) + " " + \
             str(results[int(float(l)*0.75)]) + " " + \
             str(results[int(float(l)*0.95)]) + " " + \
             str(results[-1]) +\
             "\n"
    return string

def generate_sensible_agents():
    global average_price, item_popularity, item_sparsity, subset_complementarity, subset_probability
    agents = create_agents()

    print(agent_string(agents))

    for ROUND in range(4):
        items = create_items()
        #print collections.Counter(items)
        results = list()
        for i in range(100):
            active_agents = copy.deepcopy(agents)
            random.shuffle(items)
            #print items
            value = test(items, active_agents)
            results.append(value)

        results = sorted(results)
        print(result_string(results))

        if results[-1] - results[0] > (results[int(len(results)/2)] / 5):
            #open("sensible.txt", "a").write(agent_string(agents) + "\n")
            #open("sensible.txt", "a").write(str(collections.Counter(items)) + "\n")
            #open("sensible.txt", "a").write(result_string(results) + "\n")
            #open("sensible.txt", "a").write("\n=====\n")
            return agents

    #open("not_sensible.txt", "a").write(str(agents))
    #open("not_sensible.txt", "a").write("\n=====\n")
    
    return generate_sensible_agents()
