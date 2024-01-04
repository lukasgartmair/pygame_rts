#!/usr/bin/env python3
# example_03.py

import pygame
import particlepy
import sys
import time
import random

import particle

pygame.init()

# pygame config
SIZE = 800, 800
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("ParticlePy example program")
pygame.mouse.set_visible(False)

# timing
clock = pygame.time.Clock()
FPS = 60

particle = particle.Particle()

# main loop
while True:
    # quit window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    

    particle.update()
    particle.emit_particles()
    particle.render(screen)

    # update display
    pygame.display.update()

    screen.fill((34, 40, 49))

    clock.tick(60)