#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 14:11:37 2023

@author: lukasgartmair
"""

import random
from collections import defaultdict

def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))

class Trade():
    def __init__(self, settlements, global_path):
        
        self.settlements = settlements
        self.global_path = global_path
        
        self.possible_trading_goods = sorted(["brass","silver","wood","rubins"])
        #self.possible_trading_goods = ["gold","silver"]
        
        self.global_assets = nested_dict(2, int)
        self.initialize_global_assets()
        
    def initialize_global_assets(self):
        
        for p in self.possible_trading_goods:
            self.global_assets[p]["magnitude"] = 0
            self.global_assets[p]["price"] = random.randint(1,10)
    
    def update_global_assets(self, trading_goods):
        for k,v in trading_goods.items():
            self.global_assets[k]["magnitude"] = 0
            self.global_assets[k]["magnitude"] += v
          
        # print("global_assets")
        # print(self.global_assets)
        
    def transaction(self, settlement_0, settlement_1, need, verbose=False):
        if verbose:
            print("TRANSACTION")
        
    def perform_trade(self, verbose=False):
        if verbose:
            print("perform trade")
        


    