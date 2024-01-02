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
        self.initialze_settlement_goods()
        self.preferred_good_set = False

    def initialze_settlement_goods(self):
        self.settlement.game_trade = self.game_trade
        self.settlement.gold = 15
        self.settlement.trading_goods = {}
        self.initialize_trading_goods()
        self.settlement.trading_stats = {"total": 0}

        self.settlement.preferred_good = ""
        self.settlement.preferred_good_index = -1

    def has_at_least_one_in_stock(self, trading_form):
        print(trading_form)
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
            print(
                "{} balance BEFORE: {}".format(
                    self.settlement.name, self.settlement.gold
                )
            )
            self.settlement.gold -= trading_form.price * trading_form.magnitude
            self.settlement.trading_goods[trading_form.good] += trading_form.magnitude
            self.reset_preferred_good()

            print(
                "{} balance AFTER: {}".format(
                    self.settlement.name, self.settlement.gold
                )
            )

            return True

    def sell_trading_good(self, trading_form):
        if self.has_magnitude_in_stock(trading_form):
            print(
                "{} balance BEFORE: {}".format(
                    self.settlement.name, self.settlement.gold
                )
            )
            self.settlement.gold += trading_form.price * trading_form.magnitude
            self.settlement.trading_goods[trading_form.good] -= trading_form.magnitude
            print(
                "{} balance AFTER: {}".format(
                    self.settlement.name, self.settlement.gold
                )
            )
        return True

    def reset_preferred_good(self):
        self.settlement.preferred_good_index = -1
        self.update_preferred_good()

    def restore_last_preferred_good(self):
        self.settlement.preferred_good_index -= 1
        self.update_preferred_good()

    def update_preferred_good(self):
        self.preferred_good_set = True
        self.settlement.preferred_good_index += 1

        if self.settlement.preferred_good_index == len(
            list(self.settlement.trading_goods.keys())
        ):
            self.reset_preferred_good()

        if self.settlement.preferred_good_index >= 0:
            self.settlement.preferred_good = self.game_trade.possible_trading_goods[
                self.settlement.preferred_good_index
            ]
            # introduced for test purposes, check whether it has side effects!
            if self.settlement.images:
                self.settlement.image = self.settlement.images[
                    self.settlement.preferred_good + "_image"
                ]
        else:
            self.settlement.deselect()

    def update_trading_stats(self):
        self.settlement.trading_stats["total"] = sum(
            self.settlement.trading_goods.values()
        )

    def initialize_trading_goods(self):
        for tg in self.game_trade.possible_trading_goods:
            self.settlement.trading_goods[tg] = random.randint(1, 5)
        self.game_trade.add_goods_to_global_assets(self.settlement)
