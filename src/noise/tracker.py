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
        self.timer = threading.Timer(10, self.plot_heatmap)
        self.timer.start()
        self.min_noise = float('inf')
        self.max_noise = float('-inf')

    def track_noise(self, drone: Drone):
        la = drone.current_location.latitude
        lo = drone.current_location.longitude
        noise = drone.produce_noise()
        self.max_noise = max(self.max_noise, noise)
        self.min_noise = min(self.min_noise, noise)
        self.noise.append([la, lo, noise])
    
    def plot_heatmap(self):
        heatmap = folium.Map(
            location=[37.7629, -122.4394],  # [latitude, longitude]
            zoom_start=13,
            tiles='OpenStreetMap')
        HeatMap(self.noise, radius=13).add_to(heatmap)
        heatmap.add_child(folium.LatLngPopup())
        now = datetime.now()
        name = now.strftime("%m-%d_%H-%M-%S")
        heatmap.save('noise/HeatMaps/' + name + '.html')  # 保存为HTML
        print("New heatmap has been saved to local")
        self.timer = threading.Timer(10, self.plot_heatmap)
        self.timer.start()
    
    def rescale_noise(self):
        return [[x[0], x[1], (x[2] - self.min_noise) / (self.max_noise - self.min_noise)] for x in self.noise]
    
    
if __name__ == '__main__':
    n = NoiseTracker()
    print(n)
