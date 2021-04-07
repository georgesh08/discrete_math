import networkx as nx
from networkx.algorithms import approximation
import matplotlib.pyplot as plt

free_nodes = ["CY", "MT", "IS"]

def maximum_connected_component(G):
    gr = nx.Graph(G)
    gr.remove_nodes_from(free_nodes)
    smallest = min(nx.connected_components(gr), key=len)
    gr.remove_nodes_from(smallest)
    return gr

def draw_graph(G, filename, node_color="#1F78B4", edge_color="000000"):
    plt.subplot(111)
    position = nx.planar_layout(G)
    nx.draw(G, pos=position, node_color=node_color, edge_color=edge_color, with_labels=True, width=0.7)
    plt.savefig(filename, dpi=1000)
    plt.show()

def task_b(G):
    gr = nx.Graph(G)
    print("|E| = " + str(gr.number_of_edges()))
    print("|V| = " + str(gr.number_of_nodes()))
    min = 100
    max = -100
    gr = maximum_connected_component(gr)
    for i in gr.nodes:
        if gr.degree[i] < min:
            min = gr.degree[i]
        if gr.degree[i] > max:
            max = gr.degree[i]
    print("𝛿(G) = " + str(min))
    print("Δ(G) = " + str(max))
    print("rad(G) = " + str(nx.radius(gr)))
    print("diam(G) = " + str(nx.diameter(gr)))
    print("girth(G) = " + str(len(nx.minimum_cycle_basis(G)[0])) + ", " + str(nx.minimum_cycle_basis(G)[0]))
    print("center(G) = " + str(nx.center(gr)))
    print("𝜅(G) = " + str(nx.node_connectivity(gr)))
    print("𝜆(G) = " + str(nx.edge_connectivity(gr)))

#def task_c(G):


def task_e(G):
    gr = maximum_connected_component(G)
    cliques = list(nx.enumerate_all_cliques(gr))
    print(cliques.pop())

def task_f(G):
    gr = maximum_connected_component(G)
    independent_set = nx.algorithms.approximation.maximum_independent_set(gr)
    print(independent_set)

def task_g(G):
    gr = nx.Graph(G)
    max_match = nx.max_weight_matching(gr, maxcardinality=True, weight=0)
    print(max_match)

G = nx.Graph()
file = open("input.txt")
edges = list()
for i in file.readlines():
    struct = i.split(", ")
    struct[2] = int(struct[2])
    edges.append(struct)

G.add_weighted_edges_from(edges)
G.add_nodes_from(free_nodes)

#draw_graph(G, "planar_pic") done
#task_b(G) done
#task_c(G) -
#task_d(G) -
#task_e(G) done
#task_f(G) done
task_g(G)


