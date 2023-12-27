#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 14:11:37 2023

@author: lukasgartmair
"""

import random
from collections import defaultdict
import camera
import pygame
from colors import settlement_stats_colors


def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n - 1, type))


class Trade:
    def __init__(self, settlements, global_path):
        self.settlements = settlements
        self.global_path = global_path

        self.possible_trading_goods = sorted(["brass", "silver", "wood", "rubins"])
        # self.possible_trading_goods = ["gold","silver"]

        self.global_assets = nested_dict(2, int)
        self.initialize_global_assets()

    def render_global_assets(self, screen, game_font):
        screen_dimensions = camera.get_camera_screen_dimensions(screen)
        screen_width, screen_height = screen_dimensions[0], screen_dimensions[1]
        vertical_offset = 25
        horizontal_offset = screen_width
        width = horizontal_offset
        height = screen_height - vertical_offset
        off = 0
        text = game_font.render("global_assets".upper(), True, (30, 0, 0))
        screen.blit(text, (screen_width - width, screen_height - height + off))
        off += vertical_offset
        f = "good - magn. - price"
        text = game_font.render(f, True, (30, 0, 0))
        screen.blit(text, (screen_width - width, screen_height - height + off))
        off += vertical_offset
        f = "-----------------"
        text = game_font.render(f, True, (30, 0, 0))
        screen.blit(text, (screen_width - width, screen_height - height + off))
        off += vertical_offset
        formatted_stats = []
        for k, v in self.global_assets.items():
            formatted_stats.append("{}: {} {}".format(k, self.global_assets[k]["magnitude"], self.global_assets[k]["price"]))

        for f in formatted_stats:
            text = game_font.render(f, True, (30, 0, 0))
            screen.blit(text, (screen_width - width, screen_height - height + off))
            off += vertical_offset

    def print_global_assets(self):
        for k, v in self.global_assets.items():
            print(k, self.global_assets[k]["magnitude"], self.global_assets[k]["price"])

    def initialize_global_assets(self):
        for p in self.possible_trading_goods:
            self.global_assets[p]["magnitude"] = 0
            self.global_assets[p]["price"] = random.randint(1, 10)

    def update_global_asset_magnitudes(self, trading_goods):
        for k, v in trading_goods.items():
            self.global_assets[k]["magnitude"] += v

    def transaction(self, settlement_0, settlement_1, need, verbose=False):
        if verbose:
            print("TRANSACTION")

    def perform_trade(self, verbose=False):
        if verbose:
            print("perform trade")
