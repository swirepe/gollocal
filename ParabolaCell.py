from random import gauss, random, choice

LEARNING_RATE = 0.01

class Cell():
    def __init__(self, neighbors = [], state = None):
        self.set_neighbors(neighbors)
        
        if state == None:
            self.state = choice([True, False])
        else:
            self.state = state
        
    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
        self.weights = [gauss(0, 0.1) for _ in neighbors]
        


    # ----- for learning  ------
    def logsig(self, x):
        return 1.0 / (1 + (2.718281828**(-1*x)))


    def parabola(self, x):
        return -0.1 * (x-3)**2 + 0.7

    def prep_change(self):
        """ Predict the next state for this cell using the weights of the neighbors
        and the activation function
        
        Here, the activation function is a parabola"""
        total = 0
        for i in range(len(self.neighbors)):
            total += self.neighbors[i].state * self.weights[i]

        total = self.parabola(total)
        self.next_state = (total > 0.5)
        
        
    def commit_change(self):
        self.state = self.next_state


    def get_correct_next_state(self):
        total_on = sum( [ x.state for x in self.neighbors ] )
        if total_on < 2:
            self.should_state = False
        elif total_on > 3:
            self.should_state = False
        elif total_on == 2 and self.state == False:
            self.should_state = False
        else:
            self.should_state = True
            
            
    def update_weights(self):
        # if we are right, we don't have to do anything
        self.get_correct_next_state()
        
        if self.should_state == self.next_state:
            return
        else:
            correct_direction = self.should_state - self.next_state
            for i in range(len(self.neighbors)):
                self.weights[i] += self.neighbors[i].state * (correct_direction*LEARNING_RATE)
        
    def abs_error(self):
        return abs( self.should_state - self.next_state )


