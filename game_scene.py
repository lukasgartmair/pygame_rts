#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 09:16:56 2023

@author: lukasgartmair
"""

import pygame
from scene_base import SceneBase
import settlement
from engine import GameState
import custom_events
import trade
from selection_manager import SelectionManager
import pygame.surfarray as surfarray
import scene_manager

class GameScene(SceneBase):
    def __init__(self, game_camera, game_engine, game_map, global_path, game_sound, sprite_groups):
        super().__init__(game_camera, game_engine, game_map, global_path, game_sound, sprite_groups)
        print("Game Scene")
        game_sound.play_background_music_1()
        custom_events.TRADE = custom_events.register_trade()
        self.game_trade = trade.Trade(self.settlements, self.global_path)
        self.any_settlement_clicked = False
        self.selection_manager = SelectionManager(self.settlements, self.any_settlement_clicked)

    def check_for_settlement_removals(self):

        if len(self.selection_manager.selected_settlements):
            for s in self.selection_manager.selected_settlements:
                s.remove(self.global_path, self.game_engine)
                        
    def check_for_trade_event(self, event):
        if len(self.global_path.subpaths) >= 1:
            if event.type == custom_events.TRADE:
                self.game_trade.perform_trade()

    def try_new_settlement_placement(self, mouse_position):
        valid_placement = self.game_map.check_valid_village_placement(
            mouse_position
        )
        if valid_placement:
            new_settlement = settlement.Settlement(
                mouse_position, self.game_sound, self.game_trade
            )
            overlap = pygame.sprite.spritecollideany(
                new_settlement, self.settlements
            )
            if not overlap:
                settlement_placed = self.game_engine.place_settlement()
                if settlement_placed:
                    self.settlements.add(new_settlement)
                    self.all_sprites.add(new_settlement)
                    new_settlement.placed(self.game_sound)
            else:
                new_settlement.kill()
                 
    def try_connect_settlements(self):
        
        already_connected = self.global_path.already_connected(self.selection_manager.selected_settlements)
        successfully_connected = False
        if not already_connected:
            successfully_connected = self.global_path.connect_settlements(
            self.selection_manager.selected_settlements, self.game_map, self.game_sound)
            
            if successfully_connected:
                self.selection_manager.handle_successful_connection()
                 
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            
            self.check_for_trade_event(event)

            self.selection_manager.update_selected_settlements()
            
            if self.selection_manager.check_connection_condition():
                self.try_connect_settlements()
                
            self.settlements.update(events, self.global_path, self.game_engine)
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    self.check_for_settlement_removals(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                self.selection_manager.check_any_settlement_clicked(events)
            
                if self.selection_manager.selection_and_void_click():
                    break
                
                if self.selection_manager.any_settlement_clicked:
                    self.selection_manager.process_settlement_click()
                
                if (
                    not self.selection_manager.any_settlement_clicked
                    and self.game_engine.settlements_available > 0
                ):
                    self.try_new_settlement_placement(pygame.mouse.get_pos())
                    
        self.game_engine.check_win_condition(self.settlements)

    def Update(self):
        if self.game_engine.state == GameState.ENDED:
            self.SwitchToScene(
                scene_manager.get_end_scene(
                    self.game_camera,
                    self.game_engine,
                    self.game_map,
                    self.global_path,
                    self.game_sound,
                    self.sprite_groups,
                )
            )

    def Render(self, screen, game_font):
        cam = self.game_camera.sub1
        surfarray.blit_array(cam, self.game_map.mapped_grid)
        self.global_path.render(self.game_map, self.game_camera)
        self.global_path.render_path_length(screen, game_font)
        for s in self.settlements:
            if s.hover:
                s.render_settlement_stats(screen, game_font)
        self.settlements.draw(cam)
        self.game_engine.render_settlement_count(cam, game_font)
