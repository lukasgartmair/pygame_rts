#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 08:09:39 2024

@author: lukasgartmair
"""

import pygame
import trade
import settlement
import settlement_goods
import matplotlib.pyplot as plt
import numpy as np
import simpy
import settlement
import level_map
import random
import settlement_goods
import connection_manager
import pandas as pd
import copy
from settlement_balance import SettlementBalance

pygame.init()

screen = pygame.display.set_mode((1, 1))


class TradeSimulator:
    def __init__(self):
        self.width, self.height = 100, 100
        self.number_of_settlements = 10
        self.number_of_rounds = 5
        self.game_map = level_map.GameMap(test=True)
        self.connection_manager = connection_manager.ConnectionManager(
            self.game_map)

        self.game_trade = trade.Trade([], self.connection_manager)
        self.settlements = []

        self.game_trade.settlements = self.settlements
        self.transactions = []
        self.trading_history = {}

        self.global_assets = {}
        self.transaction_history = []
        self.global_assets_df = None
        self.transaction_df = None

    def set_random_preferred_goods(self):
        # for s in random.sample(self.settlements,random.randint(0,len(self.settlements))):
        
        rnd_goods = random.sample(self.game_trade.possible_trading_goods*100,len(self.settlements))    
        
        for i,s in enumerate(self.settlements):
            s.settlement_goods.preferred_good = settlement_goods.PreferredGood(s, self.game_trade.possible_trading_goods, rnd_goods[i])

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
        s.settlement_goods = settlement_goods.SettlementGoods(
            s, self.game_trade)
        self.settlement_balance = SettlementBalance(self, game_trade)
        self.game_trade.add_goods_to_global_assets(s)
        self.settlements.append(s)

        print("settlement created")

    def run(self):
        
        for i in range(self.number_of_settlements):
            self.create_new_settlement()

        self.create_random_connections()

        for i in range(self.number_of_rounds):
            print("---------")
            print("round")
            print(i)
            
            self.set_random_preferred_goods()

            self.game_trade.perform_trade()

            self.global_assets[i] = copy.deepcopy(
                self.game_trade.global_assets)

            global_assets_formatted = self.format_global_assets()

            self.global_assets_df = pd.DataFrame(global_assets_formatted)

    def terminate(self):
        pygame.display.quit()
        pygame.quit()

    def format_global_assets(self):
        global_assets_formatted = []

        for k, v in trade_simulator.global_assets.items():
            for ki, vi in v.items():

                global_assets_formatted.append(
                    (k, ki, vi.timestamp, vi.magnitude, vi.price))

        return global_assets_formatted

    def analyze_global_assets(self):

        global_assets_formatted = self.format_global_assets()

        self.global_assets_df = pd.DataFrame(global_assets_formatted)
        col_names = ["round", "good", "timestamp", "magnitude", "price"]
        self.global_assets_df.columns = col_names
        self.global_assets_df["round"].astype('int32')

    def analyze_transactions(self):

        self.transaction_df = copy.deepcopy(self.game_trade.get_transaction_history_df())

    def plot(self):
        grouped_by_good_and_round = global_assets_df.groupby(
            ['good', 'round'], as_index=False)["magnitude"].sum()

        ax = plt.subplot()

        pivot = grouped_by_good_and_round.pivot_table(
            index="round", columns="good", values='magnitude', aggfunc='sum')
        pivot.plot()


if __name__ == "__main__":
    trade_simulator = TradeSimulator()
    trade_simulator.run()
    trade_simulator.analyze_global_assets()
    global_assets_df = trade_simulator.global_assets_df
    trade_simulator.analyze_transactions()
    transaction_df = trade_simulator.transaction_df
    # trade_simulator.plot()
    trade_simulator.terminate()
