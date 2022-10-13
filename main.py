import features.features as ft
import matplotlib.pyplot as plt
import numpy as np
import open3d
import os

root_dir = 'LabeledDB_new'

flag = True

row = 1
for sub_fold in os.listdir(root_dir):
    d = os.path.join(root_dir, sub_fold)
    for file in os.listdir(d):
        if file.endswith('.off'):
            off_path = root_dir+'/'+sub_fold+'/'+file
            mesh = open3d.io.read_triangle_mesh(off_path)
            points = np.asarray(mesh.vertices)
            
            # a1 = ft.A1(points, 5000)
            # d1 = ft.D1(points, 5000)
            d2 = ft.D2(points, 5000)
            # d3 = ft.D3(points, 5000)
            # d4 = ft.D4(points, 5000)

            ft.bin(d2, 0, 2, 20)

    plt.savefig(sub_fold+".pdf")
    plt.close()