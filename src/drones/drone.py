from commons.citymap import Coordinate
from orders.order import Order
from commons.auto_str import auto_str
from commons.my_enum import DroneStatus, OrderStatus
from datetime import datetime
import math


@auto_str
class Drone:
    def __init__(self, uuid, warehouses, start_location: Coordinate, height: float):
        self.uuid = uuid  # Unique ID
        self.warehouses = warehouses
        self.current_location = start_location  # Start location
        self.height = height  # Current height
        self.order = None  # Current Order
        self.status = DroneStatus.WAITING  # Status of the drone
        self.lo_speed = 0
        self.la_speed = 0
        self.MAX_SPEED = 1
        self.destination = None
        
    def accept(self, order: Order):
        """change"""
        order.accept()  # update order's status
        self.order = order
        self.destination = self.order.start_location
        self.update_speed()
        print(f"[{datetime.now()}] Drone '{self.uuid}' accepted Order '{self.order.uuid}'")
        self.status = DroneStatus.COLLECTING
        print(f"[{datetime.now()}] Drone '{self.uuid}' is heading to {self.order.start_location}")
        self.go_collect()
    
    def pickup(self):
        """change"""
        self.destination = self.order.end_location
        self.update_speed()
        print(f"[{datetime.now()}] Drone '{self.uuid}' collected Order '{self.order.uuid}'")
        print(f"[{datetime.now()}] Drone '{self.uuid}' is heading to {self.order.end_location}")
        self.status = DroneStatus.DELIVERING
        self.go_deliver()
    
    def give_food(self):
        """change"""
        self.destination = self.warehouses[0]
        self.update_speed()
        print(f"[{datetime.now()}] Drone '{self.uuid}' delivered Order '{self.order.uuid}'")
        self.status = DroneStatus.RETURNING
    
    def update(self):
        if self.status is DroneStatus.COLLECTING:
            self.go_collect()
        elif self.status is DroneStatus.DELIVERING:
            self.go_deliver()
        elif self.status is DroneStatus.RETURNING:
            self.go_recharge()
    
    def go_collect(self):
        """process"""
        if self.fly() is True:
            self.pickup()
    
    def go_deliver(self):
        if self.fly() is True:
            self.give_food()
            
    def go_recharge(self):
        if self.fly() is True:
            self.recharge()

    # TODO
    def recharge(self):
        self.lo_speed = 0
        self.la_speed = 0
        self.status = DroneStatus.WAITING
        self.order = None
        self.destination = None
        print(f"[{datetime.now()}] Drone '{self.uuid}' is recharging")
        
    # TODO
    def produce_noise(self):
        pass
    
    def fly(self):
        lo_delta, la_delta = self.current_location - self.destination
        if lo_delta <= math.fabs(self.lo_speed) and la_delta <= math.fabs(self.la_speed):
            self.current_location = self.destination
            return True
        else:
            self.current_location.longitude += self.lo_speed
            self.current_location.latitude += self.la_speed
            return False
    
    def update_speed(self):
        lo_distance, la_distance = self.destination - self.current_location
        self.lo_speed = lo_distance * self.MAX_SPEED / math.sqrt(math.pow(lo_distance, 2) + math.pow(la_distance, 2))
        self.la_speed = la_distance * self.MAX_SPEED / math.sqrt(math.pow(lo_distance, 2) + math.pow(la_distance, 2))


if __name__ == '__main__':
    print("DON'T TEST DRONE HERE...")
    print("Test Drone Using DroneGenerator...")
