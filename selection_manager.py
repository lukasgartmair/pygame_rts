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

    def deselect_settlement(self, settlement):
        settlement.deselect()
        self.selected_settlements.remove(settlement)

    def check_connection_condition(self):
        if len(self.selected_settlements) == 2:
            return True
        else:
            return False

    def check_any_settlement_clicked(self, mouse_position):
        self.any_settlement_clicked = False
        clicked_settlements = [
            s for s in self.settlements if s.is_clicked(mouse_position)
        ]
        self.any_settlement_clicked = any(clicked_settlements)
        if self.any_settlement_clicked:
            for s in self.settlements:
                print(s.sm_selection.current_state)
            print(clicked_settlements)
            self.clicked_settlement = clicked_settlements[0]
        else:
            self.clicked_settlement = None

    def handle_deselection_on_void_click(self):
        for s in self.settlements:
            if s.sm_selection.selected.is_active:
                self.deselect_settlement(s)

    def update_selected_settlements(self):
        self.selected_settlements = []
        for s in self.settlements:
            if s.sm_selection.selected.is_active:
                self.selected_settlements.append(s)

    def selection_and_void_click(self):
        if self.any_settlement_clicked == 0 and len(self.selected_settlements) in [
            1,
            2,
        ]:
            self.handle_deselection_on_void_click()
            return True
        else:
            return False

    def process_settlement_click(self):

        s = self.clicked_settlement

        if (
            s.sm_selection.not_selected.is_active
            and s.sm_connection.current_state == s.sm_connection.not_connected
            and len(self.selected_settlements) == 0
        ):
            s.select()
        elif (
            s.sm_selection.selected.is_active
            and s.sm_connection.not_connected.is_active
            and len(self.selected_settlements) == 1
            and s == self.selected_settlements[0]
        ):
            s.deselect()

        elif s.sm_selection.not_selected.is_active and s.sm_connection.connected.is_active and len(self.selected_settlements) == 0:
            print("here2")
            s.settlement_goods.preferred_good.update()

        if (
            len(self.selected_settlements) == 1
            and self.selected_settlements[0].sm_selection.selected.is_active
            and (self.selected_settlements[0].sm_connection.not_connected.is_active)
        ):
            s.select()

