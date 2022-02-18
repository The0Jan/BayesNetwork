# Implementation of a single Node
class Node:
    def __init__(self, id, name, prob_table ):
        self.id = id
        self.name = name
        self.children = []
        self.parents = []
        self.prob_table = prob_table

    def add_child(self, child):
        connect(self, child)

    def add_parent(self, parent):
        connect(parent, self)

    def set_value(self, value):
        self.value = value

    def show(self):
        print(f"{self.id}: '{self.name}'; {self.prob_table}; Parents:{[p.id for p in self.parents]}; Children:{[c.id for c in self.children]}")


def connect(parent, child):
    parent.children.append(child)
    child.parents.append(parent)

# Implementation of a set of Nodes that make up a network
class Bayes_network:
    def __init__(self):
        self.nodes = []
        self.id = -1

    def new_node(self, name, prob_table):
        self.id += 1
        node = Node(self.id, name, prob_table)
        self.nodes.append(node)
        return node

    def show(self):
        for node in self.nodes:
            node.show()

    def create_mass_nodes(self, nodes):
        for node in nodes:
            self.new_node(node[0], node[1])

    def create_mass_connections(self, connect):
        for connection in connect:
            self.nodes[connection[0]].add_parent(self.nodes[connection[1]])



