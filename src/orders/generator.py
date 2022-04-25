from commons.coordinate import Coordinate
from orders.order import Order
import random


class Generator:
    """
    Order Generator
    """
    
    def __init__(self, area: list, population_density=None):
        self.topLeft = area[0]
        self.topRight = area[1]
        self.bottomLeft = area[2]
        self.bottomRight = area[3]
        self.population_density = population_density
        self.use_density = population_density is not None
    
    def generate_random_order(self):
        """
        Generate an orders on the map, orders are randomly distributed
        :return: a random Order instance
        """
        start = self.generate_random_coord()
        end = self.generate_random_coord()
        return Order(start=start, end=end)
        
    def generate_random_coord(self):
        """
        Generate a random coordinate on the map
        :return: a random Coordinate instance
        """
        longitude = self.bottomLeft.longitude \
                    + random.random() * (self.bottomRight.longitude - self.bottomLeft.longitude)
        latitude = self.bottomLeft.latitude \
                   + random.random() * (self.topLeft.latitude - self.bottomLeft.latitude)
        return Coordinate(longitude=longitude, latitude=latitude)
    
    def __str__(self):
        return f"Generator: " \
               f"topLeft={self.topLeft}, topRight={self.topRight}, " \
               f"bottomLeft={self.bottomLeft}, bottomRight={self.bottomRight}" \
               f"use_density={self.use_density}"


if __name__ == '__main__':
    area = list()
    area.append(Coordinate(0, 100))
    area.append(Coordinate(100, 100))
    area.append(Coordinate(0, 0))
    area.append(Coordinate(100, 0))
    
    g = Generator(area)
    orders = []
    for i in range(10):
        orders.append(g.generate_random_order())
    for order in orders:
        print(order)
