#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 12:34:47 2023

@author: lukasgar            
"""

import pygame
import sys
import settlement
import game_map
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
import pygame.surfarray as surfarray
import engine
from a_star_pathfinding import astar

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

gm = game_map.GameMap()

ge = engine.GameEngine()

settlements = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()

pygame.font.init()
font_size = 30
font_style = pygame.font.match_font("z003")
font = pygame.font.Font(font_style, font_size)
font.set_bold(True)
text_color = (28, 0, 46)

def render_token_count(ge):
    text_color = (0, 0, 0)
    text = font.render("cities left to place: " + str(ge.get_tokens_availabe()), True, text_color)
    screen.blit(text, (SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.1))
    
def connect_tokens():
    paths = []

    for i,si in enumerate(list(settlements)):
        path = None
        for j,sj in enumerate(list(settlements)):
            if i != j:
                path = astar(gm.grid, si.center, sj.center)
            
                paths.append(path)

    for p in paths:
        if p:
            for pi in p:
                gm.mapped_grid[pi[0],pi[1]] = (0,0,255)
    
tokens_connected = False

while True:
    
    if ge.get_tokens_availabe() == 0 and not tokens_connected:
        connect_tokens()
        tokens_connected = True
    
    surfarray.blit_array(screen, gm.mapped_grid)
    
    try:
        event_list = pygame.event.get()
    except:
        pass

    for event in event_list:
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
        
            mouse_position = pygame.mouse.get_pos()
    
            valid_placement = gm.check_valid_village_placement(mouse_position)
            if valid_placement:
                token_placed = ge.place_token()
                if token_placed:
                    new_settlement = settlement.Settlement(mouse_position, screen)
                    settlements.add(new_settlement)
                    all_sprites.add(new_settlement)
            
            else:
                pass

        ge.check_win_condition()
    
    
    for entity in all_sprites:

        screen.blit(entity.surf, entity.rect)
        
    render_token_count(ge)
    pygame.display.flip()
    clock.tick(60)
