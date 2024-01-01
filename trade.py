#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 14:11:37 2023

@author: lukasgartmair
"""

import random
from collections import defaultdict
from beautifultable import BeautifulTable, BTRowCollection
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
    # BUY The bid price refers to the highest price a buyer will pay for a security
    def __init__(self, bidder, good, magnitude, price):
        self.bidder = bidder
        self.good = good
        self.magnitude = magnitude
        self.price = price


class Ask:
    # SELL The ask price refers to the lowest price a seller will accept for a security.
    def __init__(self, asker, good, magnitude, price):
        self.asker = asker
        self.good = good
        self.magnitude = magnitude
        self.price = price


class Ladder:
    def __init__(self):
        self.bids = []
        self.asks = []
        self.resolutions = []

    def clear_asks(self):
        self.asks = []

    def clear_certain_good_asks(self, good):
        for ask in self.asks:
            if ask.good == good:
                self.asks.remove(ask)

    def remove_all_other_bids_from_bidder(self, bidder):
        bids = [b for b in self.bids if b.bidder == bidder]
        for bid in bids:
            self.bids.remove(bid)

    def resolve(self):
        for bid in self.bids:
            valid_asks = [a for a in self.asks if a.good == bid.good]

            if valid_asks:

                # TODO acceptance logic, nearest first etc.

                accepted_ask = valid_asks[0]
                self.resolutions.append(Resolution(bid, accepted_ask))

                self.bids.remove(bid)
                self.asks.remove(accepted_ask)

    def check_if_bidder_already_bidding_for_this_good(self, bidder, good):
        return bool([b for b in self.bids if b.bidder == bidder and b.good == good])

    def check_if_possible_asker_is_already_bidding_the_good(self, settlement, good):
        is_bidding_for_the_good = [
            b for b in self.bids if b.bidder == settlement and b.good == good]
        return bool(is_bidding_for_the_good)

    def check_if_ask_for_certain_good_already_in_ladder(self, asker, good):
        ask_for_this_good_from_this_asker = [
            a for a in self.asks if a.asker == asker and a.good == good]
        return bool(ask_for_this_good_from_this_asker)

    def create_ladder_entry(self, settlement, good, magnitude, price, entry_type):
        if entry_type == EntryType.BID:
            if self.check_if_bidder_already_bidding_for_this_good(settlement, good) == False:
                bid = Bid(settlement, good, magnitude, price)
                self.remove_all_other_bids_from_bidder(settlement)
                self.bids.append(bid)

        elif entry_type == EntryType.ASK:
            if self.check_if_possible_asker_is_already_bidding_the_good(settlement, good) == False:
                if self.check_if_ask_for_certain_good_already_in_ladder(settlement, good) == False:
                    ask = Ask(settlement, good, magnitude, price)
                    self.asks.append(ask)


class Resolution:
    def __init__(self, bid, ask):
        self.bid = bid
        self.ask = ask

    @property
    def bid(self):
        return self._bid

    @bid.setter
    def bid(self, b):
        if not isinstance(b, Bid):
            raise Exception("bid has to be of type Bid")
        self._bid = b

    @property
    def ask(self):
        return self._ask

    @ask.setter
    def ask(self, a):
        if not isinstance(a, Ask):
            raise Exception("ask has to be of type Ask")
        self._ask = a


class TradingForm:
    def __init__(self, bidder=None, asker=None, good=None, magnitude=None, price=None):
        self.bidder = bidder
        self.asker = asker
        self.good = good
        self.magnitude = magnitude
        self.price = price

    # @property
    # def bidder(self):
    #     return self._bidder

    # @bidder.setter
    # def bidder(self, b):
    #     if not isinstance(b, Bid.bidder):
    #         raise Exception("Bidder has to be of type Bid.Bidder")
    #     self._bidder = b

    # @property
    # def asker(self):
    #     return self._asker

    # @asker.setter
    # def asker(self, a):
    #     if not isinstance(a, Ask.asker):
    #         raise Exception("Asker has to be of type Ask.Asker")
    #     self.a_asker = a


class Trade:
    def __init__(self, settlements, connection_manager):
        self.settlements = settlements
        self.connection_manager = connection_manager

        self.possible_trading_goods = sorted(
            ["brass", "silver", "wood", "rubins"])

        self.ladder = Ladder()

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
            magnitude == ask.magnitude
        return magnitude

    def perform_buy(self, trading_form):

        bought = trading_form.bidder.settlement_goods.buy_trading_good(trading_form)
        print("{} bought {} x {} for {}, {} each, from {}".format(trading_form.bidder.name, trading_form.magnitude,
              trading_form.good, trading_form.price * trading_form.magnitude, trading_form.price, trading_form.asker.name))
        return bought

    def perform_sell(self, trading_form):

        if trading_form.asker.settlement_goods.has_magnitude_in_stock(trading_form):
            sold = trading_form.asker.settlement_goods.sell_trading_good(trading_form)
            print("{} sold {} x {} for {}, {} each, to {}".format(trading_form.asker.name, trading_form.magnitude,
                  trading_form.good, trading_form.price * trading_form.magnitude, trading_form.price, trading_form.bidder.name))
        return sold

    def transaction(self, resolution):

        magnitude = 0
        magnitude = self.get_transaction_magnitudes(
            resolution.bid, resolution.ask)

        trading_form = TradingForm(bidder=resolution.bid.bidder, asker=resolution.ask.asker,
                                   good=resolution.bid.good, magnitude=magnitude, price=self.global_assets[resolution.bid.good]["price"])

        bought = self.perform_buy(trading_form)
        sold = self.perform_sell(trading_form)

        return bool(bought and sold)

    def create_possible_ask(self, settlement, good, magnitude):

        if self.ladder.check_if_ask_for_certain_good_already_in_ladder(settlement, good) == False:

            if settlement.settlement_goods.has_at_least_one_in_stock(good):
                trading_good_price = self.global_assets[good]["price"]
                self.ladder.create_ladder_entry(
                    settlement,
                    good,
                    settlement.trading_goods[good],
                    trading_good_price,
                    EntryType.ASK,
                )

    def create_possible_bids(self, settlements):
        for s in settlements:
            if s.preferred_good != "":
                trading_form = TradingForm(
                    price=self.global_assets[s.preferred_good]["price"])

                affordable_magnitude = (
                    s.settlement_goods.calculate_affordable_magnitude(
                        trading_form
                    )
                )
                if affordable_magnitude > 0:
                    self.ladder.create_ladder_entry(
                        s,
                        s.preferred_good,
                        affordable_magnitude,
                        trading_form.price,
                        EntryType.BID,
                    )

    def get_trading_settlements(self):
        trading_settlements = []
        settlement_ids = self.connection_manager.settlement_connections.get_all_connected_settlement_ids()
        for s_id in settlement_ids:
            s = [s for s in self.settlements if s.id == s_id][0]
            if s not in trading_settlements:
                trading_settlements.append(s)
        return trading_settlements

    def perform_trade(self, verbose=True):
        if verbose:
            print("perform trade")

        trading_settlements = self.get_trading_settlements()

        self.create_possible_bids(trading_settlements)

        unique_bid_goods = sorted(set([b.good for b in self.ladder.bids]))

        connected_settlements = [s for s in self.settlements if s.connected]

        for requested_good in unique_bid_goods:

            minimum_requested_magnitude = min(
                [b.magnitude for b in self.ladder.bids if b.good == requested_good])
            for connected_settlement in connected_settlements:

                self.create_possible_ask(
                    connected_settlement, requested_good, minimum_requested_magnitude)

        print("bids")
        for b in self.ladder.bids:

            print(b.__dict__)

        print("asks")
        for b in self.ladder.asks:
            print(b.__dict__)

        self.ladder.resolve()
        transactions = []
        transactions = [self.transaction(r) for r in self.ladder.resolutions]

        print(transactions)
