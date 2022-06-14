from cityMap.citymap import CityMap, Coordinate
from dispatchCenter.center import Center

if __name__ == '__main__':
    # plt.xlim(37.710808, 37.810894)
    # plt.ylim(-122.516112, -122.378443)
    # t_city_map = CityMap(Coordinate(0, 40), Coordinate(40, 40), Coordinate(0, 0), Coordinate(40, 0))
    t_city_map = CityMap(left=-122.516112, right=-122.378443,
                         bottom=37.710808, top=37.810894)
    center = Center(warehouses=[Coordinate(37.750808, -122.478443)],
                    city_map=t_city_map, num_orders=10, num_drones=3)
    center.run()
