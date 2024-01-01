#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 08:09:39 2024

@author: lukasgartmair
"""

import pygame
import trade
import settlement
import matplotlib.pyplot as plt
import numpy as np
import dist

game_trade = trade.Trade()

number_of_settlements = 5

possible_trading_goods = 