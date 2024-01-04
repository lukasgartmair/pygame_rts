#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 19:52:51 2024

@author: lukasgartmair
"""

from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("pathing_c.pyx")
)
