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

def dict_key_contains_string(string, tup):
    if string in str(tup):
        return True
    else:
        return False

class Path:
    def __init__(self, game_map, game_sound):
        self.length = 0
        self.subpaths = {}
        self.mapped_grid = game_map.mapped_grid.copy()
        self.color = path_colors[0]
        self.pathfinder = PathFinder()
        self.settlement_connections = SettlementGraph()
        
    def check_if_connection_exists(self, settlement):
        return any([settlement.name in key for key in self.subpaths])

    def add_subpath(self, a, b, length, chain):
        
        self.subpaths[a, b] = {"length": length, "chain": chain}
        
        self.settlement_connections.add_edge(a,b)

        self.remove_perturbation_keys()

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

    def remove_subpath(self, settlement):
        for k in list(self.subpaths.keys()):
            if dict_key_contains_string(settlement.name, k):
                del self.subpaths[k]
                
        self.settlement_connections.remove_settlement(settlement)

    def already_connected(self, selected_settlements):

        settlement_a = selected_settlements[0]
        settlement_b = selected_settlements[1]
        
        return self.settlement_connections.are_connected(settlement_a, settlement_b)
        
        # condition_a = (settlement_a.name, settlement_b.name) in self.subpaths.keys()
        # condition_b = (settlement_b.name, settlement_a.name) in self.subpaths.keys()
        # if condition_a or condition_b:
        #     already_connected = True

        # return already_connected

    def connect_settlements(self, selected_settlements, game_map, game_sound):
        successfully_connected = False

        settlement_a = selected_settlements[0]
        settlement_b = selected_settlements[1]

        local_path = None

        local_path = self.pathfinder.find_path(
            game_map.grid, settlement_a.center, settlement_b.center
        )

        if local_path:
            self.add_subpath(
                settlement_a.name, settlement_b.name, len(local_path), local_path
            )
            settlement_a.got_connected()
            settlement_b.got_connected()
            
            self.settlement_connections.add_settlement_connection(settlement_a, settlement_b)

            game_sound.play_connect_settlement()

            successfully_connected = True

        else:
            print("no_path_found")
            settlement_a.deselect()
            settlement_b.deselect()

            successfully_connected = False
        return successfully_connected
