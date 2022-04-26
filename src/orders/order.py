from commons.coordinate import Coordinate
from commons.auto_str import auto_str
import uuid
from datetime import datetime


@auto_str
class Order:
    """
    Food delivery orders.
    """
    
    def __init__(self, start: Coordinate, end: Coordinate, description=""):
        self.uuid = uuid.uuid4()  # Unique ID
        self.generate_time = datetime.today()  # Generated time
        self.start = start  # Start location
        self.end = end  # End location
        self.description = description  # Order description
    

if __name__ == '__main__':
    o = Order(Coordinate(1.1, 2.2), Coordinate(2.2, 4.55))
    print(o)
