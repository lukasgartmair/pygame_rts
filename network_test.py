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
import unittest
from settlement_graph import SettlementGraph

faker = Faker()

width = 100
height = 100

n_settlements = 5

weight = 1

from faker import Faker

faker = Faker()
plot = False

def get_number_of_edges(n):
    return n*(n-1)/2

class TestSettlement:
    id_iterator = itertools.count()
    
    def __init__(self):
        self.id = next(self.id_iterator)
        self.name = faker.city()
        self.center = (random.randint(0, width), random.randint(0, height))
        #self.center = (self.id, self.id)

class TestMethods(unittest.TestCase):

    def test_1(self):
        G = nx.Graph()
    
        settlements = [TestSettlement() for n in range(n_settlements)]
    
        for i,s in enumerate(settlements):
    
            G.add_node(s.id, pos=(i,i), name=s.name)
    
        print(G.nodes.data())
    
        e = (2, 3)
    
        G.add_edge(*e)
    
        labels = {}
        for s in settlements:
            labels[s.id] = s.name
        if plot:
            nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True, labels=labels)
            
    def test_1_5(self):
        G = nx.Graph()
    
        settlements = [TestSettlement() for n in range(n_settlements)]
    
        for i,s in enumerate(settlements):
            G.add_node(s.id, pos=(i,i), name=s.name)
            
        G.add_edge(s.id, 3, path=[(1,2),(0,0)])
    
        has_edge = G.has_edge(s.id, 3)
        
        self.assertEqual(has_edge, True)
        
        has_edge = G.has_edge(3, s.id)
        
        self.assertEqual(has_edge, True)

        is_connected = G.has_edge(3, s.id)
        
        self.assertEqual(has_edge, True)
        
        G.remove_node(s.id)
        has_edge = G.has_edge(s.id, 3)
        self.assertEqual(has_edge, False)
        
    def test_2(self):
        
        settlement_graph = SettlementGraph()
            
        settlements = [TestSettlement() for n in range(n_settlements)]
        
        for i,s in enumerate(settlements):
            settlement_graph.add_settlement(s)
    
        print(settlement_graph.nodes.data())
        
        if plot:
            settlement_graph.plot()
        
    def test_3(self):
        
        settlement_graph = SettlementGraph()
            
        settlements = [TestSettlement() for n in range(n_settlements)]
        
        for i,s in enumerate(settlements):
            settlement_graph.add_settlement(s)
            
        for i,s_a in enumerate(settlements):
            for j,s_b in enumerate(settlements):
                if i != j:
                    settlement_graph.add_settlement_connection(s_a, s_b)
    
        print(settlement_graph.nodes.data())
        if plot:
            settlement_graph.plot()
        
    def test_4(self):
        
        settlement_graph = SettlementGraph()
            
        settlements = [TestSettlement() for n in range(n_settlements)]
        
        print(settlements)
        
        for i,s in enumerate(settlements):
            settlement_graph.add_settlement(s)
            
        for i,s_a in enumerate(settlements):
            for j,s_b in enumerate(settlements):
                if i != j:
                    settlement_graph.add_settlement_connection(s_a, s_b)
                    
        self.assertEqual(len(settlement_graph.nodes.data()),len(settlements))

        print(settlement_graph.nodes.data())
        
        settlement_graph.remove_settlement(settlements[0])
        
        self.assertEqual(len(settlement_graph.nodes.data()),len(settlements)-1)
        if plot:
            settlement_graph.plot()
        
    def test_5(self):
        
        settlement_graph = SettlementGraph()
            
        settlements = [TestSettlement() for n in range(n_settlements)]
        
        print(settlements)
        
        for i,s in enumerate(settlements):
            settlement_graph.add_settlement(s)
            
        for i,s_a in enumerate(settlements):
            for j,s_b in enumerate(settlements):
                if i != j:
                    settlement_graph.add_settlement_connection(s_a, s_b)
                    

        self.assertEqual(len(settlement_graph.nodes.data()),len(settlements))
        self.assertEqual(len(list(settlement_graph.edges)),get_number_of_edges(n_settlements))
        print(settlement_graph.nodes.data())
        print(list(settlement_graph.edges))
        print(len(list(settlement_graph.edges)))
        settlement_graph.remove_settlement(settlements[0])
        print(len(list(settlement_graph.edges)))
        self.assertEqual(len(settlement_graph.nodes.data()),len(settlements)-1)
        self.assertEqual(len(list(settlement_graph.edges)),get_number_of_edges(n_settlements-1))
    
        if plot:
            settlement_graph.plot()
    
if __name__ == "__main__":
    unittest.main()
