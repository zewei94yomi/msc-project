from commons.auto_str import auto_str
from commons.enum import Status
from commons.util import Queue
from drones.drone import Drone
from orders.order import Order


@auto_str
class Center:
    def __init__(self, drones, generator):
        self.free_drones = Queue()
        for drone in drones:
            self.free_drones.push(drone)
        self.generator = generator
        self.deliver_drones = []
        self.orders = Queue()
    
    def add_drone(self, drone):
        self.free_drones.push(drone)
    
    def init_orders(self, num_order):
        for i in range(num_order):
            self.orders.push(self.generator.get_order())
    
    def free_drone(self):
        return self.free_drones.isEmpty() is False
    
    def new_order(self):
        return self.orders.isEmpty() is False
    
    def assign(self) -> (bool, Drone, Order):
        if self.has_new_order() and self.has_free_drone():
            order = self.orders.pop()
            order.status = Status.ACCEPTED
            drone = self.free_drones.pop()
            drone.accept_order(order)
            self.deliver_drones.append(drone)
            return True, drone, order
        else:
            return False, None, None

    def update_drones(self):
        new_free_drones = [x for x in self.deliver_drones if x.is_free or x.order is None]
        for drone in new_free_drones:
            drone.is_free = True
            if drone.order is not None:
                drone.order.status = Status.DELIVERED
                drone.order = None
            self.free_drones.push(drone)
        self.deliver_drones = [x for x in self.deliver_drones if x.is_free is False and x.order is not None]

    def update_all(self):
        pass
