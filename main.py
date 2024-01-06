#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 12:34:47 2023

@author: lukasgartmair    
"""

import pygame
import sys
from networkx import is_empty
import level_map
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, NAME
import engine
import game_font
import sound
from sprite_group import SpriteGroup
import scene_manager
import camera
import colors
import unittest
import animation
import logging

logger = logging.getLogger('root')


class Game:
    def __init__(self):
        
        self.game_map = level_map.GameMap()
        self.camera_0, self.camera_1, self.camera_2 = camera.initialize_cameras(
            self.game_map)
        self.game_engine = engine.GameEngine()
        self.game_sound = sound.Sound()
        self.font = game_font.GameFont(
            game_font.font_style, game_font.font_size)
        self.sprite_groups = SpriteGroup().get_sprite_groups()
        self.place_settlement_animation = animation.PlaceSettlementAnimation(self.camera_1)
        self.trade_animation = animation.TradeAnimation(self.camera_1)

    def run(self, starting_scene):
        pygame.init()
    
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(NAME)
    
        clock = pygame.time.Clock()
    
        active_scene = starting_scene
    
        pygame.key.set_repeat(1, 100)
    
        while active_scene is not None:
            pressed_keys = pygame.key.get_pressed()
    
            filtered_events = []
            try:
                event_list = pygame.event.get()
            except:
                pass
            for event in event_list:
                quit_attempt = False
                if event.type == pygame.QUIT:
                    quit_attempt = True
                elif event.type == pygame.KEYDOWN:
                    alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
                    if event.key == pygame.K_ESCAPE:
                        quit_attempt = True
                    elif event.key == pygame.K_F4 and alt_pressed:
                        quit_attempt = True
    
                if quit_attempt:
                    active_scene.terminate()
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
    
                if (
                    event.type == event.type == pygame.MOUSEBUTTONDOWN
                    or event.type == pygame.KEYDOWN
                    or event.type == pygame.KEYUP
                    or event.type == pygame.MOUSEMOTION
                ):
                    filtered_events.append(event)
    
                filtered_events_copy = filtered_events.copy()
                filtered_events = []
                for f in filtered_events_copy:
                    if f.type not in [fi.type for fi in filtered_events]:
                        filtered_events.append(f)
                        
            if type(active_scene).__name__ in ["GameScene"]:
                
                trading_paths = active_scene.get_scene_data()
                
                if is_empty(trading_paths) == False:
                    self.trade_animation.animate(trading_paths)
                    
                for settlement in active_scene.settlements:
                    if settlement.play_placement_animation:
                        self.place_settlement_animation.animate(settlement)
                        
                active_scene.settlements.draw(self.camera_1.camera_screen)
                
                self.camera_1.handle_user_input_camera_movement(filtered_events)
        
                screen.blit(self.camera_1.camera_screen, self.camera_1.camera.topleft)
        
                screen.blit(self.camera_2.camera_screen, self.camera_2.camera.topleft)
                self.camera_2.camera_screen.fill(colors.settlement_stats_colors[0])
        
                active_scene.process_input(filtered_events, pressed_keys, self.camera_1)
                active_scene.update()
        
                active_scene.render(self.camera_1, self.font)
                active_scene.render_second_screen(self.camera_2, self.font)
                
                self.game_engine.check_win_condition(active_scene.settlements)
                
                pygame.display.update(self.camera_1.camera_screen.get_rect())
        
            else:
                screen.blit(self.camera_0.camera_screen, self.camera_0.camera.topleft)
                active_scene.process_input(filtered_events, pressed_keys, self.camera_0)
                active_scene.update()
                active_scene.render(self.camera_0, self.font)
                
                active_scene = active_scene.next
    
            pygame.display.flip()
            clock.tick(FPS)


if __name__ == "__main__":
    # unittest.main()
    game = Game()
    game.run(
        scene_manager.get_title_scene(game.game_engine, game.game_map, game.game_sound, game.sprite_groups)
    )
