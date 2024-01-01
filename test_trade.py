#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 14:41:56 2024

@author: lukasgartmair
"""
import unittest
import trade
from faker import Faker
import itertools
import connection_manager
import level_map
from ladder import Ladder, TradingForm, EntryType, Bid, Ask
from settlement_goods import SettlementGoods

faker = Faker()


class TestSettlement:
    id_iterator = itertools.count()

    def __init__(self):
        self.id = next(self.id_iterator)
        self.name = faker.city()
        self.images = {}


class TestMethods(unittest.TestCase):
    def setUp(self):
        self.test_settlement = TestSettlement()
        self.test_settlement2 = TestSettlement()
        self.test_settlement3 = TestSettlement()
        self.settlements = [
            self.test_settlement,
            self.test_settlement2,
            self.test_settlement3,
        ]
        self.connection_manager = connection_manager.ConnectionManager(
            level_map.GameMap(test=True)
        )
        self.test_trade = trade.Trade(self.settlements, self.connection_manager)
        for s in self.settlements:
            s.settlement_goods = SettlementGoods(s, self.test_trade)

        self.test_good = "silver"
        self.test_magnitude = 2
        self.test_price = 10
        self.test_ladder = Ladder()

    def test_bid(self):
        self.test_bid = Bid(
            self.test_settlement, self.test_good, self.test_magnitude, self.test_price
        )
        self.assertEqual(self.test_bid.bidder, self.test_settlement)

    def test_ask(self):
        self.test_ask = Ask(
            self.test_settlement, self.test_good, self.test_magnitude, self.test_price
        )
        self.assertEqual(self.test_ask.asker, self.test_settlement)

    def test_ladder(self):
        self.test_ladder.create_ladder_entry(
            self.test_settlement,
            self.test_good,
            self.test_magnitude,
            self.test_price,
            EntryType.BID,
        )
        self.assertEqual(len(self.test_ladder.bids), 1)

        self.test_ladder.create_ladder_entry(
            self.test_settlement,
            self.test_good,
            self.test_magnitude,
            self.test_price,
            EntryType.ASK,
        )
        self.assertEqual(len(self.test_ladder.asks), 0)

        self.test_good = "gold"
        self.test_ladder.create_ladder_entry(
            self.test_settlement,
            self.test_good,
            self.test_magnitude,
            self.test_price,
            EntryType.ASK,
        )
        self.assertEqual(len(self.test_ladder.asks), 1)

        self.test_ladder.clear_asks()
        self.assertEqual(len(self.test_ladder.asks), 0)

    def test_ladder2(self):
        self.test_good = "rubins"
        self.test_ladder.create_ladder_entry(
            self.test_settlement,
            self.test_good,
            self.test_magnitude,
            self.test_price,
            EntryType.ASK,
        )
        self.assertEqual(len(self.test_ladder.asks), 1)

        self.test_good = "brass"
        self.test_ladder.create_ladder_entry(
            self.test_settlement,
            self.test_good,
            self.test_magnitude,
            self.test_price,
            EntryType.ASK,
        )
        self.assertEqual(len(self.test_ladder.asks), 2)

        self.test_ladder.clear_certain_good_asks(self.test_good)
        self.assertEqual(len(self.test_ladder.asks), 1)

    def test_ladder3(self):
        self.test_good = "rubins"
        self.test_ladder.create_ladder_entry(
            self.test_settlement,
            self.test_good,
            self.test_magnitude,
            self.test_price,
            EntryType.BID,
        )
        self.assertEqual(len(self.test_ladder.bids), 1)

        self.test_ladder.remove_all_other_bids_from_bidder(self.test_settlement)
        self.assertEqual(len(self.test_ladder.bids), 0)

        self.test_ladder.create_ladder_entry(
            self.test_settlement,
            self.test_good,
            self.test_magnitude,
            self.test_price,
            EntryType.BID,
        )
        self.assertEqual(len(self.test_ladder.bids), 1)

        self.test_ladder.create_ladder_entry(
            self.test_settlement,
            self.test_good,
            self.test_magnitude,
            self.test_price,
            EntryType.BID,
        )
        self.assertEqual(len(self.test_ladder.bids), 1)

    def test_ladder_resolve(self):
        self.test_good = "rubins"
        self.test_ladder.create_ladder_entry(
            self.test_settlement,
            self.test_good,
            self.test_magnitude,
            self.test_price,
            EntryType.BID,
        )

        self.test_good = "rubins"
        self.test_ladder.create_ladder_entry(
            self.test_settlement2,
            self.test_good,
            self.test_magnitude,
            self.test_price,
            EntryType.ASK,
        )

        self.test_ladder.resolve()
        self.assertEqual(len(self.test_ladder.resolutions), 1)

    def test_trading_form(self):
        self.test_bid = Bid(
            self.test_settlement, self.test_good, self.test_magnitude, self.test_price
        )
        self.test_ask = Ask(
            self.test_settlement2, self.test_good, self.test_magnitude, self.test_price
        )

        test_trading_form = TradingForm(
            bidder=self.test_bid.bidder,
            asker=self.test_ask.asker,
            good=self.test_good,
            magnitude=self.test_magnitude,
            price=self.test_price,
        )

        self.assertEqual(test_trading_form.bidder != None, True)
        self.assertEqual(test_trading_form.asker != None, True)
        self.assertEqual(test_trading_form.good != None, True)
        self.assertEqual(test_trading_form.magnitude != None, True)
        self.assertEqual(test_trading_form.price != None, True)

    def test_buy_goods(self):
        self.test_settlement.gold = 50
        self.test_good = "rubins"
        self.test_settlement.trading_goods["rubins"] = 2

        self.assertEqual(self.test_settlement.gold, 50)
        self.assertEqual(self.test_settlement.trading_goods["rubins"], 2)
        test_trading_form = TradingForm(
            good=self.test_good, magnitude=self.test_magnitude, price=self.test_price
        )

        self.test_settlement.settlement_goods.buy_trading_good(test_trading_form)

        self.assertEqual(self.test_settlement.gold, 30)
        self.assertEqual(self.test_settlement.trading_goods["rubins"], 4)

    def test_buy_goods2(self):
        self.test_settlement.gold = 19
        self.test_settlement.trading_goods["rubins"] = 2

        self.assertEqual(self.test_settlement.gold, 19)
        self.assertEqual(self.test_settlement.trading_goods["rubins"], 2)

        test_trading_form = TradingForm(
            magnitude=self.test_magnitude, price=self.test_price
        )
        is_affordable = self.test_settlement.settlement_goods.is_affordable(
            test_trading_form
        )
        self.assertEqual(is_affordable, False)

        self.test_settlement.gold = 19
        self.assertEqual(self.test_settlement.gold, 19)
        is_affordable = self.test_settlement.settlement_goods.is_affordable(
            test_trading_form
        )
        self.assertEqual(is_affordable, False)

        self.test_settlement.gold = 20
        self.assertEqual(self.test_settlement.gold, 20)
        is_affordable = self.test_settlement.settlement_goods.is_affordable(
            test_trading_form
        )
        self.assertEqual(is_affordable, True)

    def test_buy_goods3(self):
        self.test_settlement.gold = 1
        self.test_good = "rubins"
        self.test_settlement.trading_goods["rubins"] = 0

        self.assertEqual(self.test_settlement.gold, 1)
        self.assertEqual(self.test_settlement.trading_goods["rubins"], 0)
        test_trading_form = TradingForm(
            good=self.test_good, magnitude=self.test_magnitude, price=self.test_price
        )

        self.test_settlement.settlement_goods.buy_trading_good(test_trading_form)

        self.assertEqual(self.test_settlement.gold, 1)
        self.assertEqual(self.test_settlement.trading_goods["rubins"], 0)

    def test_sell_goods(self):
        self.test_settlement.gold = 0
        self.test_good = "rubins"
        self.test_settlement.trading_goods["rubins"] = 2

        self.assertEqual(self.test_settlement.gold, 0)
        self.assertEqual(self.test_settlement.trading_goods["rubins"], 2)
        test_trading_form = TradingForm(
            good=self.test_good, magnitude=self.test_magnitude, price=self.test_price
        )
        self.test_settlement.settlement_goods.sell_trading_good(test_trading_form)
        self.assertEqual(self.test_settlement.trading_goods["rubins"], 0)
        self.assertEqual(self.test_settlement.gold, 20)

        def test_sell_goods2(self):
            self.test_settlement.gold = 0
            self.test_good = "rubins"
            self.test_settlement.trading_goods["rubins"] = 0

            self.assertEqual(self.test_settlement.gold, 0)
            self.assertEqual(self.test_settlement.trading_goods["rubins"], 2)
            test_trading_form = TradingForm(
                good=self.test_good,
                magnitude=self.test_magnitude,
                price=self.test_price,
            )
            self.test_settlement.settlement_goods.sell_trading_good(test_trading_form)
            self.assertEqual(self.test_settlement.trading_goods["rubins"], 0)
            self.assertEqual(self.test_settlement.gold, 0)

    def test_transaction(self):
        self.test_good = "rubins"
        self.test_ladder.create_ladder_entry(
            self.test_settlement,
            self.test_good,
            self.test_magnitude,
            self.test_price,
            EntryType.BID,
        )

        self.test_good = "rubins"
        self.test_ladder.create_ladder_entry(
            self.test_settlement2,
            self.test_good,
            self.test_magnitude,
            self.test_price,
            EntryType.ASK,
        )

        self.test_ladder.resolve()

        resolution = self.test_ladder.resolutions[0]

        test_transaction_magnitude = self.test_trade.get_transaction_magnitudes(
            resolution.bid, resolution.ask
        )
        self.assertEqual(test_transaction_magnitude, self.test_magnitude)
        test_transaction = self.test_trade.transaction(resolution)


if __name__ == "__main__":
    unittest.main()
