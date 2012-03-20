from random import gauss, random, choice

LEARNING_RATE = 0.05

class Cell():
    def __init__(self, num_hidden_states = 12, neighbors = [], state = None):
        if neighbors != []:
            self.set_neighbors(neighbors)
        
        self.hidden_states = [False] * num_hidden_states
        self.num_hidden = num_hidden_states
        
        if state == None:
            self.state = choice([True, False])

        else:
            self.state = state
        
    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
        self.neighbor_hidden_weights = [random() for _ in range(len(neighbors) * self.num_hidden)] # neighbors x visible
        self.hidden_visible_weights = [random() for _ in self.hidden_states] # only one visible node (output state node)


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
        
        # activate the hidden from the neighbors
        for h in range(self.num_hidden):
            total = 0
            for n in range(len(self.neighbors)):
                total += self.neighbor_hidden_weights[ (len(self.neighbors) * h) + n] * self.neighbors[n].state
            total = self.logsig(total)
            self.hidden_states[h] = (total > 0.5)
        
        
        # choose the next state from the hidden states
        total = 0
        for i in range(len(self.hidden_visible_weights)):
            total += self.hidden_visible_weights[i] * self.hidden_states[i]
        total = self.logsig(total)
        self.next_state = (total > 0.5)
        
        
    def commit_change(self):
        self.state = self.next_state


    def commit_to_correct(self):
        self.state = self.should_state


    def get_correct_next_state(self):
        """
        total_on = sum( [ x.state for x in self.neighbors ] )
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
            
            hidden_deltas = [0.0] * self.num_hidden
            # update the weights between the visible node and the hidden layer           
            for h in range(self.num_hidden):
                hidden_deltas[h] = output_delta * self.hidden_visible_weights[h] * self.logsig_deriv(self.hidden_states[h])
                self.hidden_visible_weights[h] += output_delta * self.hidden_states[h] *LEARNING_RATE
        
            # update the weights between the hidden layer and the neighbor layer
            for h in range(self.num_hidden):
                for n in range(len(self.neighbors)):
                    array_pos = (len(self.neighbors) * h) + n
                    self.neighbor_hidden_weights[ array_pos ] += self.neighbors[n].state * hidden_deltas[h] * LEARNING_RATE


    def abs_error(self):
        return abs( self.should_state - self.next_state )


