from commons.coordinate import Coordinate
from orders.order import Order
from commons.auto_str import auto_str
import uuid


@auto_str
class Drone:
    def __init__(self, warehouses: list, start: Coordinate, height: float, order: Order = None):
        self.uuid = uuid.uuid4()
        self.warehouses = warehouses
        self.current_location = start
        self.height = height    # meter
        self.is_free = order is None
        self.order = order
        
    def accept_order(self, order: Order):
        pass
    
    def deliver(self):
        pass
    
    def goto(self, location: Coordinate):
        pass
    
    def produce_noise(self):
        pass
    
    def recharge(self):
        pass
        
    
if __name__ == '__main__':
    start = Coordinate(23, 44)
    drone = Drone(warehouses=list(), start=start, height=123)
    print(drone)
