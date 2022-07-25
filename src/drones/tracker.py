from commons.decorators import auto_str


@auto_str
class Tracker:
    """A drone tracker tracks the number of step and distance of each order spent by a drone"""
    def __init__(self):
        self.step = 0
        self.distance = 0
        self.end_step = []
        self.end_distance = []
        
    def total_orders(self):
        return len(self.end_step)
        
    def increment_step(self):
        self.step += 1
        
    def reset_step(self):
        self.step = 0
        
    def total_step(self):
        return sum(self.end_step)
    
    def num_step(self):
        return len(self.end_step)
    
    def increment_distance(self, distance):
        self.distance += distance
        
    def reset_distance(self):
        self.distance = 0
        
    def total_distance(self):
        return sum(self.end_distance)
    
    def num_distance(self):
        return len(self.end_distance)
    
    def record(self):
        self.end_step.append(self.step)
        self.end_distance.append(self.distance)
        self.reset_step()
        self.reset_distance()
