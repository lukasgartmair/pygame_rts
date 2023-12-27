#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 11:52:47 2023

@author: lukasgartmair
"""

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


def initialize_cameras():
    camera_0 = Camera(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    camera_1 = Camera(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2)
    camera_2 = Camera(0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2)

    return camera_0, camera_1, camera_2


def get_camera_screen_dimensions(camera_screen):
    return (camera_screen.get_width(), camera_screen.get_height())


def is_in_bounds(pos, camera_screen_dimensions):
    if 0 <= pos[0] < camera_screen_dimensions[0] and 0 <= pos[1] < camera_screen_dimensions[1]:
        return True
    else:
        return False


class Camera:
    def __init__(self, top, left, width, height):
        self.canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.camera = pygame.Rect(top, left, width, height)
        self.camera_screen = self.canvas.subsurface(self.camera)

    def get_subsurface_dimensions(self):
        return self.camera_screen.get_width(), self.camera_screen.get_height()

    def get_subsurface_topleft(self):
        return self.camera.topleft
