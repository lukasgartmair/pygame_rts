#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 12:34:47 2023

@author: lukasgartmair    
"""

import pygame
import sys
import game_map
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
import engine
import game_font
import unittest
import game_scenes
import path
import sound
from sprite_group import SpriteGroup

name = "City Trade"

gm = game_map.GameMap()

ge = engine.GameEngine()

game_sound = sound.Sound()

global_path = path.Path(gm, game_sound)

font_game = game_font.GameFont(game_font.font_style, game_font.font_size)

sprite_groups = SpriteGroup().get_sprite_groups()

def run_game(starting_scene):
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(name)
    clock = pygame.time.Clock()

    active_scene = starting_scene

    while active_scene != None:
        pressed_keys = pygame.key.get_pressed()

        filtered_events = []
        try:
            event_list = pygame.event.get()
        except:
            pass
        for event in event_list:
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True

            if quit_attempt:
                active_scene.Terminate()
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            else:
                filtered_events.append(event)

        active_scene.ProcessInput(filtered_events, pressed_keys)
        active_scene.Update()
        active_scene.Render(screen, font_game)

        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    # unittest.main()
    run_game(game_scenes.TitleScene(ge, gm, global_path, game_sound, sprite_groups))
