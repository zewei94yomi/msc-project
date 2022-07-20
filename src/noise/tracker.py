from commons.decorators import auto_str
from commons.my_util import calculate_noise_m
from commons.constants import M_2_LATITUDE, M_2_LONGITUDE
from commons.configuration import NOISE_BASE_PATH, TRACKER_ITERATIONS, SAVE_CSV
from commons.configuration import TRACK_NOISE_THRESHOLD, NOISE_CELL_LENGTH, NOISE_CELL_WIDTH, NOISE_CELL_NUM
from drones.drone import Drone
from datetime import datetime
import csv


@auto_str
class NoiseTracker:
    """Deprecated, use 'DensityMatrix'"""
    def __init__(self):
        self.noise = list()     # [latitude, longitude, noise, step slice]
        self.TIME_GAP = TRACKER_ITERATIONS
        self.time_slice = 0
        self.BASE_PATH = NOISE_BASE_PATH

    def track_noise(self, drone: Drone):
        la = drone.location.latitude
        lo = drone.location.longitude
        self.radiate(latitude=la, longitude=lo, noise=drone.NOISE)
    
    def radiate(self, latitude, longitude, noise):
        self.noise.append([latitude, longitude, noise, self.time_slice])
        for i in range(1, NOISE_CELL_NUM):
            x_dist = i * NOISE_CELL_LENGTH
            la_diff = x_dist * M_2_LATITUDE
            for j in range(1, NOISE_CELL_NUM):
                y_dist = j * NOISE_CELL_WIDTH
                lo_diff = y_dist * M_2_LONGITUDE
                new_noise = calculate_noise_m(x_dist=x_dist, y_dist=y_dist, central_noise=noise)
                if new_noise >= TRACK_NOISE_THRESHOLD:
                    self.noise.append([latitude + la_diff, longitude + lo_diff, new_noise, self.time_slice])
                    self.noise.append([latitude + la_diff, longitude - lo_diff, new_noise, self.time_slice])
                    self.noise.append([latitude - la_diff, longitude + lo_diff, new_noise, self.time_slice])
                    self.noise.append([latitude - la_diff, longitude - lo_diff, new_noise, self.time_slice])
        for i in range(1, NOISE_CELL_NUM):
            y_dist = i * NOISE_CELL_WIDTH
            la_diff = y_dist * M_2_LATITUDE
            la_new_noise = calculate_noise_m(x_dist=0, y_dist=y_dist, central_noise=noise)
            if la_new_noise >= TRACK_NOISE_THRESHOLD:
                self.noise.append([latitude + la_diff, longitude, la_new_noise, self.time_slice])
                self.noise.append([latitude - la_diff, longitude, la_new_noise, self.time_slice])
            x_dist = i * NOISE_CELL_LENGTH
            lo_diff = x_dist * M_2_LONGITUDE
            lo_new_noise = calculate_noise_m(x_dist=x_dist, y_dist=0, central_noise=noise)
            if lo_new_noise >= TRACK_NOISE_THRESHOLD:
                self.noise.append([latitude, longitude + lo_diff, lo_new_noise, self.time_slice])
                self.noise.append([latitude, longitude - lo_diff, lo_new_noise, self.time_slice])

    def save_noise(self):
        t = datetime.now().strftime("%m-%d_%H:%M:%S")
        file_path = self.BASE_PATH + "/" + t
        fields = ['Latitude', 'Longitude', 'Noise', 'Time Slice']
        with open(file_path, 'w') as f:
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(self.noise)
            print(f'Done writing noise data to \'{t}.csv\'')
            f.flush()
            f.close()
        
    def update_time_count(self):
        self.time_slice += 1
        if self.time_slice >= self.TIME_GAP:
            if SAVE_CSV:
                self.save_noise()
            self.time_slice = 0
            self.noise.clear()


if __name__ == '__main__':
    nt = NoiseTracker()
    nt.radiate(50, 50, 90)
    print(len(nt.noise))
