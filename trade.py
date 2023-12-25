#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 14:11:37 2023

@author: lukasgartmair
"""

class Trade():
    def __init__(self, settlements, global_path):
        
        self.settlements = settlements
        self.global_path = global_path
        
        self.possible_trading_goods = ["gold","silver","wood","spices"]
        #self.possible_trading_goods = ["gold","silver"]
        
    def remove_trading_good(self, settlement, out_of_stock):
        del settlement.trading_goods[out_of_stock]
        "deleted"
        
    def transaction(self, settlement_0, settlement_1, need, verbose=False):
        if verbose:
            print("TRANSACTION")

        if need not in settlement_0.trading_goods.keys():
            settlement_0.trading_goods[need] = 0
        
        if settlement_1.trading_goods[need] > 0:
            if verbose:
                print("available")
            settlement_1.trading_goods[need] -= 1
            settlement_0.trading_goods[need] += 1
            
            if verbose:
                print("after transaction")
                print("settlement_0.trading_goods[need]")
                try:
                    print(settlement_0.trading_goods[need])
                except:
                    pass
                print("settlement_1.trading_goods[need]")
                try:
                    print(settlement_1.trading_goods[need])
                except:
                    pass
                
            if settlement_1.trading_goods[need] == 0:
                self.remove_trading_good(settlement_1, need)
            
            return True

        if settlement_1.trading_goods[need] == 0:
            self.remove_trading_good(settlement_1, need)
            
            if verbose:
                print("after transaction")
                print("settlement_0.trading_goods[need]")
                try:
                    print(settlement_0.trading_goods[need])
                except:
                    pass
                print("settlement_1.trading_goods[need]")
                try:
                    print(settlement_1.trading_goods[need])
                except:
                    pass
            
            return False
        
    def perform_trade(self, verbose=False):
        if verbose:
            print("perform trade")
        
        for k,v in self.global_path.subpaths.items():
            name_settlement_0 = k[0]
            name_settlement_1 = k[1]
            
            settlement_0 = [s for s in self.settlements if s.name == name_settlement_0][0]
            settlement_1 = [s for s in self.settlements if s.name == name_settlement_1][0]
            
            if verbose:
                print("before")
                print("settlement_0.trading_goods")
                print(settlement_0.trading_goods)
                print("settlement_1.trading_goods")
                print(settlement_1.trading_goods)
            
            settlement_0_needs = []
            settlement_1_needs = []
            
            for trading_good in settlement_0.trading_goods.keys():
                if trading_good not in settlement_1.trading_goods.keys():
                    settlement_1_needs.append(trading_good)
            
            for trading_good in settlement_1.trading_goods.keys():
                if trading_good not in settlement_0.trading_goods.keys():
                    settlement_0_needs.append(trading_good)
            if verbose:
                print("settlement_0_needs")
                print(settlement_0_needs)
                print("settlement_1_needs")
                print(settlement_1_needs)
            
            successful_transactions_0 = []
            successful_transactions_1 = []
            
            if len(settlement_1_needs) == 0:    
            
                for need in settlement_0_needs:
                    result = self.transaction(settlement_0, settlement_1, need)
                    successful_transactions_0.append(result)
                    
            elif len(settlement_0_needs) == 0:
                
                for need in settlement_1_needs:
                    result = self.transaction(settlement_1, settlement_0, need)
                    successful_transactions_1.append(result)
                    
            else:

                for need in settlement_1_needs:
                    result = self.transaction(settlement_1, settlement_0, need)
                    successful_transactions_1.append(result)

                for i, need in enumerate(settlement_0_needs):
                    if i < sum(successful_transactions_0):
                        print("entered here")
                        result = self.transaction(settlement_0, settlement_1, need)
                        successful_transactions_0.append(result)
                    else:
                        break
            if verbose:
                print(successful_transactions_0)
                print(successful_transactions_1)
                print(sum(successful_transactions_0) == sum(successful_transactions_1))
                
                print("after")
                print("settlement_0.trading_goods")
                print(settlement_0.trading_goods)
                print("settlement_1.trading_goods")
                print(settlement_1.trading_goods)

    