#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 11:05:46 2024

@author: lukasgartmair
"""
from pathing import PathFinder
from colors import path_colors
from settlement_graph import SettlementGraph


def get_adjacent_cells(x, y, k=0):
    adjacent_cells = []
    for xi in range(-k, k + 1):
        for yi in range(-k, k + 1):
            adjacent_cells.append((x + xi, y + yi))
    adjacent_cells.remove((x, y))
    return adjacent_cells


class ConnectionManager:
    def __init__(self, game_map):
        self.settlement_connections = SettlementGraph()

    def check_if_connection_exists(self, settlement):
        return bool(self.settlement_connections.are_connected())

    def remove_settlement(self, settlement, game_engine):
        self.settlement_connections.remove_settlement(settlement)

        settlement.remove()
        game_engine.remove_settlement()

    def already_connected(self, selected_settlements):
        return self.settlement_connections.are_connected(
            selected_settlements[0], selected_settlements[1]
        )

    def connect_settlements(self, settlement_a, settlement_b, game_map, game_sound):
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

            game_sound.play_connect_settlement()

            successfully_connected = True

        else:
            print("no_path_found")
            settlement_a.deselect()
            settlement_b.deselect()

            successfully_connected = False
        return successfully_connected

    def map_paths_to_grid(self, game_map):
        mapped_grid = game_map.mapped_grid.copy()
        for node_a, node_b, data in self.settlement_connections.get_connections(
            include_data=True
        ):
            for p in data["path"]:
                mapped_grid[p[0], p[1]] = path_colors[0]

                adjacent_cells = get_adjacent_cells(p[0], p[1], k=3)

                for a in adjacent_cells:
                    mapped_grid[a[0], a[1]] = path_colors[0]
        return mapped_grid
