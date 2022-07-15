from cityMap.citymap import Coordinate
from typing import List
from commons.decorators import auto_str
from drones.drone import Drone
import copy


@auto_str
class DroneGenerator:
    """Drone generator: generate drones"""
    
    def __init__(self, warehouses: List[Coordinate]):
        self.warehouses = warehouses
        self.warehouse_pointer = 0
        self.ids = 0
    
    def get_drones(self, num) -> List[Drone]:
        """
        Create and initialize a list of Drone instances.

        The drone will be initialized to a warehouse. The strategy for determining which warehouse to be initialized
        in is Round Robin.
        The warehouse pointer will increment by 1 when a new drone is generated.

        :return: a list of new Drone instances
        """
        drones = list()
        for i in range(num):
            self.ids += 1
            start_location = copy.deepcopy(self.warehouses[self.warehouse_pointer])
            drone = Drone(drone_id=self.ids, warehouses=self.warehouses,
                          start_location=start_location, height=0)
            self.warehouse_pointer = (self.warehouse_pointer + 1) % len(self.warehouses)
            drones.append(drone)
        return drones
        

if __name__ == '__main__':
    w = [Coordinate(latitude=22, longitude=123)]
    dg = DroneGenerator(warehouses=w)
    print(dg)
    d = dg.get_drone()
    print(d)
