#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 14:11:37 2023

@author: lukasgartmair
"""

import random
import ladder
from beautifultable import BeautifulTable, BTRowCollection
import re
from collections import defaultdict


def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n - 1, type))


class Trade:
    def __init__(self, settlements, connection_manager):
        self.settlements = settlements
        self.connection_manager = connection_manager

        self.possible_trading_goods = sorted(["brass", "silver", "wood", "rubins"])

        self.trade_ladder = ladder.Ladder()

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
        rows = BTRowCollection(table)
        for k, v in self.global_assets.items():
            row = [
                k,
                self.global_assets[k]["magnitude"],
                self.global_assets[k]["price"],
            ]
            rows.append(row)

        splitted_table = re.split("\n", str(table))
        for line in splitted_table:
            text = game_font.render(line, True, (10, 0, 0))
            screen.blit(text, (0, offset))
            offset += vertical_offset

    def initialize_global_assets(self):
        for p in self.possible_trading_goods:
            self.global_assets[p]["magnitude"] = 0
            self.global_assets[p]["price"] = random.randint(1, 5)

    def add_goods_to_global_assets(self, settlement):
        for k, v in settlement.trading_goods.items():
            self.global_assets[k]["magnitude"] += v

    def remove_goods_from_global_assets(self, settlement):
        for k, v in settlement.trading_goods.items():
            self.global_assets[k]["magnitude"] -= v

    def get_transaction_magnitudes(self, bid, ask):
        magnitude = 0
        if bid.magnitude <= ask.magnitude:
            magnitude = bid.magnitude
        elif bid.magnitude > ask.magnitude:
            magnitude = ask.magnitude
        return magnitude

    def perform_buy(self, trading_form):
        bought = False
        bought = trading_form.bidder.settlement_goods.buy_trading_good(trading_form)
        print(
            "{} bought {} x {} for {}, {} each, from {}".format(
                trading_form.bidder.name,
                trading_form.magnitude,
                trading_form.good,
                trading_form.price * trading_form.magnitude,
                trading_form.price,
                trading_form.asker.name,
            )
        )
        return bought

    def perform_sell(self, trading_form):
        sold = False
        if trading_form.asker.settlement_goods.has_magnitude_in_stock(trading_form):
            sold = trading_form.asker.settlement_goods.sell_trading_good(trading_form)
            print(
                "{} sold {} x {} for {}, {} each, to {}".format(
                    trading_form.asker.name,
                    trading_form.magnitude,
                    trading_form.good,
                    trading_form.price * trading_form.magnitude,
                    trading_form.price,
                    trading_form.bidder.name,
                )
            )
        return sold

    def transaction(self, resolution):
        magnitude = 0
        magnitude = self.get_transaction_magnitudes(resolution.bid, resolution.ask)
        
        print(magnitude)
        
        transaction_successfull = False
        

        trading_form = ladder.TradingForm(
            bidder=resolution.bid.bidder,
            asker=resolution.ask.asker,
            good=resolution.bid.good,
            magnitude=magnitude,
            price=self.global_assets[resolution.bid.good]["price"],
        )

        bought = self.perform_buy(trading_form)
        sold = self.perform_sell(trading_form)

        transaction_successfull = bool(bought and sold)
        
        if bought == False:
            print("Failure in buying process")
        elif sold == False:
            print("Failure in selling process")
            
        return transaction_successfull

    def get_trading_settlements(self):
        trading_settlements = []
        settlement_ids = (
            self.connection_manager.settlement_connections.get_all_connected_settlement_ids()
        )
        for s_id in settlement_ids:
            s = [s for s in self.settlements if s.id == s_id][0]
            if s not in trading_settlements:
                trading_settlements.append(s)
        return trading_settlements

    def perform_trade(self, verbose=True):
        if verbose:
            print("perform trade")

        trading_settlements = self.get_trading_settlements()

        self.trade_ladder.create_possible_bids(trading_settlements, self.global_assets)

        unique_bid_goods = sorted(set([b.good for b in self.trade_ladder.bids]))

        connected_settlements = [s for s in self.settlements if s.connected]

        for requested_good in unique_bid_goods:
            minimum_requested_magnitude = min(
                [
                    b.magnitude
                    for b in self.trade_ladder.bids
                    if b.good == requested_good
                ]
            )
            for connected_settlement in connected_settlements:
                self.trade_ladder.create_possible_ask(
                    connected_settlement,
                    requested_good,
                    minimum_requested_magnitude,
                    self.global_assets,
                )

        print("bids")
        for b in self.trade_ladder.bids:
            print(b.__dict__)

        print("asks")
        for b in self.trade_ladder.asks:
            print(b.__dict__)

        self.trade_ladder.resolve()
        transactions = []
        transactions = [self.transaction(r) for r in self.trade_ladder.resolutions]