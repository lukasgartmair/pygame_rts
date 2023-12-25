#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 09:13:54 2023

@author: lukasgartmair
"""

import pygame

class SpriteGroups:
    def __init__(self):
        
        self.settlements = pygame.sprite.Group()
        self.selected_settlements = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

    def get_sprite_groups(self):
        return [self.settlements, self.selected_settlements, self.all_sprites]