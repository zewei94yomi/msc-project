from commons.coordinate import Coordinate
from orders.order import Order
from commons.auto_str import auto_str
import uuid


@auto_str
class Drone:
    def __init__(self, start: Coordinate, height: float, order: Order = None):
        self.uuid = uuid.uuid4()
        self.current_location = start
        self.height = height
        self.is_free = order is None
        self.order = order
