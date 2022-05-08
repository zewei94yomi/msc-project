from commons.citymap import Coordinate
from typing import List
from commons.auto_str import auto_str
from drones.drone import Drone
from commons.my_util import get_uuid


@auto_str
class DroneGenerator:
    """Drone generator: generate drones"""
    
    def __init__(self, warehouses: List[Coordinate]):
        self.warehouses = warehouses
        self.warehouse_pointer = 0
    
    def get_drone(self) -> Drone:
        """
        Create and initialize a Drone instance.
        
        The drone will be initialized to a warehouse. The strategy for determining
        which warehouse to be initialized in is Round Robin.
        The drone will be initialized at 0 meters high.
        The warehouse pointer will increment by 1 when a new drone is generated.
        
        :return: a new Drone instance
        """
        drone = Drone(uuid=get_uuid(), warehouses=self.warehouses, start_location=self.warehouses[self.warehouse_pointer], height=0)
        self.warehouse_pointer = (self.warehouse_pointer + 1) % len(self.warehouses)
        return drone
    
    
if __name__ == '__main__':
    w = [Coordinate(longitude=123, latitude=22)]
    dg = DroneGenerator(warehouses=w)
    print(dg)
    d = dg.get_drone()
    print(d)
