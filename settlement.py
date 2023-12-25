#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 14:15:39 2023

@author: lukasgartmair
"""

import pygame
from colors import settlement_colors
from faker import Faker
import pygame.gfxdraw

faker = Faker()

def circleSurface(radius, color):
    shape_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    # pygame.gfxdraw.aacircle(shape_surf, radius, radius, radius, color)
    # pygame.gfxdraw.filled_circle(shape_surf, radius, radius, radius, color)
    return shape_surf

def update_selected_settlements(selected_settlements, global_path, game_map, game_sound):

    if len(selected_settlements) == 2:
        global_path.connect_settlements(selected_settlements, game_map, game_sound)
        for s in selected_settlements:
            s.deselect()
        selected_settlements.empty()
    elif len(selected_settlements) > 2:
        selected_settlements.pop()
    else:
        pass
    return selected_settlements

class Settlement(pygame.sprite.Sprite):

    def __init__(self, center, game_sound):
        super().__init__()
        self.center = center
        self.color = settlement_colors[1]
        self.radius = 10
        self.surf = circleSurface(self.radius,self.color)
        self.rect = self.surf.get_rect(center=center)
        self.selected = False
        self.callback = self.on_click
        self.image = self.surf
        self.clicks = 0
        self.name = faker.city()
                
    def placed(self, game_sound):
        print(self.name)
        game_sound.play_place_settlement()

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos):
                    if self.clicks > 0:
                        self.callback()
                    self.clicks += 1

    def check_removal(self, events):
        for event in events:   
            if event.type == pygame.KEYDOWN:
                if event.key== pygame.K_DELETE:
                    if self.selected:
                            self.kill()
                            return True
        return False

    def deselect(self):
        self.selected = False
        self.color = settlement_colors[1]
        self.surf.fill(self.color)

    def on_click(self):
        if self.selected == False:
            self.selected = True
            self.color = settlement_colors[0]
        else:
            self.selected = False
            self.color = settlement_colors[1]

        self.surf.fill(self.color)
