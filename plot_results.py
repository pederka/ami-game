import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler

colors = ['red', 'blue', 'black', 'orange', 'green', 'purple']
linewidth = 2.0

# Load data
attacker_data = np.genfromtxt('attackers')
defender_data = np.genfromtxt('defenders')
utility_data = np.genfromtxt('utility')
type_data = np.genfromtxt('node_types.txt')
type_names = ['HES','Collector', 'Meter/Collector', 'Meter'] 

generations = attacker_data.shape[0]
if generations > 40:
    markfreq = int(generations/40)
else:
    markfreq = 1

attacker_data_type = np.zeros((generations, 4))
attacker_data_level = np.zeros((generations, 4))

defender_data_type = np.zeros((generations, 4))
defender_data_level = np.zeros((generations, 4))

for i in range(0, attacker_data.shape[1]):
    attacker_data_type[:, type_data[i, 0]] += attacker_data[:, i]
    attacker_data_level[:, type_data[i, 1]] += attacker_data[:, i]

for i in range(0, defender_data.shape[1]):
    defender_data_type[:, type_data[i, 0]] += defender_data[:, i]
    defender_data_level[:, type_data[i, 1]] += defender_data[:, i]

# Utility evolution
plt.figure(3)
gens = range(1, utility_data.shape[0]+1) 
plt.plot(gens, utility_data[:, 0], marker='o', 
        markevery=markfreq,
        linewidth=linewidth,
            label='Attackers')
plt.plot(gens, utility_data[:, 1], marker='o', 
        markevery=markfreq,
        linewidth=linewidth,
            label='Defenders')

plt.ylabel('Average population utility')
plt.xlabel('Generation #')
plt.legend(loc='best')
plt.savefig('utility_evolution.pdf')

# Attacker level evolution
plt.figure(4) 
for i in range(0, attacker_data_level.shape[1]):
    gens = range(1, generations+1) 
    plt.plot(gens, attacker_data_level[:, i], marker='o',
            markevery=markfreq,
            linewidth=linewidth,
                label='Level '+str(i+1))
plt.ylabel('Attack rate')
plt.xlabel('Generation #')
plt.legend(loc='upper right')
plt.savefig('attack_rate_level_evolution.pdf')

# Attacker type evolution
plt.figure(5) 
for i in range(0, attacker_data_type.shape[1]):
    gens = range(1, generations+1) 
    plt.plot(gens, attacker_data_type[:, i], marker='o',
            markevery=markfreq,
            linewidth=linewidth,
                label='Type '+type_names[i])
plt.ylabel('Attack rate')
plt.xlabel('Generation #')
plt.legend(loc='upper right')
plt.savefig('attack_rate_type_evolution.pdf')

# Defender level evolution
plt.figure(6) 
for i in range(0, defender_data_level.shape[1]):
    gens = range(1, generations+1) 
    plt.plot(gens, defender_data_level[:, i], marker='o',
            markevery=markfreq,
            linewidth=linewidth,
                label='Level '+str(i+1))
plt.ylabel('Defence rate')
plt.xlabel('Generation #')
plt.legend(loc='upper right')
plt.savefig('defence_rate_level_evolution.pdf')

# Defender type evolution
plt.figure(7) 
for i in range(0, defender_data_type.shape[1]):
    gens = range(1, generations+1) 
    plt.plot(gens, defender_data_type[:, i], marker='o',
            markevery=markfreq,
            linewidth=linewidth,
            label='Type: '+type_names[i])
plt.ylabel('Defence rate')
plt.xlabel('Generation #')
plt.legend(loc='upper right')
plt.savefig('defence_rate_type_evolution.pdf')

plt.show()
