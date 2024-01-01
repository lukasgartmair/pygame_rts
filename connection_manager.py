#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 11:05:46 2024

@author: lukasgartmair
"""

from settlement_graph import SettlementGraph
from path import Path

class ConnectionManager:
    def __init__(self, game_map, game_sound):
        
        self.path = Path(game_map, game_sound)
        self.settlement_connections = SettlementGraph()

    def check_if_connection_exists(self, settlement):
        return bool(self.settlement_connections.are_connected())

    def add_settlement_connection(self, a, b, length, chain):
        
        self.settlement_connections.add_edge(a,b)
        
        self.path.subpaths[a, b] = {"length": length, "chain": chain}
        self.path.remove_perturbation_keys()

    def remove_settlement(self, settlement, game_engine):
        
        if any([settlement.name in key for key in self.path.subpaths]):
            del self.path.subpaths[settlement.name]
        self.settlement_connections.remove_settlement(settlement)
        
        settlement.remove()
        game_engine.remove_settlement()
        
    def already_connected(self, selected_settlements):
        return self.settlement_connections.are_connected(selected_settlements[0], selected_settlements[1])

    def connect_settlements(self, settlement_a, settlement_b, game_map, game_sound):
        successfully_connected = False

        local_path = None

        local_path = self.path.pathfinder.find_path(
            game_map.grid, settlement_a.center, settlement_b.center
        )

        if local_path:
            
            self.settlement_connections.add_settlement_connection(settlement_a, settlement_b)

            self.add_settlement_connection(
                settlement_a.name, settlement_b.name, len(local_path), local_path
            )
            settlement_a.got_connected()
            settlement_b.got_connected()
            
            game_sound.play_connect_settlement()

            successfully_connected = True

        else:
            print("no_path_found")
            settlement_a.deselect()
            settlement_b.deselect()

            successfully_connected = False
        return successfully_connected