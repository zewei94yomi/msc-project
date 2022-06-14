from commons.decorators import auto_str
from cityMap.citymap import Coordinate
from drones.drone import Drone


@auto_str
class NoiseTracker:
    
    def __init__(self):
        self.noise = list()

    def trackNoise(self, drone: Drone):
        lo = drone.current_location.longitude
        la = drone.current_location.latitude
        self.noise.append([lo, la, drone.produce_noise()])
    
    def roundCoord(self, coord: Coordinate):
        pass
    
    def getNoiseData(self):
        return self.noise
        
    
if __name__ == '__main__':
    n = NoiseTracker()
    print(n)
