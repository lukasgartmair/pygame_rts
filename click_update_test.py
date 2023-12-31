#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 20:40:17 2023

@author: lukasgartmair
"""

import pygame, sys, random
from pygame.locals import *
from pynput import mouse

pygame.init()
 
colors = {0:(255, 255, 255), 1:(0, 0, 0)}

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('My Game!')

# A simple generator for Fibonacci Numbers 
def fib(limit): 

    # Initialize first two Fibonacci Numbers  
    a, b = 0, 1

    # One by one yield next Fibonacci Number 
    while a < limit: 
        yield a 
        a, b = b, a + b 
        
x = fib(10) 

clicked = False

def on_move(x, y):
    pass

def on_click(x, y, button, pressed):
    global clicked
    if button == mouse.Button.left:
        clicked = True
    return False

def main () :
    color = 0
    counter = 0

    for event in pygame.event.get() :
      if event.type == pygame.QUIT :
          pygame.quit()
          sys.exit()
      # with mouse.Listener(on_click=on_click, on_move=on_move) as listener:
      #     listener.join()
      if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1:

              WINDOW.fill(colors[color])
              if color == 0:
                  color = 1
              else:
                  color = 0
              pygame.display.flip()
              next(x)

      counter += 1
      print(counter)


 
main()