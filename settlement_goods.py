#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 09:42:21 2023

@author: lukasgartmair
"""

import random

class SettlementGoods:
    
        def __init__(self, settlement, game_trade):
            self.settlement = settlement
            self.game_trade = game_trade
            self.initialze_trading_attributes()
            
            
        def initialze_trading_attributes(self):
            
            self.settlement.game_trade = self.game_trade
            self.settlement.gold = 20
            self.settlement.trading_goods = {}
            self.initialize_trading_goods()
            self.settlement.trading_stats = {"total": 0}
            
            self.settlement.preferred_good = ""
            self.settlement.preferred_good_index = -1
            
        def trading_good_available(self, trading_good):
            if self.settlement.trading_goods[trading_good] > 0:
                return True
            else:
                return False
            
        def is_affordable(self, price, magnitude):
            if self.settlement.gold >= price * magnitude:
                return True
            else:
                return False
            
        def buy_trading_good(self, trading_good, price, magnitude):
            if self.settlement.is_affordable(price, magnitude):
                self.settlement.gold -= price
                self.settlement.trading_goods[trading_good] += magnitude
            
        def sell_trading_good(self, trading_good, price, magnitude):
            self.settlement.gold += price*magnitude
            self.settlement.trading_goods[trading_good] -= magnitude
    
        def update_preferred_good(self):
            print(self.settlement.preferred_good_index)
            self.settlement.preferred_good_index += 1
            if self.settlement.preferred_good_index >= len(list(self.settlement.trading_goods.keys()))-1:
                self.settlement.preferred_good_index = -1
            
            # if self.settlement.preferred_good_index == len(list(self.settlement.trading_goods.keys())):
            #     self.settlement.select()
            #     return
                
            self.settlement.preferred_good = self.game_trade.possible_trading_goods[self.settlement.preferred_good_index]
            self.settlement.image = self.settlement.images[self.settlement.preferred_good+"_image"]
            if self.settlement.selected:
                self.settlement.deselect()
                
            print(self.settlement.preferred_good_index)
            print("-----")
        
        def update_trading_stats(self):
            self.settlement.trading_stats["total"] = sum(self.settlement.trading_goods.values())
    
        def initialize_trading_goods(self):
            for tg in self.game_trade.possible_trading_goods:
                self.settlement.trading_goods[tg] = random.randint(1, 5)
            self.game_trade.update_global_assets(self.settlement.trading_goods)