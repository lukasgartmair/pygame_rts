#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 11:42:48 2024

@author: lukasgartmair
"""


import numpy as np

from CGAL.CGAL_Kernel import Point_3
from CGAL.CGAL_Triangulation_3 import Delaunay_triangulation_3


class Delauny:


    def run(self, points):
        if isinstance(points, list):    

            # points = np.random.rand(10,3)*100
            points =  np.array(points).astype(np.float32)

        vertices = []
        for p in points:
            vertices.append(Point_3(p[0], p[1], p[2]))

        T = Delaunay_triangulation_3(vertices)
        tri_verts = [v for v in T.all_vertices()]

        verts = []
        for t in tri_verts:
            verts.append((t.point().x(), t.point().y(), t.point().z()))

        verts = np.round(verts).astype(int)
        
        tri_edges = [v for v in T.all_edges()]
        
        edges = []
        for t in tri_edges[:1]:
            x = np.round(t.first.vertex(0).point().x())
            print(x)
            y =  np.round(t.first.vertex(0).point().y())
            print(y)
            x = np.round(t.first.vertex(1).point().x())
            print(x)
            y =  np.round(t.first.vertex(1).point().y())
            print(y)
            x = np.round(t.first.vertex(2).point().x())
            print(x)
            y =  np.round(t.first.vertex(2).point().y())
            print(y)
            x = np.round(t.first.vertex(3).point().x())
            print(x)
            y =  np.round(t.first.vertex(3).point().y())
            print(y)

            edges.append(())
        edges = np.round(edges).astype(int)

        faces = []
        for t in tri_verts:
            verts.append((t.point().x(), t.point().y(), t.point().z()))

        verts = np.round(verts).astype(int)


        return verts, edges, faces


def test_delauny():
    # points = np.random.rand(10, 3)*100
    points =     [
        [-1, -1, -1],
        [+1, -1, -1],
        [+1, +1, -1],
        [-1, +1, -1],
        [-1, -1, +1],
        [+1, -1, +1],
        [+1, +1, +1],
        [-1, +1, +1],
    ]
    d = Delauny()
    v, e, f = d.run(points)
    print(v)
    print(e)
    print(f)