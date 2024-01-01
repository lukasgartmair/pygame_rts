#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 08:44:25 2024

@author: lukasgartmair
"""

import networkx as nx
import matplotlib.pyplot as plt
        
class SettlementGraph(nx.Graph):

    def __init__(self):
        super(SettlementGraph, self).__init__()
        self = nx.Graph()
        
    def add_settlement(self, settlement):
        self.add_node(settlement.id, pos=settlement.center, name=settlement.name)
        
    def remove_settlement(self, settlement):
        self.remove_node(settlement.id)
        
    def add_settlement_connection(self, settlement_a, settlement_b):
        if settlement_a != settlement_b:
            self.add_edge(settlement_a.id, settlement_b.id, weight=1)

    def remove_settlement_connection(self, settlement_a, settlement_b):
        if settlement_a != settlement_b:
            self.remove_edge(settlement_a.id, settlement_b.id)

    def plot(self):
        fig, ax = plt.subplots()
        nx.draw(self, nx.get_node_attributes(self, 'pos'), with_labels=True, labels=nx.get_node_attributes(self, 'name'))