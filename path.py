#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 23:56:22 2023

@author: lukasgartmair
"""

from pathing import PathFinder
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from colors import path_colors
from settlement_graph import SettlementGraph

def get_adjacent_cells(x, y, k=0):
    adjacent_cells = []
    for xi in range(-k, k + 1):
        for yi in range(-k, k + 1):
            adjacent_cells.append((x + xi, y + yi))
    adjacent_cells.remove((x, y))
    return adjacent_cells

class Path:
    def __init__(self, game_map, game_sound):
        self.length = 0
        self.subpaths = {}
        self.mapped_grid = game_map.mapped_grid.copy()
        self.color = path_colors[0]
        self.pathfinder = PathFinder()
        self.settlement_connections = SettlementGraph()
        
    def get_total_length(self):
        self.length = 0
        for k, v in self.subpaths.items():
            self.length += int(v["length"])
        return self.length

    def remove_perturbation_keys(self):
        for k, v in list(self.subpaths.items()):
            if (k[1], k[0]) in self.subpaths.keys():
                del self.subpaths[k[1], k[0]]

    def map_paths_to_grid(self, game_map):
        self.remove_perturbation_keys()
        self.mapped_grid = game_map.mapped_grid.copy()
        for k, v in self.subpaths.items():
            for p in v["chain"]:
                self.mapped_grid[p[0], p[1]] = self.color

                adjacent_cells = get_adjacent_cells(p[0], p[1], k=3)

                for a in adjacent_cells:
                    self.mapped_grid[a[0], a[1]] = self.color

