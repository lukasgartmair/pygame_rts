#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 09:18:06 2023

@author: lukasgartmair
"""

import pygame
from scene_base import SceneBase
import image
import scene_manager
import pygame.surfarray as surfarray

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
                        scene_manager.get_title_scene(
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
