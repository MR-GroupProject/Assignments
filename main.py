import features.features as ft
import matplotlib.pyplot as plt
import matplotlib.transforms as mt
import numpy as np
import open3d
import reader

obj_types = reader.read_subfold()

for obj_type in obj_types:
    file_paths = reader.read_file(obj_type)
    fig = plt.figure(figsize=(30, 5))
    
    for obj in file_paths:
        mesh = open3d.io.read_triangle_mesh(obj)
        points = np.asarray(mesh.vertices)
        plt.subplot(1, 5, 1)
        ft.bin(ft.A1(points, 5000), 0, 1, 20)
        plt.subplot(1, 5, 2)
        ft.bin(ft.D1(points, 5000), 0, 1, 20)
        plt.subplot(1, 5, 3)
        ft.bin(ft.D2(points, 5000), 0, 1, 20)
        plt.subplot(1, 5, 4)
        ft.bin(ft.D3(points, 5000), 0, 1, 20)
        plt.subplot(1, 5, 5)
        ft.bin(ft.D4(points, 5000), 0, 1, 20)
    plt.tight_layout()
    plt.savefig("features/All_"+obj_type+".pdf")
    # fig.savefig(
    #     "features/A1_"+obj_type+".pdf",
    #     bbox_inches = mt.Bbox([[0, 0], [0.2, 1]]).transformed(
    #         fig.transFigure - fig.dpi_scale_trans
    #     )
    # )
    # fig.savefig(
    #     "features/D1_"+obj_type+".pdf",
    #     bbox_inches = mt.Bbox([[0.2, 0], [0.4, 1]]).transformed(
    #         fig.transFigure - fig.dpi_scale_trans
    #     )
    # )
    # fig.savefig(
    #     "features/D2_"+obj_type+".pdf",
    #     bbox_inches = mt.Bbox([[0.4, 0], [0.6, 1]]).transformed(
    #         fig.transFigure - fig.dpi_scale_trans
    #     )
    # )
    # fig.savefig(
    #     "features/D3_"+obj_type+".pdf",
    #     bbox_inches = mt.Bbox([[0.6, 0], [0.8, 1]]).transformed(
    #         fig.transFigure - fig.dpi_scale_trans
    #     )
    # )
    # fig.savefig(
    #     "features/D4_"+obj_type+".pdf",
    #     bbox_inches = mt.Bbox([[0.8, 0], [1, 1]]).transformed(
    #         fig.transFigure - fig.dpi_scale_trans
    #     )
    # )
    plt.close()
    break