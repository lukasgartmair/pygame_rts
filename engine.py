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


class GameEngine:
    def __init__(self):
        self.state = None
        self.currentPlayer = None
        self.settlements_available = 5
        self.win_condition = 100
        self.state = GameState.PLAYING

    def get_settlements_availabe(self):
        return self.settlements_available

    def remove_settlement(self):
        self.settlements_available += 1

    def place_settlement(self):
        if self.settlements_available > 0:
            self.settlements_available -= 1
            return True
        else:
            return False

    def check_win_condition(self, settlements):
        trading_good_sums = []
        for s in settlements:
            sum_goods = sum(s.trading_goods.values())
            trading_good_sums.append(sum_goods)
            if sum_goods >= self.win_condition:
                self.state = GameState.ENDED

        # print(max(trading_good_sums, default=0))

    def game_ended_by_player(self):
        self.state = GameState.ENDED

    def render_settlement_count(self, screen, font_game):
        text = font_game.render(
            "cities left to place: " + str(self.get_settlements_availabe()),
            True,
            font_game.text_color,
        )
        screen.blit(text, (SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.1))
