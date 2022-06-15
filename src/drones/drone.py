from cityMap.citymap import Coordinate
from orders.order import Order
from commons.decorators import auto_str
from commons.enum import DroneStatus
from commons.my_util import distance, nearest_neighbor
from datetime import datetime
from typing import List
import math


@auto_str
class Drone:
    def __init__(self, drone_id, uuid, warehouses: List[Coordinate], start_location: Coordinate, height: float):
        self.drone_id = drone_id                    # Drone's id
        self.uuid = uuid                            # Unique ID
        self.warehouses = warehouses                # Locations of warehouse
        self.current_location = start_location      # Current location of the drone
        self.height = height                        # Current height of the drone
        self.order = None                           # Current Order the drone has accepted
        self.status = DroneStatus.WAITING           # Status of the drone
        self.lo_speed = 0                           # Current longitude speed
        self.la_speed = 0                           # Current latitude speed
        self.MAX_SPEED = 0.002                      # Maximum straight-line speed
        self.NOISE = 0.15
        # TODO: 未来可以重构这里，把destination变成一个list，那么路径就是destination里的一个个坐标点
        self.destination = None                     # Location of the next destination
    
    def accept_order(self, order: Order):
        """
        Drone accepts an order.
        
        Update the order's status from 'WAITING' to 'ACCEPTED'.
        Set a new destination for the drone and calculate speed based on the new destination.
        Update drone's status from 'WAITING' to 'COLLECTING'.
        """
        self.order = order
        self.order.accept()
        self.status = DroneStatus.COLLECTING
        self.destination = self.order.start_location
        self.update_speed()
        print(f"[{datetime.now()}] Drone '{self.drone_id}' accepted Order '{self.order.order_id}'")
        print(f"[{datetime.now()}] Drone '{self.drone_id}' is flying to {self.destination} to pick up food")
    
    def collect_food(self):
        """
        Drone collects the food at the start location of the order.
        
        Update the order's status from 'ACCEPTED' to 'DELIVERING'.
        Set a new destination for the drone and calculate speed based on the new destination.
        Update drone's status from 'COLLECTING' to 'DELIVERING'.
        """
        self.order.deliver()
        self.status = DroneStatus.DELIVERING
        self.destination = self.order.end_location
        self.update_speed()
        print(f"[{datetime.now()}] Drone '{self.drone_id}' collected Order '{self.order.order_id}'")
        print(f"[{datetime.now()}] Drone '{self.drone_id}' is flying to {self.destination} to deliver food")
    
    def give_food(self):
        """
        Drone gives food to the customer and starts to return to one of warehouses.
        
        Update the order's status from 'DELIVERING' to 'COMPLETE'.
        Find the nearest warehouse and set it as the new destination for the drone,
        and calculate speed based on the new destination.
        Update drone's status from 'DELIVERING' to 'RETURNING'.
        """
        self.order.complete()
        self.status = DroneStatus.RETURNING
        self.destination = nearest_neighbor(neighbors=self.warehouses, target=self.current_location)
        self.update_speed()
        print(f"[{datetime.now()}] Drone '{self.drone_id}' delivered Order '{self.order.order_id}'")
        print(f"[{datetime.now()}] Drone '{self.drone_id}' is flying to {self.destination} to recharge")
    
    def recharge(self):
        """
        Drone arrives at one of the warehouses and start to recharge.
        
        Remove destination and speeds.
        Update drone's status from 'RETURNING' to 'WAITING'.
        Drone is waiting for new orders.
        """
        self.status = DroneStatus.WAITING
        self.order = None
        self.destination = None
        self.lo_speed = 0
        self.la_speed = 0
        print(f"[{datetime.now()}] Drone '{self.drone_id}' returned to the nearest warehouse and start to recharge")
        print(f"[{datetime.now()}] Drone '{self.drone_id}' is recharging and waiting for new orders")
    
    def update(self):
        """Update drone's position and status based on its current status"""
        if self.status is DroneStatus.COLLECTING:
            if self.fly() is True:
                self.collect_food()
        elif self.status is DroneStatus.DELIVERING:
            if self.fly() is True:
                self.give_food()
        elif self.status is DroneStatus.RETURNING:
            if self.fly() is True:
                self.recharge()
        else:
            # Current status is DroneStatus.WAITING
            print(f"[{datetime.now()}] Drone '{self.drone_id}' is waiting for new orders")
    
    def produce_noise(self):
        return self.NOISE
    
    def fly(self) -> bool:
        """
        Fly to the current destination
        
        If the drone reaches the destination after this fly update, return True; otherwise return False
        """
        la_delta, lo_delta = self.current_location - self.destination
        if math.fabs(la_delta) <= math.fabs(self.la_speed) and math.fabs(lo_delta) <= math.fabs(self.lo_speed):
            self.current_location.latitude = self.destination.latitude
            self.current_location.longitude = self.destination.longitude
            return True
        else:
            self.current_location.latitude += self.la_speed
            self.current_location.longitude += self.lo_speed
            return False
    
    def update_speed(self):
        """Update speed according to the current destination"""
        la_distance, lo_distance, direct_distance = distance(self.current_location, self.destination)
        if direct_distance == 0:
            self.la_speed = self.lo_speed = 0
        else:
            self.la_speed = round(la_distance * self.MAX_SPEED / direct_distance, 7)
            self.lo_speed = round(lo_distance * self.MAX_SPEED / direct_distance, 7)


if __name__ == '__main__':
    print("DO NOT TEST HERE...")
    print("Test Drone Using DroneGenerator...")
