import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from bresenham import bresenham

TIME_LIMIT = 15

strategies = ["astar", "diagonal"]

class PathFinder:
    def __init__(self, strategy="diagonal"):
        self.strategy = "diagonal"
    
    def fix_matrix_rotation(self, matrix):
        matrix = np.rot90(matrix, k=3)
        matrix = np.fliplr(matrix)
        return matrix

    def find_path(self, matrix, start, end):
        
        local_path = []
        
        if self.strategy == "diagonal":
            
            local_path = list(bresenham(start[0], start[1], end[0], end[1]))
        
        elif self.strategy == "astar":
            
            find = AStarFinder
            finder = find()
        
            matrix = self.fix_matrix_rotation(matrix)
        
            grid = Grid(matrix=matrix, inverse=False)
        
            start_node = grid.node(start[0], start[1])
        
            end_node = grid.node(end[0], end[1])
        
            finder = AStarFinder(
                time_limit=TIME_LIMIT, diagonal_movement=DiagonalMovement.always
            )
            
            try:
                path, runs = finder.find_path(start_node, end_node, grid)
        
                for p in path:
                    local_path.append((p.x, p.y))
        
                # print(find.__name__)
                # print(grid.grid_str(path=path, start=start_node, end=end_node))
        
                # print('path: {}'.format(path))
        
            except:
                print("no path found, time limit exceeded")
    
        return local_path
