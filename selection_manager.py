#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 08:31:43 2023

@author: lukasgartmair
"""

class SelectionManager:
    def __init__(self, settlements, any_settlement_clicked):
        self.settlements = settlements
        self.selected_settlements = []
        self.any_settlement_clicked = any_settlement_clicked
        
    def check_connection_condition(self):
        if len(self.selected_settlements) == 2:
            return True
        else:
            return False
        
    def check_any_settlement_clicked(self, events):

        self.any_settlement_clicked = False
        self.any_settlement_clicked = any(
            [s.check_if_clicked(events) for s in self.settlements])
        
    def handle_deselection_on_void_click(self):
        for s in self.settlements:
            if s.connected:
                s.deselect_connected()
            else:
                s.deselect()
        self.selected_settlements = []
        
    def update_selected_settlements(self):
        self.selected_settlements = []
        for s in self.settlements:
            if s.selected:
                self.selected_settlements.append(s)