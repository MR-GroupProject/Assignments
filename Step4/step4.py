import sys

import numpy as np
import open3d
import pymeshlab
import resampling
import transform
from scipy.spatial import distance
from scipy.stats import wasserstein_distance

from Tools import reader

sys.path.append("..")
from Step3 import features as ft

query_path = '../LabeledDB_new/Airplane/61.off'
ms = pymeshlab.MeshSet()
query_mesh = ms.load_new_mesh(query_path)

query_mesh = transform.translation(ms, query_path)
query_mesh = resampling.re_mesh(ms = query_mesh)

ms.save_current_mesh('query remesh.off')

query_mesh = open3d.io.read_triangle_mesh('./query remesh.off')


qef = []
qs = ft.surface_area(query_mesh)
qv = ft.volume(query_mesh)
qd = ft.diameter(query_mesh)
qe = ft.eccentricity(query_mesh)
qef.extend([qs, qv, qd, qe])
print(qef)

def shape_descriptor():
    obj_types = reader.read_subfold()

    EXT_features = []
    EXT_path = []
    for obj_type in obj_types:
        print(obj_type)
        file_paths = reader.read_file(obj_type)
        for obj in file_paths:

            mesh = open3d.io.read_triangle_mesh(obj)

            s = ft.surface_area(mesh)
            v = ft.volume(mesh)
            d = ft.diameter(mesh)
            e = ft.eccentricity(mesh)

            EXT_features.append([s,v,d,e])
            EXT_path.append(str(obj))
            print(obj)
            print([s,v,d,e])
    return EXT_features, EXT_path

def euc (a, b):
    a = np.array(a)
    b = np.array(b)
    return(np.linalg.norm(a-b))

def co(a, b):
    return(1 - distance.cosine(a, b))

def EMD(a, b):
    return(wasserstein_distance(a, b))

def compare_feature(query_feature, database, threshold=100):
    result = []
    index = []
    i = 0
    for data in database:
        dis = EMD(query_feature, data)
        if dis < threshold:
            index.append(i)
        result.append(dis)
        i += 1
    print(result)
    
    return index



database_features, database_index = shape_descriptor()
print(database_features)
print(database_index)
result = compare_feature(qef, database_features, threshold=2)
for i in result:
    print(database_index[i])