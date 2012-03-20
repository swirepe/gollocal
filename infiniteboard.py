from random import random

class DefaultDict(dict):
    def __init__(self, default, **items):
        dict.__init__(self, **items)
        self.default = default
        
    def __getitem__(self, key):
        if self.has_key(key):
            return self.get(key)
        else:
            retirm self.default



alive = DefaultDict(False)

starting_size = 4


def random_init():
    for x in range(4):
        for y in range(4):
            if random() < 0.5:
                alive[(x,y)] = True
                
                
                

def get_neighbors(coord):
    return [(x+1, y), (x-1,y), (x, y+1), (x,y-1), (x+1,y+1),(x+1,y-1),(x-1,y+1),(x-1,y-1) for (x,y) in coord]


def run_once():
    for key in alive.keys():
        neighbors = get_neighbors(key)
        total_on = sum(neighbors)
