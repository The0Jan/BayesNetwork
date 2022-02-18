import random 
from model import  network, model_states, certainNodes, uncertainNodes, pos_states

# Generates state table filling known states or filling at random uknown states
def generate_states():
    states = [None] * len(network.nodes)
    for node in network.nodes:
        if node in certainNodes:
            states[node.id] = model_states[node.id]
        else:
            states[node.id] = random.choice(pos_states)

    return states

# Normalize the given arguments in a table
def normal(arguments):
    summ = 0
    for prob in arguments:
        summ += prob
    result = [prob/summ for prob in arguments]
    return result

# Get probability for parents
def get_parents_prob(states, node):
    search = node.prob_table
    for parent in (node.parents):
        search = search[states[parent.id]]
    return (search, 1 - search)


# Perform the probability under Markov blanket on the given node
def markov_blanket(states, node):
    parent_prob = get_parents_prob(states, node)[::states[node.id] *-2 +1]
    for child in node.children:

        parent_prob = [parent1 * parent2 for parent1,parent2 in zip(parent_prob, get_parents_prob(states, child)[::(states[child.id] * 2 -1)])]

    parent_prob = parent_prob[::states[node.id] *-2 +1]

    return normal(parent_prob)


# Choose the more probable outcome
def choose_rand( prob):
    rng = random.random()
    if rng < prob:
        return 1
    else:
        return 0

# Perform the random stroling algorithm
def  random_stroling(amount, repeat, states,check ):
    repeated = []
    counter = [0, 0]
    start = 1
    times = []
    for i in range(amount):
        ind = random.randrange(0, len(uncertainNodes))
        node = uncertainNodes[ind]
        states[node.id] = choose_rand(markov_blanket(states,node)[0])
        counter[states[network.nodes[check].id]] += 1
        if i == start:
            repeated.append([counter[0],counter[1]])
            times.append(start)
            start *= repeat
    return counter, repeated, times


def to_percent(number):
    return round(number * 10000) / 100

# Printing
def print_result(result, probed_results, times, check):
    print_final(result, check)
    print("Probe results:")
    for i, j in enumerate(times):
        print(f'{to_percent(probed_results[i][1])}% for and {to_percent(probed_results[i][0])}% against at {j} iterations')
    print()

def print_final(result, check):
    print(f'"{network.nodes[check].name}" has {to_percent(result[1])}% chance of happening!')


# Perfom sampling on one and give back the value based on the number of iterations
def sampling_one(amount, repeat, check):
    states = generate_states()
    # Gibbs
    counter, repeated, times = random_stroling(amount, repeat, states,check)

    # Normalize 
    repeated_results = [normal(reap) for reap in repeated]
    result = normal(counter)

    # Give back values
    print_result(result, repeated_results, times, check)

#Perform sampling on some of the nodes
def sampling_many(amount, repeat, check):
    results = []
    for checked in check:
        states = generate_states()
        # Gibbs
        counter, repeated, times = random_stroling(amount, repeat, states,checked)

        # Normalize 
        result = normal(counter)

        # Give results
        print_final(result, checked)
        results.append(result)
        
    # Return values
    return results


# Test each individual node
#sampling_one(1000000, 10, 5)
#sampling_one(1000000, 10, 4)
#sampling_one(1000000, 10, 3)
#sampling_one(1000000, 10, 2)
#sampling_one(1000000, 10, 1)
#sampling_one(1000000, 10, 0)

# Test for all nodes
sampling_many(100000,10, [0,1,2,3,4,5])
