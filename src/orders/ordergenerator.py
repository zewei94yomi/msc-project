from commons.citymap import Coordinate
from commons.auto_str import auto_str
from commons.citymap import CityMap
from orders.order import Order
from faker import Faker
from datetime import datetime
from commons.my_util import get_uuid


@auto_str
class OrderGenerator:
    """
    Order OrderGenerator
    """
    
    def __init__(self, city_map: CityMap):
        self.city_map = city_map
        self.faker = Faker()
        self.ids = 0
    
    def get_order(self, start_time=datetime.now(),
                  end_time=datetime.now(), use_density=False) -> Order:
        """
        Create and initialize an Order instance on the given map
        
        :return: a Order instance
        """
        self.ids += 1
        if use_density is False:
            start_location = self.city_map.generate_random_coord()
            end_location = self.city_map.generate_random_coord()
            fake_time = self.faker.date_time_between(start_date=start_time,
                                                     end_date=end_time)
            return Order(order_id=self.ids, uuid=get_uuid(), start_location=start_location, end_location=end_location,
                         time=fake_time)
        else:
            # TODO: generate orders using population density (end location)
            pass
        
        
if __name__ == '__main__':
    t_city_map = CityMap(Coordinate(0, 100), Coordinate(100, 100), Coordinate(0, 0), Coordinate(100, 0))
    g = OrderGenerator(t_city_map)
    order = g.get_order()
    order.delivered()
    print(g.get_order(start_time=datetime.fromisoformat('2022-05-02 12:22:03.123'),
                      end_time=datetime.fromisoformat('2022-07-02 12:22:03.123')))
