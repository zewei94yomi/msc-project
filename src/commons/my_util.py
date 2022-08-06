import math
from cityMap.citymap import Coordinate
import numpy as np
from typing import List
import random
from commons.constants import M_2_LATITUDE, M_2_LONGITUDE, DRONE_NOISE
from matplotlib import pyplot as plt
import seaborn as sns


def offset_coordinate(coordinate: Coordinate, la_range, lo_range):
    """
    Add offset to a coordinate.
    
    :param coordinate:
    :param la_range: latitude offset range (0, la_range)
    :param lo_range: longitude offset range (0, lo_range)
    :return: An offset coordinate
    """
    coordinate.latitude += random.uniform(-la_range, la_range)
    coordinate.longitude += random.uniform(-lo_range, lo_range)


def distance(c1: Coordinate, c2: Coordinate):
    """
    Calculate distances between two coordinates

    :param c1: current coordinate
    :param c2: another coordinate
    :return:
        1. la_distance: latitude distance from c1 to c2 in latitude
        2. lo_distance: longitude distance from c1 to c2 in longitude
        3. meter_distance: straight-line distance from c1 to c2 in meters
    """
    la_distance, lo_distance = c2 - c1
    meter_distance = math.sqrt(math.pow(la_distance / M_2_LATITUDE, 2) + math.pow(lo_distance / M_2_LONGITUDE, 2))
    return la_distance, lo_distance, meter_distance


def straight_distance_matrix(row1, col1, row2, col2):
    """Calculate the straight distance in matrix"""
    dx = abs(col1 - col2)
    dy = abs(row1 - row2)
    return math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))


def diagonal_distance_matrix(row1, col1, row2, col2):
    """Calculate the diagonal distance in matrix"""
    dx = abs(col1 - col2)
    dy = abs(row1 - row2)
    return math.sqrt(2) * min(dx, dy) + abs(dx - dy)


def difference(list1, list2):
    """Return a list of elements that in list1 but not in list2"""
    return list(set(list1).difference(set(list2)))


def union(list1, list2):
    """Return a list of elements that in list1 or list2"""
    return list(set(list1).union(set(list2)))


def intersection(list1, list2):
    """Return a list of elements that in both list1 and list2"""
    return list(set(list1).intersection(set(list2)))


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


def heuristic(row1, col1, row2, col2, step_cost):
    """
    Heuristic function calculates heuristic cost from (row1, col1) to (row2, col2) with a given step cost.
    
    :param row1: row index of node1
    :param col1: column index of node1
    :param row2: row index of node2
    :param col2: column index of node2
    :param step_cost: movement cost
    :return: heuristic cost
    """
    d = straight_distance_matrix(row1, col1, row2, col2)
    return step_cost * d


def cost_1(row1, col1, row2, col2, avg_matrix, priority_K):
    """
    Calculate the expansion cost from parent node to child node.
    
    :param row1: parent node row
    :param col1: parent node col
    :param row2: child node row
    :param col2: child node col
    :param avg_matrix: average-noise matrix
    :param priority_K: priority parameter, K
    :return: cost from parent to child
    """
    d = diagonal_distance_matrix(row1, col1, row2, col2)
    expand_cost = d * DRONE_NOISE + priority_K * avg_matrix[row2][col2]
    return expand_cost


def cost_2(row1, col1, row2, col2, avg_matrix, priority_P):
    """
    Calculate the expansion cost from parent node to child node.

    :param row1: parent node row
    :param col1: parent node col
    :param row2: child node row
    :param col2: child node col
    :param avg_matrix: average-noise matrix
    :param priority_P: priority parameter, P
    :return: cost from parent to child
    """
    d = diagonal_distance_matrix(row1, col1, row2, col2)
    expand_cost = d * DRONE_NOISE + math.pow(avg_matrix[row2][col2], priority_P)
    return expand_cost


def backtrack(row0, col0, current):
    """
    Find the path from the current node to the start node.
    
    :param row0: row index of the initial node
    :param col0: column index of the initial node
    :param current: current node
    :return: a path, i.e., a list of nodes
    """
    grid_path = []
    row, col = current.row, current.col
    while row != row0 or col != col0:
        grid_path.insert(0, [row, col])
        p_node = current.parent
        if p_node is not None:
            current = p_node
            row, col = current.row, current.col
        else:
            break
    grid_path.insert(0, [row, col])
    return grid_path


def pop_lowest_priority(open_nodes: List):
    """
    Pop the node with the lowest priority.
    
    :param open_nodes: a list of nodes
    :return: A node with the lowest priority in the list
    """
    min_priority = float('inf')
    min_index = 0
    for i in range(len(open_nodes)):
        node = open_nodes[i]
        if node.fn < min_priority:
            min_priority = node.fn
            min_index = i
    return open_nodes.pop(min_index)


def find_node(row, col, open_nodes: List):
    """
    Find a node in a 2d array.
    
    :param row: row index
    :param col: column index
    :param open_nodes: 2d array
    :return: open_nodes[row][col]
    """
    idx = -1
    for i in range(len(open_nodes)):
        if open_nodes[i].row == row and open_nodes[i].col == col:
            idx = i
            break
    if idx != -1:
        return open_nodes[idx]
    else:
        return None


def plot_matrix(X, Y, Z, title, path, color_min, color_max):
    """
    Plot a density matrix.
    
    :param X: X-axis in pcolormesh
    :param Y: Y-axis in pcolormesh
    :param Z: Z-axis (data) in pcolormesh
    :param title: figure title
    :param path: figure saving path
    :param color_min: min value of color bar
    :param color_max: max value of color bar
    :return:
    """
    fig, ax = plt.subplots()
    plt.pcolormesh(X, Y, Z)
    plt.colorbar()
    plt.clim(vmin=color_min, vmax=color_max)
    plt.title(title)
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    

def plot_histogram(data, title, path, y_bottom, y_top):
    """
    Plot a histogram.
    
    :param data: histogram data (from a pandas dataframe)
    :param title: figure title
    :param path: figure saving path
    :param y_bottom: bottom bar value
    :param y_top: top bar value
    :return:
    """
    fig, ax = plt.subplots()
    plt.ylim(y_bottom, y_top)
    plt.title(title)
    sns.histplot(data=data, kde=True)
    plt.savefig(path, bbox_inches='tight')
    plt.close()
