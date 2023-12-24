import  numpy as np
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.finder.ida_star import IDAStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

TIME_LIMIT = 10

def fix_matrix_rotatrion(matrix):
    matrix = np.rot90(matrix,k=3)
    matrix = np.fliplr(matrix)
    return matrix

def find_path(matrix, start, end):
    
    find = IDAStarFinder
    finder = find()
    
    matrix = fix_matrix_rotatrion(matrix)
    
    grid = Grid(matrix=matrix,inverse=False)
    
    start_node = grid.node(start[0], start[1])
    
    end_node = grid.node(end[0], end[1])
    
    finder = AStarFinder(time_limit=TIME_LIMIT,diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start_node, end_node, grid)
    
    local_path = []
    for p in path:
        local_path.append((p.x,p.y))
    
    # print(find.__name__)
    # print(grid.grid_str(path=path, start=start_node, end=end_node))
    
    # print('path: {}'.format(path))
        
    return local_path

