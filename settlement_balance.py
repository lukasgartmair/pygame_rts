#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 16:27:47 2024

@author: lukasgartmair
"""

import logging
import animation

logger = logging.getLogger('root')


class SettlementBalance:
    def __init__(self, settlement, game_trade):
        self.settlement = settlement
        self.game_trade = game_trade
        self.gold_history = {}
        self.initialze_settlement_balance()

    def initialze_settlement_balance(self):
        self.gold = 15
        
    def calculate_affordable_magnitude(self, trading_form):
        affordable_magnitude = self.gold // trading_form.price
        return affordable_magnitude
    
    def is_affordable(self, trading_form):
        if self.gold >= trading_form.price * trading_form.magnitude:
            return True
        else:
            return False

    def buy_trading_good(self, trading_form):
        if self.is_affordable(trading_form):

            logger.debug(
                "{} balance BEFORE: {}".format(
                    self.settlement.name, self.settlement.settlement_balance.gold
                )
            )
            self.gold -= trading_form.price * trading_form.magnitude
            self.settlement.trading_goods[trading_form.good] += trading_form.magnitude

            logger.debug(
                "{} balance AFTER: {}".format(
                    self.settlement.name, self.settlement.settlement_balance.gold
                )
            )

            self.settlement.settlement_goods.preferred_good.set_back_to_default()

            return True

    def sell_trading_good(self, trading_form):
        if self.settlement.settlement_goods.has_magnitude_in_stock(trading_form):

            logger.debug(
                "{} balance BEFORE: {}".format(
                    self.settlement.name, self.gold
                )
            )
            self.gold += trading_form.price * trading_form.magnitude
            self.settlement.trading_goods[trading_form.good] -= trading_form.magnitude

            logger.debug(
                "{} balance AFTER: {}".format(
                    self.settlement.name, self.gold
                )
            )

        return True
