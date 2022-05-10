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
import matplotlib.pyplot as plt
from typing import List


@auto_str
class Center:
    def __init__(self, warehouses: List[Coordinate], city_map: CityMap):
        self.warehouses = warehouses
        self.city_map = city_map
        self.order_generator = OrderGenerator(city_map=self.city_map)
        self.drone_generator = DroneGenerator(warehouses=self.warehouses)
        self.waiting_orders = Queue()   # first come, first serve
        self.free_drones = list()
        self.delivering_drones = list()
        self.plot_delivering_drones_x = list()
        self.plot_delivering_drones_y = list()
        self.plot_warehouses_x = [x.longitude for x in self.warehouses]
        self.plot_warehouses_y = [x.latitude for x in self.warehouses]
        self.plot_orders_x = list()
        self.plot_orders_y = list()
        self.img = plt.imread("../commons/map.jpeg")
        self.fig, self.ax = plt.subplots()
        self.init_plot()
    
    def add_drone(self, drone=None):
        if drone is None:
            drone = self.drone_generator.get_drone()
        self.free_drones.append(drone)
    
    def add_order(self, order=None):
        if order is None:
            order = self.order_generator.get_order()
        self.waiting_orders.push(order)
    
    def init(self, order_num, drone_num):
        for i in range(order_num):
            self.add_order()
        for i in range(drone_num):
            self.add_drone()
            
    def init_plot(self):
        plt.xlim(-10, 50)
        plt.ylim(-10, 50)
        plt.ion()

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
        self.plot_delivering_drones_x.clear()
        self.plot_delivering_drones_y.clear()
        self.plot_orders_x.clear()
        self.plot_orders_y.clear()
        for drone in self.delivering_drones:
            drone.update()
            self.plot_delivering_drones_x.append(drone.current_location.longitude)
            self.plot_delivering_drones_y.append(drone.current_location.latitude)
            if drone.order is not None:
                self.plot_orders_x.append(drone.order.start_location.longitude)
                self.plot_orders_x.append(drone.order.end_location.longitude)
                self.plot_orders_y.append(drone.order.start_location.latitude)
                self.plot_orders_y.append(drone.order.end_location.latitude)
            # Select and remove waiting drones who have completed their orders from the list of delivering drones
            if drone.status is DroneStatus.WAITING:
                self.delivering_drones.remove(drone)
                # add waiting drones to the list of free drones
                self.free_drones.append(drone)
        
    def plot(self):
        # TODO: optimize and make the whole process more smooth
        plt.cla()
        self.ax.imshow(self.img, extent=[-10, 50, -10, 50])
        plt.scatter(self.plot_warehouses_x, self.plot_warehouses_y, color='blue')
        plt.scatter(self.plot_delivering_drones_x, self.plot_delivering_drones_y, color='red')
        plt.scatter(self.plot_orders_x, self.plot_orders_y, color='green')
        plt.draw()
        plt.pause(0.0001)

    def run(self):
        while True:
            if self.has_new_order() or self.has_working_drone():
                self.process()
                self.update_drones()
                self.plot()
            
    def nearest_free_drone(self, order: Order) -> Drone:
        distances = []
        for drone in self.free_drones:
            _, _, line_distance = distance(order.start_location, drone.current_location)
            distances.append(line_distance)
        return self.free_drones[np.argmin(distances)]


if __name__ == '__main__':
    t_city_map = CityMap(Coordinate(0, 40), Coordinate(40, 40), Coordinate(0, 0), Coordinate(40, 0))
    center = Center(warehouses=[Coordinate(0, 40), Coordinate(40, 0)], city_map=t_city_map)
    center.init(order_num=25, drone_num=8)
    center.run()

