from commons.decorators import auto_str
from cityMap.citymap import CityMap, Coordinate
from orders.order import Order
from faker import Faker
from datetime import datetime
from commons.configuration import ORDER_BASE_PATH
from commons.configuration import USE_LOCAL_ORDER
import csv
import pandas as pd


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
        Initialize Order instances on the given map

        :return: a list of Order instances
        """
        orders = []
        if USE_LOCAL_ORDER:
            orders = self.load_orders(num_orders=num)
        if len(orders) != 0:
            return orders
        else:
            return self.generate_orders(num=num, start_time=start_time, end_time=end_time, bias=bias)
        
    def generate_orders(self, num, start_time=datetime.now(), end_time=datetime.now(), bias=True):
        orders = []
        start_coords = self.city_map.get_coord(num=num, bias=bias)  # restaurant
        end_coords = self.city_map.get_coord(num=num, bias=bias)  # customers
        for i in range(num):
            self.ids += 1
            fake_time = self.faker.date_time_between(start_date=start_time,
                                                     end_date=end_time)
            order = Order(order_id=self.ids,
                          start_location=start_coords[i], end_location=end_coords[i],
                          time=fake_time, description="")
            orders.append(order)
        return orders
    
    def save_orders(self, num, start_time=datetime.now(), end_time=datetime.now(), bias=True):
        orders = self.get_orders(num, start_time, end_time, bias)
        orders_list = []
        for order in orders:
            orders_list.append([order.order_id,
                                order.start_location.latitude, order.start_location.longitude,
                                order.end_location.latitude, order.end_location.longitude,
                                order.generate_time, order.description])
        fields = ['Order ID',
                  'Start Latitude', 'Start Longitude',
                  'End Latitude', 'End Longitude',
                  'Generate Time', 'Description']
        path = ORDER_BASE_PATH
        with open(path, 'w') as f:
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(orders_list)
            print(f'Done writing orders data to \'{path}\'')
            f.flush()
            f.close()
    
    def load_orders(self, num_orders):
        print(f'Loading orders data from \'{ORDER_BASE_PATH}\'')
        order_df = pd.read_csv(ORDER_BASE_PATH)
        print(f'Done loading orders data from \'{ORDER_BASE_PATH}\'')
        orders = []
        print(f'Initializing orders from local data...')
        for i, line in order_df.iterrows():
            if i >= num_orders:
                break
            order = Order(order_id=line['Order ID'],
                          start_location=Coordinate(line['Start Latitude'], line['Start Longitude']),
                          end_location=Coordinate(line['End Latitude'], line['End Longitude']),
                          time=line['Generate Time'],
                          description=line['Description'])
            orders.append(order)
            
        print(f'Done initializing orders')
        return orders
