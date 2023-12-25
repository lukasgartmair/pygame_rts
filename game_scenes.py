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

class TitleScene(SceneBase):
    def __init__(self, game_engine, game_map, global_path, game_sound, sprite_groups):
        super().__init__(game_engine, game_map, global_path, game_sound, sprite_groups)
        print("Title Scene")

    def ProcessInput(self, events, pressed_keys):
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
        custom_events.register_trade()
        self.game_trade = trade.Trade(self.global_path)
        
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            
            if event.type == custom_events.TRADE:
                self.game_trade.perform_trade()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()

                settlement_clicked = False
                for s in self.settlements:
                    if s.rect.collidepoint(mouse_position[0], mouse_position[1]):
                        settlement_clicked = True

                if not settlement_clicked and len(self.selected_settlements) == 1:
                    for s in self.settlements:
                        s.deselect()
                    self.selected_settlements.empty()
                    continue

                if (
                    not settlement_clicked
                    and self.game_engine.settlements_available > 0
                ):
                    valid_placement = self.game_map.check_valid_village_placement(
                        mouse_position
                    )
                    if valid_placement:
                        new_settlement = settlement.Settlement(
                            mouse_position, self.game_sound
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

                else:
                    pass

            for s in self.settlements:
                if s.selected == True:
                    self.selected_settlements.add(s)
            for s in self.selected_settlements:
                removed = s.check_removal(events)
                if removed:
                    self.global_path.remove_subpath(s.name)
                    self.game_engine.remove_settlement()

            self.selected_settlements = settlement.update_selected_settlements(
                self.selected_settlements,
                self.global_path,
                self.game_map,
                self.game_sound,
            )

            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.game_engine.game_ended_by_player()

        self.settlements.update(events)

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

        self.game_map.mapped_grid = image.invert_grid(self.game_map.mapped_grid)
        print("End Scene")

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
