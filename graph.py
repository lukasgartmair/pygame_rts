#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 08:44:25 2024

@author: lukasgartmair
"""

import networkx as nx
import matplotlib.pyplot as plt

class SettlementGraph:
    
    def __init__(self):
        
        self.graph = nx.Graph()
        self.nodes = {}
        self.edges = {}
        
    def add_node(self, settlement):
        
        self.graph.add_node(settlement.id, name=settlement.name)    
        self.nodes[settlement.id]["pos"] = settlement.center
        
    def get_node_position_dict(self):
        
        for n, p in self.nodes.items():
            self.graph.nodes[n]['pos'] = p
    
    def plot(self):
        nx.draw(self.graph, self.get_node_position_dict())
        plt.show()
