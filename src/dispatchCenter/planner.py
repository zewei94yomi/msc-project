from noise.matrix import DensityMatrix
from cityMap.citymap import Coordinate
from commons.decorators import auto_str
from commons.my_util import heuristic, cost, pop_lowest_priority, find_node, backtrack
from commons.constants import DRONE_NOISE


@auto_str
class Node:
    def __init__(self, row, col, parent, gn, hn):
        self.row = row                  # row in the matrix
        self.col = col                  # col in the matrix
        self.parent = parent            # parent Node
        self.gn = gn                    # gn: actual cost
        self.hn = hn                    # hn: heuristic cost
        self.fn = self.gn + self.hn     # priority


@auto_str
class PathPlanner:
    def __init__(self, matrix: DensityMatrix):
        self.matrix = matrix
        
    def plan(self, start: Coordinate, end: Coordinate, time_count):
        """A-star search"""
        grid_path = []
        first_cell = self.matrix.get_cell(start)
        last_cell = self.matrix.get_cell(end)
        avg_matrix = self.matrix.get_average_matrix(time_count)
        
        open_nodes = list()  # [Node, Node, ...]
        close_nodes = set()  # {[row, col], ...}
        
        first_hn = heuristic(first_cell.row, first_cell.col, last_cell.row, last_cell.col, 0)
        first_node = Node(first_cell.row, first_cell.col, None, 0, first_hn)
        open_nodes.append(first_node)
        while len(open_nodes) != 0:
            # pop up the node with the lowest priority
            current = pop_lowest_priority(open_nodes)
            row, col = current.row, current.col
            if row == last_cell.row and col == last_cell.col:
                # if the current node is the end node:
                # find the path from the end node to the start node
                grid_path = backtrack(first_cell.row, first_cell.col, current)
                break
            else:
                # if the current node is not the end node
                close_nodes.add((row, col))  # mark the current position as visited
                children = self.expand(current)
                for child in children:
                    if (child.row, child.col) in close_nodes:
                        # this child has already been reached
                        continue
                    # TODO: consider population density
                    child_gn = current.gn + cost(current.row, current.col, child.row, child.col, avg_matrix)
                    child_hn = heuristic(child.row, child.col, last_cell.row, last_cell.col, DRONE_NOISE)
                    res_node = find_node(child.row, child.col, open_nodes)
                    if res_node is not None:
                        if res_node.gn > child_gn:
                            # Update res_node
                            res_node.parent = current
                            res_node.gn = child_gn
                            res_node.fn = res_node.gn + res_node.hn
                    else:
                        child.gn = child_gn
                        child.hn = child_hn
                        child.fn = child.gn + child.hn
                        open_nodes.append(child)
        real_path = []
        for row, col in grid_path:
            real_path.append(self.matrix.matrix[row][col].centroid)
        real_path.append(end)
        return real_path
    
    def expand(self, old_node):
        """Expand current node to 8 directions"""
        children = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_row = old_node.row + i
                new_col = old_node.col + j
                if new_row == old_node.row and new_col == old_node.col:
                    continue
                if 0 <= new_row < self.matrix.rows and 0 <= new_col < self.matrix.cols:
                    children.append(Node(new_row, new_col, old_node, 0, 0))
        return children


if __name__ == '__main__':
    pp = PathPlanner(DensityMatrix())
    print("")
