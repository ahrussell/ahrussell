import collections, random

class State(collections.defaultdict):
 
    def __init__(self, dict=None):
        collections.defaultdict.__init__(self, int)
        
        if dict != None:
            for side, weight in dict.iteritems():
                self[side] = weight
 
    def add_side(self, side):
        self[side] += 1
        
        return self
        
    def set_side(self, side, weight):
        self[side] = weight
        
        return self
 
    def total_sides(self):
        return sum(self.values())
 
    def roll(self):
        random_num = random.randint(0, self.total_sides())
        total_pos = 0
        for side, qty in self.items():
            total_pos += qty
            if random_num <= total_pos:
                return side

class MarkovChain(collections.defaultdict):
    def __init__(self):
        collections.defaultdict.__init__(self, State)
        
        self.state = None
    
    def set_state(self, name, state):
        self[name] = state
    
    def set_current_state(self, name):
        self.state = name
        
        return name
    
    def next(self):
        if self.state == None:
            raise ValueError("No current state set")
        else:
            next_state = self[self.state].roll()
            
            return next_state
        