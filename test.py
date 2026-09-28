payoff_dict = {0: 1, 1: 3, 2: 3}

revenge_dict = {0: [1, 2]}
for node in revenge_dict:
    sufferers = revenge_dict[node]
    print(sufferers)
    payoff_dict[node] -= payoff_dict[node] * 0.2
    payoff_dict[sufferers] -= payoff_dict[node] * 1.0