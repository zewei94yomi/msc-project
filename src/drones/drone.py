from cityMap.citymap import Coordinate
from orders.order import Order
from commons.decorators import auto_str
from commons.enum import DroneStatus
from commons.my_util import nearest_neighbor, distance
from commons.constants import DRONE_NOISE
from commons.configuration import PRINT_TERMINAL, MAP_TOP, MAP_LEFT, MAP_RIGHT, MAP_BOTTOM
from datetime import datetime
from typing import List
from drones.tracker import Tracker


@auto_str
class Drone:
    def __init__(self, drone_id, warehouses: List[Coordinate], start_location: Coordinate, height):
        self.drone_id = drone_id  # Drone id
        self.warehouses = warehouses  # Locations of all warehouses
        self.location = start_location  # Location of the drone
        self.height = height  # TODO: Height of the drone
        self.order = None  # Current order
        self.status = DroneStatus.WAITING  # Drone's status, initially waiting
        self.NOISE = DRONE_NOISE  # Default maximum drone noise
        self.destination = None  # Next destination
        self.need_planning = True  # Whether the drone needs path planner to plan a path
        self.path = []  # A planned path (list of coordinate)
        self.tracker = Tracker()  # Tracker tracks drone steps and moving distance
    
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
        self.tracker.record()
        if PRINT_TERMINAL:
            print(f"[{datetime.now()}] Drone '{self.drone_id}' returned to the nearest warehouse and start to recharge")
            print(f"[{datetime.now()}] Drone '{self.drone_id}' is recharging and waiting for new orders")
    
    def update(self):
        """
        Update drone's position and status based on its current status.
        
        Drone's status will change: COLLECTING -> DELIVERING -> RETURNING -> WAITING
        """
        if self.out_of_map():
            # if the drone is out of the map, print an error message
            # and send it to the nearest warehouse
            if PRINT_TERMINAL:
                print(f"ERROR: {self} is out of boundary, {self.order} is failed to be delivered, "
                      f"{self} has been sent to the nearest warehouse")
            self.order = None
            self.destination = None
            self.status = DroneStatus.WAITING
            self.location = nearest_neighbor(neighbors=self.warehouses, target=self.location)
        else:
            if self.has_path():
                self.fly_path()
                if self.reach_destination():
                    self.need_planning = True
                    if self.status is DroneStatus.COLLECTING:
                        self.collect_food()
                    elif self.status is DroneStatus.DELIVERING:
                        self.give_food()
                    elif self.status is DroneStatus.RETURNING:
                        self.recharge()
            else:
                if PRINT_TERMINAL:
                    print(f"WARNING: {self} has no path")
    
    def receive_path(self, path):
        """
        Receive a path.
        
        :param path: a path planned by 'PathPlanner'
        """
        self.path = path
        self.need_planning = False
    
    def fly_path(self):
        """
        Fly to the next coordinate on the path. While flying, use tracker to track step and distance.
        """
        next_location = self.path.pop(0)
        _, _, d = distance(self.location, next_location)
        self.location = next_location
        self.tracker.increment_distance(d)
        self.tracker.increment_step()
    
    def out_of_map(self):
        """
        Check if the drone is within the boundary of the map
        """
        if self.location.latitude > MAP_TOP or self.location.latitude < MAP_BOTTOM \
                or self.location.longitude > MAP_RIGHT or self.location.longitude < MAP_LEFT:
            return True
        else:
            return False
    
    def has_path(self):
        """
        Check if the drone has a path.
        """
        return len(self.path) > 0
    
    def reach_destination(self):
        """
        Check if the drone has reached the current destination.
        """
        return self.destination is not None and self.location == self.destination


if __name__ == '__main__':
    print("DO NOT TEST HERE...")
    print("Test Drone Using DroneGenerator...")
