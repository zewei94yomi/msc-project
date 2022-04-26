from commons.coordinate import Coordinate
from commons.map import Map
from orders.order import Order


class Generator:
    """
    Order Generator
    """
    
    def __init__(self, map: Map):
        self.map = map
    
    def generate_order(self, use_density=False):
        """
        Generate an orders on the given map
        
        :return: a Order instance
        """
        if use_density is False:
            start = self.map.generate_random_coord()
            end = self.map.generate_random_coord()
            return Order(start=start, end=end)
        else:
            # TODO: generate orders using population density (end location)
            pass
        
    def __str__(self):
        return f"Generator(map={self.map})"


if __name__ == '__main__':
    map = Map(Coordinate(0, 100), Coordinate(100, 100), Coordinate(0, 0), Coordinate(100, 0))
    
    g = Generator(map)
    orders = []
    for i in range(10):
        orders.append(g.generate_order())
    for order in orders:
        print(order)
