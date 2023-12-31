#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 17:48:53 2023

@author: lukasgartmair
"""

import pygame
import sys
import level_map
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
import engine
import game_font
import unittest
import path
import sound
from sprite_group import SpriteGroup
import scene_manager
import camera
import colors
import asyncio

WEBBROWSER = True

name = "City Trade"

camera_0, camera_1, camera_2 = camera.initialize_cameras()

game_map = level_map.GameMap(camera_1)

game_engine = engine.GameEngine()

game_sound = sound.Sound()

global_path = path.Path(game_map, game_sound)

font_game = game_font.GameFont(game_font.font_style, game_font.font_size)

sprite_groups = SpriteGroup().get_sprite_groups()

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(name)
clock = pygame.time.Clock()

pygame.key.set_repeat(1, 100)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(name)
clock = pygame.time.Clock()

pygame.key.set_repeat(1, 100)


def run_game(starting_scene):
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

        if type(active_scene).__name__ == "GameScene":
            screen.blit(camera_1.camera_screen, camera_1.camera.topleft)

            screen.blit(camera_2.camera_screen, camera_2.camera.topleft)
            camera_2.camera_screen.fill(colors.settlement_stats_colors[0])

            active_scene.ProcessInput(
                filtered_events,
                pressed_keys,
                camera_1.get_camera_screen_dimensions(camera_1.camera_screen),
            )
            active_scene.Update()
            active_scene.Render(camera_1, font_game)
            active_scene.RenderSecondScreen(camera_2, font_game)

        else:
            screen.blit(camera_0.camera_screen, camera_0.camera.topleft)
            active_scene.ProcessInput(
                filtered_events,
                pressed_keys,
                camera_1.get_camera_screen_dimensions(camera_0.camera_screen),
            )
            active_scene.Update()
            active_scene.Render(camera_0, font_game)

        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(FPS)


# if WEBBROWSER:


async def main():
    run_game(
        scene_manager.get_title_scene(
            game_engine, game_map, global_path, game_sound, sprite_groups
        )
    )
    await asyncio.sleep(0)  # Let other tasks run


asyncio.run(main())

# else:
#     if __name__ == "__main__":
#         # unittest.main()
#         run_game(scene_manager.get_title_scene(game_engine, game_map, global_path, game_sound, sprite_groups))