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
import pandas as pd

pygame.init()

screen = pygame.display.set_mode((1, 1))

class TradeSimulator:
    def __init__(self):
        self.width, self.height = 100, 100
        self.number_of_settlements = 3
        self.number_of_rounds = 3
        self.game_map = level_map.GameMap(test=True)
        self.connection_manager = connection_manager.ConnectionManager(self.game_map)

        self.game_trade = trade.Trade([], self.connection_manager)
        self.settlements = []

        self.game_trade.settlements = self.settlements
        self.transactions = []
        self.trading_history = {}

        self.global_assets = []
        self.transaction_history = []
        self.df = None
        
    def set_random_preferred_goods(self):
        # for s in random.sample(self.settlements,random.randint(0,len(self.settlements))):
        for s in self.settlements:
            s.preferred_good = random.choice(
                self.game_trade.possible_trading_goods + [""]
            )

    def create_random_connections(self):
        for settlement_a in self.settlements:
            for settlement_b in self.settlements:
                if settlement_a != settlement_b:
                    self.connection_manager.connect_settlements(
                        settlement_a, settlement_b, self.game_map
                    )
                    
    def create_new_settlement(self):
        s = settlement.Settlement(
            (random.randint(0, self.width), random.randint(0, self.height))
        )
        s.settlement_goods = settlement_goods.SettlementGoods(s, self.game_trade)
        self.game_trade.add_goods_to_global_assets(s)
        self.settlements.append(s)
        
        print("settlement created")

    def run(self):

        for i in range(self.number_of_rounds):
            
            self.global_assets = []
            
            if len(self.settlements) < self.number_of_settlements:
                self.create_new_settlement()
                
            print(len(self.settlements))
            
            self.set_random_preferred_goods()

            self.create_random_connections()

            self.game_trade.perform_trade()
            
            self.global_assets = self.game_trade.global_assets
            
            # print(self.global_assets)
            
            global_assets_formatted = self.format_global_assets()
            
            self.df = pd.DataFrame(global_assets_formatted)
            
            print(self.df)

    def terminate(self):
        pygame.display.quit()
        pygame.quit()
        
    def format_global_assets(self):
        global_assets_formatted = []
                            
        for assets in self.global_assets:
            for k,v in assets[1].items():
                global_assets_formatted.append((assets[0],k,v["magnitude"],v["price"]))
        return global_assets_formatted

    def analyze(self):

        successfull_transactions = {}
        failed_transactions = {}
        for x in self.transaction_history:
            for k,v in x.items():
                if v[1] == True:
                    successfull_transactions[k] = v
                else:
                    failed_transactions[k] = v
                    
        global_assets_formatted = self.format_global_assets()
        self.df = pd.DataFrame(global_assets_formatted)

if __name__ == "__main__":
    trade_simulator = TradeSimulator()
    trade_simulator.run()
    trade_simulator.analyze()
    df = trade_simulator.df
    trade_simulator.terminate()
