#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 14:32:31 2024

@author: lukasgartmair
"""

import unittest

loader = unittest.TestLoader()
start_dir = "."
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()

if __name__ == "__main__":
    runner.run(suite)
