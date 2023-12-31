#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 12:37:25 2023

@author: lukasgartmair
"""

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
import random
import numpy as np
import pygame.surfarray as surfarray
from enum import Enum
from colors import terrain_colors


class Terrains(Enum):
    VOID = 0
    EARTH = 1
    WATER = 2


def inside_screen_boundaries(x, y):
    if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
        return True
    else:
        return False


class MapGenerator:
    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.grid = np.zeros((self.width, self.height))
        z_dimensions = 3
        self.mapped_grid = np.zeros((self.width, self.height, z_dimensions))
        self.earth_water_ratio = 0.1

    def map_colors(self):
        for k, v in terrain_colors.items():
            indices = np.where(self.grid == k)
            self.mapped_grid[indices] = v

    def generate_terrain(self, terrain, ratio):
        number_of_pixels = SCREEN_WIDTH * SCREEN_HEIGHT
        ratio = self.earth_water_ratio
        max_amount_terrain = number_of_pixels * (1 - ratio)

        current_amount = 0

        s = ((random.randint(0, SCREEN_WIDTH)), random.randint(0, SCREEN_HEIGHT))
        x_temp = int(s[0])
        y_temp = int(s[1])

        # s = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        # x_temp = int(s[0])
        # y_temp = int(s[1])

        # for x in range(50):
        #     x_temp += 1
        #     for y in range(50):
        #         y_temp += 1
        #         if inside_screen_boundaries(x_temp,y_temp):
        #             self.grid[x_temp, y_temp] = terrain

        while current_amount <= max_amount_terrain:
            direction = random.randint(0, 4)
            if direction == 0:
                x_temp += 1
            elif direction == 1:
                x_temp -= 1
            elif direction == 2:
                y_temp += 1
            elif direction == 3:
                y_temp -= 1
            if inside_screen_boundaries(x_temp, y_temp):
                self.grid[x_temp, y_temp] = terrain
                current_amount += 1
            else:
                next

    def generate_rnd_map(self):
        self.grid[:, :] = Terrains.EARTH.value

        self.generate_terrain(Terrains.WATER.value, self.earth_water_ratio)

        self.map_colors()
