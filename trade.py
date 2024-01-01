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
    def __init__(self, max_asks):
        self.max_asks = max_asks
        self.bids = []
        self.asks = []

    def clear_asks(self):
        self.asks = []
        
    def clear_certain_good_asks(self, good):
        for ask in self.asks:
            if ask.good == good:
                self.asks.remove(ask)
                
    def update(self):
        pass

    def add_ask(self, ask):
        self.asks.append(ask)

    def add_bid(self, bid):
        self.bids.append(bid)
        
    def remove_all_other_bids_from_bidder(self, bidder):
        bids = [b for b in self.bids if b.bidder == bidder]
        for bid in bids:
            self.bids.remove(bid)

    def resolve(self):
        resolutions = []
        for bid in self.bids:
            valid_asks = [a for a in self.asks if a.good == bid.good and a.magnitude > 0]

            if valid_asks:
                random.shuffle(valid_asks)
                accepted_ask = valid_asks[0]
                resolutions.append((accepted_ask,bid))
                
                self.bids.remove(bid)
                self.asks.remove(accepted_ask)

        return resolutions

    def check_if_bidder_already_bidding_for_this_good(self, bidder, good):
        return bool([b for b in self.bids if b.bidder == bidder and b.good == good])
    
    def check_if_possible_asker_is_already_bidding_the_good(self, settlement, good):
        is_bidding_for_the_good = [b for b in self.bids if b.bidder == settlement and b.good == good]
        return bool(is_bidding_for_the_good)       

    def check_if_ask_for_certain_good_already_in_ladder(self, asker, good):
        ask_for_this_good_from_this_asker = [a for a in self.asks if a.asker == asker and a.good == good]
        return bool(ask_for_this_good_from_this_asker)       
    
    def create_ladder_entry(self, settlement, good, magnitude, price, entry_type):
        if entry_type == EntryType.BID:
            if self.check_if_bidder_already_bidding_for_this_good(settlement, good) == False:
                bid = Bid(settlement, good, magnitude, price)
                self.remove_all_other_bids_from_bidder(settlement)
                self.add_bid(bid)
                
        elif entry_type == EntryType.ASK:
            if self.check_if_possible_asker_is_already_bidding_the_good(settlement, good) == False:
                if self.check_if_ask_for_certain_good_already_in_ladder(settlement, good) == False:
                    ask = Ask(settlement, good, magnitude, price)
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

    def update_global_asset_magnitudes(self, trading_goods):
        for k, v in trading_goods.items():
            self.global_assets[k]["magnitude"] += v

    def transaction(self, ask, bid):
        
        good = bid.good
        
        magnitude = 0
        if bid.magnitude <= ask.magnitude:
            magnitude = bid.magnitude
        elif bid.magnitude > ask.magnitude:
            magnitude == ask.magnitude
        
        bid.bidder.settlement_goods.buy_trading_good(good, self.global_assets[good]["price"], magnitude)
        print("{} bought {} x {} for {} from {}".format(bid.bidder.name, magnitude, good, self.global_assets[good]["price"] * bid.magnitude, ask.asker.name))
        ask.asker.settlement_goods.sell_trading_good(good, self.global_assets[good]["price"], magnitude) 
        print("{} sold {} x {} for {} to {}".format(ask.asker.name, magnitude, good, self.global_assets[good]["price"] * magnitude, bid.bidder.name))
        return True
    
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

        trading_settlements = []
        
        for k, v in self.global_path.subpaths.items():
            print(k)

            settlement_a = [s for s in self.settlements if s.name == k[0]][0]
            settlement_b = [s for s in self.settlements if s.name == k[1]][0]
            
            trading_settlements.append((settlement_a, settlement_b))

        for traders in trading_settlements:
            
            settlement_a, settlement_b = traders

            self.create_possible_bids([settlement_a, settlement_b])
            
        unique_bid_goods = sorted(set([b.good for b in self.ladder.bids]))
        
        connected_settlements = [s for s in self.settlements if s.connected]
        
        for requested_good in unique_bid_goods:
            
            minimum_requested_magnitude = min([b.magnitude for b in self.ladder.bids if b.good == requested_good])
            for connected_settlement in connected_settlements:
                
                self.create_possible_ask(connected_settlement, requested_good, minimum_requested_magnitude)
                
        print("bids")
        for b in self.ladder.bids:

            print(b.__dict__)
        
        print("asks")        
        for b in self.ladder.asks:
            print(b.__dict__)
                
        resolutions = []
        resolutions = self.ladder.resolve()
        transactions = []
        transactions = [self.transaction(a, b) for a,b in resolutions]
        
        print(transactions)
        
