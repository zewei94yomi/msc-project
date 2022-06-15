import shortuuid
import math
from cityMap.citymap import Coordinate
import numpy as np
from typing import List


def get_uuid():
    """Create a unique numeric UID with a length of 8"""
    return shortuuid.ShortUUID(alphabet="0123456789").random(8)


def distance(c1: Coordinate, c2: Coordinate):
    """
    Calculate distances between two coordinates
    
    :param c1: current coordinate
    :param c2: another coordinate
    :return:
        1. la_distance: latitude distance from c1 to c2
        2. lo_distance: longitude distance from c1 to c2
        3. line_distance: straight-line distance from c1 to c2
    """
    la_distance, lo_distance = c2 - c1
    line_distance = math.sqrt(math.pow(la_distance, 2) + math.pow(lo_distance, 2))
    return la_distance, lo_distance, line_distance
    

def nearest_neighbor_idx(neighbors: List[Coordinate], target: Coordinate) -> int:
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
    
    
def nearest_neighbor(neighbors: List[Coordinate], target: Coordinate) -> Coordinate:
    """
    Find the nearest neighbor to the target location.
    
    :param neighbors: All candidate neighbors around the target
    :param target:  The target location
    :return: The location of the nearest neighbor
    """
    return neighbors[nearest_neighbor_idx(neighbors, target)]


def nearest_free_drone(order, free_drones):
    """Find the nearest drone among free drones to a given order
    
    :param order: the target order
    :param free_drones: all free drones that can chosen from
    :return the nearest drone
    """
    return free_drones[nearest_neighbor_idx(
        neighbors=[x.current_location for x in free_drones],
        target=order.start_location)]


if __name__ == '__main__':
    print("My Util test...")