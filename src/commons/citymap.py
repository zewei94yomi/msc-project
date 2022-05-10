import math
import random
from commons.auto_str import auto_str


# @auto_str
class Coordinate:
    """
    Coordinate of a location on maps.
    """
    
    def __init__(self, longitude: float, latitude: float):
        self.longitude = longitude  # 经度
        self.latitude = latitude  # 纬度
    
    def __eq__(self, other):
        return math.isclose(self.longitude, other.longitude, rel_tol=0, abs_tol=0.00001) and \
               math.isclose(self.latitude, other.latitude, rel_tol=0, abs_tol=0.00001)
    
    def __sub__(self, other):
        return self.longitude - other.longitude, self.latitude - other.latitude
    
    def __str__(self):
        return f"[lo={round(self.longitude, 4)}, la={round(self.latitude, 4)}]"


@auto_str
class CityMap:
    """ The city map of drones food delivery """
    
    def __init__(self, topLeft: Coordinate, topRight: Coordinate, bottomLeft: Coordinate, bottomRight: Coordinate,
                 population_density=None):
        # Boundary of the city map
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        # Population density of the whole city map
        self.population_density = population_density
        # TODO: Grids
    
    def generate_random_coord(self):
        """
        Generate a random coordinate on the given map
        :return: a random Coordinate instance
        """
        lo = self.bottomLeft.longitude + random.random() * (self.bottomRight.longitude - self.bottomLeft.longitude)
        la = self.bottomLeft.latitude + random.random() * (self.topLeft.latitude - self.bottomLeft.latitude)
        return Coordinate(longitude=round(lo, 5), latitude=round(la, 5))


if __name__ == '__main__':
    city_map = CityMap(Coordinate(0, 100), Coordinate(100, 100), Coordinate(0, 0), Coordinate(100, 0))
    print(city_map)
    t1 = Coordinate(1, 2)
    t2 = Coordinate(1, 4)
    print(t1 - t2)
