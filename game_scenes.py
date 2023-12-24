#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 23:07:57 2023

@author: lukasgartmair
"""

import pygame
from scene_base import SceneBase
import pygame.surfarray as surfarray
import settlement
import image
from engine import GameState

class TitleScene(SceneBase):
    def __init__(self, game_engine, game_map, global_path):
        super().__init__(game_engine, game_map, global_path)
        print("Title Scene")
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                print("here")
                if event.key == pygame.K_RETURN:
                    self.SwitchToScene(GameScene(self.game_engine, self.game_map, self.global_path))
    
    def Update(self):
        pass
    
    def Render(self, screen, game_font):
        
        background_start = image.load_title_screen_background(screen)
        screen.blit(background_start, (0, 0))
    
        message = "Start Game by pressing ENTER!"
        text = game_font.render(message, True, (200, 0, 0))
        screen.blit(text, (20, 50))

class GameScene(SceneBase):
    def __init__(self, game_engine, game_map, global_path):
        super().__init__(game_engine, game_map, global_path)
        print("Game Scene")

        self.global_path = global_path
        self.game_engine = game_engine    
        self.game_map = game_map
        self.settlements = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.selected_settlements = pygame.sprite.Group()
        
    def ProcessInput(self, events, pressed_keys):
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:                        
    
                mouse_position = pygame.mouse.get_pos()
                
                settlement_clicked = False
                for s in self.settlements:
                    if s.rect.collidepoint(mouse_position[0],mouse_position[1]):
                        settlement_clicked = True
                        
                if not settlement_clicked and self.game_engine.tokens_available > 0:
    
                    valid_placement = self.game_map.check_valid_village_placement(mouse_position)
                    if valid_placement:
                        new_settlement = settlement.Settlement(
                            mouse_position)
                        overlap =  pygame.sprite.spritecollideany(new_settlement, self.settlements)
                        if not overlap:
                            token_placed = self.game_engine.place_token()
                            if token_placed:
                                self.settlements.add(new_settlement)
                                self.all_sprites.add(new_settlement)
                        else:
                            new_settlement.kill()
    
                else:
                    pass
    
            for s in self.settlements:
                if s.selected == True:
                    self.selected_settlements.add(s)
            for s in self.selected_settlements:
                removed = s.check_removal(events)
                if removed:
                    self.global_path.remove_subpath(s.name)
                    self.game_engine.remove_token()
                    
            self.selected_settlements = settlement.update_selected_settlements(self.selected_settlements, self.global_path, self.game_map)
    
            self.game_engine.check_win_condition()
    
        self.settlements.update(events)
        
    def Update(self):
        if self.game_engine.state == GameState.ENDED:
            self.SwitchToScene(EndScene(self.game_engine, self.game_map, self.global_path))
    
    def Render(self, screen, game_font):
        surfarray.blit_array(screen, self.game_map.mapped_grid)
        self.global_path.render(self.game_map, screen)
        self.global_path.render_path_length(screen, game_font)
        self.settlements.draw(screen)
        self.game_engine.render_token_count(screen, game_font)

        
class EndScene(SceneBase):
    def __init__(self, game_engine, game_map, global_path):
        super().__init__(game_engine, game_map, global_path)
        print("End Scene")

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.SwitchToScene(TitleScene())
                    
    def Update(self):
        pass
    
    def Render(self, screen, game_font):
        surfarray.blit_array(screen, self.game_map.mapped_grid)
        self.global_path.render(self.game_map, screen)
        self.global_path.render_path_length(screen, game_font)
        self.settlements.draw(screen)
        self.game_engine.render_token_count(screen, game_font)