import matplotlib.pyplot as plt
from typing import List
from commons.citymap import Coordinate


class Plotter:
    def __init__(self, warehouses: List[Coordinate]):
        self.img = plt.imread("commons/map.jpeg")
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
    
    def update(self, d_x, d_y, o_x, o_y):
        self.drone_x.clear()
        self.drone_y.clear()
        self.order_x.clear()
        self.order_y.clear()
        self.drone_x = d_x
        self.drone_y = d_y
        self.order_x = o_x
        self.order_y = o_y
        
    def plot(self):
        plt.cla()
        self.ax.imshow(self.img, extent=[-10, 50, -10, 50])
        plt.scatter(self.warehouses_x, self.warehouses_y, color='blue')
        plt.scatter(self.drone_x, self.drone_y, color='red')
        plt.scatter(self.order_x, self.order_y, color='green')
        plt.draw()
        plt.pause(0.0001)
