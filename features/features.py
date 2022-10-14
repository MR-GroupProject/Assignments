import math
import matplotlib.pyplot as plt
import numpy as np
import open3d
import pandas as pd

def surface_area(mesh):
    return open3d.geometry.TriangleMesh.get_surface_area(mesh)

def volume(mesh):
    return open3d.geometry.TriangleMesh.get_volume(mesh)

def aabb(mesh):
    return open3d.geometry.AxisAlignedBoundingBox.get_axis_aligned_bounding_box(mesh)


def pca(points, n):
    mean_val = np.mean(points, axis=0)    # get mean of mesh's matrix
    new_points = points - mean_val       # set the mesh on new origin

    cov_np = np.cov(new_points, rowvar=0)    #calculate the covariance matrix

    feature_val, feature_vect = np.linalg.eig(np.mat(cov_np))

    feature_val_index = np.argsort(feature_val)
    number_feature_val_index = feature_val_index[-1:-(n+1):-1]
    number_feature_vect = feature_vect[:,number_feature_val_index]
    lowD_martix = new_points * number_feature_vect
    #rebuild_matrix = (lowD_martix * number_feature_vect.T) + mean_val

    return [number_feature_vect, lowD_martix, new_points]

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
        indeces = np.random.choice(l, 3, replace=False)
        vec1 = points[indeces[1]]-points[indeces[0]]
        vec2 = points[indeces[2]]-points[indeces[0]]
        arc = math.acos(np.dot(vec1, vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2)))
        sample.append(math.degrees(arc))
    print(np.max(sample))
    return sample

def D1(points, n):
    l = points.shape[0]
    
    sample = []

    for i in range(n):
        index = np.random.randint(l)
        distance = np.linalg.norm(points[index])
        sample.append(distance)
    return sample

def D2(points, n):
    l = points.shape[0]
    
    sample = []

    for i in range(n):
        indeces = np.random.choice(l, 2, replace=False)
        vec = points[indeces[1]]-points[indeces[0]]
        distance = np.linalg.norm(vec)
        sample.append(distance)
    return sample

def D3(points, n):
    l = points.shape[0]
    
    sample = []

    for i in range(n):
        indeces = np.random.choice(l, 3, replace=False)
        vec1 = points[indeces[1]]-points[indeces[0]]
        vec2 = points[indeces[2]]-points[indeces[0]]
        area = np.linalg.norm(abs(np.cross(vec1, vec2))/2)
        sample.append(area)
    return sample

def D4(points, n):
    l = points.shape[0]
    
    sample = []

    for i in range(n):
        indeces = np.random.choice(l, 4, replace=False)
        row0 = np.append(points[indeces[0]], 1)
        row1 = np.append(points[indeces[1]], 1)
        row2 = np.append(points[indeces[2]], 1)
        row3 = np.append(points[indeces[3]], 1)
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

