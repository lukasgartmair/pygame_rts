#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 20:22:34 2023

@author: lukasgartmair
"""

import pygame

pygame.init()

def get_default_font():

    font_size = 30
    font_style = pygame.font.match_font("z003")
    font = pygame.font.Font(font_style, font_size)
    font.set_bold(True)
    text_color = (28, 0, 46)
    
    return font
