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
        self.clicked_settlement = None
        
    def check_connection_condition(self):
        if len(self.selected_settlements) == 2:
            return True
        else:
            return False
        
    def check_any_settlement_clicked(self, events):

        self.any_settlement_clicked = False
        clicked_settlements = [s for s in self.settlements if s.is_clicked(events)]
        self.any_settlement_clicked = any(
            clicked_settlements
            )
        if self.any_settlement_clicked:
            self.clicked_settlement = clicked_settlements[0]
        else:
            self.clicked_settlement = None
            
    def handle_deselection_on_void_click(self):
        for s in self.settlements:
            if s.connected:
                s.deselect_connected()
            else:
                s.deselect()
        self.selected_settlements = []
        
    def handle_successful_connection(self):

        for s in self.selected_settlements:
            if s.selected:
                s.deselect()
        
    def update_selected_settlements(self):
        self.selected_settlements = []
        for s in self.settlements:
            if s.selected:
                self.selected_settlements.append(s)
                
    def selection_and_void_click(self):
        if not self.any_settlement_clicked and len(self.selected_settlements) in [1,2]:
            self.handle_deselection_on_void_click()
            return True
        else:
            return False
        
    def process_settlement_click(self):

        s = self.clicked_settlement
        if not s.selected and not s.connected:
            s.select()
    
        if not s.selected and s.connected:
            if len(self.selected_settlements) == 0:
                s.select_connected()
            
        
        
        
    # def select_settlement(self, settlement):
        
    # def deselect_settlement(self, settlement):
        
        
        