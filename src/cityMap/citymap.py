import math
import random
from commons.decorators import auto_str


class Coordinate:
    """
    Coordinate of a location on maps.
    """
    
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude    # y
        self.longitude = longitude  # x
    
    def __eq__(self, other):
        return math.isclose(self.latitude, other.latitude, rel_tol=0, abs_tol=0.00001) and \
               math.isclose(self.longitude, other.longitude, rel_tol=0, abs_tol=0.00001)
    
    def __sub__(self, other):
        return self.latitude - other.latitude, self.longitude - other.longitude
    
    def __str__(self):
        return f"[la={round(self.latitude, 4)}, lo={round(self.longitude, 4)}]"


@auto_str
class CityMap:
    """ The city map of drones food delivery """
    
    def __init__(self, left, right, bottom, top,
                 population_density=None):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        # TODO: Population density of the whole city map, 使用我找的人口密度图的网站！上面有位置坐标！
        self.population_density = population_density
        # TODO: Grids that grid the whole city map
    
    def generate_random_coord(self) -> Coordinate:
        """
        Generate a random coordinate on the given map
        :return: a random Coordinate instance
        """
        la = self.bottom + random.random() * (self.top - self.bottom)
        lo = self.left + random.random() * (self.right - self.left)
        return Coordinate(latitude=round(la, 8), longitude=round(lo, 8))


if __name__ == '__main__':
    city_map = CityMap(left=0, right=40, bottom=0, top=40)
    print(city_map)
    t1 = Coordinate(1, 2)
    t2 = Coordinate(1, 4)
    print("t1: " + str(t1))
    print("t2: " + str(t2))
    print(t1 - t2)
