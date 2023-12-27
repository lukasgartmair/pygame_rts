#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 09:13:54 2023

@author: lukasgartmair
"""

import pygame


class SpriteGroup:
    def __init__(self):
        self.settlements = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

    def get_sprite_groups(self):
        sprite_groups = {}
        for k, v in self.__dict__.items():
            sprite_groups[k] = v
        return sprite_groups
