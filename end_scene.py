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
    def __init__(self, *kargs):
        super().__init__(*kargs)

        self.game_map.mapped_grid = image.invert_grid(self.game_map.mapped_grid)
        print("End Scene")
        trading_good_sums = []
        for s in self.settlements:
            sum_goods = sum(s.trading_goods.values())
            trading_good_sums.append(sum_goods)
            print(s.trading_goods)

        print(max(trading_good_sums, default=0))

    def process_input(self, events, pressed_keys, screen):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.switch_to_scene(
                        scene_manager.get_title_scene(
                            self.game_engine,
                            self.game_map,
                            self.game_sound,
                            self.sprite_groups,
                        )
                    )

    def update(self):
        pass

    def render(self, game_camera, game_font):
        screen = game_camera.camera_screen
        surfarray.blit_array(
            screen, game_camera.get_map_cutout(self.game_map.mapped_grid)
        )
        tmp = game_camera.get_map_cutout(self.game_map.mapped_grid)
        surfarray.blit_array(screen, tmp)
        surfarray.blit_array(screen, tmp)

        self.settlements.draw(screen)
        self.game_engine.render_settlement_count(screen, game_font)


