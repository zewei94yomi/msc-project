from commons.decorators import auto_str
from commons.configuration import NOISE_CELL_LENGTH, NOISE_CELL_WIDTH
from commons.configuration import MAP_LEFT, MAP_RIGHT, MAP_TOP, MAP_BOTTOM
from commons.constants import M_2_LONGITUDE, M_2_LATITUDE
from commons.my_util import multi_source_sound_level, distance, calculate_noise_coord
from cityMap.citymap import Coordinate
import math
import numpy as np


@auto_str
class Cell:
    def __init__(self, latitude, longitude, row, col):
        self.row = row
        self.col = col
        self.centroid = Coordinate(latitude, longitude)
        self.total_noise = 0
        self.max_noise = 0
    
    def receive_noise(self, noise):
        """
        Cell receives a mixed noise and update its total and maximum noise.
        
        :param noise: a mixed noise
        :return:
        """
        self.total_noise += noise
        self.max_noise = max(self.max_noise, noise)
        
        
@auto_str
class DensityMatrix:
    def __init__(self):
        self.left = MAP_LEFT
        self.right = MAP_RIGHT
        self.top = MAP_TOP
        self.bottom = MAP_BOTTOM
        self.cell_length_m = NOISE_CELL_LENGTH
        self.cell_width_m = NOISE_CELL_WIDTH
        self.cell_length_lo = self.cell_length_m * M_2_LONGITUDE
        self.cell_width_la = self.cell_width_m * M_2_LATITUDE
        self.rows = math.floor((MAP_TOP - MAP_BOTTOM) / self.cell_width_la)
        self.cols = math.floor((MAP_RIGHT - MAP_LEFT) / self.cell_length_lo)
        self.matrix = [[Cell(latitude=self.top - (i + 1 / 2) * self.cell_width_la,
                             longitude=self.left + (j + 1 / 2) * self.cell_length_lo,
                             row=i, col=j)
                        for j in range(self.cols)] for i in range(self.rows)]

    def is_valid(self, longitude, latitude):
        if longitude >= self.right or longitude < self.left:
            return False
        if latitude >= self.top or latitude < self.bottom:
            return False
        return True
    
    def get_average_matrix(self, time_count):
        return np.array([[self.matrix[i][j].total_noise / time_count for j in range(self.cols)]
                         for i in range(self.rows)])
    
    def get_maximum_matrix(self):
        return np.array([[self.matrix[i][j].max_noise for j in range(self.cols)]
                         for i in range(self.rows)])
    
    def get_cell(self, coordinate: Coordinate):
        lon = coordinate.longitude
        lat = coordinate.latitude
        if self.is_valid(lon, lat) is False:
            print(f"WARNING: No cell is found at (lon:{lon}, lat:{lat})")
            return None
        else:
            row = math.floor(abs(lat - self.top) / (self.cell_width_m * M_2_LATITUDE))
            col = math.floor(abs(lon - self.left) / (self.cell_length_m * M_2_LONGITUDE))
            return self.matrix[row][col]
    
    def track_noise(self, drones):
        """
        The matrix tracks all drones' noise and record them to the matrix.
        
        :param drones: a list of working drones
        :return:
        """
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.matrix[i][j]
                noises = []
                for drone in drones:
                    lat_dist, lon_dist, line_dist = distance(cell.centroid, drone.location)
                    if line_dist == 0:
                        noise = drone.NOISE
                    else:
                        noise = calculate_noise_coord(x_dist=lon_dist, y_dist=lat_dist, central_noise=drone.NOISE)
                    noises.append(noise)
                mixed_noise = multi_source_sound_level(noises)
                cell.receive_noise(mixed_noise)
    
    def calculate_std(self, time_count):
        return np.std(self.get_average_matrix(time_count))
