#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 12:37:25 2023

@author: lukasgartmair
"""

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
import random
import numpy as np
from enum import Enum
from colors import terrain_colors
import scipy.ndimage


class Terrains(Enum):
    EARTH = 1
    WATER = 0


walkable_terrains = [Terrains.EARTH.value]


class Structures(Enum):
    VILLAGE = 2


def inside_screen_boundaries(x, y):
    if 0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT:
        return True
    else:
        return False


class MapGenerator:
    def __init__(self, game_map):
        self.grid = np.zeros((game_map.size_x, game_map.size_y))
        self.earth_water_ratio = 0.5

    def process(self):
        binary = self.grid
        img_fill_holes = scipy.ndimage.binary_fill_holes(binary[:, :]).astype(int)
        img_fill_holes2 = scipy.ndimage.gaussian_filter(img_fill_holes, sigma=0.5)
        self.grid = img_fill_holes2

    def generate_rnd_walk(self, terrain):
        number_of_pixels = SCREEN_WIDTH * SCREEN_HEIGHT
        ratio = self.earth_water_ratio
        max_amount_terrain = number_of_pixels * (1 - ratio)

        current_amount = 0

        s = ((random.randint(0, SCREEN_WIDTH)), random.randint(0, SCREEN_HEIGHT))
        x_temp = int(s[0])
        y_temp = int(s[1])

        counter = 0
        max_iterations = 1000000
        while current_amount <= max_amount_terrain:
            if counter >= max_iterations:
                break

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
            counter += 1

    def generate_seas(self, terrain=Terrains.WATER.value):
        number_of_seas = random.randint(0, 7)
        number_of_pixels = SCREEN_WIDTH * SCREEN_HEIGHT
        ratio = 0.4
        max_amount_terrain = number_of_pixels * (1 - ratio)

        current_amount = 0
        counter = 0

        for n in range(number_of_seas):
            s = ((random.randint(0, SCREEN_WIDTH)), random.randint(0, SCREEN_HEIGHT))
            x_temp = int(s[0])
            y_temp = int(s[1])

            counter = 0
            max_iterations = 1000000
            while current_amount <= max_amount_terrain:
                if counter >= max_iterations:
                    break

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
                counter += 1

    def generate_terrain(self, terrain, ratio):
        number_of_pixels = SCREEN_WIDTH * SCREEN_HEIGHT
        ratio = self.earth_water_ratio
        max_amount_terrain = number_of_pixels * (1 - ratio)

        current_amount = 0

    def generate_rnd_map(self):
        self.grid[:, :] = Terrains.EARTH.value

        # self.generate_terrain(Terrains.WATER.value, self.earth_water_ratio)
        self.generate_seas()


class GameMap:
    def __init__(self):
        self.size_x = SCREEN_WIDTH
        self.size_y = SCREEN_HEIGHT
        self.grid = np.zeros((self.size_x, self.size_y))
        self.mapped_grid = np.zeros((self.size_x, self.size_y, 3))
        self.generate()

    def generate(self):
        m = MapGenerator(self)
        m.generate_rnd_map()
        m.process()
        self.grid = m.grid.copy()
        self.map_colors()

    def map_colors(self):
        for k, v in terrain_colors.items():
            indices = np.where(self.grid == k)
            self.mapped_grid[indices] = v

    def check_valid_village_placement(self, position):
        if self.grid[position[0], position[1]] == Terrains.EARTH.value:
            return True
        else:
            return False

    def place_village(self, village):
        pass
