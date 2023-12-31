#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 11:52:47 2023

@author: lukasgartmair
"""

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from settings import CAMERA_0_X, CAMERA_0_Y, CAMERA_0_WIDTH, CAMERA_0_HEIGHT
from settings import CAMERA_1_X, CAMERA_1_Y, CAMERA_1_WIDTH, CAMERA_1_HEIGHT
from settings import CAMERA_2_X, CAMERA_2_Y, CAMERA_2_WIDTH, CAMERA_2_HEIGHT


def initialize_cameras(game_map):
    camera_0 = Camera(CAMERA_0_X, CAMERA_0_Y, CAMERA_0_WIDTH, CAMERA_0_HEIGHT, game_map)
    camera_1 = Camera(CAMERA_1_X, CAMERA_1_Y, CAMERA_1_WIDTH, CAMERA_1_HEIGHT, game_map)
    camera_2 = Camera(CAMERA_2_X, CAMERA_2_Y, CAMERA_2_WIDTH, CAMERA_2_HEIGHT, game_map)

    return camera_0, camera_1, camera_2


class Camera:
    def __init__(self, top, left, width, height, game_map):
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.game_map = game_map
        self.canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.camera = pygame.Rect(self.top, self.left, self.width, self.height)
        self.camera_screen = self.canvas.subsurface(self.camera)
        self.scroll_speed = 50
        self.topleft = (self.top, self.left)
        self.set_topleft_center_view()

    def get_camera_screen_dimensions(self):
        return (self.camera_screen.get_width(), self.camera_screen.get_height())

    def is_in_bounds(self, pos):
        return (
            0 <= pos[0] < self.get_camera_screen_dimensions()[0]
            and 0 <= pos[1] < self.get_camera_screen_dimensions()[1]
        )

    def within_boundaries(self, x_temp, y_temp):
        inside = [
            x_temp >= 0
            and y_temp >= 0
            and x_temp <= self.game_map.width - SCREEN_WIDTH
            and y_temp <= self.game_map.height - SCREEN_HEIGHT
        ]
        return all(inside)

    def set_topleft_center_view(self):
        # print("SET TOPLEFT")
        x_offset = (self.game_map.width // 2) - (SCREEN_WIDTH // 2)
        y_offset = (self.game_map.height // 2) - (SCREEN_HEIGHT // 2)
        self.topleft = (x_offset, y_offset)

    def get_map_cutout(self, grid):
        x, y = self.topleft
        grid = grid[x : x + self.width, y : y + self.height]
        return grid

    def get_absolute_map_position(self, position):
        return (position[0] + self.topleft[0], position[1] + self.topleft[1])

    def get_relative_screen_position(self, position):
        return (position[0] - self.topleft[0], position[1] - self.topleft[1])

    def get_subsurface_dimensions(self):
        return self.camera_screen.get_width(), self.camera_screen.get_height()

    def get_subsurface_topleft(self):
        return self.camera.topleft

    def get_current_view(self):
        pass

    def handle_user_input_camera_movement(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.try_move_left(event)
                self.try_move_right(event)
                self.try_move_up(event)
                self.try_move_down(event)

                if event.key == pygame.K_RETURN:
                    self.set_topleft_center_view()

    def try_move_left(self, event):
        if event.key in [pygame.K_a, pygame.K_LEFT]:
            x_temp, y_temp = (self.topleft[0] - self.scroll_speed, self.topleft[1])
            if self.within_boundaries(x_temp, y_temp):
                self.topleft = (x_temp, y_temp)

    def try_move_right(self, event):
        if event.key in [pygame.K_d, pygame.K_RIGHT]:
            x_temp, y_temp = (self.topleft[0] + self.scroll_speed, self.topleft[1])
            if self.within_boundaries(x_temp, y_temp):
                self.topleft = (x_temp, y_temp)

    def try_move_up(self, event):
        if event.key in [pygame.K_w, pygame.K_UP]:
            x_temp, y_temp = (self.topleft[0], self.topleft[1] - self.scroll_speed)
            if self.within_boundaries(x_temp, y_temp):
                self.topleft = (x_temp, y_temp)

    def try_move_down(self, event):
        if event.key in [pygame.K_s, pygame.K_DOWN]:
            x_temp, y_temp = (self.topleft[0], self.topleft[1] + self.scroll_speed)
            if self.within_boundaries(x_temp, y_temp):
                self.topleft = (x_temp, y_temp)
