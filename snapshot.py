import networkx as nx
import random
from math import exp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


def payoff_matrix(strategy1, strategy2):
    if strategy1 == 'C' and strategy2 == 'C':
        return 1
    elif strategy1 == 'C' and strategy2 == 'D':
        return -r
    elif strategy1 == 'D' and strategy2 == 'C':
        return 1 + r
    elif strategy1 == 'D' and strategy2 == 'D':
        return 0


def Fermi_function(x, y):
    return 1 / (1 + exp((x - y) / K))


def init_graph():
    graph = nx.grid_graph((L, L), periodic=True)
    for node in graph.nodes:
        if random.random() < 0.5:
            graph.add_node(node, strategy='C')
        else:
            graph.add_node(node, strategy='D')
    return graph


def calculate_cooperator_rate():
    c = 0
    for value in strategies.values():
        if value == 'C':
            c += 1
    cooperator_rate = c / len(G.nodes)
    return cooperator_rate


def calculate_payoff():
    payoff_dictionary = {}
    for node in nodes:
        neighbors = [neighbor for neighbor in nx.neighbors(G, node)]
        payoff = 0
        own_strategy = strategies[node]
        for neighbor in neighbors:
            neighbor_strategy = strategies[neighbor]
            payoff += payoff_matrix(own_strategy, neighbor_strategy)
        payoff_dictionary[node] = payoff
    return payoff_dictionary


def calculate_constant_cooperator_nodes():
    constant_cooperator_nodes = []
    for node in nodes:
        if last_strategies[node] == 'C' and strategies[node] == 'C':
            constant_cooperator_nodes.append(node)
    return constant_cooperator_nodes


def calculate_revenge_pairs():
    revenge_dict = {}
    for node in constant_cooperator_nodes:
        neighbors = nx.neighbors(G, node)
        sufferers = []
        for neighbor in neighbors:
            if last_strategies[neighbor] == 'C' and strategies[neighbor] == 'D':
                sufferers.append(neighbor)
        if len(sufferers) > 0:
            revenge_dict[node] = sufferers
    return revenge_dict


def revenge_function(parameter1, parameter2):
    for node in revenge_nodes:
        if payoff_dict[node] <= 0:
            continue
        else:
            sufferers = revenge_dict[node]
            for sufferer in sufferers:
                payoff_dict[node] -= K * payoff_dict[node] * parameter1
                payoff_dict[sufferer] -= K * payoff_dict[node] * parameter2


def generate_snapshot():
    snapshot = np.zeros((40, 40))
    shape = snapshot.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            if strategies[list(nodes)[40 * i + j]] == 'C':
                snapshot[i][j] = 1
            else:
                snapshot[i][j] = 0
    return snapshot


L = 40
time_steps = 10001
r = 0.02
K = 1
time_points = [0, 5000, 10000]
fig, ax = plt.subplots(nrows=1, ncols=len(time_points), figsize=(50, 50), dpi=100)
G = init_graph()
strategies = nx.get_node_attributes(G, 'strategy')
count = 0
nodes = G.nodes
rho_r = 0.2
rho_s = 0.8
path = "C:\\Users\\ZYZ\\Desktop\\网络科学\\第一篇论文\\data\\snapshots\\"
isExists = os.path.exists(path + str(rho_r) + " " + str(rho_s))
if not isExists:
    newdir = str(rho_r) + " " + str(rho_s)
    print(newdir)
    os.makedirs(path + newdir)
    print(path + newdir)
for time_step in range(time_steps):
    payoff_dict = calculate_payoff()
    if time_step == time_points[count]:
        snapshot = generate_snapshot()
        ax[count].imshow(snapshot, cmap='gray', origin='lower')
        snapshot = pd.DataFrame(snapshot)
        snapshot.to_csv("data//snapshots//0.2 0.8//" + str(time_step) + ".csv",
                        index=False,
                        header=False)
        print(count)
        count += 1

    if time_step >= 1:
        constant_cooperator_nodes = calculate_constant_cooperator_nodes()
        revenge_dict = calculate_revenge_pairs()
        revenge_nodes = [value for value in revenge_dict.keys()]
        revenge_function(rho_r, rho_s)
    random_nodes = random.sample(nodes, 160)
    for node in random_nodes:
        own_payoff = payoff_dict[node]
        neighbors = [neighbor for neighbor in nx.neighbors(G, node)]
        random_neighbor = random.choice(neighbors)
        random_neighbor_payoff = payoff_dict[random_neighbor]
        probability = Fermi_function(own_payoff, random_neighbor_payoff)
        if random.random() <= probability:
            G.nodes[node]['strategy'] = strategies[random_neighbor]
    last_strategies = strategies
    strategies = nx.get_node_attributes(G, 'strategy')
# plt.savefig("snapshots.png")
plt.show()
#
time_points = [0, 5000, 10000]
for time in time_points:
    snapshot = pd.read_csv("C:\\Users\\ZYZ\\Desktop\\网络科学\\第一篇论文\\data\\snapshots\\0.2 0.6\\" + str(time) + ".csv")
    snapshot = np.array(snapshot)
    plt.imshow(snapshot, cmap='gray')
    ax = plt.gca()
    ax.axes.xaxis.set_ticks([])
    ax.axes.yaxis.set_ticks([])
    plt.savefig("snapshot " + str(time) + " 0.2 0.6.pdf")
plt.show()
