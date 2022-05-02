from commons.coordinate import Coordinate
from orders.order import Order
from commons.auto_str import auto_str
import uuid


@auto_str
class Drone:
    def __init__(self, warehouses: list, start_location: Coordinate, height: float):
        self.uuid = uuid.uuid4()
        self.warehouses = warehouses
        self.current_location = start_location
        self.height = height    # meter
        self.is_free = True
        self.order = None
        
    def accept_order(self, order: Order):
        self.is_free = False
        self.order = order
    
    def deliver(self):
        pass
    
    def goto(self, location: Coordinate):
        pass
    
    def produce_noise(self):
        pass
    
    def recharge(self):
        pass
        
#
# if __name__ == '__main__':
#     start_location = Coordinate(23, 44)
#     drone = Drone(warehouses=list(), start_location=start_location, height=123)
#     print(drone)
