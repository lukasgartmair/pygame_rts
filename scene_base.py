#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 20:10:50 2023

@author: lukasgartmair
"""


class SceneBase:
    def __init__(self, game_engine=None, game_map=None, global_path=None, game_sound=None, sprite_groups=None):
        self.next = self
        self.game_engine = game_engine
        self.game_map = game_map
        self.global_path = global_path
        self.game_sound = game_sound
        self.sprite_groups = sprite_groups

        for k, v in self.sprite_groups.items():
            setattr(self, k, v)

    def ProcessInput(self, events, pressed_keys, screen):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, camera, font_game):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)
