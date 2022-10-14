import features.features as ft
import matplotlib.pyplot as plt
import numpy as np
import open3d
import reader

obj_types = reader.read_subfold()

for obj_type in obj_types:
    a1s = []
    # d1s = []
    # d2s = []
    # d3s = []
    # d4s = []
    file_paths = reader.read_file(obj_type)
    for obj in file_paths:
        mesh = open3d.io.read_triangle_mesh(obj)
        points = np.asarray(mesh.vertices)
        a1s.append(ft.A1(points, 5000))
        # d1s.append(ft.D1(points, 5000))
        # d2s.append(ft.D2(points, 5000))
        # d3s.append(ft.D3(points, 5000))
        # d4s.append(ft.D4(points, 5000))
    
    plt.xlim(0, 180)
    for i in a1s:
        ft.bin(i, 0, 180, 45)
    plt.savefig("features/"+obj_type+"_a1.pdf")
    plt.close()