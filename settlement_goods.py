#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 09:42:21 2023

@author: lukasgartmair
"""

import random
import logging

logger = logging.getLogger('root')

class PreferredGood:
    def __init__(self, settlement, possible_trading_goods, name=""):
        self.settlement = settlement
        self.possible_trading_goods = possible_trading_goods
        self.name = ""
        self.once_manually_set = False
        self.index = 0
        
    def set_last_index(self):
        self.index -= 1
        
    def set_back_to_default(self):
        self.index = 0
        if self.settlement.images:
            self.settlement.image = self.settlement.images[
                "main_image"
            ]
        
    def update(self):

        print(self.index)
        self.once_manually_set = True
        self.index += 1

        if self.index == len(
            list(self.possible_trading_goods)
        )+1:
            self.set_back_to_default()

        if self.index > 0:      
                self.name = self.possible_trading_goods[self.index-1]
                self.settlement.image = self.settlement.images[
                self.name + "_image"
            ]
            
        print(self.index)
        print("-----")

class SettlementGoods:
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

        self.preferred_good = PreferredGood(self.settlement, self.game_trade.possible_trading_goods)
        
        self.gold_history = {}

    def has_at_least_one_in_stock(self, trading_form):
        logger.debug(trading_form)
        if self.settlement.trading_goods[trading_form.good] > 0:
            return True
        else:
            return False

    def has_magnitude_in_stock(self, trading_form):
        if self.settlement.trading_goods[trading_form.good] >= trading_form.magnitude:
            return True
        else:
            return False

    def calculate_affordable_magnitude(self, trading_form):
        affordable_magnitude = self.settlement.gold // trading_form.price
        return affordable_magnitude

    def is_affordable(self, trading_form):
        if self.settlement.gold >= trading_form.price * trading_form.magnitude:
            return True
        else:
            return False

    def buy_trading_good(self, trading_form):
        if self.settlement.settlement_goods.is_affordable(trading_form):

            logger.debug(
                "{} balance BEFORE: {}".format(
                    self.settlement.name, self.settlement.gold
                )
            )
            self.settlement.gold -= trading_form.price * trading_form.magnitude
            self.settlement.trading_goods[trading_form.good] += trading_form.magnitude

            logger.debug(
                "{} balance AFTER: {}".format(
                    self.settlement.name, self.settlement.gold
                )
            )

            self.preferred_good.set_back_to_default()

            return True

    def sell_trading_good(self, trading_form):
        if self.has_magnitude_in_stock(trading_form):

            logger.debug(
                "{} balance BEFORE: {}".format(
                    self.settlement.name, self.settlement.gold
                )
            )
            self.settlement.gold += trading_form.price * trading_form.magnitude
            self.settlement.trading_goods[trading_form.good] -= trading_form.magnitude

            logger.debug(
                "{} balance AFTER: {}".format(
                    self.settlement.name, self.settlement.gold
                )
            )
        return True

    def reset_preferred_good_index(self):
        print("here")
        self.preferred_good.index = 0
        self.settlement.image = self.settlement.images[
            self.preferred_good.name + "_image"]

    def restore_last_preferred_good(self):
        self.preferred_good.set_last_index()
        self.preferred_good.update()


    def update_trading_stats(self):
        self.settlement.trading_stats["total"] = sum(
            self.settlement.trading_goods.values()
        )

    def initialize_trading_goods(self):
        for tg in self.game_trade.possible_trading_goods:
            self.settlement.trading_goods[tg] = random.randint(1, 5)
        self.game_trade.add_goods_to_global_assets(self.settlement)
