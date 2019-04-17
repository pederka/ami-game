import numpy as np
import sys

class Population:
    ''' Class for a population of attackers and defender in a given game '''

    def __init__(self, game, attacker_distribution, defender_distribution,
                    replicator='REQN', k=0.2, dt=0.1, delta = 0.1):
        ''' Constructor for the Population class

        Arguments:

        game: a Game object
        attacker_distribution: normalized numpy array of size 
                               <number of strategies> giving the attacker 
                               population distribution 
        defender_distribution: normalized numpy array of size 
                               <number of strategies> giving the defender
                               population distribution 
        replicator: the type of replicator dynamic to use. 
        k: (only applies to truncation replicator) the fraction of the
           population to truncate
        dt: (only applies to the REQN replicator) the time step between 
            generations in the 
        delta: (only applies to the REQN replicator) parameter scaling the 
               random noise introduced between each generation

        '''
        self.game = game
        self.replicator = replicator
        self.k = k
        self.dt = dt
        self.attacker_population = attacker_distribution
        self.defender_population = defender_distribution
        self.delta = delta/attacker_distribution.shape[0]
        self.attacker_strategies = game.attacker_strategies()
        self.defender_strategies = game.defender_strategies()

    def calculate_utilities(self):
        ''' Calculates average utilities for both attackers and defenders '''
        self.average_utility_attacker = self.average_payoff_attacker()
        self.average_utility_defender = self.average_payoff_defender()

    def replicate(self):
        ''' Updates the attacker and defender populations using a method 
        given in the class variable replicator '''
        self.calculate_utilities()
        if self.replicator == 'REQN':
            # Calculate attacker population change
            dp_s = np.zeros(len(self.attacker_population))
            for si, attacker in enumerate(self.attacker_population):
                dp_s[si] = attacker*(self.expected_payoff_attacker(\
                        self.attacker_strategies[si, :]) \
                        - self.average_utility_attacker)

            # Calculate defender population change
            dp_t = np.zeros(len(self.defender_population))
            for ti, defender in enumerate(self.defender_population):
                dp_t[ti] = defender*(self.expected_payoff_defender(\
                        self.defender_strategies[ti, :]) \
                        - self.average_utility_defender)

            # Update population
            self.attacker_population = self.attacker_population + self.dt*dp_s
            self.defender_population = self.defender_population + self.dt*dp_t

            # Add random fluctuation
            N_A = self.attacker_population.shape[0]
            N_D = self.defender_population.shape[0]
            self.attacker_population += self.delta*np.random.rand(N_A)/N_A
            self.defender_population += self.delta*np.random.rand(N_D)/N_D

            # Remove any negative populations
            self.attacker_population[self.attacker_population < 0] = 0
            self.defender_population[self.defender_population < 0] = 0

            # Normalization step
            self.attacker_population = self.attacker_population\
                    /np.sum(self.attacker_population)
            self.defender_population = self.defender_population\
                    /np.sum(self.defender_population)

        elif self.replicator == 'truncation':
            
            # Extract subset of strategies with non-zero population
            attackers_nonzero = np.nonzero(self.attacker_population)[0]
            s_nonzero = list([self.attacker_strategies[i, :] for i in 
                    attackers_nonzero])
            defenders_nonzero = np.nonzero(self.defender_population)[0]
            t_nonzero = list([self.defender_strategies[i, :] for i in
                    defenders_nonzero])
            attacker_population_nonzero = \
                    self.attacker_population[attackers_nonzero]
            defender_population_nonzero = \
                    self.defender_population[defenders_nonzero]

            # Calculate utilities for every strategy (of non-zero population)
            utilities_attacker = np.zeros(len(s_nonzero))
            utilities_defender = np.zeros(len(t_nonzero))
            for si, s in enumerate(s_nonzero):
                utilities_attacker[si] = self.expected_payoff_attacker(s)

            for ti, t in enumerate(t_nonzero):
                utilities_defender[ti] = self.expected_payoff_defender(t)

            # Sort by utility
            sorted_attackers = np.argsort(utilities_attacker)
            sorted_defenders = np.argsort(utilities_defender)

            # Move population for lowest k percent to highest k percent
            for ik in range(0, int(self.k*sorted_attackers.size)):
                attacker_population_nonzero[sorted_attackers[ik]] += \
                        attacker_population_nonzero[sorted_attackers[-ik-1]]
                attacker_population_nonzero[sorted_attackers[-ik-1]] = 0.0
            for ik in range(0, int(self.k*sorted_defenders.size)):
                defender_population_nonzero[sorted_defenders[ik]] += \
                        defender_population_nonzero[sorted_defenders[-ik-1]]
                defender_population_nonzero[sorted_defenders[-ik-1]] = 0.0

            # Update full population
            self.attacker_population[attackers_nonzero] = \
                                    attacker_population_nonzero
            self.defender_population[defenders_nonzero] = \
                                    defender_population_nonzero

    def expected_payoff_attacker(self, attacker_strategy):
        ''' Calculates the expected payoff associated with a given attacker
        strategy

        Arguments:

        attacker_strategy: numpy array of size <number of nodes in tree>
                           giving an attacker strategy

        Returns:

        expected_payoff
        '''
        expected_payoff = np.inner(self.game.attacker_utility(attacker_strategy,
                               self.defender_strategies),
                                       self.defender_population)
        return expected_payoff
    
    def expected_payoff_defender(self, defender_strategy):
        ''' Calculates the expected payoff associated with a given defender
        strategy

        Arguments:

        defender_strategy: numpy array of size <number of nodes in tree>
                           giving an defender strategy

        Returns:

        expected_payoff
        '''
        expected_payoff = np.inner(self.game.defender_utility(\
                    self.attacker_strategies,
                    defender_strategy),self.attacker_population)
        return expected_payoff
    
    def average_payoff_attacker(self):
        ''' Calculates the average payoff of an attacker given the current
        attacker and defender populations '''
        average_payoff = 0.0
        for ia in range(0, self.attacker_strategies.shape[0]):
            average_payoff += self.expected_payoff_attacker( \
                    self.attacker_strategies[ia, :]) \
                    *self.attacker_population[ia]
        return average_payoff

    def average_payoff_defender(self):  
        ''' Calculates the average payoff of a defender given the current
        attacker and defender populations '''
        average_payoff = 0.0
        for di in range(0, self.defender_strategies.shape[0]):
            average_payoff += self.expected_payoff_defender( \
                    self.defender_strategies[di, :]) \
                    *self.defender_population[di]
        return average_payoff

    def get_attack_profiles(self):
        ''' Returns the attack profiles given the current attacker and defender
        populations, i.e. a numpy array of size <number of nodes in tree>
        giving to what degree the different nodes are attacked '''
        return np.dot(self.attacker_population, self.attacker_strategies)

    def get_defence_profiles(self):
        ''' Returns the defence profiles given the current attacker and defender
        populations, i.e. a numpy array of size <number of nodes in tree>
        giving to what degree the different nodes are defended '''
        return np.dot(self.defender_population, self.defender_strategies)

    def get_average_attacker_utility(self):
        ''' Returns the average attacker utility that was last calculated '''
        return self.average_utility_attacker
   
    def get_average_defender_utility(self):
        ''' Returns the average defender utility that was last calculated '''
        return self.average_utility_defender

