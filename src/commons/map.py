from commons.coordinate import Coordinate
from commons.auto_str import auto_str
import random


@auto_str
class Map:
    """ The map of drones food delivery """
    
    def __init__(self, topLeft: Coordinate, topRight: Coordinate, bottomLeft: Coordinate, bottomRight: Coordinate,
                 population_density=None):
        # Boundary of the map
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        # Population density of the whole map
        self.population_density = population_density
        # TODO: Grids
    
    def generate_random_coord(self):
        """
        Generate a random coordinate on the given map
        :return: a random Coordinate instance
        """
        longitude = self.bottomLeft.longitude \
                    + random.random() * (self.bottomRight.longitude - self.bottomLeft.longitude)
        latitude = self.bottomLeft.latitude \
                   + random.random() * (self.topLeft.latitude - self.bottomLeft.latitude)
        return Coordinate(longitude=longitude, latitude=latitude)
    

if __name__ == '__main__':
    map = Map(Coordinate(0, 100), Coordinate(100, 100), Coordinate(0, 0), Coordinate(100, 0))
    print(map)
