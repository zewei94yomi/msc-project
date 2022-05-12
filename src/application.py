from cityMap.citymap import CityMap, Coordinate
from dispatchCenter.center import Center

if __name__ == '__main__':
    t_city_map = CityMap(Coordinate(0, 40), Coordinate(40, 40), Coordinate(0, 0), Coordinate(40, 0))
    center = Center(warehouses=[Coordinate(0, 35), Coordinate(35, 0)], city_map=t_city_map, num_orders=5, num_drones=3)
    center.run()
