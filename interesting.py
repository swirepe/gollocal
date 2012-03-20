from itertools import combinations
from math import sqrt

#todo: spawn a thread/process for each rule, run more than 1 rule

logfile = open("C:\\Users\\swirepe\\Documents\\interesting.txt", "w")

NUM_GENERATIONS = 500
WIDTH = 4
HEIGHT = 4

def run_all():
    logfile.write("rule,"                      )
    logfile.write("abs_growth,"                )
    logfile.write("average_size,"              )
    logfile.write("avg_distance_travelled,"    )
    logfile.write("max_distance_travelled,"    )
    logfile.write("avg_repetition,"            )
    logfile.write("time_to_death,"              )
    logfile.write("board_number\n"             )
    
    for rule in all_rules():
        board_number = 0
        for cell_combo in all_cell_combinations(WIDTH, HEIGHT):
            board_number += 1
            prev_gen = cell_combo
            curr_gen = None
            gen_number = 0
            size = 1.0 * len(prev_gen)
            repetition = 0.0
            distances = []
            # run until you hit the ceiling or die out
            for gen_number in range(NUM_GENERATIONS):
                curr_gen = next_generation(prev_gen, rule)
                
                # gather some stats
                size += len(curr_gen)
                repetition += len ( prev_gen.intersection(curr_gen))
                distances.append(distance_travelled(curr_gen))
                
                # stop if you have to
                if len(curr_gen) == 0:
                    break
            
            size /= (gen_number + 1)
            repetition /= (gen_number + 1)
            avg_distance = sum(distances) / (gen_number + 1)
            max_distance = max(distances)
            growth = absolute_growth(cell_combo, curr_gen)
            
            
            
            logfile.write(str(rule) + ",")
            logfile.write(str(growth) + ",")
            logfile.write(str(size) + ",")
            logfile.write(str(avg_distance) + ",")
            logfile.write(str(max_distance) + ",")
            logfile.write(str(repetition) + ",")
            logfile.write(str(gen_number) + ",")
            logfile.write(str(board_number) + "\n")
    

class Rule():
    def __init__(self, born, alive):
        self.born = set(born)    # what it takes to be born
        self.alive = set(alive)  # what it takes to stay alive


    def _compress(self, c):
        return "".join(map(str,c))
            
    def __str__(self):
        return "B" + self._compress(self.born) + "/S" + self._compress(self.alive) 


def all_cell_combinations(width, height):
    """ generates every possible combination of cells on
    within the box at 0,0 as designated by width and height"""
    cells = [ (x,y) for x in range(width) for y in range(height)]
    
    for i in range(1, len(cells) + 1):
        cell_comb = combinations(cells, i)
        for x in cell_comb:
            yield set(x)



def all_rules():
    """ generate rules for every possible value of "get born" and "stay alive" """
    for i in range(1, 8+1):
        for j in range(1, 8+1):
            comb_born = combinations( range(0,9), i)
            comb_alive = combinations( range(0,9), j)
            for born in comb_born:
                for alive in comb_alive:
                    yield Rule(born, alive)



def get_neighbors(cell):
    """Returns the cells in the moore neighborhood of a cell, along
    with the cell passed in"""
    x = 0
    y = 1
    xs = [cell[x]+1, cell[x]-1, cell[x]] 
    ys = [cell[y]+1, cell[y]-1, cell[y]]
    return [(x,y) for x in xs for y in ys]


def next_generation(prev_gen, rule):
    """progress from on generation to the next using a rule"""
    next_gen = set()
    for cell in prev_gen:
        # we have to look at the neighbors of 
        # each cell in the previous generation,
        # because those are the ones that can change in this one
        neighbors = get_neighbors(cell)
        
        
        for test in neighbors:
            # the born stage
            alive_neighbors = len( prev_gen.intersection( get_neighbors(test)))
            if alive_neighbors in rule.born:
                next_gen.add(test)
        
            # the stay alive stage
            if test in prev_gen and alive_neighbors in rule.alive:
                next_gen.add(test)
                
    return next_gen
    

#### metrics
def distance_travelled(last_gen):
    if len(last_gen) == 0:
        return 0.0
    distances = map( lambda (x, y): sqrt(x**2 + y**2), last_gen)
    return 1.0 * max(distances)


def absolute_growth(first_gen, last_gen):
    return 1.0 * len(last_gen) / len(first_gen)
    



if __name__ == "__main__":
    run_all()
    pass
