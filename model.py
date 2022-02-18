from bayes_network import Bayes_network

# Network creation
network = Bayes_network()

# Nodes with their probability tables

network.create_mass_nodes([["Kupiłem jedzenie", 2 / 3],
                            ["Współlokator kupił jedzenie", 4 * 1/10],
                            ["Jedzenie kupiono", [[0.13, 0.05], [0.89, 0.63]]],
                            ["Dostałem jedzenie od babci", 2/31],
                            ["Dostałem jedzenie z domu", 1/14],
                            ["Mam jedzenie", [[[0.01, 0.04], [0.5, 0.23]],[[ 0.6, 0.53], [0.7, 0.43]]]]])


# Add connections between nodes
network.create_mass_connections([[2,0], [2,1], [5,2], [5,3], [5,4]])


# Network test
if __name__ == "__main__":
    network.show()

# Possible states that a node can take
pos_states = [0, 1]

# The states of the given model
model_states = [-1, -1, -1, -1, -1, -1]

# Lists with nodes that are certain and that are uncertain
certainNodes = []
uncertainNodes = []

for index,node in enumerate(network.nodes):
    if model_states[index] == -1:
        uncertainNodes.append(node)
    else:
        certainNodes.append(node)
    

