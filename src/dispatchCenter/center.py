from commons.auto_str import auto_str
from commons.my_enum import OrderStatus, DroneStatus
from commons.util import Queue
from commons.citymap import Coordinate, CityMap
from drones.dronegenerator import DroneGenerator
from drones.drone import Drone
from orders.order import Order
from orders.ordergenerator import OrderGenerator


@auto_str
class Center:
    def __init__(self, order_generator, drone_generator):
        self.free_drones = Queue()
        self.orders = Queue()
        self.deliver_drones = list()
        self.order_generator = order_generator
        self.drone_generator = drone_generator
    
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
            order.status = OrderStatus.ACCEPTED
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
                drone.order.status = OrderStatus.DELIVERED
                drone.order = None
            self.free_drones.push(drone)
        self.deliver_drones = [x for x in self.deliver_drones if x.is_free is False and x.order is not None]

    def update_all(self):
        # TODO
        pass


if __name__ == '__main__':
    city_map = CityMap(Coordinate(20, 40), Coordinate(50, 40), Coordinate(20, 20), Coordinate(50, 20))
    og = OrderGenerator(city_map)
    dg = DroneGenerator(warehouses=[Coordinate(20, 40)])
    o = og.get_order()
    d = dg.get_drone()
    d.accept(o)
    while d.status != DroneStatus.WAITING:
        d.update()
