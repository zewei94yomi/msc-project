from commons.decorators import auto_str
from cityMap.citymap import Coordinate
from drones.drone import Drone
import threading
import folium
from folium.plugins import HeatMap
from datetime import datetime


@auto_str
class NoiseTracker:
    
    def __init__(self):
        self.noise = list()
        self.timer = threading.Timer(10, self.heatMap)
        self.timer.start()
        self.min_noise = float('inf')
        self.max_noise = float('-inf')

    def trackNoise(self, drone: Drone):
        la = drone.current_location.latitude
        lo = drone.current_location.longitude
        noise = drone.produce_noise()
        self.max_noise = max(self.max_noise, noise)
        self.min_noise = min(self.min_noise, noise)
        self.noise.append([la, lo, noise])
    
    def roundCoord(self, coord: Coordinate):
        pass
    
    def heatMap(self):
        China_map = folium.Map(
            location=[37.7749, -122.4194],  # location 经纬度 [纬度,经度]
            zoom_start=13,  # 初始地图大小
            tiles='OpenStreetMap')
        HeatMap(self.noise).add_to(China_map)
        China_map.add_child(folium.LatLngPopup())
        now = datetime.now()
        name = now.strftime("%m-%d_%H-%M-%S")
        China_map.save('noise/HeatMaps/' + name + '.html')  # 保存为HTML
        print("New heat map has been saved to local")
        self.timer = threading.Timer(10, self.heatMap)
        self.timer.start()
    
    def rescale(self):
        return [[x[0], x[1], (x[2] - self.min_noise) / (self.max_noise - self.min_noise)] for x in self.noise]
    
    
if __name__ == '__main__':
    n = NoiseTracker()
    print(n)
