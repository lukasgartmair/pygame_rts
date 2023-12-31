#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 14:11:37 2023

@author: lukasgartmair
"""

import random
from collections import defaultdict
import pygame
from beautifultable import BeautifulTable
import re

from enum import Enum


class EntryType(Enum):
    BID = 0
    ASK = 1


def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n - 1, type))


class Bid:
    # SELLER
    # OFFER The bid price refers to the highest price a buyer will pay for a security
    def __init__(self, bidder, good, magnitude, price):
        self.bidder = bidder
        self.good = good
        self.magnitude = magnitude
        self.price = price


class Ask:
    # GEBOT The ask price refers to the lowest price a seller will accept for a security.
    def __init__(self, asker, good, magnitude, price):
        self.asker = asker
        self.good = good
        self.magnitude = magnitude
        self.price = price


class Ladder:
    def __init__(self, max_asks):
        self.max_asks = max_asks
        self.bids = []
        self.asks = []

    def add_ask(self, ask):
        self.asks.append(ask)

    def add_bid(self, bid):
        self.bids.append(bid)

    def resolve_open(self):
        pass

    def check_if_bidder_already_in_ladder(self, bidder):
        return any([b for b in self.bids if b.bidder == bidder])

    def check_if_max_asks_in_ladder_reached(self, asker):
        print([a for a in self.asks if a.asker == asker])
        return sum([True for a in self.asks if a.asker == asker]) <= self.max_asks

    def create_ladder_entry(self, settlement, good, magnitude, price, entry_type):
        if entry_type == EntryType.BID:
            bid = Bid(settlement, 1, good, price)
            if not self.check_if_bidder_already_in_ladder(settlement):
                self.add_bid(bid)
        elif entry_type == EntryType.ASK:
            ask = Ask(settlement, 1, good, price)
            if self.check_if_max_asks_in_ladder_reached(settlement):
                self.add_ask(ask)


class Trade:
    def __init__(self, settlements, global_path):
        self.settlements = settlements
        self.global_path = global_path

        self.possible_trading_goods = sorted(["brass", "silver", "wood", "rubins"])

        self.max_asks = len(self.possible_trading_goods)

        self.ladder = Ladder(self.max_asks)

        self.global_assets = nested_dict(2, int)
        self.initialize_global_assets()

    def render_global_assets(self, screen, game_font):
        vertical_offset = 25
        offset = 0

        table = BeautifulTable()
        table.set_style(BeautifulTable.STYLE_COMPACT)
        table.columns.alignment = BeautifulTable.ALIGN_LEFT
        table.rows.alignment = BeautifulTable.ALIGN_LEFT
        table.columns.header = ["good", "magnitude", "price"]
        for k, v in self.global_assets.items():
            row = [
                k,
                self.global_assets[k]["magnitude"],
                self.global_assets[k]["price"],
            ]
            table.append_row(row)

        splitted_table = re.split("\n", table.get_string())
        for line in splitted_table:
            text = game_font.render(line, True, (10, 0, 0))
            screen.blit(text, (0, offset))
            offset += vertical_offset

    def initialize_global_assets(self):
        for p in self.possible_trading_goods:
            self.global_assets[p]["magnitude"] = 0
            # self.global_assets[p]["price"] = random.randint(1, 10)
            self.global_assets[p]["price"] = 1

    def update_global_asset_magnitudes(self, trading_goods):
        for k, v in trading_goods.items():
            self.global_assets[k]["magnitude"] += v

    def transaction(self, ask, bid, verbose=False):
        if verbose:
            print("TRANSACTION")

    def create_possible_bids(self, settlements):
        for s in settlements:
            if s.preferred_good != "":
                preferred_good_price = self.global_assets[s.preferred_good]["price"]
                affordable_magnitude = (
                    s.settlement_goods.calculate_affordable_magnitude(
                        preferred_good_price
                    )
                )
                if affordable_magnitude > 0:
                    self.ladder.create_ladder_entry(
                        s,
                        s.preferred_good,
                        affordable_magnitude,
                        preferred_good_price,
                        EntryType.BID,
                    )

    def perform_trade(self, verbose=True):
        if verbose:
            print("perform trade")

        for k, v in self.global_path.subpaths.items():
            print(k)

            settlement_0 = [s for s in self.settlements if s.name == k[0]][0]
            settlement_1 = [s for s in self.settlements if s.name == k[1]][0]

            ss = [settlement_0, settlement_1]

            self.create_possible_bids(ss)

            for s in ss:
                for trading_good in self.possible_trading_goods:
                    trading_good_price = self.global_assets[trading_good]["price"]
                    if s.settlement_goods.is_in_stock(trading_good):
                        self.ladder.create_ladder_entry(
                            s,
                            trading_good,
                            s.trading_goods[trading_good],
                            trading_good_price,
                            EntryType.ASK,
                        )

        print(self.ladder.bids)
        print(self.ladder.asks)
        print(len(self.ladder.asks))
