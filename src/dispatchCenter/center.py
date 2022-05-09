from commons.auto_str import auto_str
from commons.my_enum import OrderStatus, DroneStatus
from commons.my_util import distance
from commons.util import Queue
from commons.citymap import Coordinate, CityMap
from drones.dronegenerator import DroneGenerator
from drones.drone import Drone
from orders.order import Order
from orders.ordergenerator import OrderGenerator
import numpy as np


@auto_str
class Center:
    def __init__(self, order_generator: OrderGenerator, drone_generator: DroneGenerator):
        self.waiting_orders = Queue()
        self.free_drones = list()
        self.delivering_drones = list()
        self.order_generator = order_generator
        self.drone_generator = drone_generator
    
    def add_drone(self, drone=None):
        if drone is None:
            drone = self.drone_generator.get_drone()
        self.free_drones.append(drone)
    
    def add_order(self, order=None):
        if order is None:
            order = self.order_generator.get_order()
        self.waiting_orders.push(order)
    
    def init_orders(self, num):
        for i in range(num):
            self.add_order()
            
    def init_drones(self, num):
        for i in range(num):
            self.add_drone()
    
    def has_free_drone(self):
        return len(self.free_drones) > 0
    
    def has_new_order(self):
        return self.waiting_orders.isEmpty() is False
    
    def dispatch(self):
        while self.has_new_order() and self.has_free_drone():
            order = self.waiting_orders.pop()       # pop the least recent order
            drone = self.nearest_free_drone(order)  # find the index of
            drone.accept(order)                     # let the drone accept the order
            self.free_drones.remove(drone)          # remove the drone from the list of free drones
            self.delivering_drones.append(drone)    # add the drone to the list of delivering drones

    def nearest_free_drone(self, order: Order) -> Drone:
        distances = []
        for drone in self.free_drones:
            _, _, line_distance = distance(order.start_location, drone.current_location)
            distances.append(line_distance)
        return self.free_drones[np.argmin(distances)]

    def update_drones(self):
        for drone in self.delivering_drones:
            drone.update()
            # Select and remove waiting drones who have completed their orders from the list of delivering drones
            if drone.status is DroneStatus.WAITING:
                self.delivering_drones.remove(drone)
                # add waiting drones to the list of free drones
                self.free_drones.append(drone)

    def run(self):
        # while there are new orders or delivering drones...
        while self.has_new_order() or len(self.delivering_drones) != 0:
            # print(f"[{datetime.now()}] {self.waiting_orders.size()} waiting, {len(self.delivering_drones)} working")
            self.dispatch()
            self.update_drones()


if __name__ == '__main__':
    city_map = CityMap(Coordinate(20, 40), Coordinate(50, 40), Coordinate(20, 20), Coordinate(50, 20))
    og = OrderGenerator(city_map)
    dg = DroneGenerator(warehouses=[Coordinate(32, 20), Coordinate(25, 20), Coordinate(47, 20)])
    center = Center(order_generator=og, drone_generator=dg)
    center.init_drones(10)
    center.init_orders(200)
    center.run()

