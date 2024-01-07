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
import itertools
import logging
import time
from dataclasses import dataclass
from datetime import datetime
from time import mktime
import pandas as pd
import copy
import trading_good

logger = logging.getLogger('root')

def convert_time_to_datetime(time_object):
    return datetime.fromtimestamp(mktime(time.gmtime(time_object)))


@dataclass
class GlobalAsset:

    def __init__(self, trading_good):

        self.good: str = trading_good
        self.timestamp: float = time.time()
        self.magnitude: int = 0
        self.price: int = random.randint(1, 5)


class Trade:

    def __init__(self, settlements, connection_manager):
        self.id_iterator = itertools.count()
        self.settlements = settlements
        self.connection_manager = connection_manager

        self.possible_trading_goods = trading_good.get_trading_goods()

        self.trade_ladder = ladder.Ladder()

        self.global_assets = {}

        self.transaction_history = {}

        self.transaction_id = -1

        self.initialize_global_assets()

    def initialize_global_assets(self):
        for p in self.possible_trading_goods:
            self.global_assets[p] = GlobalAsset(p)

    def increase_transaction_id(self):
        self.transaction_id = next(self.id_iterator)

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
                self.global_assets[k].magnitude,
                self.global_assets[k].price,
            ]
            rows.append(row)

        splitted_table = re.split("\n", str(table))
        for line in splitted_table:
            text = game_font.render(line, True, (10, 0, 0))
            screen.blit(text, (0, offset))
            offset += vertical_offset

    def add_goods_to_global_assets(self, settlement):
        for k, v in settlement.trading_goods.items():
            self.global_assets[k].timestamp = time.time()
            self.global_assets[k].magnitude += v

    def remove_goods_from_global_assets(self, settlement):
        for k, v in settlement.trading_goods.items():
            self.global_assets[k].timestamp = time.time()
            self.global_assets[k].magnitude -= v

    def get_transaction_magnitudes(self, bid, ask):
        magnitude = 0
        if bid.magnitude <= ask.magnitude:
            magnitude = bid.magnitude
        elif bid.magnitude > ask.magnitude:
            magnitude = ask.magnitude
        return magnitude

    def perform_buy(self, trading_form):
        bought = False
        bought = trading_form.bidder.settlement_balance.buy_trading_good(
            trading_form)

        logger.debug(
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
            sold = trading_form.asker.settlement_balance.sell_trading_good(
                trading_form)

            logger.debug(
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

    def create_transaction_history_entry(self, transaction_successful, trading_form, bidder_gold, asker_gold):
        
        self.transaction_history[self.transaction_id] = time.time(
        ), transaction_successful, trading_form, bidder_gold, asker_gold

    def get_transaction_history_df(self):

        transaction_data = []
    
        for k, v in self.transaction_history.items():
            transaction_data.append([k, convert_time_to_datetime(
                v[0]), v[1], v[2].good, v[2].magnitude, v[2].price,  v[2].magnitude * v[2].price, v[2].bidder.id,v[3], v[2].asker.id, v[4]])

        self.transaction_df = pd.DataFrame(transaction_data, columns=["id", "timestamp", "successful",
                    "good", "magnitude", "price_good",  "price_total", "bidder_id", "bidder_gold", "asker_id", "asker_gold"])

        return self.transaction_df

    def transaction(self, resolution):
        self.increase_transaction_id()
        print("transaction_id:  {}".format(self.transaction_id))
        magnitude = 0
        magnitude = self.get_transaction_magnitudes(
            resolution.bid, resolution.ask)

        transaction_successful = False

        trading_form = ladder.TradingForm(
            bidder=resolution.bid.bidder,
            asker=resolution.ask.asker,
            good=resolution.bid.good,
            magnitude=magnitude,
            price=self.global_assets[resolution.bid.good].price,
        )

        bought = self.perform_buy(trading_form)
        sold = self.perform_sell(trading_form)

        transaction_successful = bool(bought and sold)
        
        # print(transaction_successful)

        # print("here")
        self.create_transaction_history_entry(
            transaction_successful, trading_form, resolution.bid.bidder.settlement_balance.gold, resolution.ask.asker.settlement_balance.gold)
        
        # print(self.transaction_history)
        
        logger.debug("TRANSACTION ID")
        logger.debug(self.transaction_id)

        if bought == False:
            logger.debug("Failure in buying process")
        elif sold == False:
            logger.debug("Failure in selling process")
            
        self.trade_ladder.resolutions.remove(resolution)

        return trading_form

    def perform_trade(self):

        logger.debug("perform trade")
            
        settlements_connected_with_preferred_goods = [s for s in self.settlements if s.settlement_goods.preferred_good.name != "" and s.connected == True]

        self.trade_ladder.create_possible_bids(
            settlements_connected_with_preferred_goods, self.global_assets)
        
        if self.trade_ladder.bids:
            self.trade_ladder.create_possible_asks(
                self.settlements,
                self.possible_trading_goods,
                self.global_assets,
            )
            
        print(len(self.trade_ladder.bids))
        print(len(self.trade_ladder.asks))
        
        # print("bids")
        # for b in self.trade_ladder.bids:
        #     print(b.__dict__)

        # print("asks")
        # for b in self.trade_ladder.asks:
        #     print(b.__dict__)
        
        self.trade_ladder.resolve(
            self.connection_manager.settlement_connections)
        
        for s in self.settlements:
            self.trade_ladder.bids = []
            s.settlement_goods.preferred_good.set_back_to_default()
        
        for r in self.trade_ladder.resolutions:
            print(r.bid)
            print(r.ask)
            print("------")

        transactions = []
        transactions = [self.transaction(r)
                        for r in self.trade_ladder.resolutions]
        
        print(transactions)
        
        return transactions
