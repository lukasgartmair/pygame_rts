#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 08:09:39 2024

@author: lukasgartmair
"""

import pygame
import trade
import settlement
import matplotlib.pyplot as plt
import numpy as np
import simpy
import settlement
import level_map
import random
import settlement_goods
import connection_manager

pygame.init()

screen = pygame.display.set_mode((1, 1))

class TradeSimulator:
    def __init__(self):
        self.width, self.height = 100, 100
        self.number_of_settlements = 5
        self.number_of_trades = 3
        self.game_map = level_map.GameMap(test=True)
        self.connection_manager = connection_manager.ConnectionManager(
            self.game_map
        )

        self.game_trade = trade.Trade([], self.connection_manager)
        self.settlements = [settlement.Settlement((random.randint(0,self.width),random.randint(0,self.height)), self.game_trade)
                            for i in range(self.number_of_settlements)]
        self.game_trade.settlements = self.settlements
        self.transactions = []
        self.trading_history= {}
        
        self.global_assets = []
        self.transaction_history = []

        
        for s in self.settlements:
            s.settlement_goods = settlement_goods.SettlementGoods(s, self.game_trade)
            
    def set_random_preferred_goods(self):
            # for s in random.sample(self.settlements,random.randint(0,len(self.settlements))):
            for s in self.settlements:
                s.preferred_good = random.choice(self.game_trade.possible_trading_goods + [""])
        
    def create_random_connections(self):
        
        for settlement_a in self.settlements:
            for settlement_b in self.settlements:
                if settlement_a != settlement_b:
                    self.connection_manager.connect_settlements(settlement_a, settlement_b, self.game_map)

    def perform_trade(self):
        
        for i in range(self.number_of_trades):
            self.set_random_preferred_goods()

            self.create_random_connections()
            
            
            global_assets, transaction_history = self.game_trade.perform_trade()
            
            self.global_assets.append(global_assets)
            self.transaction_history.append(transaction_history)
            
    def terminate(self):
        pygame.display.quit()
        pygame.quit()
                
    def analyze(self):
        pass
                
if __name__ == "__main__":
    
    trade_simulator = TradeSimulator()
    trade_simulator.perform_trade()
    trade_simulator.terminate()
