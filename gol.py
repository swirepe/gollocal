# Peter Swire
# Ugly code that learns the game of life


from EchoStateCell import Cell



class Board():
    
    def run(self, pre_generations, post_generations):      
        for i in xrange(pre_generations):
            self.prep_all()
            self.update_all_weights()

            gen_error = self.abs_board_error()
            print "Generation " + str(i)
            print "Generation error: " + str(gen_error)
            print "Average Per-Cell error: " + str(1.0 * gen_error / (self.width*self.height))
            self.correct_all()
    
    
    
    
    def update_all_weights(self):
        for h in range(self.height):
            for w in range(self.width):
                self.cells[h][w].update_weights()
                
                
    def abs_board_error(self):
        total = 0
        for h in range(self.height):
            for w in range(self.width):
                total += self.cells[h][w].abs_error()
                
        return total
    
    
    def prep_all(self):
        for h in range(self.height):
            for w in range(self.width):
                self.cells[h][w].prep_change()     
    

    def correct_all(self):
        for h in range(self.height):
            for w in range(self.width):
                self.cells[h][w].commit_to_correct() 


    def commit_all(self):
        for h in range(self.height):
            for w in range(self.width):
                self.cells[h][w].commit_change()      
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[None] * width] * height
        
        
        for h in range(height):
            for w in range(width):
                self.cells[h][w] = Cell()
        
        
        for h in range(height):
            for w in range(width):
                neighbors = []
                
                # Basically add the moore neighborhood as much as you can
                # and don't complain when you walk off the end of your matrix
                try:
                    neighbors.append(self.cells[h-1][w]   )
                except:
                    pass
                try:
                    neighbors.append(self.cells[h-1][w-1] )
                except:
                    pass
                try:
                    neighbors.append(self.cells[h-1][w+1] )
                except:
                    pass
                try:
                    neighbors.append(self.cells[h][w-1]   )
                except:
                    pass
                try:
                    neighbors.append(self.cells[h][w+1]   )
                except:
                    pass
                try:
                    neighbors.append(self.cells[h+1][w]   )
                except:
                    pass
                try:
                    neighbors.append(self.cells[h+1][w-1] )
                except:
                    pass
                try:
                    neighbors.append(self.cells[h+1][w+1] )
                except:
                    pass
                
                    
                self.cells[h][w].set_neighbors(neighbors)
                
if __name__ == "__main__":
    b = Board(100,100)
    b.run(100, 100)
    
    
    
    
    
# http://mihaiv.wordpress.com/2010/02/08/backpropagation-algorithm/
