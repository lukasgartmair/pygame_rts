#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 14:50:46 2023

@author: lukasgartmair
"""

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
import sys


def initialize_cameras():
    camera_1 = Camera(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2)
    camera_2 = Camera(0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2)

    return camera_1, camera_2


class Camera:
    def __init__(self, top, left, width, height):
        self.canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.camera = pygame.Rect(top, left, SCREEN_WIDTH, SCREEN_HEIGHT // 2)
        self.subsurf = self.canvas.subsurface(self.camera)

    def get_subsurface_dimensions(self):
        return self.subsurface.get_width(), self.subsurface.get_height()

    def get_subsurface_topleft(self):
        return self.camera.topleft


camera_1 = Camera(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2)
camera_2 = Camera(0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2)

name = ""
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(name)
clock = pygame.time.Clock()

bg = (0, 0, 255)
bg2 = (0, 255, 0)


def main():
    looping = True

    while looping:
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
                pygame.quit()
                sys.exit()
            else:
                filtered_events.append(event)

            screen.blit(camera_1.subsurf, camera_1.camera.topleft)
            camera_1.subsurf.fill(bg)

            screen.blit(camera_2.subsurf, camera_2.camera.topleft)
            camera_2.subsurf.fill(bg2)

            pygame.display.update()
            clock.tick(FPS)


main()
