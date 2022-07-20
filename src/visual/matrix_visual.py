from commons.decorators import auto_str
from commons.configuration import NOISE_BASE_PATH, HEATMAP_BASE_PATH
from commons.configuration import TRACKER_ITERATIONS, NOISE_CELL_LENGTH, NOISE_CELL_WIDTH
from commons.configuration import MAP_LEFT, MAP_RIGHT, MAP_TOP, MAP_BOTTOM
from commons.constants import M_2_LONGITUDE, M_2_LATITUDE
from commons.my_util import multi_source_sound_level
import math
import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


@auto_str
class Cell:
    def __init__(self):
        self.noise = list()
        self.temp_noise = list()
    
    def receive_noise(self, noise):
        self.temp_noise.append(noise)
    
    def reset(self):
        self.temp_noise.clear()
        self.noise.clear()
    
    def update_noise(self):
        if len(self.temp_noise) == 1:
            self.noise.append(self.temp_noise[0])
        elif len(self.temp_noise) > 1:
            mix_noise = multi_source_sound_level(self.temp_noise)
            self.noise.append(mix_noise)
        self.temp_noise.clear()


@auto_str
class DensityMatrix:
    def __init__(self):
        self.left = MAP_LEFT
        self.right = MAP_RIGHT
        self.top = MAP_TOP
        self.bottom = MAP_BOTTOM
        self.TIME_GAP = TRACKER_ITERATIONS
        self.cell_length_m = NOISE_CELL_LENGTH
        self.cell_width_m = NOISE_CELL_WIDTH
        self.cell_length_lo = self.cell_length_m * M_2_LONGITUDE
        self.cell_width_la = self.cell_width_m * M_2_LATITUDE
        self.rows = math.floor((MAP_TOP - MAP_BOTTOM) / self.cell_width_la)
        self.cols = math.floor((MAP_RIGHT - MAP_LEFT) / self.cell_length_lo)
        self.matrix = [[Cell() for j in range(self.cols)] for i in range(self.rows)]
    
    def is_valid(self, longitude, latitude):
        if longitude >= self.right or longitude < self.left:
            return False
        if latitude >= self.top or latitude < self.bottom:
            return False
        return True
    
    def get_cell(self, longitude, latitude):
        if self.is_valid(longitude, latitude) is False:
            print(f"WARNING: No cell is found at ({longitude}, {latitude})")
            return None
        else:
            row = math.floor(abs(latitude - self.top) / (self.cell_width_m * M_2_LATITUDE))
            col = math.floor(abs(longitude - self.left) / (self.cell_length_m * M_2_LONGITUDE))
            return self.matrix[row][col]
    
    def save_temp_noise(self, longitude, latitude, noise):
        cell = self.get_cell(longitude, latitude)
        if cell is not None:
            cell.receive_noise(noise)
    
    def reset(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j].reset()
    
    def update_all(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.matrix[i][j].update_noise()
    
    def load_data(self, file_path):
        noise_df = pd.read_csv(file_path)
        prev_time_slice = 0
        for i, line in noise_df.iterrows():
            la, lo, noise, time_slice = line['Latitude'], line['Longitude'], line['Noise'], line['Time Slice']
            if time_slice != prev_time_slice:
                self.update_all()
                prev_time_slice = time_slice
            else:
                self.save_temp_noise(longitude=lo, latitude=la, noise=noise)
        print(f"Done loading data from \'{file_path}\'")
    
    def calculate_maximum(self, file_name):
        la = np.linspace(self.top, self.bottom, self.rows)
        lo = np.linspace(self.left, self.right, self.cols)
        noise = [[0 for x in range(self.cols)] for y in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                if len(self.matrix[i][j].noise) == 0:
                    noise[i][j] = 0
                else:
                    noise[i][j] = max(self.matrix[i][j].noise)
        Z = np.array(noise)
        X, Y = np.meshgrid(lo, la)
        save_path = "../" + HEATMAP_BASE_PATH + "/matplotlib/maximum/" + file_name
        title = "Maximum Noise Level in " + str(TRACKER_ITERATIONS) + " step slice"
        self.plot_pcolormesh(X, Y, Z, 10, 100, title, save_path)
        
    def calculate_average(self, file_name):
        la = np.linspace(self.top, self.bottom, self.rows)
        lo = np.linspace(self.left, self.right, self.cols)
        noise = [[0 for x in range(self.cols)] for y in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                if len(self.matrix[i][j].noise) == 0:
                    noise[i][j] = 0
                else:
                    noise[i][j] = sum(self.matrix[i][j].noise) / self.TIME_GAP
        Z = np.array(noise)
        X, Y = np.meshgrid(lo, la)
        save_path = "../" + HEATMAP_BASE_PATH + "/matplotlib/average/" + file_name
        title = "Average Noise Level in " + str(TRACKER_ITERATIONS) + " step slice"
        self.plot_pcolormesh(X, Y, Z, 10, 100, title, save_path)
        
    def plot_pcolormesh(self, X, Y, Z, colorbar_min, colorbar_max, title, save_path):
        plt.pcolormesh(X, Y, Z)
        plt.colorbar()
        plt.clim(colorbar_min, colorbar_max)
        plt.title(title)
        plt.savefig(save_path, bbox_inches='tight')
        print(f"Done saving noise density matrix map to \'{save_path}\'")
        plt.close()
        
    def generate_matrix(self):
        directory_path = "../" + NOISE_BASE_PATH
        for filename in os.listdir(directory_path):
            file_path = directory_path + "/" + filename
            self.load_data(file_path=file_path)
            self.calculate_average(file_name=filename)
            self.calculate_maximum(file_name=filename)
            self.reset()


if __name__ == '__main__':
    dm = DensityMatrix()
    dm.generate_matrix()
