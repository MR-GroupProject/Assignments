import features.features as ft
import matplotlib.pyplot as plt
import matplotlib.transforms as mt
import numpy as np
import open3d
import reader

mesh = open3d.io.read_triangle_mesh(("./LabeledDB_new/Airplane/72.off"))

def diameter(mesh):
    ch_mesh, ch_indeces = open3d.geometry.TriangleMesh.compute_convex_hull(mesh)
    points = np.asarray(mesh.vertices)
    ch_points = []
    diameter = 0
    for i in ch_indeces:
        point = points[i]
        for ch_point in ch_points:
            distance = np.linalg.norm(point-ch_point)
            if(distance > diameter):
                diameter = distance
        ch_points.append(point)
    return diameter
    
diameter(mesh)