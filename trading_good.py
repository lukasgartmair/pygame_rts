#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 18:33:07 2024

@author: lukasgartmair
"""


class TradingGood:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        
trading_goods = {
    "brass": TradingGood("brass", (255, 209, 33)),
    "rubins": TradingGood("rubins",(122, 17, 17)),     
    "silver": TradingGood("silver",(140, 140, 140)),     
    "wood": TradingGood("wood", (64, 0, 0)),

}

def get_trading_goods():
    return sorted(list(trading_goods.keys()))