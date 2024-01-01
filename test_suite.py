#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 22:13:25 2023

@author: lukasgartmair
"""

import unittest
from connection_manager import get_adjacent_cells

class TestMethods(unittest.TestCase):
    def setUp(self):
        self.test_x = 0
        self.test_y = 0
        
    def test_get_adjacent_cells(self):


        solution = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        result = get_adjacent_cells(self.test_x, self.test_y, k=1)

        for i, s in enumerate(result):
            self.assertEqual(result[i], solution[i])

        solution = [
            (-2, -2),
            (-2, -1),
            (-2, 0),
            (-2, 1),
            (-2, 2),
            (-1, -2),
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (-1, 2),
            (0, -2),
            (0, -1),
            (0, 1),
            (0, 2),
            (1, -2),
            (1, -1),
            (1, 0),
            (1, 1),
            (1, 2),
            (2, -2),
            (2, -1),
            (2, 0),
            (2, 1),
            (2, 2),
        ]

        result = get_adjacent_cells(self.test_x, self.test_y, k=2)

        for i, s in enumerate(result):
            self.assertEqual(result[i], solution[i])

if __name__ == "__main__":
    unittest.main()
