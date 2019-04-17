import numpy as np
import pickle
import sys
sys.path.append("..")
from ami_game.game import ConfidentialityGame
from ami_game.population import Population
from ami_game.node import Node

# Generate tree
n1 = Node()
n1.value = 33.0
n1.cost_defence = 0.6
n1.cost_attack = 10.0

n2 = Node()
n2.value = 15.0
n2.cost_defence = 0.6
n2.cost_attack = 6.0

n3 = Node()
n3.value = 18.0
n3.cost_defence = 0.6
n3.cost_attack = 6.0

n4 = Node()
n4.value = 3.0
n4.cost_defence = 0.8
n4.cost_attack = 0.01

n5 = Node()
n5.value = 12.0
n5.cost_defence = 0.8
n5.cost_attack = 0.01

n6 = Node()
n6.value = 9.0
n6.cost_defence = 0.8
n6.cost_attack = 0.01

n7 = Node()
n7.value = 9.0
n7.cost_defence = 0.6
n7.cost_attack = 6.0

n8 = Node()
n8.value = 3.0
n8.cost_defence = 0.8
n8.cost_attack = 0.01

n9 = Node()
n9.value = 3.0
n9.cost_defence = 0.8
n9.cost_attack = 0.01

n10 = Node()
n10.value = 3.0
n10.cost_defence = 0.8
n10.cost_attack = 0.01

n11 = Node()
n11.value = 3.0
n11.cost_defence = 0.8
n11.cost_attack = 0.01

n12 = Node()
n12.value = 3.0
n12.cost_defence = 0.8
n12.cost_attack = 0.01

n13 = Node()
n13.value = 3.0
n13.cost_defence = 0.8
n13.cost_attack = 0.01

n14 = Node()
n14.value = 3.0
n14.cost_defence = 0.8
n14.cost_attack = 0.01

n15 = Node()
n15.value = 3.0
n15.cost_defence = 0.8
n15.cost_attack = 0.01

# Make structure
n1.add_child(n2)
n1.add_child(n3)

n2.add_child(n4)
n2.add_child(n5)

n3.add_child(n6)
n3.add_child(n7)

n5.add_child(n8)
n5.add_child(n9)
n5.add_child(n10)

n6.add_child(n11)
n6.add_child(n12)

n7.add_child(n13)
n7.add_child(n14)
n7.add_child(n15)

tree = [n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15]

# Initialize game and get strategy spaces
game = ConfidentialityGame(tree, K=3, a=0.0, defender_budget=1.0)

print('Validating parameters')
for node in tree:
    node.validate(game.a)

s = game.attacker_strategies()
t = game.defender_strategies()

# Generate initial populations
attacker_population = 1.0/len(s)*np.ones(len(s))
defender_population = 1.0/len(t)*np.ones(len(t))

population = Population(game, attacker_population, defender_population,
        dt=0.1, delta=100.0)

attack_profiles = np.zeros((0, len(tree)))
defence_profiles = np.zeros((0, len(tree)))
average_utility = np.zeros((0, 2))

population.calculate_utilities()
average_utility = np.append(average_utility,
            np.array([population.get_average_attacker_utility(),
                      population.get_average_defender_utility()])[np.newaxis],
            axis=0)
# Calculating attack profile
attack_profiles = np.append(attack_profiles,
        population.get_attack_profiles()[np.newaxis], axis=0)
# Calculating defence profile
defence_profiles = np.append(defence_profiles,
        population.get_defence_profiles()[np.newaxis],
        axis=0)

# Evolove population
N_populations = 200
for i in range(0, N_populations):
    print('Population number '+str(i))
    # Copy population
    population.replicate()
    average_utility = np.append(average_utility,
            np.array([population.get_average_attacker_utility(),
                      population.get_average_defender_utility()])[np.newaxis],
            axis=0)
    # Calculating attack profile
    attack_profiles = np.append(attack_profiles,
            population.get_attack_profiles()[np.newaxis], axis=0)
    # Calculating defence profile
    defence_profiles = np.append(defence_profiles,
            population.get_defence_profiles()[np.newaxis],
            axis=0)

np.savetxt('attackers', attack_profiles)
np.savetxt('defenders', defence_profiles)
np.savetxt('utility', average_utility)

# Save for future continue
pickle.dump(population, open('population_dump', 'w'))
