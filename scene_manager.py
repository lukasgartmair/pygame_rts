#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 23:07:57 2023

@author: lukasgartmair
"""

from title_scene import TitleScene
from game_scene import GameScene
from end_scene import EndScene

def get_title_scene(game_engine, game_map, global_path, game_sound, sprite_groups):
    return TitleScene(game_engine, game_map, global_path, game_sound, sprite_groups)

def get_game_scene(game_engine, game_map, global_path, game_sound, sprite_groups):
    return GameScene(game_engine, game_map, global_path, game_sound, sprite_groups)

def get_end_scene(game_engine, game_map, global_path, game_sound, sprite_groups):
    EndScene(game_engine, game_map, global_path, game_sound, sprite_groups)
