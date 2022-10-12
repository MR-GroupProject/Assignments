from pandas import DataFrame as df

import math
import matplotlib.pyplot as plt
import numpy as np
import open3d
import pandas as pd


file_path = "./LabeledDB_new/Airplane/75.off"

mesh = open3d.io.read_triangle_mesh(file_path)

vertices = np.asarray(mesh.vertices)
triangles = np.asarray(mesh.triangles)

open3d.geometry.TriangleMesh.get_surface_area(mesh)
open3d.geometry.TriangleMesh.get_volume(mesh)
open3d.geometry.AxisAlignedBoundingBox.get_axis_aligned_bounding_box(mesh)


def pca(mesh, n):
    mesh_np = mesh.vertices       # get mesh matrix
    mean_val = np.mean(mesh_np, axis=0)    # get mean of mesh's matrix
    new_mesh_np = mesh_np - mean_val       # set the mesh on new origin

    cov_np = np.cov(new_mesh_np, rowvar=0)    #calculate the covariance matrix

    feature_val, feature_vect = np.linalg.eig(np.mat(cov_np))

    feature_val_index = np.argsort(feature_val)
    number_feature_val_index = feature_val_index[-1:-(n+1):-1]
    number_feature_vect = feature_vect[:,number_feature_val_index]
    lowD_martix = new_mesh_np * number_feature_vect
    #rebuild_matrix = (lowD_martix * number_feature_vect.T) + mean_val

    return [number_feature_vect, lowD_martix, new_mesh_np]

"""
Self-implemented surface area computing
"""

# def surface_area(vertices, faces):
#     area = 0
#     for face in faces:
#         a = face[0]
#         b = face[1]
#         c = face[2]
#         ba = vertices[b]-vertices[a]
#         ca = vertices[c]-vertices[a]
#         area += np.linalg.norm(np.cross(ba, ca))/2
#     return area

"""
Self-implemented volume computing
"""

# def volume(vertices, faces):
#     area = 0
#     for face in faces:
#         a = face[0]
#         b = face[1]
#         c = face[2]
#         area += np.dot(np.cross(vertices[a], vertices[b]), vertices[c])/6
#     return area

def A1(points, n):
    l = points.shape[0]
    
    sample = []

    for i in range(n):
        indeces = np.random.randint(0, l, 3)
        vec1 = points[indeces[1]]-points[indeces[0]]
        vec2 = points[indeces[2]]-points[indeces[0]]
        arc = math.acos(np.dot(vec1, vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2)))
        sample.append(math.degrees(arc))
    return sample

def D1(points, n):
    l = points.shape[0]
    
    sample = []

    for i in range(n):
        index = np.random.randint(0, l)
        distance = np.linalg.norm(points[index])
        sample.append(distance)
    return sample

def D2(points, n):
    l = points.shape[0]
    
    sample = []

    for i in range(n):
        indeces = np.random.randint(0, l, 2)
        vec = points[indeces[1]]-points[indeces[0]]
        distance = np.linalg.norm(vec)
        sample.append(distance)
    return sample

def D3(points, n):
    l = points.shape[0]
    
    sample = []

    for i in range(n):
        indeces = np.random.randint(0, l, 3)
        vec1 = points[indeces[1]]-points[indeces[0]]
        vec2 = points[indeces[2]]-points[indeces[0]]
        area = np.linalg.norm(abs(np.cross(vec1, vec2))/2)
        sample.append(area)
    return sample

def D4(points, n):
    l = points.shape[0]
    
    sample = []

    for i in range(n):
        indeces = np.random.randint(0, l, 4)
        row0 = points[indeces[0]].append(1)
        row1 = points[indeces[1]].append(1)
        row2 = points[indeces[2]].append(1)
        row3 = points[indeces[3]].append(1)
        det = [row0, row1, row2, row3]
        sample.append(abs(np.linalg.det(det))/6)
    return sample

def bin(sample, low, high, n):
    step = (high-low)/n
    bins = []
    for i in range(n):
        bins.append(round(low+step*i, 4))
    bins.append(high)
    labels = bins[:n]
    cut = pd.cut(sample, bins, labels=labels)
    count = pd.value_counts(cut)
    x = labels
    y = [count[i] for i in labels]
    plt.plot(x, y)
    plt.savefig("feature.png")

sample = D2(vertices, 5000)
bins = bin(sample, 0, 2, 200)


# plt.plot()
# plt.show()