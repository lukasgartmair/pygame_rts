#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 23:56:22 2023

@author: lukasgartmair
"""

from pathing import find_path
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
import pygame.surfarray as surfarray

def get_adjacent_cells_too(x,y):
    return [(x,y),(x+1,y),(x+1,y-1),(x,y-1),(x-1,y-1),(x-1,y),(x-1,y+1),(x,y+1)]

def dict_key_contains_string(string, tup):
    if string in str(tup):
        return True
    else:
        return False
            
class Path():
    
    def __init__(self, game_map):
        self.length = 0
        self.subpaths = {}
        self.mapped_grid = game_map.mapped_grid.copy()
        self.color = (0, 0, 255)
        
    def add_subpath(self, a, b, length, chain):
        self.subpaths[a,b] = {"length":length, "chain":chain}
        
    def get_total_length(self):
        self.length = 0
        for k,v in self.subpaths.items():
            self.length += int(v["length"])
        return self.length
    
    def render(self, game_map, screen):
        self.mapped_grid = game_map.mapped_grid.copy()
        for k,v in self.subpaths.items():
            for p in v['chain']:
                self.mapped_grid[p[0], p[1]] = self.color
        surfarray.blit_array(screen,self.mapped_grid)
        
    def render_path_length(self, screen, font_game):

        text = font_game.render("path length: " +
                           str(self.get_total_length()), True, font_game.text_color)
        screen.blit(text, (SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.15))
            
    def remove_subpath(self, settlement_name):
        for k in list(self.subpaths.keys()):
            if dict_key_contains_string(settlement_name, k):
                del self.subpaths[k]
                
    def connect_settlements(self, selected_settlements, gm):
    
        already_connected = False
        condition_1 = (list(selected_settlements)[0].name, list(selected_settlements)[1].name) in self.subpaths.keys()
        condition_2 = (list(selected_settlements)[1].name, list(selected_settlements)[0].name) in self.subpaths.keys()
        if condition_1 or condition_2:
            already_connected = True
            print("already connected")
        
        if not already_connected:
            print("connecting cities")
        
            local_path = None
    
            local_path = find_path(gm.grid, list(selected_settlements)[
                         0].center, list(selected_settlements)[1].center)
    
            if local_path:
                self.add_subpath(list(selected_settlements)[
                    0].name, list(selected_settlements)[
                    1].name, len(local_path), local_path)
            else:
                print("no_path_found")