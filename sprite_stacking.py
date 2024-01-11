#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 09:24:51 2024

@author: lukasgartmair
"""

import numpy as np
from itertools import product
from matplotlib import pyplot as plt
import random
from enum import Enum

class Buildings(Enum):
    EARTH = 0
    STREET = 1
    HOUSE = 2

dim_x, dim_y, dim_z = 99,99,33

def get_rnd_house_height():
    return random.randint(dim_z//4,dim_z//4*2)

def chance(p=0.6):
    return random.random() < p

def is_in_bounds(pos):
    return bool(
        0 <= pos[0] < dim_x
        and 0 <= pos[1] < dim_y
    )

def get_adjacent_cells(x, y, k=0):
    adjacent_cells = []
    for xi in range(-k, k + 1):
        for yi in range(-k, k + 1):
            adjacent_cells.append((x + xi, y + yi))
    return adjacent_cells

# def build_rnd_3d_settlement():
    
dimensions = (dim_z, dim_x, dim_y)

center = (dim_x // 2, dim_y // 2)

matrix = np.zeros(dimensions)

matrix[0,center[0],center[1]] = Buildings.HOUSE.value
    
    # return matrix
    
visited_cells = []

radius = dim_x // 4

for i in range(radius):
    adjacent_cells = get_adjacent_cells(center[0],center[1],k=i)
    for k,cell in enumerate(adjacent_cells):
        if is_in_bounds(cell):
            if cell not in visited_cells:
                if matrix[0,cell[0],cell[1]] == Buildings.EARTH.value:
                    c = chance()
                    
                    if c == True:
                        matrix[0,cell[0],cell[1]] = Buildings.STREET.value
                    else:
                        matrix[0,cell[0],cell[1]] =  Buildings.HOUSE.value
   
for i in range(dim_x):
    for j in range(dim_y):
        if matrix[0,i,j] == Buildings.HOUSE.value:
            matrix[:get_rnd_house_height(),i,j] = Buildings.HOUSE.value

# unique, counts = np.unique(matrix, return_counts=True)

# n_houses = dict(zip(unique, counts))[Buildings.HOUSE.value]

# mu, sigma = 0, 2
# normal_distribution = np.random.normal(mu, sigma, n_houses)            

top_view = matrix[0,:,:]
skyline_view_1 = np.flipud(np.sum(matrix,axis=1))
skyline_view_2 = np.flipud(np.sum(matrix,axis=2))

plt.matshow(top_view)
plt.colorbar()


# fig = plt.figure(figsize=(10,10))
# ax = fig.add_subplot(projection="3d")
# ax.scatter(matrix)