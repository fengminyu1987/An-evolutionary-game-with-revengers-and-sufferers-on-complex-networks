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
    # graph = nx.grid_graph((L, L), periodic=True)
    graph = nx.random_graphs.watts_strogatz_graph(1600, 4, 0.3)
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


L = 40
time_steps = 10000
r = 0.05
K = 1
simulations = 100
total_cooperator_rates = np.zeros(time_steps)
for i in range(simulations):
    print(i)
    G = init_graph()
    strategies = nx.get_node_attributes(G, 'strategy')
    cooperator_rates = []
    nodes = G.nodes
    for time_step in range(time_steps):
        payoff_dict = calculate_payoff()
        cooperator_rate = calculate_cooperator_rate()
        print(cooperator_rate)
        cooperator_rates.append(cooperator_rate)
        random_nodes = random.sample(nodes, 160)
        for node in random_nodes:
            own_payoff = payoff_dict[node]
            neighbors = [neighbor for neighbor in nx.neighbors(G, node)]
            random_neighbor = random.choice(neighbors)
            random_neighbor_payoff = payoff_dict[random_neighbor]
            probability = Fermi_function(own_payoff, random_neighbor_payoff)
            if random.random() < probability:
                G.nodes[node]['strategy'] = strategies[random_neighbor]
        last_strategies = strategies
        strategies = nx.get_node_attributes(G, 'strategy')
    total_cooperator_rates += cooperator_rates
average_cooperator_rates = total_cooperator_rates / simulations
plt.plot(range(time_steps), average_cooperator_rates, label='traditional cooperator')

average_cooperator_rates = pd.DataFrame(average_cooperator_rates)
average_cooperator_rates.to_csv("tradition.csv", index=False, header=False)

rhos = [0.2, 0.4, 0.6, 0.8, 1]
# style = ['bs', 'g^', 'm>', 'r*', 'c<']
count = 0
for rho in rhos:
    total_cooperator_rates = np.zeros(time_steps)
    for i in range(simulations):
        print(i)
        G = init_graph()
        strategies = nx.get_node_attributes(G, 'strategy')
        cooperator_rates, defector_rates = [], []
        nodes = G.nodes
        for time_step in range(time_steps):
            payoff_dict = calculate_payoff()
            cooperator_rate = calculate_cooperator_rate()
            cooperator_rates.append(cooperator_rate)
            if time_step >= 1:
                constant_cooperator_nodes = calculate_constant_cooperator_nodes()
                revenge_dict = calculate_revenge_pairs()
                revenge_nodes = [value for value in revenge_dict.keys()]
                revenge_function(0, rho)
            random_nodes = random.sample(nodes, 160)
            for node in random_nodes:
                own_payoff = payoff_dict[node]
                neighbors = [neighbor for neighbor in nx.neighbors(G, node)]
                random_neighbor = random.choice(neighbors)
                random_neighbor_payoff = payoff_dict[random_neighbor]
                probability = Fermi_function(own_payoff, random_neighbor_payoff)
                if random.random() < probability:
                    G.nodes[node]['strategy'] = strategies[random_neighbor]
            last_strategies = strategies
            strategies = nx.get_node_attributes(G, 'strategy')
        total_cooperator_rates += cooperator_rates
    average_cooperator_rates = total_cooperator_rates / simulations
    plt.plot(range(time_steps), average_cooperator_rates, label='revenge_cooperator rho = ' + str(rho))
    average_cooperator_rates = pd.DataFrame(average_cooperator_rates)
    average_cooperator_rates.to_csv("data//SL//rho_s varies//rho_r 0 rho_s " + str(rho) + ".csv", index=False, header=False)
    count += 1

plt.legend(loc='best')
plt.show()

