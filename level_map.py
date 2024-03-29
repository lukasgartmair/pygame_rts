#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 12:37:25 2023

@author: lukasgartmair
"""

import random
from enum import Enum
import numpy as np
from colors import terrain_colors
import scipy.ndimage
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Terrains(Enum):
    EARTH = 1
    WATER = 0


walkable_terrains = [Terrains.EARTH.value]


class Structures(Enum):
    VILLAGE = 2


class MapGenerator:
    def __init__(self, game_map):

        self.width = game_map.width
        self.height = game_map.height
        self.grid = np.zeros((game_map.width, game_map.height))
        self.earth_water_ratio = 0.5

    def inside_screen_boundaries(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def process(self):
        binary = self.grid
        img_fill_holes = scipy.ndimage.binary_fill_holes(binary[:, :]).astype(int)
        img_fill_holes2 = scipy.ndimage.gaussian_filter(img_fill_holes, sigma=0.5)
        self.grid = img_fill_holes2

    def generate_rnd_walk(self, terrain):
        number_of_pixels = self.width * self.height
        ratio = self.earth_water_ratio
        max_amount_terrain = number_of_pixels * (1 - ratio)

        current_amount = 0

        x_temp, y_temp = (
            (random.randint(0, self.width)),
            random.randint(0, self.height),
        )

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
            if self.inside_screen_boundaries(x_temp, y_temp):
                self.grid[x_temp, y_temp] = terrain
                current_amount += 1

            counter += 1

    def generate_seas(self, terrain=Terrains.WATER.value):
        number_of_seas = random.randint(0, 7)
        number_of_pixels = self.width * self.height
        ratio = 0.4
        max_amount_terrain = number_of_pixels * (1 - ratio)

        current_amount = 0
        counter = 0

        for n in range(number_of_seas):
            x_temp, y_temp = (
                (random.randint(0, self.width)),
                random.randint(0, self.height),
            )

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
                if self.inside_screen_boundaries(x_temp, y_temp):
                    self.grid[x_temp, y_temp] = terrain
                    current_amount += 1

                counter += 1

    def generate_terrain(self, terrain, ratio):
        number_of_pixels = self.width * self.height
        ratio = self.earth_water_ratio
        max_amount_terrain = number_of_pixels * (1 - ratio)

        current_amount = 0

    def generate_rnd_map(self):
        self.grid[:, :] = Terrains.EARTH.value

        # self.generate_terrain(Terrains.WATER.value, self.earth_water_ratio)
        self.generate_seas()


class GameMap:
    def __init__(self, dimensions=2, test=False):
        self.dimensions = dimensions
        if test:
            self.width = 1
            self.height = 1
        else:
            self.width = SCREEN_WIDTH * 2
            self.height = SCREEN_HEIGHT * 2
        self.grid = np.zeros((self.width, self.height))
        self.mapped_grid = np.zeros((self.width, self.height, 3))
        self.generate()

    def generate(self):
        mg = MapGenerator(self)
        if self.dimensions == 2:
            mg.generate_rnd_map()
            mg.process()
            self.grid = mg.grid.copy()
            self.map_colors()
        elif self.dimensions == 3:
            mg.generate_rnd_3D_map()       

    def map_colors(self):
        for k, v in terrain_colors.items():
            indices = np.where(self.grid == k)
            self.mapped_grid[indices] = v

    def check_valid_village_placement(self, position):
        if self.grid[position[0], position[1]] == Terrains.EARTH.value:
            return True
        else:
            return False
