#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 11:05:46 2024

@author: lukasgartmair
"""
from pathing import PathFinder
from settlement_graph import SettlementGraph

class ConnectionManager:
    def __init__(self, game_map):
        self.settlement_connections = SettlementGraph()

    def check_if_connection_exists(self, settlement):
        return bool(self.settlement_connections.are_connected())

    def remove_settlement(self, settlement, game_trade, game_engine):
        self.settlement_connections.remove_settlement(settlement)

        settlement.remove()
        game_trade.remove_goods_from_global_assets(settlement)
        game_engine.remove_settlement()

    def already_connected(self, selected_settlements):
        return self.settlement_connections.are_connected(
            selected_settlements[0], selected_settlements[1]
        )

    def connect_settlements(self, settlement_a, settlement_b, game_map):
        successfully_connected = False

        path = None

        pathfinder = PathFinder()
        path = pathfinder.find_path(
            game_map.grid, settlement_a.center, settlement_b.center
        )

        if path:
            self.settlement_connections.add_settlement_connection(
                settlement_a, settlement_b, path=path
            )

            settlement_a.got_connected()
            settlement_b.got_connected()

            # game_sound.play_connect_settlement()

            successfully_connected = True

        else:
            print("no_path_found")
            settlement_a.deselect()
            settlement_b.deselect()

            successfully_connected = False
        return successfully_connected
