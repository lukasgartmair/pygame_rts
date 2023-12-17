#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 14:15:39 2023

@author: lukasgartmair
"""

import pygame

def circleSurface(color, radius):
    shape_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    return shape_surf 

class Settlement(pygame.sprite.Sprite):

    def __init__(self, center, screen):
        super().__init__()
        self.center = center
        self.color = (255,0,0)
        self.radius = 30
        
        self.surf =  circleSurface(self.color, self.radius)
        self.rect = self.surf.get_rect(center=center)

       