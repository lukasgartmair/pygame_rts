#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 12:34:47 2023

@author: lukasgartmair    
"""

import pygame
import sys
import settlement
import game_map
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
import pygame.surfarray as surfarray
import engine
from pathing import find_path
from scene_base import SceneBase
import game_font    
import numpy as np
import unittest
import test_suite

gm = game_map.GameMap()

ge = engine.GameEngine()

global_path = game_map.Path(gm)

font_game = game_font.GameFont(game_font.font_style, game_font.font_size)

def render_path_length(screen):

    text = font_game.render("path length: " +
                       str(global_path.get_total_length()), True, font_game.text_color)
    screen.blit(text, (SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.15))

def render_token_count(screen, ge):
    text = font_game.render("cities left to place: " +
                       str(ge.get_tokens_availabe()), True, font_game.text_color)
    screen.blit(text, (SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.1))

def update_selected_settlements(selected_settlements, gm):

    if len(selected_settlements) == 2:
        connect_tokens(selected_settlements, gm)
        for s in selected_settlements:
            s.deselect()
        selected_settlements.empty()
    elif len(selected_settlements) > 2:
        selected_settlements.pop()
    else:
        pass
    return selected_settlements


def connect_tokens(selected_settlements, gm):
    print("connecting cities")
    already_connected = False
    condition_1 = (list(selected_settlements)[0].name, list(selected_settlements)[1].name) in global_path.subpaths.keys()
    condition_2 = (list(selected_settlements)[1].name, list(selected_settlements)[0].name) in global_path.subpaths.keys()
    if condition_1 or condition_2:
        already_connected = True
    
    if not already_connected:
    
        local_path = None

        local_path = find_path(gm.grid, list(selected_settlements)[
                     0].center, list(selected_settlements)[1].center)

        if local_path:
            global_path.add_subpath(list(selected_settlements)[
                0].name, list(selected_settlements)[
                1].name, len(local_path), local_path)
            
            # for p in local_path:
            #     gm.mapped_grid[p[0], p[1]] = (0, 0, 255)
        else:
            print("no_path_found")

def run_game():

    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('City Connector')
    clock = pygame.time.Clock()
    
    settlements = pygame.sprite.Group()
    
    all_sprites = pygame.sprite.Group()
    
    selected_settlements = pygame.sprite.Group()

    while True:
        
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
                
                settlement_clicked = False
                for s in settlements:
                    if s.rect.collidepoint(mouse_position[0],mouse_position[1]):
                        settlement_clicked = True
                        
                if not settlement_clicked and ge.tokens_available > 0:
    
                    valid_placement = gm.check_valid_village_placement(mouse_position)
                    if valid_placement:
                        new_settlement = settlement.Settlement(
                            mouse_position, screen)
                        overlap =  pygame.sprite.spritecollideany(new_settlement, settlements)
                        if not overlap:
                            token_placed = ge.place_token()
                            if token_placed:
                                settlements.add(new_settlement)
                                all_sprites.add(new_settlement)
                        else:
                            new_settlement.kill()
    
                else:
                    pass
    
            for s in settlements:
                if s.selected == True:
                    selected_settlements.add(s)
            for s in selected_settlements:
                removed = s.check_removal(event_list)
                if removed:
                    global_path.remove_subpath(s.name)
                    ge.remove_token()
                    
            selected_settlements = update_selected_settlements(selected_settlements, gm)
    
            ge.check_win_condition()
    
        render_token_count(screen, ge)
        
        settlements.update(event_list)
        global_path.render(gm, screen)
        settlements.draw(screen)
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    unittest.main()
    run_game()
