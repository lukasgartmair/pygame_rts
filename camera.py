#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 11:52:47 2023

@author: lukasgartmair
"""
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self):

        self.canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.camera_1 = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2)
        self.camera_2 = pygame.Rect(0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2)
        
        self.sub1 = self.canvas.subsurface(self.camera_1)

    def get_subsurface_dimensions(self):
        return self.sub1.get_width(), self.sub1.get_height()
    
    def get_subsurface_center(self):
        return self.sub1.center[0], self.sub1.center[1]