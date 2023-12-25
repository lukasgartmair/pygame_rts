#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 22:13:25 2023

@author: lukasgartmair
"""

import unittest
from path import dict_key_contains_string
from path import get_adjacent_cells

class TestMethods(unittest.TestCase):

    def test_dict_key_contains_string(self):
        test_string = 'munich'
        test_tuple = ('munich','cologne')
        self.assertEqual(dict_key_contains_string(test_string, test_tuple), True)
        test_string = 'bremen'
        self.assertEqual(dict_key_contains_string(test_string, test_tuple), False)
        
    def test_get_adjacent_cells(self):
        
        test_x = 0
        test_y = 0
        
        solution = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        result = get_adjacent_cells(test_x, test_y, k=1)
        
        for i,s in enumerate(result):
            self.assertEqual(result[i], solution[i])
            
        solution = [(-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (0, -2), (0, -1), (0, 1), (0, 2), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2)]
        
        result = get_adjacent_cells(test_x, test_y, k=2)
        
        for i,s in enumerate(result):
            self.assertEqual(result[i], solution[i])