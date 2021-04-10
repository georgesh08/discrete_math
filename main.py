import networkx as nx
from networkx.algorithms import approximation
import matplotlib.pyplot as plt

free_nodes = ["CY", "MT", "IS"]
color_map = ['b', 'g', 'y', "#9457EB", "#004242", "#FF43A4", "#FA8837", "#05AFB2", "#B22030", "#A0785A"]

def maximum_connected_component(G):
    gr = nx.Graph(G)
    gr.remove_nodes_from(free_nodes)
    smallest = min(nx.connected_components(gr), key=len)
    gr.remove_nodes_from(smallest)
    return gr

def find_weight(g):
    weight = 0
    p = nx.Graph(g)
    edges = list(p.edges)
    for edge in edges:
        weight += p.get_edge_data(edge[0], edge[1], "weight").get("weight")
    return weight

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


def task_c(G):
    # we can't use less, than 4 colors because of the clique maximum ['BY', 'PL', 'RU', 'UA']
    res_file = open('vertex_coloring.txt', 'w')
    gr = maximum_connected_component(G)
    coloring = nx.greedy_color(gr, strategy="DSATUR")
    for k, v in coloring.items():
        string = str(k) + ":" + str(v) + "\n"
        res_file.write(string)
    res_file.close()


def task_c_pic(G, filename):
    gr = maximum_connected_component(G)
    file = open("vertex_coloring.txt")
    colors = dict()
    nodes = (gr.nodes.keys())
    for line in file.readlines():
        colors[line.split(":")[0]] = int(line.split(":")[1])
    nodes_color = list()
    for i in nodes:
        nodes_color.append(color_map[colors[i]])
    draw_graph(gr, filename, node_color=nodes_color)

def task_d(G):
    # max degree in our graph is 9(for example: Germany), so we can't use less, than 9 colors. Lets color edges to prove that 9 is minimum
    gr = maximum_connected_component(G)
    file = open("edge_coloring.txt")
    edges_colors = list()
    colors = dict()
    for line in file.readlines():
        colors[(line.split(" ")[0], line.split(" ")[1])] = int(line.split(" ")[2])
    edges = (gr.edges.keys())
    for i in edges:
        edges_colors.append(color_map[colors[i]])
    draw_graph(gr, "edge_coloring.png", edge_color=edges_colors, node_color="#FF2603")

def task_e(G):
    gr = maximum_connected_component(G)
    cliques = list(nx.enumerate_all_cliques(gr))
    print("Maximum clique: " + str(cliques.pop()))

def task_f(G):
    gr = maximum_connected_component(G)
    independent_set = nx.algorithms.approximation.maximum_independent_set(gr)
    print("Size of stable: " + str(len(independent_set)))
    print("Stable set: " + str(independent_set))

def task_g(G):
    gr = maximum_connected_component(G)
    max_match = nx.max_weight_matching(gr, maxcardinality=True, weight=0)
    print("Size of maximum matching: " + str(len(max_match)))
    print("Maximum matching: " + str(max_match))

def task_h(G):
    gr = maximum_connected_component(G)
    min_v_cover = nx.algorithms.approximation.min_weighted_vertex_cover(gr, weight=0)
    print("Number of vertex in minimum cover: " + str(len(min_v_cover)))
    print("Minimum vertex cover of G: " + str(min_v_cover))

def task_i(G):
    gr = maximum_connected_component(G)
    min_e_cover = nx.algorithms.min_edge_cover(gr)
    print("Number of edges in minimum cover: " + str(len(min_e_cover)))
    print("Minimum edge cover of G: " + str(min_e_cover))

def task_m(G):
    two_edge_connected_components = list(nx.algorithms.connectivity.bridge_components(G))
    print("Total components: " + str(len(two_edge_connected_components)))
    print("Vertex in this components: " + str(two_edge_connected_components))

def find_max_biconnected_component(G):
    gr = maximum_connected_component(G)
    bnodes = nx.biconnected_component_edges(gr)
    return list(bnodes).pop()

def mst(G):
    gr = maximum_connected_component(G)
    spantree = nx.minimum_spanning_tree(gr)
    return spantree

def task_q(spantree):
    new_labels = dict()
    i = 0
    for node in spantree.nodes:
        new_labels[node] = i
        i+=1
    spntr = nx.relabel_nodes(spantree, new_labels)
    prufer = nx.to_prufer_sequence(spntr)
    print("Prufer code: " + str(prufer))

def task_p(span_tree):
    num = span_tree.number_of_nodes()
    component_weights = dict()
    centroid = list()
    for node in list(span_tree.nodes):
        tmp = nx.Graph(span_tree)
        tmp.remove_node(node)
        temp_list = [tmp.subgraph(c).copy() for c in nx.connected_components(tmp)]
        max = -1
        for sub in temp_list:
            deleted_edges = list()
            tmp_max = find_weight(sub)
            if tmp_max > max:
                component_weights[node] = tmp_max
                max = tmp_max
    min = 1000000
    for elem in component_weights:
        if component_weights[elem] < min:
            min = component_weights[elem]
    for elem in component_weights:
        if component_weights[elem] == min:
            centroid.append(elem)
    print(centroid)

G = nx.Graph()
file = open("input.txt")
edges = list()
for i in file.readlines():
    struct = i.split(", ")
    struct[2] = int(struct[2])
    edges.append(struct)
file.close()
G.add_weighted_edges_from(edges)
G.add_nodes_from(free_nodes)

draw_graph(G, "planar_pic")
task_b(G)
task_c(G)
task_c_pic(G, "vertex_coloring")
task_d(G)
task_e(G)
task_f(G)
task_g(G)
task_h(G)
task_i(G)
task_m(G)
span_tree = nx.Graph()
span_tree = mst(G)
task_p(span_tree)
task_q(span_tree)
draw_graph(span_tree, "mst.png")
