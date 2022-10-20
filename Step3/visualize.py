from Step3 import features as ft
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.transforms as mt
import numpy as np
import open3d
from Tools import reader


# import visualize as vz

def boxplot(data, range, title, xlabel='', ylabel='', show=False, save=''):
    fig, ax = plt.subplots(figsize=(16, 5))
    ax.boxplot(data,
               widths=.6,
               patch_artist=True,
               showmeans=False,
               showfliers=True,
               medianprops={"color": "white", "linewidth": 2},
               boxprops={"facecolor": "C0", "edgecolor": "white",
                         "linewidth": 0.5},
               whiskerprops={"color": "C0", "linewidth": 1.5},
               capprops={"color": "C0", "linewidth": 2},
               flierprops={"markerfacecolor": "C0", "markeredgecolor": "C0"})

    ax.set_xticklabels(range)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.yaxis.grid(True)
    if show:
        plt.show()
    if save != '':
        plt.savefig("visualization/" + save)


def shape_descriptor():
    obj_types = reader.read_subfold()

    surface_areas = []
    volumes = []
    diameters = []
    eccentricities = []

    for obj_type in obj_types:
        print(obj_type)
        file_paths = reader.read_file(obj_type)
        sfa = []
        vol = []
        dmt = []
        ect = []
        for obj in file_paths:
            mesh = open3d.io.read_triangle_mesh(obj)
            sfa.append(ft.surface_area(mesh))
            vol.append(ft.volume(mesh))
            dmt.append(ft.diameter(mesh))
            ect.append(ft.eccentricity(mesh))
            print(obj)
        surface_areas.append(sfa)
        volumes.append(vol)
        diameters.append(dmt)
        eccentricities.append(ect)

    boxplot(surface_areas, obj_types, "surface_areas", save="surface_areas.pdf")
    boxplot(volumes, obj_types, "volumes", save="volumes.pdf")
    boxplot(diameters, obj_types, "diameters", save="diameters.pdf")
    boxplot(eccentricities, obj_types, "eccentricities", save="eccentricities.pdf")


def shape_property():
    obj_types = reader.read_subfold()

    for obj_type in obj_types:
        file_paths = reader.read_file(obj_type)
        fig = plt.figure(figsize=(30, 5))

        for obj in file_paths:
            mesh = open3d.io.read_triangle_mesh(obj)
            points = np.asarray(mesh.vertices)
            plt.subplot(1, 5, 1)
            ft.bin(ft.A3(points, 5000), 0, 1, 20)
            plt.subplot(1, 5, 2)
            ft.bin(ft.D1(points, 5000), 0, 1, 20)
            plt.subplot(1, 5, 3)
            ft.bin(ft.D2(points, 5000), 0, 1, 20)
            plt.subplot(1, 5, 4)
            ft.bin(ft.D3(points, 5000), 0, 1, 20)
            plt.subplot(1, 5, 5)
            ft.bin(ft.D4(points, 5000), 0, 1, 20)
        plt.tight_layout()
        plt.savefig("features/All_" + obj_type + ".pdf")
        fig.savefig(
            "features/A1_" + obj_type + ".pdf",
            bbox_inches=mt.Bbox([[0, 0], [0.2, 1]]).transformed(
                fig.transFigure - fig.dpi_scale_trans
            )
        )
        fig.savefig(
            "features/D1_" + obj_type + ".pdf",
            bbox_inches=mt.Bbox([[0.2, 0], [0.4, 1]]).transformed(
                fig.transFigure - fig.dpi_scale_trans
            )
        )
        fig.savefig(
            "features/D2_" + obj_type + ".pdf",
            bbox_inches=mt.Bbox([[0.4, 0], [0.6, 1]]).transformed(
                fig.transFigure - fig.dpi_scale_trans
            )
        )
        fig.savefig(
            "features/D3_" + obj_type + ".pdf",
            bbox_inches=mt.Bbox([[0.6, 0], [0.8, 1]]).transformed(
                fig.transFigure - fig.dpi_scale_trans
            )
        )
        fig.savefig(
            "features/D4_" + obj_type + ".pdf",
            bbox_inches=mt.Bbox([[0.8, 0], [1, 1]]).transformed(
                fig.transFigure - fig.dpi_scale_trans
            )
        )
        plt.close()


def shape_property_grouped():
    obj_types = reader.read_subfold()
    matplotlib.rcParams['xtick.labelsize'] = 30
    matplotlib.rcParams['ytick.labelsize'] = 30
    title = ['A3', 'D1', 'D2', 'D3', 'D4']
    for i in range(5):
        fig = plt.figure(figsize=(40, 40))
        j = 1
        if i==0:
            break
        for obj_type in obj_types:
            file_paths = reader.read_file(obj_type)
            print(j)
            for obj in file_paths:
                mesh = open3d.io.read_triangle_mesh(obj)
                points = np.asarray(mesh.vertices)
                plt.subplot(5, 4, j)
                if i == 0:
                    ft.bin(ft.A3(points, 5000), 0, 1, 20)
                elif i == 1:
                    ft.bin(ft.D1(points, 5000), 0, 1, 20)
                elif i == 2:
                    ft.bin(ft.D2(points, 5000), 0, 1, 20)
                elif i == 3:
                    ft.bin(ft.D3(points, 5000), 0, 1, 20)
                else:
                    ft.bin(ft.D4(points, 5000), 0, 1, 20)
            plt.title(title[i] + ' for group: ' + obj_type, fontsize=30, fontweight='semibold')
            j += 1
        plt.tight_layout()
        plt.subplots_adjust(hspace=0.2)
        fig.savefig("Visualization/All_" + str(i) + ".pdf")
        plt.close()
