#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 23:56:22 2023

@author: lukasgartmair
"""

from pathing import PathFinder
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
import pygame.surfarray as surfarray
from colors import path_colors


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

    def add_subpath(self, a, b, length, chain):
        self.subpaths[a, b] = {"length": length, "chain": chain}
        
        self.remove_perturbation_keys()

    def get_total_length(self):
        self.length = 0
        for k, v in self.subpaths.items():
            self.length += int(v["length"])
        return self.length
    
    def remove_perturbation_keys(self):

        for k,v in list(self.subpaths.items()):
            if (k[1],k[0]) in self.subpaths.keys():
                del self.subpaths[k[1],k[0]]

    def render(self, game_map, screen):
        self.remove_perturbation_keys()
        self.mapped_grid = game_map.mapped_grid.copy()
        for k, v in self.subpaths.items():
            for p in v["chain"]:
                self.mapped_grid[p[0], p[1]] = self.color

                adjacent_cells = get_adjacent_cells(p[0], p[1], k=3)

                for a in adjacent_cells:
                    self.mapped_grid[a[0], a[1]] = self.color

        surfarray.blit_array(screen, self.mapped_grid)

    def render_path_length(self, screen, font_game):
        text = font_game.render(
            "path length: " + str(self.get_total_length()), True, font_game.text_color
        )
        screen.blit(text, (SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.15))

    def remove_subpath(self, settlement_name):
        for k in list(self.subpaths.keys()):
            if dict_key_contains_string(settlement_name, k):
                del self.subpaths[k]
                
    def already_connected(self, selected_settlements):
        already_connected = False
        settlement_0 = selected_settlements[0]
        settlement_1 = selected_settlements[1]
        condition_1 = (settlement_0.name, settlement_1.name) in self.subpaths.keys()
        condition_2 = (settlement_1.name, settlement_0.name) in self.subpaths.keys()
        if condition_1 or condition_2:
            already_connected = True
            
        return already_connected

    def connect_settlements(self, selected_settlements, game_map, game_sound):
        
        successfully_connected = False
            
        settlement_0 = selected_settlements[0]
        settlement_1 = selected_settlements[1]

        local_path = None

        local_path = self.pathfinder.find_path(
            game_map.grid, settlement_0.center, settlement_1.center
        )

        if local_path:
            self.add_subpath(
                settlement_0.name, settlement_1.name, len(local_path), local_path
            )
            settlement_0.got_connected()
            settlement_1.got_connected()

            game_sound.play_connect_settlement()
            
            successfully_connected = True

        else:
            print("no_path_found")
            settlement_0.deselect()
            settlement_1.deselect()
            
            successfully_connected = False
        return successfully_connected
