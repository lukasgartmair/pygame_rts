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

def get_camera_screen_dimensions(camera_screen):
    return (camera_screen.get_width(), camera_screen.get_height())


def is_in_bounds(pos, camera_screen_dimensions):
    return 0 <= pos[0] < camera_screen_dimensions[0] and 0 <= pos[1] < camera_screen_dimensions[1]

class Camera:
    def __init__(self, top, left, width, height, game_map):
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        print(self.height)
        self.game_map = game_map
        self.canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.camera = pygame.Rect(self.top, self.left, self.width, self.height)
        self.camera_screen = self.canvas.subsurface(self.camera)
        self.scroll_speed = 5
        self.topleft = (self.top, self.left)
        self.set_topleft_center_view()          
        
    def check_screen_boundaries(self):
        
        print(self.topleft)
        x,y = self.topleft
        if x < 0:
            self.topleft = (0,y)
            print("no more left")
        elif y < 0:
            self.topleft = (x,0)
            print("no more left")
        elif x >= self.game_map.width-SCREEN_WIDTH:
            self.topleft = (self.game_map.width-SCREEN_WIDTH, y)
            print("no more right")
        elif y >= self.game_map.height-SCREEN_HEIGHT:
            self.topleft = (x, self.game_map.height-SCREEN_HEIGHT)
            print("no more down")
        else:
            pass
        
    def set_topleft_center_view(self):

        if self.game_map.width == SCREEN_WIDTH and self.game_map.height == SCREEN_HEIGHT:
            self.topleft = (0,0)
        else:
            x_offset = (self.game_map.width - SCREEN_WIDTH) // 2
            y_offset = (self.game_map.height - SCREEN_HEIGHT) // 2
            self.update_topleft = (x_offset, y_offset)
            
    def get_map_cutout(self, grid):
        x,y = self.topleft
        # grid = np.zeros((self.width, self.height))
        grid = grid[x:x+self.width,y:y+self.height]
        return grid

    def get_subsurface_dimensions(self):
        return self.camera_screen.get_width(), self.camera_screen.get_height()

    def get_subsurface_topleft(self):
        return self.camera.topleft
        
    def get_current_view(self):
        pass
        
    def check_user_input_camera_movement(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.move_left()
                if event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.move_right()
                if event.key in [pygame.K_w ,pygame.K_UP]:
                    self.move_up()
                if event.key in [pygame.K_s, pygame.K_DOWN]:
                    self.move_down()
        
        # TODO apply offset for camera with arrow movement
    def move_left(self):
        print("move left")
        self.check_screen_boundaries()
    def move_right(self):
        print("move right")
        self.check_screen_boundaries()
    def move_up(self):
        print("move up")
        self.check_screen_boundaries()
    def move_down(self):
        print("move down")
        self.check_screen_boundaries()

        