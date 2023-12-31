#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 20:22:34 2023

@author: lukasgartmair
"""

import pygame

pygame.font.init()

styles = pygame.font.get_fonts()
# monospaced_ 2, 6, 7
font_style = pygame.font.match_font(styles[7])
font_size = 30


class GameFont(pygame.font.Font):
    def __init__(self, font_style, font_size):
        super().__init__(font_style, font_size)
        self.text_color = (0, 0, 0)
        self.set_bold(True)
