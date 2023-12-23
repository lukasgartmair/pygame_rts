#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 17:29:36 2023

@author: lukasgartmair
"""

from enum import Enum

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