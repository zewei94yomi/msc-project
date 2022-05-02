from commons.auto_str import auto_str
from dispatchCenter.center import Center


@auto_str
class Plotter:
    def __init__(self, center: Center):
        self.center = center
    
    def plot_map(self):
        pass
    
    def plot_drones(self):
        pass
        
    def plot_orders(self):
        pass
    
    def plot_hubs(self):
        pass
    
    def plot_population_density(self):
        pass
    
    def plot_noise_distribution(self):
        pass
