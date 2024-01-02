#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 16:47:50 2023

@author: lukasgartmair
"""
import numpy as np
from colour import Color

selection_colors = {0: (255, 125, 0)}

path_colors = {0: (21, 21, 21)}

terrain_colors = {0: (0, 21, 36), 1: (120, 41, 15)}

settlement_stats_colors = {0: (255, 236, 209)}

def get_gradients(color_a="blue", color_b="gold"):
    color_a, color_b = Color(color_a), Color(color_b)
    colours = list(color_a.range_to(color_b,20))
    colours = [c.get_rgb() for c in colours]
    colours = [tuple(np.array(c) * 255 // 1) for c in colours]
    return colours