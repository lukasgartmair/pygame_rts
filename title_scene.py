#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 09:15:03 2023

@author: lukasgartmair
"""

import pygame
from scene_base import SceneBase
import scene_manager
import image

class TitleScene(SceneBase):
    def __init__(self, *kargs):
        super().__init__(*kargs)
        print("Title Scene")
        self.skip = False

    def ProcessInput(self, events, pressed_keys, screen):
        if self.skip:
            self.SwitchToScene(
                scene_manager.get_game_scene(
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
                    scene_manager.get_game_scene(
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