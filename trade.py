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
        
    def perform_trade(self):
        
        for k,v in self.global_path.subpaths.items():
            pass
        