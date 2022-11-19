from step3 import features as ft
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import open3d
from tools import reader, dataset

# import visualize as vz
all_features = dataset.get_all_data('../data/feature_data_6_n_20bin.xlsx')
database_features = np.asarray(all_features)[:, :-1].astype(float)
database_filepaths = np.asarray(all_features)[:, -1:]
const_features = database_features[:, :6]


def boxplot(data, ranges, title, xlabel='', ylabel='', show=False, save=''):
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

    ax.set_xticklabels(ranges)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.yaxis.grid(True)
    if show:
        plt.show()
    if save != '':
        plt.savefig("../visualization/elementary" + save)


def shape_descriptor():
    obj_types = reader.read_sub_fold()

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


def shape_property_grouped():
    obj_types = reader.read_sub_fold()
    matplotlib.rcParams['xtick.labelsize'] = 30
    matplotlib.rcParams['ytick.labelsize'] = 30
    title = ['A3', 'D1', 'D2', 'D3', 'D4']
    for i in range(5):
        fig = plt.figure(figsize=(45, 45))
        j = 1
        if i < 1:
            continue
        for obj_type in obj_types:
            plt.subplot(5, 4, j)
            plt.ylim(0, 0.6)
            file_paths = reader.read_file(obj_type)
            print(j)
            for obj in file_paths:
                mesh = open3d.io.read_triangle_mesh(obj)
                points = np.asarray(mesh.vertices)
                if i == 0:
                    x, y = ft.bin(ft.A3(points, 3000), 20)
                elif i == 1:
                    x, y = ft.bin(ft.D1(points, 1500), 20)
                elif i == 2:
                    x, y = ft.bin(ft.D2(points, 2000), 20)
                elif i == 3:
                    x, y = ft.bin(ft.D3(points, 2000), 20)
                else:
                    x, y = ft.bin(ft.D4(points, 2000), 20)
                plt.plot(x, y)
            plt.title(title[i] + ' for group: ' + obj_type, fontsize=30, fontweight='semibold')
            j += 1

        plt.tight_layout()
        plt.subplots_adjust(wspace=0.12, hspace=0.2)
        fig.savefig("../visualization/bins/bin_" + str(i) + ".pdf")
        plt.close()
        break


shape_descriptor()
shape_property_grouped()
