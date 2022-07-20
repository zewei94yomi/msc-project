import random
from commons.decorators import auto_str
from commons.configuration import CRS, GEO_PATH, PD_PATH, RANDOM_LA_COORD_OFFSET, RANDOM_LO_COORD_OFFSET
import pandas as pd
import geopandas as gpd
import numpy as np
from typing import List


class Coordinate:
    """
    Coordinate of a location on maps.
    
    (latitude, longitude)
    """
    
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude    # y
        self.longitude = longitude  # x
    
    def __eq__(self, other):
        return self.latitude == other.latitude and self.longitude == other.longitude
    
    def __sub__(self, other):
        return self.latitude - other.latitude, self.longitude - other.longitude
    
    def __str__(self):
        return f"[la={self.latitude}, lo={self.longitude}]"


@auto_str
class CityMap:
    """ The city map of drones food delivery """
    
    def __init__(self, left: float, right: float, bottom: float, top: float):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        self.geo = gpd.read_file(GEO_PATH)
        self.pd_data = pd.read_csv(PD_PATH)
        pd_sum = self.pd_data['Population_Density_in_2010'].sum()
        self.pd_prob = [x / pd_sum for x in self.pd_data['Population_Density_in_2010']]
    
    def get_coord(self, num, bias=True) -> List[Coordinate]:
        """
        Generate a list of coordinates.
        
        :param num: the number of coordinates that need to be generated
        :param bias: whether bias coordinates to population density distribution
        :return: a list of coordinates
        """
        if bias:
            return self.get_n_bias_coord(num)
        else:
            return self.get_n_random_coord(num)
    
    def get_n_random_coord(self, num) -> List[Coordinate]:
        """
        Generate a list of random coordinates on the given map
        :return: a list of random Coordinate
        """
        coords = list()
        for i in range(num):
            latitude = self.bottom + random.random() * (self.top - self.bottom)
            longitude = self.left + random.random() * (self.right - self.left)
            coords.append(Coordinate(latitude=latitude, longitude=longitude))
        return coords
    
    def get_n_bias_coord(self, num) -> List[Coordinate]:
        """
        Generate a list of coordinate bias to population density distribution
        :return: a list of biased coordinates
        """
        count = 0
        pop_coords = list()
        while count < num:
            tracts = np.random.choice(self.pd_data['tract'], num - count, p=self.pd_prob)
            for tract in tracts:
                geo = self.geo[self.geo['id2'] == tract]
                if geo.empty is False:
                    centroid = geo.to_crs(CRS).centroid.to_crs(self.geo.crs).values[0]
                    centroid_lo = centroid.x + random.uniform(-RANDOM_LO_COORD_OFFSET, RANDOM_LO_COORD_OFFSET)
                    centroid_la = centroid.y + random.uniform(-RANDOM_LA_COORD_OFFSET, RANDOM_LA_COORD_OFFSET)
                    pop_coords.append(Coordinate(latitude=centroid_la, longitude=centroid_lo))
                    count += 1
        return pop_coords
        

if __name__ == '__main__':
    city_map = CityMap(left=0, right=40, bottom=0, top=40)
    print(city_map)
    t1 = Coordinate(1, 2)
    t2 = Coordinate(1, 4)
    print("t1: " + str(t1))
    print("t2: " + str(t2))
    print(t1 - t2)
