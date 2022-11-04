import numpy as np
import open3d
from matplotlib import pyplot as plt

from step3 import visualize as vz
from step3 import features as ft
from tools import reader

'''vz.shape_descriptor()
vz.shape_property()'''
vz.shape_property_grouped()



def shape_property():
    fig = plt.figure(figsize=(30, 5))
    for i in range(3):
        if i == 0:
            mesh = open3d.io.read_triangle_mesh('../Remesh/Bearing/353.off')
        elif i == 1:
            mesh = open3d.io.read_triangle_mesh('../Remesh/Bearing/350.off')
        else:
            mesh = open3d.io.read_triangle_mesh('../Remesh/Bearing/349.off')
        points = np.asarray(mesh.vertices)

        plt.subplot(1, 5, 1)
        plt.ylim(0, 0.6)
        x, y = ft.bin(ft.A3(points, 8000), 0, 1, 20)
        plt.plot(x, y)
        plt.subplot(1, 5, 2)
        plt.ylim(0, 0.6)
        x, y = ft.bin(ft.D1(points, 3000), 0, 1, 20)
        plt.plot(x, y)
        plt.subplot(1, 5, 3)
        plt.ylim(0, 0.6)
        x, y = ft.bin(ft.D2(points, 5000), 0, 1, 20)
        plt.plot(x, y)
        plt.subplot(1, 5, 4)
        plt.ylim(0, 0.6)
        x, y = ft.bin(ft.D3(points, 8000), 0, 1, 20)
        plt.plot(x, y)
        plt.subplot(1, 5, 5)
        plt.ylim(0, 0.6)
        x, y = ft.bin(ft.D4(points, 8000), 0, 1, 20)
        plt.plot(x, y)

    plt.tight_layout()
    plt.savefig("../All_test_353.pdf")

    plt.close()

#shape_property()