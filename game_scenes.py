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
import custom_events
import trade
import random


class TitleScene(SceneBase):
    def __init__(self, game_engine, game_map, global_path, game_sound, sprite_groups):
        super().__init__(game_engine, game_map, global_path, game_sound, sprite_groups)
        print("Title Scene")
        self.skip = True

    def ProcessInput(self, events, pressed_keys):
        if self.skip:
            self.SwitchToScene(
                GameScene(
                    self.game_engine,
                    self.game_map,
                    self.global_path,
                    self.game_sound,
                    self.sprite_groups,
                )
            )

        for event in events:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or (
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            ):
                self.SwitchToScene(
                    GameScene(
                        self.game_engine,
                        self.game_map,
                        self.global_path,
                        self.game_sound,
                        self.sprite_groups,
                    )
                )

    def Update(self):
        pass

    def Render(self, screen, game_font):
        background_start = image.load_title_screen_background(screen)
        screen.blit(background_start, (0, 0))

        message = "Start Game by pressing ENTER!"
        text = game_font.render(message, True, (200, 0, 0))
        screen.blit(text, (20, 50))


class GameScene(SceneBase):
    def __init__(self, game_engine, game_map, global_path, game_sound, sprite_groups):
        super().__init__(game_engine, game_map, global_path, game_sound, sprite_groups)
        print("Game Scene")
        game_sound.play_background_music_1()
        custom_events.TRADE = custom_events.register_trade()
        self.game_trade = trade.Trade(self.settlements, self.global_path)

    def check_any_settlement_clicked(self, events):

        any_settlement_clicked = False
        any_settlement_clicked = any(
            [s.check_if_clicked(events) for s in self.settlements])
        return any_settlement_clicked
        
    def handle_deselection_on_void_click(self):
        for s in self.settlements:
            s.deselect()
        self.selected_settlements.empty()

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

    def get_selected_settlements(self):
        for s in self.settlements:
            if s.selected:
                self.selected_settlements.add(s)
                
    def update_selected_settlement_variable(self):
        for s in self.settlements:
                 s.update_number_of_other_selected_settlements(
                     self.selected_settlements)
                 
    def check_selected_settlements_for_connections(self):
       
        already_connected = False
        if len(self.selected_settlements) == 2:
            already_connected = self.global_path.connect_settlements(
                self.selected_settlements, self.game_map, self.game_sound)
            for s in self.selected_settlements:
                if not already_connected:
                    s.deselect()
                else:
                    print("here")
                    s.deselect_connected()
            self.selected_settlements.empty()
        else:
            pass

    def ProcessInput(self, events, pressed_keys):
        for event in events:

            if len(self.global_path.subpaths) >= 1:
                if event.type == custom_events.TRADE:
                    self.game_trade.perform_trade()
                    
            self.check_selected_settlements_for_connections()
            self.settlements.update(events, self.global_path, self.game_engine)
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DELETE:
                        if len(self.selected_settlements):
                            for s in self.selected_settlements:
                                s.remove(self.global_path, self.game_engine)

            if event.type == pygame.MOUSEBUTTONDOWN:

                # print("clicked"+str(random.randint(0,1000000)))

                mouse_position = pygame.mouse.get_pos()
                any_settlement_clicked = self.check_any_settlement_clicked(events)
                if not any_settlement_clicked and len(self.selected_settlements) in [1,2]:
                    self.handle_deselection_on_void_click()
                    break
                if (
                    not any_settlement_clicked
                    and self.game_engine.settlements_available > 0
                ):
                    self.try_new_settlement_placement(mouse_position)
                    
                self.get_selected_settlements()
                self.update_selected_settlement_variable()

        self.game_engine.check_win_condition(self.settlements)

    def Update(self):
        if self.game_engine.state == GameState.ENDED:
            self.SwitchToScene(
                EndScene(
                    self.game_engine,
                    self.game_map,
                    self.global_path,
                    self.game_sound,
                    self.sprite_groups,
                )
            )

    def Render(self, screen, game_font):
        surfarray.blit_array(screen, self.game_map.mapped_grid)
        self.global_path.render(self.game_map, screen)
        self.global_path.render_path_length(screen, game_font)
        for s in self.settlements:
            if s.hover:
                s.render_settlement_stats(screen, game_font)
        self.settlements.draw(screen)
        self.game_engine.render_settlement_count(screen, game_font)


class EndScene(SceneBase):
    def __init__(self, game_engine, game_map, global_path, game_sound, sprite_groups):
        super().__init__(game_engine, game_map, global_path, game_sound, sprite_groups)

        self.game_map.mapped_grid = image.invert_grid(
            self.game_map.mapped_grid)
        print("End Scene")
        trading_good_sums = []
        for s in self.settlements:
            sum_goods = sum(s.trading_goods.values())
            trading_good_sums.append(sum_goods)
            print(s.trading_goods)

        print(max(trading_good_sums, default=0))

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.SwitchToScene(
                        TitleScene(
                            self.game_engine,
                            self.game_map,
                            self.global_path,
                            self.game_sound,
                            self.sprite_groups,
                        )
                    )

    def Update(self):
        pass

    def Render(self, screen, game_font):
        surfarray.blit_array(screen, self.game_map.mapped_grid)
        self.global_path.render(self.game_map, screen)
        self.global_path.render_path_length(screen, game_font)
        self.settlements.draw(screen)
        self.game_engine.render_settlement_count(screen, game_font)
