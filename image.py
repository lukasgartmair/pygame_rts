#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 23:48:08 2023

@author: lukasgartmair
"""

import pygame
import os


def invert_color(color):
    return (255 - color[0], 255 - color[1], 255 - color[2])


def invert_grid(grid):
    inverted_grid = grid.copy()
    return 255 - inverted_grid


_image_library = {}


def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace("/", os.sep).replace("\\", os.sep)
        image = pygame.image.load(canonicalized_path).convert()
        _image_library[path] = image
    return image


def load_settlement_images(name):
    path = "images/"
    filenames = next(os.walk("images"), (None, None, []))[2]
    filenames_filtered = [f for f in filenames if f.startswith(name)]
    images = {}
    
    for f in filenames_filtered:
        if f.endswith("blue.png"):
            images["main_image"] = get_image(path + f)
        if f.endswith("night.png"):
            images["select_image"] = get_image(path + f)
        if f.endswith("brass.png"):
            images["brass_image"] = get_image(path + f)
        if f.endswith("silver.png"):
            images["silver_image"] = get_image(path + f)
        if f.endswith("wood.png"):
            images["wood_image"] = get_image(path + f)
        if f.endswith("red.png"):
            images["rubins_image"] = get_image(path + f)

        # if not f.endswith("night.png"):
        #     images.append(get_image(path + f))

    return images


def load_title_screen_background(screen):
    path = "images/start_background.png"
    image = get_image(path)
    image = pygame.transform.smoothscale(image, screen.get_size())
    return image
