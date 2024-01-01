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
import simpy
import settlement

class TradingSimulator:
    def __init__(self):
        self.number_of_settlements = 5
        self.settlements = [settlement()
                            for i in range(self.number_of_settlements)]

    def initialize_settlements(self):
