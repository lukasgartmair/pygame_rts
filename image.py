#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 23:48:08 2023

@author: lukasgartmair
"""

import pygame
import numpy as np
import os

def invert_color(color):
    red=color[0]
    green=color[1]
    blue=color[2]
    inverted_color= (255-red,255-green,255-blue)
    return inverted_color

def invert_grid(grid):
    inverted_grid = grid.copy()
    inverted_grid = 255-inverted_grid
    return inverted_grid

_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path).convert()
                _image_library[path] = image
        return image


def load_title_screen_background(screen):
    title_screen_bg_path = 'images/start_background.png'
    background = get_image(title_screen_bg_path)
    background = pygame.transform.smoothscale(background, screen.get_size())
    return background