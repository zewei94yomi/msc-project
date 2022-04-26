from commons.coordinate import Coordinate
import random


class Map:
    """ The map of drone food delivery """
    
    def __init__(self, topLeft: Coordinate, topRight: Coordinate, bottomLeft: Coordinate, bottomRight: Coordinate,
                 population_density=None):
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        self.population_density = population_density
    
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
    
    def __str__(self):
        return f"Map(TL={self.topLeft}, TR={self.topRight}, BL={self.bottomLeft}, BR={self.bottomRight}, " \
               f"population_density={self.population_density})"


if __name__ == '__main__':
    map = Map(Coordinate(0, 100), Coordinate(100, 100), Coordinate(0, 0), Coordinate(100, 0))
    print(map)
