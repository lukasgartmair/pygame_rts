#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 12:34:47 2023

@author: lukasgartmair
"""

import pygame
import sys
import settlement
import map_generator
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
import pygame.surfarray as surfarray

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

m = map_generator.MapGenerator()
m.generate_rnd_map()

settlements = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()

while True:

    surfarray.blit_array(screen, m.mapped_grid)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    if event.type == pygame.MOUSEBUTTONUP:
        mouse_position = pygame.mouse.get_pos()

        new_settlement = settlement.Settlement(mouse_position, screen)

        settlements.add(new_settlement)
        all_sprites.add(new_settlement)

    for entity in all_sprites:

        screen.blit(entity.surf, entity.rect)

    pygame.display.flip()
    clock.tick(60)
