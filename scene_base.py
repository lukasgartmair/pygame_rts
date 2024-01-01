#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 20:10:50 2023

@author: lukasgartmair
"""


class SceneBase:
    def __init__(
        self,
        game_engine=None,
        game_map=None,
        game_sound=None,
        sprite_groups=None,
    ):
        self.next = self
        self.game_engine = game_engine
        self.game_map = game_map
        self.game_sound = game_sound
        self.sprite_groups = sprite_groups

        for k, v in self.sprite_groups.items():
            setattr(self, k, v)

    def process_input(self, mouse_position, pressed_keys, game_camera):
        print("uh-oh, you didn't override this in the child class")

    def update(self):
        print("uh-oh, you didn't override this in the child class")

    def render(self, game_camera, game_font):
        print("uh-oh, you didn't override this in the child class")

    def switch_to_scene(self, next_scene):
        self.next = next_scene

    def terminate(self):
        self.switch_to_scene(None)
