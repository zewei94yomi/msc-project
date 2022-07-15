from commons.decorators import auto_str
from cityMap.citymap import CityMap
from orders.order import Order
from faker import Faker
from datetime import datetime


@auto_str
class OrderGenerator:
    """
    Order OrderGenerator
    """
    
    def __init__(self, city_map: CityMap):
        self.city_map = city_map
        self.faker = Faker()
        self.ids = 0
    
    def get_orders(self, num, start_time=datetime.now(), end_time=datetime.now(), bias=True):
        """
        Create and initialize Order instances on the given map

        :return: a Order instance
        """
        self.ids += 1
        orders = list()
        start_coords = self.city_map.get_coord(num=num, bias=bias)  # restaurant
        end_coords = self.city_map.get_coord(num=num, bias=bias)    # customers
        for i in range(num):
            fake_time = self.faker.date_time_between(start_date=start_time,
                                                     end_date=end_time)
            order = Order(order_id=self.ids,
                          start_location=start_coords[i], end_location=end_coords[i],
                          time=fake_time)
            orders.append(order)
        return orders
