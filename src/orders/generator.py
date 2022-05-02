from commons.coordinate import Coordinate
from commons.auto_str import auto_str
from commons.map import Map
from orders.order import Order
from faker import Faker
from datetime import datetime


@auto_str
class Generator:
    """
    Order Generator
    """
    
    def __init__(self, map: Map):
        self.map = map
        self.faker = Faker()
    
    def get_order(self, start_time=datetime.now(),
                  end_time=datetime.now(), use_density=False) -> Order:
        """
        Generate an orders on the given map
        
        :return: a Order instance
        """
        if use_density is False:
            start_loc = self.map.generate_random_coord()
            end_loc = self.map.generate_random_coord()
            fake_time = self.faker.date_time_between(start_date=start_time,
                                                     end_date=end_time)
            return Order(start_loc=start_loc, end_loc=end_loc, time=fake_time)
        else:
            # TODO: generate orders using population density (end location)
            pass


if __name__ == '__main__':
    map = Map(Coordinate(0, 100), Coordinate(100, 100), Coordinate(0, 0), Coordinate(100, 0))
    
    g = Generator(map)
    print(g)
    print(g.get_order(start_time=datetime.fromisoformat('2022-05-02 12:22:03.123'),
                      end_time=datetime.fromisoformat('2022-07-02 12:22:03.123')))
    print(g.get_order())
    orders = []
    for i in range(10):
        orders.append(g.get_order())
    for order in orders:
        print(order)
