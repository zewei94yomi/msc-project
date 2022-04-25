import math


class Coordinate:
    
    """
    Coordinate of a location on maps.
    """
    
    def __init__(self, longitude: float, latitude: float):
        self.longitude = longitude
        self.latitude = latitude
        
    def __str__(self):
        return "Coordinate: (%f, %f)" % (self.longitude, self.latitude)
     
    def __eq__(self, other):
        return math.isclose(self.longitude, other.longitude, rel_tol=0, abs_tol=0.0001) and \
               math.isclose(self.latitude, other.latitude, rel_tol=0, abs_tol=0.0001)
        
        
if __name__ == '__main__':
    # Test equality
    test1 = Coordinate(1.00001, 2.555)
    test2 = Coordinate(1, 2.555)
    print(test1)
    print(test2)
    print("Test1 == Test2 ? " + str(test1 == test2))