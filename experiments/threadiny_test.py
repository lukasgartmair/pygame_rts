#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 08:56:23 2024

@author: lukasgartmair
"""

import pygame
import threading

pygame.init()
window = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

color = "red"
def get_input():
    global color
    color = input('enter color (e.g. blue): ')

input_thread = threading.Thread(target=get_input)
input_thread.start()

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False          

    window_center = window.get_rect().center
    window.fill(0)
    pygame.draw.circle(window, color, window_center, 100)
    pygame.display.flip()

pygame.quit()
exit()