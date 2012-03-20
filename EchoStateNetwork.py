
from random import gauss, random, randint, choice

LEARNING_RATE = 0.05

# realistically, reservoir is doing all the work/
# that could be made the entire esn

class EchoStateNetwork():
    def __init__(self, reservoir_size, connectivity, input_len, rear_len=10):
        self.res_size = reservoir_size
        self.conn = connectivity
        self.rear_len = rear_len
        self.res = Reservoir(reservoir_size, connectivity, input_len, rear_len)
        
    
    def activate(self):
        self.res.activate()
    
    def get_rear_states(self):
        return self.res.rear_states
     
    def update_weights(self, rear_deltas):
        self.res.update_weights(rear_deltas)
     
     
    def set_forward_states(self, f):
        self.res.forward_states = f
        
     
class Reservoir():
    def __init__(self, internal_size, connectivity, forward_layer=8, rear_layer=10):
        self.size = internal_size
        self.connectivity = connectivity
        self.node_connections = {}
        self.node_states = [choice([True, False]) for _ in range(internal_size)]
        
        
        self.fsize = forward_layer
        self.rsize = rear_layer
        self.forward_states = [choice([True, False]) for _ in range(forward_layer)]
        self.rear_states = [choice([True, False]) for _ in range(rear_layer)]
        self.internal_rear_connections = {}
        
        
        self.initial_connect()
        self.neural_fn = self.logsig
        self.neural_thresh = 0.5
        
   
    def neural_fn_deriv(self, x):
       epsilon = 0.00001
       fx = self.neural_fn(x)
       fxe = self.neural_fn(x + epsilon)
       fxne = self.neural_fn(x - epsilon)
       
       pos_deriv = (fx + fxe) / (2*x + epsilon) 
       neg_deriv = (fx + fxne)/ (2*x - epsilon)
       return (pos_deriv + neg_deriv) / 2.0
       
   
    def logsig(self, x):
        if x <= -50:
            return 0.0001
        if x >= 50:
            return 0.9999
        return 1.0 / (1 + (2.718281828**(-1*x)))
        
        
    def initial_connect(self):
        """Connect each node to each other node with some probability.
        We'll interpret A -> [(B, .2), (C, -.1), (D, 0.1)] as
        "A takes into account b, c, and d when activating,
        using their respective weights"
        """
        # connect the internal nodes together
        # randomly connect nodes to other nodes (with some probability)
        # for connections between the forward and the internal, the forward 
        # will be address as the numbers past the size of the reservoir
        for i in range(self.size):
            self.node_connections[i] = [(x, gauss(0.0, 0.3) ) for x in range(self.size + self.fsize -1 ) if random() < self.connectivity]
        
        
        # initialize the connections between the internal nodes and the rear layer
        # stipulation: every rear node has to have at least one connection
        # node: these are lists instead of tuples, because these weights will be updated
        for i in range(self.rsize):
            self.internal_rear_connections[i] = [ [x, gauss(0.0, 0.3)] for x in range(self.size) if random() < self.connectivity]
            if self.internal_rear_connections[i] == []:
                self.internal_rear_connections[i] = [[randint(0, self.size-1), gauss(0.0, 0.3)]]
        
        
        # TODO: prune out the ones that have nothing connected
        # to them and aren't connected to anything

    def set_forward_states(self, states):
        self.forward_states = states


    def update_weights(self, rear_deltas):
        
        for r in range(len(rear_deltas)):
            rear_deltas[r] *= self.neural_fn_deriv(self.rear_states[r])
        
        for r in range(self.rsize):
            for connection in self.internal_rear_connections[r]:
                connection[1] += self.node_states[connection[0]] * rear_deltas[r] * LEARNING_RATE
                


    def activate(self):
        """Activate the internal and the rear nodes
        Be sure to set the forward nodes before you run this."""
        to_state = self.node_states[:]  # a copy
        
        # activate the internal nodes
        for i in range(self.size):
            if self.node_connections.has_key(i):
                total = 0.0
                for key, weight in self.node_connections[i]:
                    # nodes outside of the size of the internal are the forewardnodes
                    if key >= self.size:
                        total += self.forward_states[key - self.size] * weight
                    else:
                        total += self.node_states[key] * weight
                        
                total = self.neural_fn(total)
                to_state[i] = (total > self.neural_thresh)
                
        self.node_states = to_state[:]
        
        
        # activate the rear nodes
        to_state = self.rear_states[:]
        for i in range(self.rsize):
            total = 0.0
            for key, weight in self.internal_rear_connections[i]:
                total += self.node_states[key] * weight
            total = self.neural_fn(total)
            to_state[i] = (total > self.neural_thresh)
            
        self.rear_states = to_state[:]
            
                
                
                
                
