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
        self.camera_1 = pygame.Rect(0,0,int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2))
        self.camera_2 = pygame.Rect(int(SCREEN_WIDTH/2),0,int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2))
        self.camera_3 = pygame.Rect(0,int(SCREEN_HEIGHT/2),int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2))
        self.camera_4 = pygame.Rect(int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2),int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2))
        
        self.sub1 = self.canvas.subsurface(self.camera_1)
        self.sub2 = self.canvas.subsurface(self.camera_2)
        self.sub3 = self.canvas.subsurface(self.camera_3)
        self.sub4 = self.canvas.subsurface(self.camera_4)