import math
from cityMap.citymap import Coordinate
import numpy as np
from typing import List
import random
from commons.constants import M_2_LATITUDE, M_2_LONGITUDE


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
    """
    Find the nearest drone among free drones to a given order

    :param order: the target order
    :param free_drones: all free drones that can chosen from
    :return the nearest drone
    """
    return free_drones[nearest_neighbor_idx(
        neighbors=[x.location for x in free_drones],
        target=order.start_location)]


def offset_coordinate(coordinate: Coordinate, la_range, lo_range):
    coordinate.latitude += random.uniform(-la_range, la_range)
    coordinate.longitude += random.uniform(-lo_range, lo_range)


def calculate_noise_m(x_dist, y_dist, central_noise):
    """
    Calculate the noise at distance.
    
    :param x_dist: x-axis distance to center x in meters
    :param y_dist: y-axis distance to center y
    :param central_noise: the center noise level
    :return: the noise at (center_x + x_dist, center_y + y_dist)
    """
    return central_noise - math.fabs(10 * math.log10(math.pow(x_dist, 2) + math.pow(y_dist, 2)))


def calculate_noise_coord(x_dist, y_dist, central_noise):
    """
    Calculate the noise at distance.

    :param x_dist: x-axis distance to center x in longitude
    :param y_dist: y-axis distance to center y in latitude
    :param central_noise: the center noise level
    :return: the noise at (center_x + x_dist, center_y + y_dist)
    """
    return central_noise - math.fabs(10 * math.log10(math.pow(x_dist / M_2_LONGITUDE, 2) +
                                                     math.pow(y_dist / M_2_LATITUDE, 2)))

    
def difference(list1, list2):
    """Return a list of elements that in list1 but not in list2"""
    return list(set(list1).difference(set(list2)))


def union(list1, list2):
    """Return a list of elements that in list1 or list2"""
    return list(set(list1).union(set(list2)))


def intersection(list1, list2):
    """Return a list of elements that in both list1 and list2"""
    return list(set(list1).intersection(set(list2)))


def multi_source_sound_level(sources):
    """
    Calculate the mixed sound level from multiple sound sources
    
    :param sources: a list of sound level
    :return: the mixed sound level
    """
    if sources is None or len(sources) == 0:
        return 0
    summation = 0
    for source in sources:
        summation += np.power(10, source / 10)
    return 10 * np.log10(summation)
