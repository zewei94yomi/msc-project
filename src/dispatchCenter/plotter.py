import matplotlib.pyplot as plt
from typing import List
from cityMap.citymap import Coordinate
from drones.drone import Drone
from cityMap.citymap import CityMap
from commons.configuration import BACKGROUND_IMAGE_PATH


class Plotter:
    def __init__(self, warehouses: List[Coordinate], city_map: CityMap):
        self.img = plt.imread(BACKGROUND_IMAGE_PATH)
        self.figure, self.ax = plt.subplots()
        self.warehouses_x = [x.longitude for x in warehouses]
        self.warehouses_y = [x.latitude for x in warehouses]
        self.drone_x = []
        self.drone_y = []
        self.order_x = []
        self.order_y = []
        la_diff = city_map.right - city_map.left
        lo_diff = city_map.top - city_map.bottom
        self.mapLeft = city_map.left - 0.1 * lo_diff
        self.mapRight = city_map.right + 0.1 * lo_diff
        self.mapBottom = city_map.bottom - 0.1 * la_diff
        self.mapTop = city_map.top + 0.1 * la_diff
        plt.sca(self.ax)
        plt.xlim(self.mapLeft, self.mapRight)
        plt.ylim(self.mapBottom, self.mapTop)
        plt.ion()
        
    def plot(self, drones: List[Drone]):
        """
        Store locations of drones and orders and plot them on the map.
        
        :param drones: a list of working drones
        :return:
        """
        for drone in drones:
            self.drone_x.append(drone.location.longitude)
            self.drone_y.append(drone.location.latitude)
            self.order_x.append(drone.order.start_location.longitude)
            self.order_x.append(drone.order.end_location.longitude)
            self.order_y.append(drone.order.start_location.latitude)
            self.order_y.append(drone.order.end_location.latitude)
        self.plot_everything()

    def clearData(self):
        """Clear coordinates cache data."""
        self.drone_x.clear()
        self.drone_y.clear()
        self.order_x.clear()
        self.order_y.clear()

    def plot_everything(self):
        """Plot drones, orders and warehouses on the map."""
        plt.sca(self.ax)
        plt.cla()
        self.ax.imshow(self.img, extent=[self.mapLeft, self.mapRight, self.mapBottom, self.mapTop])
        plt.scatter(self.warehouses_x, self.warehouses_y, color='blue', marker='p', linewidths=5)
        plt.scatter(self.drone_x, self.drone_y, color='red', linewidths=0.5)
        plt.scatter(self.order_x, self.order_y, color='green', marker='v', linewidths=1)
        self.clearData()
        plt.title("Drone Delivery Simulation")
        plt.pause(0.0001)
