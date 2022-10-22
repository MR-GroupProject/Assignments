import sys

import numpy as np
import open3d
import pymeshlab
import trimesh
from scipy.spatial import distance
from scipy.stats import wasserstein_distance

from tools import reader
from tools import normalize

sys.path.append("..")
from Step3 import features as ft

query_path = '../LabeledDB_new/Airplane/61.off'
ms = pymeshlab.MeshSet()
ms.load_new_mesh(query_path)

normalize.re_mesh(ms)
normalize.clean_ms(ms)

center = ms.get_geometric_measures().get('barycenter')
ms.compute_matrix_from_translation(traslmethod=3, neworigin=center)
# alignment
normalize.pca(ms)
ms.save_current_mesh('query remesh.off')
# flip
normalize.flip(ms, 'query remesh.off')

ms.save_current_mesh('query remesh.off')

query_mesh = open3d.io.read_triangle_mesh('./query remesh.off')

qef = []
qs = ft.surface_area(query_mesh)
qv = ft.volume(query_mesh)
qd = ft.diameter(query_mesh)
qe = ft.eccentricity(query_mesh)
points = np.asarray(query_mesh.vertices)
a3 = ft.bin(ft.A3(points, 5000), 0, 1, 20)
qef.extend([qs, qv, qd, qe])
qef.extend(a3)
print(qef)


def shape_descriptor():
    obj_types = reader.read_sub_fold()

    EXT_features = []
    EXT_path = []

    j = 0
    for obj_type in obj_types:
        print(obj_type)
        file_paths = reader.read_file(obj_type)
        i = 0
        if j == 10:
            break
        for obj in file_paths:
            if query_path == file_paths:
                continue
            if i == 5:
                break
            mesh = open3d.io.read_triangle_mesh(obj)
            data_features = []
            s = ft.surface_area(mesh)
            v = ft.volume(mesh)
            d = ft.diameter(mesh)
            e = ft.eccentricity(mesh)
            p = np.asarray(mesh.vertices)
            a = ft.bin(ft.A3(p, 5000), 0, 1, 20)

            data_features.extend([s, v, d, e])
            data_features.extend(a)
            EXT_features.append(data_features)
            EXT_path.append(str(obj))
            print(obj)

            i += 1
        j+=1
    return EXT_features, EXT_path


def euc(a, b):
    a = np.array(a)
    b = np.array(b)
    return (np.linalg.norm(a - b))


def co(a, b):
    return (1 - distance.cosine(a, b))


def EMD(a, b):
    return (wasserstein_distance(a, b))


def compare_feature(query_feature, database, threshold=100):
    result = []
    index = []
    dic = {}
    i = 0
    for data in database:
        dis = EMD(query_feature, data)
        dic.update({dis: i})
        if dis < threshold:
            index.append(i)
        result.append(dis)
        i += 1
    # print(result)

    return index, result, dic


database_features, database_index = shape_descriptor()
print(database_features)
print(database_index)
result_i, result_d, dic = compare_feature(qef, database_features, threshold=2)
result_d.sort()
for i in range(8):
    print(database_index[dic[result_d[i]]])

print('..')
for i in result_i:
    print(database_index[i])
