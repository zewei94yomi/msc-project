import matplotlib.pyplot as plt
from typing import List
from cityMap.citymap import Coordinate
from drones.drone import Drone


class Plotter:
    def __init__(self, warehouses: List[Coordinate]):
        self.img = plt.imread("recourses/map.jpeg")
        self.fig, self.ax = plt.subplots()
        self.warehouses_x = [x.longitude for x in warehouses]
        self.warehouses_y = [x.latitude for x in warehouses]
        self.drone_x = []
        self.drone_y = []
        self.order_x = []
        self.order_y = []
        plt.xlim(-10, 50)
        plt.ylim(-10, 50)
        plt.ion()
    
    def saveData(self, drone: Drone):
        self.drone_x.append(drone.current_location.longitude)
        self.drone_y.append(drone.current_location.latitude)
        self.order_x.append(drone.order.start_location.longitude)
        self.order_x.append(drone.order.end_location.longitude)
        self.order_y.append(drone.order.start_location.latitude)
        self.order_y.append(drone.order.end_location.latitude)

    def clearData(self):
        self.drone_x.clear()
        self.drone_y.clear()
        self.order_x.clear()
        self.order_y.clear()

    def plot(self):
        plt.cla()
        self.ax.imshow(self.img, extent=[-10, 50, -10, 50])
        # plot warehouse
        plt.scatter(self.warehouses_x, self.warehouses_y, color='blue', marker='p', linewidths=5)
        # plot drones
        plt.scatter(self.drone_x, self.drone_y, color='red', linewidths=0.5)
        # plot orders
        plt.scatter(self.order_x, self.order_y, color='green', marker='v', linewidths=1)
        # clear plotter cache
        self.clearData()
        plt.pause(0.0001)
