import numpy as np
import itertools

def multichoose(n,k):
    ''' Returns all possible permitations of n number which sum is below or
    equal to k '''
    if k < 0 or n < 0: return "Error"
    if not k: return [[0]*n]
    if not n: return []
    if n == 1: return [[k]]
    return [[0]+val for val in multichoose(n-1,k)] + \
        [[val[0]+1]+val[1:] for val in multichoose(n,k-1)]

class ConfidentialityGame():
    ''' Class for the confidentiality game '''
    attack_strategies = None
    defend_strategies = None

    def __init__(self, tree, K=5, a=0.3, attacker_budget=1.0,
                        defender_budget=1.5):
        ''' Constructor for the confidentiality game.

        Arguments:

        tree: list of Nodes defining the tree structure of the game
        K: resulution of the strategy space (integer > 1)
        a: the detection rate
        attacker_budget: the budget of the attacker population
        defender_budget: the budget of the defender population
        '''
        self.K = K
        self.a = a
        self.attacker_budget = attacker_budget
        self.defender_budget = defender_budget
        self.N = len(tree)
        self.tree = tree
        print('Initializing game')
        print('# \t v_i \t C_A \t C_D \t s^* \t t^*')
        for ni, node in enumerate(self.tree):
            value = node.value
            s_star = node.cost_defence/value/(1-self.a)
            t_star = 1.0-node.cost_attack/value/(1-self.a)
            print('{0:3d} \t {1:0.2f} \t {2:0.2f} \t {3:0.2f} ' \
                    '\t {4:0.2f} \t {5:0.2f}'.format(tree.index(node), value, 
                            node.cost_attack,
                        node.cost_defence, s_star, t_star))

    def attacker_strategies(self):
        ''' Returns all possible attacker strategies as a numpy array of
        dimensions <number of strategies> x <number of nodes in tree> '''
        if self.attack_strategies is None:
            budget = int(self.K*self.attacker_budget)
            self.attack_strategies = np.asarray(
                    multichoose(self.N, budget))/float(self.K)
        return self.attack_strategies

    def defender_strategies(self):
        ''' Returns all possible defender strategies as a numpy array of
        dimensions <number of strategies> x <number of nodes in tree> '''
        if self.defend_strategies is None:
            budget = int(self.K*self.defender_budget)
            self.defend_strategies = np.asarray(
                        multichoose(self.N, budget))/float(self.K)
        return self.defend_strategies

    def attacker_utility(self, attack_strategy, defence_strategies):
        ''' Returns the utility of a given attack strategy for each of a list
        of given defence strategies

        Arguments:
        
        attack_strategy: numpy array of size <number of nodes in tree> giving
                         a specified attack strategy
        defence_strategies: numpy array of size <number of strategies> x
                            <number of nodes in tree>
        
        Returns:

        utility: numpy array of attacker utilities of size <number of
                 strategies>

        '''
        utility = np.zeros(defence_strategies.shape[0])
        for ni, node in enumerate(self.tree):
            children_utility = np.zeros(defence_strategies.shape[0])
            for childnode in node.children:
                children_utility += childnode.value\
                        *attack_strategy[ni]\
                        *(1-self.a)*(1-defence_strategies[:,
                            self.tree.index(childnode)])
            utility += node.value*attack_strategy[ni]*(1-self.a)\
                    *(1.0-defence_strategies[:, ni]) \
                    - attack_strategy[ni]*node.cost_attack \
                    + children_utility
        return utility

    def defender_utility(self, attack_strategies, defence_strategy):
        ''' Returns the utility of a given defence strategy for each of a list
        of given attack strategies

        Arguments:
        
        attack_strategies: numpy array of size <number of strategies> x
                            <number of nodes in tree>
        defence_strategy: numpy array of size <number of nodes in tree> giving
                         a specified defence strategy

        Returns:

        utility: numpy array of attacker utilities of size <number of
                 strategies>

        '''
        utility = np.zeros(attack_strategies.shape[0])
        for ni, node in enumerate(self.tree):
            children_utility = np.zeros(attack_strategies.shape[0])
            for childnode in node.children:
                children_utility += childnode.value\
                        *attack_strategies[:, ni]\
                        *(1-self.a)*(1-defence_strategy[
                            self.tree.index(childnode)])
            utility += - node.value*attack_strategies[:, ni]*(1-self.a)\
                    *(1.0-defence_strategy[ni]) \
                    - defence_strategy[ni]*node.cost_defence \
                    - children_utility
        return utility
