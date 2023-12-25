#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 16:41:08 2023

@author: lukasgartmair
"""

import pygame
import numpy as np
import sys
import pygame.surfarray as surfarray

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()

    striped = np.zeros((SCREEN_WIDTH, SCREEN_HEIGHT, 3))
    striped[:] = (255, 0, 0)
    striped[:, ::3] = (0, 255, 255)
    surfarray.blit_array(screen, striped)

    pygame.display.flip()
