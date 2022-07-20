from cityMap.citymap import Coordinate
from orders.order import Order
from commons.decorators import auto_str
from commons.enum import DroneStatus
from commons.my_util import distance_coordinates, nearest_neighbor
from commons.constants import DRONE_NOISE
from commons.configuration import PRINT_TERMINAL, MAP_TOP, MAP_LEFT, MAP_RIGHT, MAP_BOTTOM
from datetime import datetime
from typing import List
import math


@auto_str
class Drone:
    def __init__(self, drone_id, warehouses: List[Coordinate], start_location: Coordinate, height):
        self.drone_id = drone_id                    # Drone id
        self.warehouses = warehouses                # Coordinates of warehouses
        self.location = start_location              # Location of the drone
        self.height = height                        # Height of the drone TODO: implement height of drones
        self.order = None                           # Current accepted order
        self.status = DroneStatus.WAITING           # Drone's status
        self.lo_speed = 0                           # Current longitude speed
        self.la_speed = 0                           # Current latitude speed
        self.MAX_SPEED = 0.01                       # Maximum straight-line speed TODO: lon max-speed and lat max-speed
        self.NOISE = DRONE_NOISE                    # Default maximum drone noise
        # TODO: treat 'destination' as a list，so the path would be locations in 'destination'
        self.destination = None                     # Next destination
    
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
        if PRINT_TERMINAL:
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
        if PRINT_TERMINAL:
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
        self.destination = nearest_neighbor(neighbors=self.warehouses, target=self.location)
        self.update_speed()
        if PRINT_TERMINAL:
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
        if PRINT_TERMINAL:
            print(f"[{datetime.now()}] Drone '{self.drone_id}' returned to the nearest warehouse and start to recharge")
            print(f"[{datetime.now()}] Drone '{self.drone_id}' is recharging and waiting for new orders")
    
    def update(self):
        """Update drone's position and status based on its current status"""
        if self.location.latitude > MAP_TOP or self.location.latitude < MAP_BOTTOM \
            or self.location.longitude > MAP_RIGHT or self.location.longitude < MAP_LEFT:
            print(f"ERROR: {self} is out of boundary")
        else:
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
                if PRINT_TERMINAL:
                    print(f"[{datetime.now()}] Drone '{self.drone_id}' is waiting for new orders")
    
    def fly(self) -> bool:
        """
        Fly to the current destination
        
        If the drone reaches the destination after this update, return True; otherwise return False
        """
        la_delta, lo_delta = self.destination - self.location
        if math.fabs(la_delta) <= math.fabs(self.la_speed) or math.fabs(lo_delta) <= math.fabs(self.lo_speed):
            self.location.latitude = self.destination.latitude
            self.location.longitude = self.destination.longitude
            return True
        else:
            self.location.latitude += self.la_speed
            self.location.longitude += self.lo_speed
            return False
    
    def update_speed(self):
        """Update speed according to the current destination"""
        la_distance, lo_distance, direct_distance = distance_coordinates(self.location, self.destination)
        if direct_distance == 0:
            self.la_speed = self.lo_speed = 0
        else:
            self.la_speed = la_distance * self.MAX_SPEED / direct_distance
            self.lo_speed = lo_distance * self.MAX_SPEED / direct_distance


if __name__ == '__main__':
    print("DO NOT TEST HERE...")
    print("Test Drone Using DroneGenerator...")
