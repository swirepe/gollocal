from random import gauss, random, choice

from EchoStateNetwork import *

LEARNING_RATE = 0.05

class Cell():
    def __init__(self, res_size = 50, connectivity = 0.05, state = None):
        self.res_size = res_size
        self.connectivity = connectivity
        
        # we'll hold off on actually making the esn until we get our neighbors
        if state == None:
            self.state = choice([True, False])

        else:
            self.state = state
            
        
    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
        self.input_len = len(neighbors)
        self.esn = EchoStateNetwork(self.res_size, self.connectivity, self.input_len)
        self.output_rear_weights = [random() for _ in range(self.esn.rear_len)]  # only one visible node (output state node)


    # ----- for learning  ------
    def logsig(self, x):
        if x <= -50:
            return 0.0001
        if x >= 50:
            return 0.9999
        return 1.0 / (1 + (2.718281828**(-1*x)))


    def logsig_deriv(self, x):
        v = self.logsig(x)
        return v*(1-v)

    def prep_change(self):
        """ Predict the next state for this cell
        """
        
        # activate the esn from the neighbors
        self.esn.set_forward_states([ x.state for x in self.neighbors])
        self.esn.activate()
        
        # choose the next state from the rear of our esn
        total = 0.0
        rear_states = self.esn.get_rear_states()
        for i in range(self.esn.rear_len):
            total += self.output_rear_weights[i] * rear_states[i]
        total = self.logsig(total)
        self.next_state = (total > 0.5)
        
        
    def commit_change(self):
        self.state = self.next_state


    def commit_to_correct(self):
        self.state = self.should_state


    def get_correct_next_state(self):
        """total_on = sum( [ x.state for x in self.neighbors ] )
        if total_on < 2:
            self.should_state = False
        elif total_on > 3:
            self.should_state = False
        elif total_on == 2 and self.state == False:
            self.should_state = False
        else:
            self.should_state = True"""
            
        # pick minority class
        total_on = sum( [ x.state for x in self.neighbors ] )
        if 1.0 * total_on / len(self.neighbors) <= 0.5:
            self.should_state = True
        else:
            self.should_state = False
            
            
    def update_weights(self):
        """Not used in this version.  We are updating parameters instead"""
        self.get_correct_next_state()
        
        # if we are right, we don't have to do anything
        if self.should_state == self.next_state:
            return
        else:
            output_delta = (self.should_state - self.next_state) * self.logsig_deriv(self.next_state)
            
            rear_deltas = [0.0] * self.esn.rear_len
            rear_states = self.esn.get_rear_states()
            # update the weights between the visible node and the rear layer           
            for r in range(self.esn.rear_len):
                rear_deltas[r] = output_delta * self.output_rear_weights[r]
                self.output_rear_weights[r] += output_delta * rear_states[r] *LEARNING_RATE
        
            self.esn.update_weights(rear_deltas)


    def abs_error(self):
        return abs( self.should_state - self.next_state )


