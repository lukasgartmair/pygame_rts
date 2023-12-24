#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 17:29:36 2023

@author: lukasgartmair
"""

from enum import Enum
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class GameState(Enum):
    PLAYING = 0
    ENDED = 1

class GameEngine():
    
    def __init__(self):

        self.state = None
        self.currentPlayer = None
        self.tokens = 5
        self.tokens_available = self.tokens

        self.state = GameState.PLAYING
        
    def get_tokens_availabe(self):
        return self.tokens_available
    
    def remove_token(self):
        self.tokens_available += 1
    
    def place_token(self):
        if self.tokens_available > 0:
            self.tokens_available -= 1
            return True
        else:
            return False
        
    def check_win_condition(self):
        pass
    
    def render_token_count(self, screen, font_game):
        text = font_game.render("cities left to place: " +
                           str(self.get_tokens_availabe()), True, font_game.text_color)
        screen.blit(text, (SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.1))