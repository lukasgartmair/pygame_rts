#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 20:22:34 2023

@author: lukasgartmair
"""

import pygame


class Font:
    def __init__(self):
        self.font = pygame.font.Font(self.font_style, self.font_size)
        self.font.set_bold(True)
        self.font_size = 30
        self.font_style = pygame.font.match_font("z003")
        self.text_color = (28, 0, 46)

    def get_default_font(self):
        return self.font
