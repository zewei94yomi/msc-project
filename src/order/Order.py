from commons.Coordinate import Coordinate
import uuid
from datetime import datetime


class Order:
    """
    Food delivery order.
    """
    
    def __init__(self, start: Coordinate, end: Coordinate, description=""):
        self.uuid = uuid.uuid4()  # Unique ID
        self.time = datetime.today()  # Generated time
        self.start = start  # Start location
        self.end = end  # End location
        self.description = description  # Order description
    
    def __str__(self):
        return f"Order: uuid={self.uuid}, time={self.time}, start={self.start}, end={self.end}, " \
               f"description={self.description}"


if __name__ == '__main__':
    o = Order(Coordinate(1.1, 2.2), Coordinate(2.2, 4.55))
    print(o)
