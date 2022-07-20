from commons.decorators import auto_str
from commons.configuration import NOISE_CELL_LENGTH, NOISE_CELL_WIDTH
from commons.configuration import MAP_LEFT, MAP_RIGHT, MAP_TOP, MAP_BOTTOM
from commons.configuration import MATRIX_BASE_PATH
from commons.configuration import OVERLAY_BASE_PATH, GEO_PATH, PD_PATH, CRS
from commons.configuration import style_function, highlight_function
from commons.constants import M_2_LONGITUDE, M_2_LATITUDE
from commons.my_util import multi_source_sound_level, distance_coordinates, calculate_noise_coord
from cityMap.citymap import Coordinate
import math
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime
import geopandas as gpd
import pandas as pd
import os
import folium
from folium.raster_layers import ImageOverlay


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
                    lat_dist, lon_dist, line_dist = distance_coordinates(cell.centroid, drone.location)
                    if line_dist == 0:
                        noise = drone.NOISE
                    else:
                        noise = calculate_noise_coord(x_dist=lon_dist, y_dist=lat_dist, central_noise=drone.NOISE)
                    noises.append(noise)
                mixed_noise = multi_source_sound_level(noises)
                cell.receive_noise(mixed_noise)
    
    def calculate_std(self, time_count):
        return np.std(self.get_average_matrix(time_count))
    
    def plot_matrix(self, time_count):
        """
        Plot a maximum and an average density matrix in 'time_count'.
        
        :param time_count: a period of step
        :return:
        """
        la = np.linspace(self.top, self.bottom, self.rows)
        lo = np.linspace(self.left, self.right, self.cols)
        avg_noises = [[self.matrix[i][j].total_noise / time_count for j in range(self.cols)] for i in range(self.rows)]
        max_noises = [[self.matrix[i][j].max_noise for j in range(self.cols)] for i in range(self.rows)]
        Z_avg = np.array(avg_noises)
        Z_max = np.array(max_noises)
        X, Y = np.meshgrid(lo, la)
        time = datetime.now().strftime("%m-%d_%H:%M:%S")
        avg_title = f"Average Noise Matrix in {time_count}, std={self.calculate_std(time_count)}"
        max_title = f"Maximum Noise Matrix in {time_count}"
        avg_path = MATRIX_BASE_PATH + "/images/average/" + time
        max_path = MATRIX_BASE_PATH + "/images/maximum/" + time
        self.plot_pcolormesh(X, Y, Z_avg, avg_title, avg_path)
        self.plot_pcolormesh(X, Y, Z_max, max_title, max_path)
        self.overlay()

    def plot_pcolormesh(self, X, Y, Z, title, path):
        fig, ax = plt.subplots()
        plt.pcolormesh(X, Y, Z)
        plt.colorbar()
        plt.title(title)
        plt.savefig(path, bbox_inches='tight')
        plt.close()
    
    def overlay(self):
        geo = gpd.read_file(GEO_PATH)
        pd_data = pd.read_csv(PD_PATH)
        popup = geo.merge(pd_data, left_on="id2", right_on="tract")
        threshold_scale = list(pd_data["Population_Density_in_2010"].quantile([0, 0.2, 0.4, 0.6, 0.8, 1]))
        x_center = geo.to_crs(CRS).centroid.to_crs(geo.crs).x.mean()
        y_center = geo.to_crs(CRS).centroid.to_crs(geo.crs).y.mean()
        directory_path = MATRIX_BASE_PATH + '/images'
        max_path = directory_path + '/maximum'
        avg_path = directory_path + '/average'
        for filename in os.listdir(max_path):
            mymap = folium.Map(location=[y_center, x_center], zoom_start=13)
            folium.TileLayer('CartoDB positron', name="Light Map", control=False).add_to(mymap)
            folium.Choropleth(
                geo_data=popup,
                name='Choropleth',
                data=pd_data,
                columns=['tract', 'Population_Density_in_2010'],
                key_on="properties.id2",
                fill_color='YlGnBu',
                fill_opacity=0.7,
                line_opacity=0.2,
                threshold_scale=threshold_scale,
                legend_name='Population Density',
                smooth_factor=0
            ).add_to(mymap)
    
            NIL = folium.features.GeoJson(
                popup,
                style_function=style_function,
                control=False,
                highlight_function=highlight_function,
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['tract', 'Name', 'Population_Density_in_2010'],
                    aliases=['Tract: ', 'Name: ', 'Population Density (people in per sq mi): '],
                    style="background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;"
                )
            )
            mymap.add_child(NIL)
            mymap.keep_in_front(NIL)

            max_img_path = max_path + "/" + filename
            average_img_path = avg_path + "/" + filename
            ImageOverlay(max_img_path,
                         [[MAP_BOTTOM * 0.9998, MAP_LEFT * 1.00018], [MAP_TOP * 1.00015, MAP_RIGHT * 0.99955]],
                         name='maximum',
                         opacity=0.8,
                         ).add_to(mymap)
            ImageOverlay(average_img_path,
                         [[MAP_BOTTOM * 0.9998, MAP_LEFT * 1.00018], [MAP_TOP * 1.00015, MAP_RIGHT * 0.99955]],
                         name='average',
                         opacity=0.8,
                         ).add_to(mymap)
            folium.LayerControl().add_to(mymap)
            html_path = MATRIX_BASE_PATH + "/html/" + filename.split('.')[0] + ".html"
            print(f"Done loading maximum and average density matrix")
            mymap.save(html_path)
            print(f"Done saving overlay image to \'{filename.split('.')[0]}.html\'")
