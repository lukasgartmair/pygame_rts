#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 14:05:38 2023

@author: lukasgartmair
"""

import pygame
import random

TRADE = None
SECOND = None

def register_trade():
    trade = pygame.USEREVENT + 1

    pygame.time.set_timer(trade, 1000)

    return trade

def register_count_second():
    countsecond = pygame.USEREVENT + 2

    pygame.time.set_timer(countsecond, 1000)

    return countsecond