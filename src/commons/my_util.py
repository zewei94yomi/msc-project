import shortuuid
import math
from commons.citymap import Coordinate
import numpy as np


def get_uuid():
    return shortuuid.ShortUUID(alphabet="0123456789").random(8)


def distance(c1: Coordinate, c2: Coordinate):
    """
    Calculate distance between two coordinates
    
    :param c1: current coordinate
    :param c2: another coordinate in the distance
    :return:
        1. lo_distance: the longitude distance from c1 to c2
        2. la_distance: the latitude distance from c1 to c2
        3. line_distance: the straight-line distance from c1 to c2
    """
    lo_distance, la_distance = c2 - c1
    line_distance = math.sqrt(math.pow(lo_distance, 2) + math.pow(la_distance, 2))
    return lo_distance, la_distance, line_distance
    
    
def nearest_neighbor(neighbors, target: Coordinate) -> Coordinate:
    """
    Find the nearest neighbor to the target location.
    
    :param neighbors: All candidate neighbors around the target
    :param target:  The target location
    :return: The location of the nearest neighbor
    """
    min_distance = float('inf')
    nearest = None
    for neighbor in neighbors:
        _, _, line_distance = distance(neighbor, target)
        if line_distance < min_distance:
            nearest = neighbor
            min_distance = line_distance
    return nearest


def nearest_neighbor_idx(neighbors, target: Coordinate) -> int:
    """
    Find the index of the nearest neighbor to the target location.

    :param neighbors: All candidate neighbors around the target
    :param target:  The target location
    :return: The index of the nearest neighbor
    """
    distances = []
    for neighbor in neighbors:
        _, _, line_distance = distance(neighbor, target)
        distances.append(line_distance)
    return np.argmin(distances)


if __name__ == '__main__':
    print("Main test...")