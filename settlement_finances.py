#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 16:27:47 2024

@author: lukasgartmair
"""

import settlement

class SettlementBalance:
    def __init__(self, settlement, game_trade):
        self.settlement = settlement
        self.game_trade = game_trade
        self.initialze_settlement_goods()

    def initialze_settlement_goods(self):
        self.settlement.game_trade = self.game_trade
        self.settlement.gold = 15
        self.settlement.trading_goods = {}
        self.initialize_trading_goods()
        self.settlement.trading_stats = {"total": 0}