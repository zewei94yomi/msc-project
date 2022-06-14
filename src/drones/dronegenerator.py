from cityMap.citymap import Coordinate
from typing import List
from commons.decorators import auto_str
from drones.drone import Drone
from commons.my_util import get_uuid
import copy


@auto_str
class DroneGenerator:
    """Drone generator: generate drones"""
    
    def __init__(self, warehouses: List[Coordinate]):
        self.warehouses = warehouses
        self.warehouse_pointer = 0
        self.ids = 0
    
    def get_drone(self) -> Drone:
        """
        Create and initialize a Drone instance.
        
        The drone will be initialized to a warehouse. The strategy for determining which warehouse to be initialized
        in is Round Robin.
        The warehouse pointer will increment by 1 when a new drone is generated.
        
        :return: a new Drone instance
        """
        self.ids += 1
        start_location = copy.deepcopy(self.warehouses[self.warehouse_pointer])
        drone = Drone(drone_id=self.ids, uuid=get_uuid(), warehouses=self.warehouses,
                      start_location=start_location, height=0)
        self.warehouse_pointer = (self.warehouse_pointer + 1) % len(self.warehouses)
        return drone


if __name__ == '__main__':
    w = [Coordinate(latitude=22, longitude=123)]
    dg = DroneGenerator(warehouses=w)
    print(dg)
    d = dg.get_drone()
    print(d)
