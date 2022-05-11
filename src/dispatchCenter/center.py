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
from typing import List
from plotter.plotter import Plotter


@auto_str
class Center:
    def __init__(self, warehouses: List[Coordinate], city_map: CityMap, num_orders, num_drones):
        # Coordinates of all warehouses
        self.warehouses = warehouses
        # The city map which contains the coordinates of four corners, and a population density map
        self.city_map = city_map
        # Order generator which generates new orders
        self.order_generator = OrderGenerator(city_map=self.city_map)
        # Drone generator which generates new (free) drones
        self.drone_generator = DroneGenerator(warehouses=self.warehouses)
        # Queue for waiting orders: orders first come, first served
        self.waiting_orders = Queue()
        # List of free drones
        self.free_drones = list()
        # List of delivering drones
        self.delivering_drones = list()
        self.create_order(num_orders)
        self.create_drones(num_drones)
        self.plotter = Plotter(warehouses=self.warehouses)
    
    def add_drone(self, drone=None):
        if drone is None:
            drone = self.drone_generator.get_drone()
        self.free_drones.append(drone)
    
    def add_order(self, order=None):
        if order is None:
            order = self.order_generator.get_order()
        self.waiting_orders.push(order)
    
    def create_drones(self, num):
        for i in range(num):
            self.add_drone()
    
    def create_order(self, num):
        for i in range(num):
            self.add_order()
            
    def has_free_drone(self):
        return len(self.free_drones) > 0
    
    def has_working_drone(self):
        return len(self.delivering_drones) > 0
    
    def has_new_order(self):
        return self.waiting_orders.isEmpty() is False
    
    def process(self):
        while self.has_new_order() and self.has_free_drone():
            order = self.waiting_orders.pop()       # pop the least recent order
            drone = self.nearest_free_drone(order)  # find the index of
            drone.accept(order)                     # let the drone accept the order
            self.free_drones.remove(drone)          # remove the drone from the list of free drones
            self.delivering_drones.append(drone)    # add the drone to the list of delivering drones

    def update_drones(self):
        # TODO: optimize
        drone_x = []
        drone_y = []
        order_x = []
        order_y = []
        for drone in self.delivering_drones:
            drone.update()
            drone_x.append(drone.current_location.longitude)
            drone_y.append(drone.current_location.latitude)
            if drone.order is not None:
                order_x.append(drone.order.start_location.longitude)
                order_x.append(drone.order.end_location.longitude)
                order_y.append(drone.order.start_location.latitude)
                order_y.append(drone.order.end_location.latitude)
            # Select and remove waiting drones who have completed their orders from the list of delivering drones
            # TODO: the problem of suddenly missing order points might be caused by this part of code
            if drone.status is DroneStatus.WAITING:
                self.delivering_drones.remove(drone)
                self.free_drones.append(drone)
        self.plotter.update(drone_x, drone_y, order_x, order_y)
        
    def run(self):
        while True:
            if self.has_new_order() or self.has_working_drone():
                self.process()
                self.update_drones()
                self.plotter.plot()
            
    def nearest_free_drone(self, order: Order) -> Drone:
        distances = []
        for drone in self.free_drones:
            _, _, line_distance = distance(order.start_location, drone.current_location)
            distances.append(line_distance)
        return self.free_drones[np.argmin(distances)]

