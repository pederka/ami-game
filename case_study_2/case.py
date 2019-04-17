import numpy as np
import pickle
import pydot
import sys
from ami_game.game import ConfidentialityGame
from ami_game.population import Population
from ami_game.node import Node

if len(sys.argv) > 1 and sys.argv[1] == 'continue':
    print 'Continuing on previous simulation'
    population = pickle.load(open('population_dump', 'r'))    
    attack_profiles = np.genfromtxt('attackers')
    defence_profiles = np.genfromtxt('defenders')
    average_utility = np.genfromtxt('utility')
    s = population.game.attacker_strategies()
    t = population.game.defender_strategies()
    tree = population.game.tree

else:
    # Generate tree
    n1 = Node(0)
    n1.value = 65.0
    n1.cost_attack = 0.2
    n1.cost_defence = 0.05

    # The root node is its own parent. Cut value by half to avoid inconsitency
    n1.parent = 1
    n1.value = n1.value*0.5
    
    ###

    n2 = Node(1)
    n2.value = 20.0
    n2.cost_attack = 0.2
    n2.cost_defence = 0.05

    n3 = Node(2)
    n3.value = 40.0
    n3.cost_attack = 0.2
    n3.cost_defence = 0.05

    n1.add_child(n2)
    n1.add_child(n3)

    ###

    n4 = Node(3)
    n4.value = 14.0
    n4.cost_attack = 0.2
    n4.cost_defence = 0.05

    n5 = Node(4)
    n5.value = 6.0
    n5.cost_attack = 0.2
    n5.cost_defence = 0.05

    n6 = Node(5)
    n6.value = 29.0
    n6.cost_attack = 0.2
    n6.cost_defence = 0.05

    n7 = Node(6)
    n7.value = 4.0
    n7.cost_attack = 0.2
    n7.cost_defence = 0.05

    n8 = Node(7)
    n8.value = 15.0
    n8.cost_attack = 0.2
    n8.cost_defence = 0.05

    n2.add_child(n4)
    n2.add_child(n5)
    n3.add_child(n6)
    n3.add_child(n7)
    n3.add_child(n8)

    ###

    n9 = Node(8)
    n9.value = 1.0
    n9.cost_attack = 0.2
    n9.cost_defence = 0.05

    n10 = Node(9)
    n10.value = 2.0
    n10.cost_attack = 0.2
    n10.cost_defence = 0.05

    n11 = Node(10)
    n11.value = 1.0
    n11.cost_attack = 0.2
    n11.cost_defence = 0.05

    n12 = Node(11)
    n12.value = 5.0
    n12.cost_attack = 0.2
    n12.cost_defence = 0.05

    n4.add_child(n9)
    n4.add_child(n10)
    n4.add_child(n11)
    n4.add_child(n12)

    ###
    
    n13 = Node(12)
    n13.value = 3.0
    n13.cost_attack = 0.2
    n13.cost_defence = 0.05

    n14 = Node(13)
    n14.value = 1.5
    n14.cost_attack = 0.2
    n14.cost_defence = 0.05

    n5.add_child(n13)
    n5.add_child(n14)

    ###

    n15 = Node(14)
    n15.value = 1.0
    n15.cost_attack = 0.2
    n15.cost_defence = 0.05

    n16 = Node(15)
    n16.value = 4.0
    n16.cost_attack = 0.2
    n16.cost_defence = 0.05

    n17 = Node(16)
    n17.value = 6.0
    n17.cost_attack = 0.2
    n17.cost_defence = 0.05

    n18 = Node(17)
    n18.value = 4.0
    n18.cost_attack = 0.2
    n18.cost_defence = 0.05

    n19 = Node(18)
    n19.value = 3.0
    n19.cost_attack = 0.2
    n19.cost_defence = 0.05

    n6.add_child(n15)
    n6.add_child(n16)
    n6.add_child(n17)
    n6.add_child(n18)
    n6.add_child(n19)

    ###

    n20 = Node(19)
    n20.value = 1.0
    n20.cost_attack = 0.2
    n20.cost_defence = 0.05

    n21 = Node(20)
    n21.value = 1.5
    n21.cost_attack = 0.2
    n21.cost_defence = 0.05

    n7.add_child(n20)
    n7.add_child(n21)

    ###

    n22 = Node(21)
    n22.value = 3.0
    n22.cost_attack = 0.2
    n22.cost_defence = 0.05

    n23 = Node(22)
    n23.value = 5.0
    n23.cost_attack = 0.2
    n23.cost_defence = 0.05

    n24 = Node(23)
    n24.value = 1.5
    n24.cost_attack = 0.2
    n24.cost_defence = 0.05

    n8.add_child(n22)
    n8.add_child(n23)
    n8.add_child(n24)


    tree = [n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14,
            n15, n16, n17, n18, n19, n20, n21, n22, n23, n24]

    # Initialize game and get strategy spaces
    game = ConfidentialityGame(tree, K=2, a=0.6, attacker_budget=1.0,
            defender_budget=4.0)

    print 'Calculating strategy spaces'
    s = game.attacker_strategies()
    t = game.defender_strategies()

    # Generate initial populations
    print 'Setting up initial populations'
    attacker_population = 1.0/len(s)*np.ones(len(s))
    defender_population = 1.0/len(t)*np.ones(len(t))

    population = Population(game, attacker_population, defender_population,
            k=0.2)
    
    attack_profiles = np.zeros((0, len(tree)))
    defence_profiles = np.zeros((0, len(tree)))
    average_utility = np.zeros((0, 2))

# Evolove population
N_populations = 25
for i in range(0, N_populations):
    print 'Population number '+str(i)
    # Copy population
    population.replicate()
    average_utility = np.append(average_utility,
            np.array([population.get_average_attacker_utility(),
                      population.get_average_defender_utility()])[np.newaxis],
            axis=0)
    # Calculating attack profile
    attack_profiles = np.append(attack_profiles, 
            population.get_attack_profiles()[np.newaxis],
            axis=0)
    # Calculating defence profile
    defence_profiles = np.append(defence_profiles,
            population.get_defence_profiles()[np.newaxis],
            axis=0)

np.savetxt('attackers', attack_profiles)
np.savetxt('defenders', defence_profiles)
np.savetxt('utility', average_utility)

# Save for future continue
pickle.dump(population, open('population_dump', 'w'))
