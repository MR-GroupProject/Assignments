import features as ft
import open3d
import numpy as np
from tools import dataset
from tools import reader


def get_features():
    features = []
    path = []

    obj_types = reader.read_sub_fold()
    for obj_type in obj_types:
        print(obj_type)
        file_paths = reader.read_file(obj_type)
        for obj in file_paths:
            mesh = open3d.io.read_triangle_mesh(obj)
            data_features = []
            s = ft.surface_area(mesh)
            v = ft.volume(mesh)
            d = ft.diameter(mesh)
            e = ft.eccentricity(mesh)
            p = np.asarray(mesh.vertices)
            a3 = ft.bin(ft.A3(p, 5000), 0, 1, 10)
            d1 = ft.bin(ft.D1(p, 3000), 0, 1, 10)
            d2 = ft.bin(ft.D2(p, 5000), 0, 1, 10)
            d3 = ft.bin(ft.D3(p, 5000), 0, 1, 10)
            d4 = ft.bin(ft.D4(p, 5000), 0, 1, 10)

            data_features.extend([s, v, d, e])
            data_features.extend(a3)
            data_features.extend(d1)
            data_features.extend(d2)
            data_features.extend(d3)
            data_features.extend(d4)
            features.append(data_features)
            path.append(str(obj))
            print(obj)

    return features, path


wb, ws = dataset.create_table('feature_data.xlsx')
descriptors, file_path = get_features()
dataset.write_data(descriptors, ws)
wb.close()
