#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 09:16:56 2023

@author: lukasgartmair
"""

import pygame
from pygame import surfarray
from scene_base import SceneBase
import settlement
from engine import GameState
import custom_events
import trade
from selection_manager import SelectionManager
import scene_manager
from colors import settlement_stats_colors


class GameScene(SceneBase):
    def __init__(self, *kargs):
        super().__init__(*kargs)
        print("Game Scene")
        self.game_sound.play_background_music_1()
        custom_events.TRADE = custom_events.register_trade()
        self.game_trade = trade.Trade(self.settlements, self.global_path)
        self.any_settlement_clicked = False
        self.selection_manager = SelectionManager(
            self.settlements, self.any_settlement_clicked
        )

    def check_for_settlement_removals(self):
        if self.selection_manager.selected_settlements:
            for s in self.selection_manager.selected_settlements:
                s.remove(self.global_path, self.game_engine)

    def check_for_trade_event(self, event):
        if len(self.global_path.subpaths) >= 1:
            if event.type == pygame.TRADE:
                self.game_trade.perform_trade()

    def check_mouse_click_in_bounds(self, mouse_position, game_camera):
        return game_camera.is_in_bounds(mouse_position)

    def try_new_settlement_placement(self, game_camera, mouse_position):
        valid_placement = self.game_map.check_valid_village_placement(mouse_position)
        if valid_placement:
            absolute_map_position = game_camera.get_absolute_map_position(
                mouse_position
            )
            new_settlement = settlement.Settlement(
                absolute_map_position, self.game_sound, self.game_trade
            )
            overlap = pygame.sprite.spritecollideany(new_settlement, self.settlements)
            if not overlap:
                settlement_placed = self.game_engine.place_settlement()
                if settlement_placed:
                    self.settlements.add(new_settlement)
                    self.all_sprites.add(new_settlement)
                    new_settlement.placed(self.game_sound)
            else:
                new_settlement.kill()

    def try_connect_settlements(self):
        already_connected = self.global_path.already_connected(
            self.selection_manager.selected_settlements
        )
        successfully_connected = False
        if not already_connected:
            successfully_connected = self.global_path.connect_settlements(
                self.selection_manager.selected_settlements,
                self.game_map,
                self.game_sound,
            )

            if successfully_connected:
                self.selection_manager.handle_successful_connection()

    def process_input(self, events, pressed_keys, game_camera):
        for event in events:
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
            # self.check_for_trade_event(event)

                    self.game_trade.perform_trade()

                    
                    
            self.selection_manager.update_selected_settlements()

            if self.selection_manager.check_connection_condition():
                self.try_connect_settlements()

            self.settlements.update(
                events, game_camera, self.global_path, self.game_engine
            )

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    self.check_for_settlement_removals()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    
                    mouse_position = pygame.mouse.get_pos()

                    if self.check_mouse_click_in_bounds(mouse_position, game_camera):
                        self.selection_manager.check_any_settlement_clicked(events)

                        if self.selection_manager.selection_and_void_click():
                            break

                        if self.selection_manager.any_settlement_clicked:
                            self.selection_manager.process_settlement_click()

                        if (
                            not self.selection_manager.any_settlement_clicked
                            and self.game_engine.settlements_available > 0
                        ):
                            self.try_new_settlement_placement(
                                game_camera, mouse_position
                            )
                    else:
                        pass

        self.game_engine.check_win_condition(self.settlements)

    def update(self):
        # if self.game_engine.state == GameState.ENDED:
        #     self.switch_to_scene(
        #         scene_manager.get_end_scene(
        #             self.game_engine,
        #             self.game_map,
        #             self.global_path,
        #             self.game_sound,
        #             self.sprite_groups,
        #         )
        #     )

        pass

    def render(self, game_camera, game_font):
        screen = game_camera.camera_screen
        surfarray.blit_array(
            screen, game_camera.get_map_cutout(self.game_map.mapped_grid)
        )
        tmp = game_camera.get_map_cutout(self.game_map.mapped_grid)
        surfarray.blit_array(screen, tmp)
        self.global_path.map_paths_to_grid(self.game_map)
        tmp = game_camera.get_map_cutout(self.global_path.mapped_grid)
        surfarray.blit_array(screen, tmp)

        self.settlements.draw(screen)
        self.game_engine.render_settlement_count(screen, game_font)

    def render_second_screen(self, game_camera, game_font):
        screen = game_camera.camera_screen
        screen.get_rect()
        screen_dimensions = game_camera.get_camera_screen_dimensions()
        pygame.draw.rect(
            screen,
            (settlement_stats_colors[0]),
            pygame.Rect(0, 0, screen_dimensions[0], screen_dimensions[1]),
        )

        for s in self.settlements:
            if s.hover:
                s.render_settlement_stats(game_camera, game_font)

        self.game_trade.render_global_assets(screen, game_font)
