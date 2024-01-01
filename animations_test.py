#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 21:27:22 2024

@author: lukasgartmair
"""

# Importing the pygame module
import pygame
from pygame.locals import *

# Initiate pygame and give permission
# to use pygame's functionality
pygame.init()

# Create a display surface object
# of specific dimension
window = pygame.display.set_mode((600, 600))


# Create a list of different sprites
# that you want to use in the animation
image_sprite = [pygame.image.load("sprite1.png").convert(),
                pygame.image.load("sprite2.png").convert()]


# Creating a new clock object to
# track the amount of time
clock = pygame.time.Clock()

# Creating a new variable
# We will use this variable to
# iterate over the sprite list
value = 0

# Creating a boolean variable that
# we will use to run the while loop
run = True

# Creating an infinite loop
# to run our game
while run:

    # Setting the framerate to 3fps just
    # to see the result properly
    clock.tick(0.5)

    # Setting 0 in value variable if its
    # value is greater than the length
    # of our sprite list
    if value >= len(image_sprite):
        value = 0

    # Storing the sprite image in an
    # image variable
    image = image_sprite[value]

    # Creating a variable to store the starting
    # x and y coordinate
    x = 0

    # Changing the y coordinate
    # according the value stored
    # in our value variable
    if value == 0:
        y = 100
    else:
        y = 0

    # Displaying the image in our game window
    window.blit(image, (x, y))

    # Updating the display surface
    pygame.display.update()

    # Filling the window with black color
    window.fill((0, 0, 0))

    # Increasing the value of value variable by 1
    # after every iteration
    value += 1