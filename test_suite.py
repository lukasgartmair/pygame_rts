#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 22:13:25 2023

@author: lukasgartmair
"""

import unittest
from game_map import dict_key_contains_string

class TestMethods(unittest.TestCase):

    def test_dict_key_contains_string(self):
        test_string = 'munich'
        test_tuple = ('munich','cologne')
        self.assertEqual(dict_key_contains_string(test_string, test_tuple), True)
        test_string = 'bremen'
        self.assertEqual(dict_key_contains_string(test_string, test_tuple), False)