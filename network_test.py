#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 08:12:46 2024

@author: lukasgartmair
"""

import networkx as nx
import random
import itertools
from faker import Faker
import matplotlib.pyplot as plt

faker = Faker()

width = 100
height = 100

n_settlements = 5

weight = 1

def test_1():
    G = nx.Graph()

    settlements = [Settlement() for n in range(n_settlements)]

    for i,s in enumerate(settlements):

        G.add_node(s.id, pos=(i,i), name=s.name)

    print(G.nodes.data())

    e = (2, 3)

    G.add_edge(*e)

    labels = {}
    for s in settlements:
        labels[s.id] = s.name

    nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, labels=labels)
    
def test_2():
    
    settlement_graph = SettlementGraph()
        
    settlements = [Settlement() for n in range(n_settlements)]
    
    for i,s in enumerate(settlements):
        settlement_graph.add_settlement(s)

    print(settlement_graph.nodes.data())
        
    settlement_graph.plot()

class Settlement:
    id_iterator = itertools.count()

    def __init__(self):
        self.id = next(self.id_iterator)
        self.name = faker.city()
        #self.center = (random.randint(0, width), random.randint(0, height))
        self.center = (self.id, self.id)
        
class SettlementGraph(nx.Graph):

    def __init__(self):
        super(SettlementGraph, self).__init__()
        self = nx.Graph()
        
    def add_settlement(self, settlement):
        self.add_node(settlement.id, pos=settlement.center, name=settlement.name)
        
    def add_settlement_connection(self, settlement_a, settlement_b):
        self.add_edge(settlement_a.id, settlement_b)

    def plot(self):
        nx.draw(self, nx.get_node_attributes(self, 'pos'), with_labels=True, labels=nx.get_node_attributes(self, 'name'))

test_2()
