from commons.decorators import auto_str
from commons.enum import DroneStatus
from commons.my_util import nearest_free_drone
from commons.util import Queue
from cityMap.citymap import Coordinate, CityMap
from drones.dronegenerator import DroneGenerator
from orders.ordergenerator import OrderGenerator
from typing import List
from plotter.plotter import Plotter
from noise.tracker import NoiseTracker


@auto_str
class Center:
    def __init__(self, warehouses: List[Coordinate], city_map: CityMap, num_orders, num_drones):
        self.warehouses = warehouses
        self.order_generator = OrderGenerator(city_map=city_map)
        self.drone_generator = DroneGenerator(warehouses=self.warehouses)
        self.waiting_orders = Queue()   # orders first come, first serve
        self.free_drones = list()
        self.delivering_drones = list()
        self.plotter = Plotter(warehouses=self.warehouses, city_map=city_map)
        self.noise_tracker = NoiseTracker()
        self.init_drones(num_drones)
        self.init_orders(num_orders)

    # TODO
    def generate_orders(self):
        """Randomly generate new orders to simulate reality"""
        pass
    
    def process_orders(self):
        """
        Process all waiting orders
        
        If there are waiting orders and free drones, allocate these orders to the free drones.
        """
        while self.has_waiting_order() and self.has_free_drone():
            order = self.waiting_orders.pop()       # pop the least recent order
            drone = nearest_free_drone(order, self.free_drones)       # find the nearest free drone
            drone.accept_order(order)                     # let the drone accept the order
            self.free_drones.remove(drone)          # remove the drone from the list of free drones
            self.delivering_drones.append(drone)    # add the drone to the list of delivering drones

    def update_drones(self):
        """
        Update delivering (working) drones' status and position.
        
        Record the current position of each working drone.
        Update drones and orders' status and positions.
        If any delivering drone completes its order, update its status and move it to the list of free drones.
        """
        for drone in self.delivering_drones:
            drone.update()
            self.noise_tracker.track_noise(drone)
            if drone.status is DroneStatus.WAITING:
                self.free_drones.append(drone)
        self.delivering_drones = [x for x in self.delivering_drones if x not in self.free_drones]
        
    def run(self):
        """Run the center"""
        while True:
            if self.has_waiting_order() or self.has_working_drone():
                self.process_orders()
                self.update_drones()
                self.plotter.save_and_plot(self.delivering_drones)
            # self.generate_orders()

    def init_drones(self, num):
        """
        Create a number of drones and add them to the list of free drones
        """
        for i in range(num):
            self.free_drones.append(self.drone_generator.get_drone())

    def init_orders(self, num):
        """
        Create a number of orders and add them to the queue of waiting orders
        """
        for i in range(num):
            self.waiting_orders.push(self.order_generator.get_order())

    def has_free_drone(self) -> bool:
        """Check if there is any free (recharging) drone"""
        return len(self.free_drones) > 0

    def has_working_drone(self) -> bool:
        """Check if there is any flying (working) drone"""
        return len(self.delivering_drones) > 0

    def has_waiting_order(self) -> bool:
        """Check if there is any new (waiting) order"""
        return self.waiting_orders.isEmpty() is False
