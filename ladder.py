#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 19:35:23 2024

@author: lukasgartmair
"""

from enum import Enum
import time


class EntryType(Enum):
    BID = 0
    ASK = 1


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
            
    def ask_is_valid(self, ask, bid):
        return ask.good == bid.good

    def get_accepted_ask(self, bid, valid_asks, settlement_connections):
        
        # neighbors_of_the_bidder = [n for n in settlement_connections.neighbors(bid.bidder.id)]
        # print(neighbors_of_the_bidder)

        return valid_asks[0]

    def resolve(self, settlement_connections):
        for bid in self.bids:
            valid_asks = [ask for ask in self.asks if self.ask_is_valid(ask, bid)]

            if valid_asks:
                accepted_ask = self.get_accepted_ask(bid, valid_asks, settlement_connections)
                self.resolutions.append(Resolution(bid, accepted_ask))

                self.bids.remove(bid)
                self.asks.remove(accepted_ask)

    def check_if_bidder_already_bidding_for_this_good(self, bidder, good):
        return bool([b for b in self.bids if b.bidder == bidder and b.good == good])

    def check_if_possible_asker_is_already_bidding_the_good(self, settlement, good):
        is_bidding_for_the_good = [
            b for b in self.bids if b.bidder == settlement and b.good == good
        ]
        return bool(is_bidding_for_the_good)

    def check_if_ask_for_certain_good_already_in_ladder(self, asker, good):
        ask_for_this_good_from_this_asker = [
            a for a in self.asks if a.asker == asker and a.good == good
        ]
        return bool(ask_for_this_good_from_this_asker)

    def create_ladder_entry(self, settlement, good, magnitude, price, entry_type):
        if entry_type == EntryType.BID:
            # time.sleep(0.5)
            if (
                self.check_if_bidder_already_bidding_for_this_good(settlement, good)
                == False
            ):
                bid = Bid(settlement, good, magnitude, price)
                self.remove_all_other_bids_from_bidder(settlement)
                self.bids.append(bid)

        elif entry_type == EntryType.ASK:
            if (
                self.check_if_possible_asker_is_already_bidding_the_good(
                    settlement, good
                )
                == False
            ):
                if (
                    self.check_if_ask_for_certain_good_already_in_ladder(
                        settlement, good
                    )
                    == False
                ):
                    ask = Ask(settlement, good, magnitude, price)
                    self.asks.append(ask)

    def create_possible_ask(self, settlement, good, magnitude, global_assets):
        if (
            self.check_if_ask_for_certain_good_already_in_ladder(settlement, good)
            == False
        ):
            trading_form = TradingForm(good=good)
            if settlement.settlement_goods.has_at_least_one_in_stock(trading_form):
                trading_good_price = global_assets[good].price
                self.create_ladder_entry(
                    settlement,
                    good,
                    settlement.trading_goods[good],
                    trading_good_price,
                    EntryType.ASK,
                )

    def create_possible_bids(self, settlements, global_assets):
        for s in settlements:
            if s.preferred_good != "":
                trading_form = TradingForm(
                    price=global_assets[s.preferred_good].price
                )

                affordable_magnitude = (
                    s.settlement_goods.calculate_affordable_magnitude(trading_form)
                )
                if affordable_magnitude > 0:
                    self.create_ladder_entry(
                        s,
                        s.preferred_good,
                        affordable_magnitude,
                        trading_form.price,
                        EntryType.BID,
                    )


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
