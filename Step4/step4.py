import numpy as np
import open3d
import pymeshlab
from scipy.spatial import distance
from scipy.stats import wasserstein_distance

from tools import dataset
from tools import normalize
from Step3 import features as ft

query_path = '../LabeledDB_new/Ant/82.off'
tmp_save = './query remesh.off'
ms = pymeshlab.MeshSet()
ms.load_new_mesh(query_path)

normalize.re_mesh(ms)
normalize.clean_ms(ms)

center = ms.get_geometric_measures().get('barycenter')
ms.compute_matrix_from_translation(traslmethod=3, neworigin=center)
# alignment
normalize.pca(ms)
ms.save_current_mesh(tmp_save)
# flip
normalize.flip(ms, tmp_save)
# scaling
ms.compute_matrix_from_scaling_or_normalization(unitflag=True)
ms.save_current_mesh(tmp_save)

query_mesh = open3d.io.read_triangle_mesh(tmp_save)
qef = ft.get_feature(tmp_save)


'''def shape_descriptor():
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
    return EXT_features, EXT_path'''


def euc(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.linalg.norm(a - b)


def co(a, b):
    return distance.cosine(a, b)


def EMD(a, b):
    t = np.array(range(10))
    return wasserstein_distance(t, t, a, b)


def compare_feature(query_feature, database, threshold=100):
    result = []
    indexes = []
    dic = {}
    index = 0
    for data in database:
        dist = EMD(query_feature, data)
        dic.update({dist: index})
        if dist < threshold:
            indexes.append(index)
        result.append(dist)
        index += 1
    # print(result)

    return indexes, result, dic


'''database_features, database_index = shape_descriptor()
print(database_features)
print(database_index)'''


all_features = dataset.get_all_data('../feature_data_normed.xlsx')
database_filepath = np.asarray(all_features)[:, -1:]
database_features = np.asarray(all_features)[:, :-1].astype(float)
# normed_features = database_features[:, :5]
# normed_features = normalize.standardization(normed_features)
# database_features[:, :5] = normed_features
# qef = np.asarray(qef)[5:]
'''result_i, result_d, dic = compare_feature(qef, database_features, threshold=2)
result_d.sort()
for i in range(11):
    print(database_filepath[dic[result_d[i]]])'''

distance_results = []
for i in range(5):
    d = database_features[:, (i*10+5):(i*10+15)]
    d_q = np.asarray(qef)[(i*10+5):(i*10+15)]
    result_i, result_d, dic = compare_feature(d_q, d, threshold=2)
    distance_results.append(result_d)
    print('..')
    result_d.sort()
    for i in range(11):
        print(database_filepath[dic[result_d[i]]])





'''for i in result_i:
    print(database_filepath[i])'''
