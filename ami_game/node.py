class Node(object):
    '''Class for a node in an tree.'''

    def __init__(self, children=None, cost_attack=1.0,
            cost_defence=1.0, value=3.0):
        ''' Constructor for the Node class

        Arguments:

        children: list of children nodes
        cost_attack: the cost of attacking the node, C_A
        cost_defence: the cost of defending a node, C_D
        value: the value of the node, v
        '''
        self.value = value
        self.cost_attack = cost_attack
        self.cost_defence = cost_defence
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
        
    def add_child(self, node):
        ''' Adds a node to the list of children '''
        assert isinstance(node, Node)
        self.children.append(node)

    def validate(self, a):
        ''' Raises error if the parameters of the node break constraints of
        the game 
        
        Arguments:

        a: the detection rate of the game
        '''
        if self.cost_attack > self.value*(1-a):
            raise ValueError('Attacking an undefended node must pay off')
        if self.cost_defence > self.value*(1-a):
            raise ValueError('Defending a fully attacked node must pay off')
