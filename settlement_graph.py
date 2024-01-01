#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 08:44:25 2024

@author: lukasgartmair
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math


class SettlementGraph(nx.Graph):
    def __init__(self):
        super(SettlementGraph, self).__init__()
        self = nx.Graph()

    def get_connections(self, include_data=False):
        return self.edges(data=include_data)

    def get_all_connected_settlement_ids(self):
        return np.unique(list(self.edges)).tolist()

    def get_node_data(self, node):
        print(self[node])
        return self[node]

    def print_data(self):
        print(list(self.nodes))
        print(self.nodes.data())

    def add_settlement(self, settlement):
        self.add_node(settlement.id, pos=settlement.center, name=settlement.name)

    def remove_settlement(self, settlement):
        self.remove_node(settlement.id)

    def add_settlement_connection(self, settlement_a, settlement_b, path):
        if settlement_a != settlement_b:
            self.add_edge(
                settlement_a.id,
                settlement_b.id,
                weight=1,
                path=path,
                distance=math.dist(settlement_a.center, settlement_b.center),
            )

    def remove_settlement_connection(self, settlement_a, settlement_b):
        if settlement_a != settlement_b:
            self.remove_edge(settlement_a.id, settlement_b.id)

    def is_connected(self, settlement):
        return any([(settlement.id in edge) for edge in list(self.edges)])

    def are_connected(self, settlement_a, settlement_b):
        return self.has_edge(settlement_a.id, settlement_b.id)

    def plot(self):
        fig, ax = plt.subplots()
        nx.draw(
            self,
            nx.get_node_attributes(self, "pos"),
            with_labels=True,
            labels=nx.get_node_attributes(self, "name"),
        )
