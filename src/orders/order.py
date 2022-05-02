from commons.coordinate import Coordinate
from commons.auto_str import auto_str
from commons.enum import Status
import uuid
from datetime import datetime


@auto_str
class Order:
    """
    Food delivery orders.
    """
    
    def __init__(self, start_loc: Coordinate, end_loc: Coordinate, time: datetime, description=""):
        self.uuid = uuid.uuid4()  # Unique ID
        self.start_loc = start_loc  # Start location
        self.end_loc = end_loc  # End location
        self.generate_time = time  # Generated time
        self.status = Status.WAITING
        self.description = description  # Order description


if __name__ == '__main__':
    o = Order(Coordinate(1.1, 2.2), Coordinate(2.2, 4.55), datetime.today())
    print(o)
    print(type(o.generate_time))
