#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 23:48:08 2023

@author: lukasgartmair
"""

import pygame

def load_title_screen_background(screen):
    background = pygame.image.load('images/start_background.png').convert()
    background = pygame.transform.smoothscale(background, screen.get_size())
    return background