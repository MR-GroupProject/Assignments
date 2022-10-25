from sklearn.decomposition import PCA
from tools import normalize
import math
import matplotlib.pyplot as plt
import numpy as np
import open3d
import pandas as pd


'''def surface_area(mesh):
    area = 0
    vertices = np.asarray(mesh.vertices)
    faces = np.asarray(mesh.triangles)
    for face in faces:
        a = face[0]
        b = face[1]
        c = face[2]
        ba = vertices[b] - vertices[a]
        ca = vertices[c] - vertices[a]
        area += np.linalg.norm(np.cross(ba, ca)) / 2
    return area'''


def surface_area(mesh):
    return mesh.get_surface_area()


def compactness(mesh):
    a = mesh.get_surface_area()
    v = volume(mesh)
    return pow(a, 3) / (36 * math.pi * pow(v, 2))


def volume(mesh):
    area = 0
    vertices = np.asarray(mesh.vertices)
    faces = np.asarray(mesh.triangles)
    for face in faces:
        a = face[0]
        b = face[1]
        c = face[2]
        area += np.dot(np.cross(vertices[a], vertices[b]), vertices[c]) / 6
    return area


def rectangularity(mesh):
    v = volume(mesh)
    bbox = open3d.geometry.AxisAlignedBoundingBox.get_axis_aligned_bounding_box(mesh)
    bbox_v = bbox.volume()
    return v / bbox_v


def diameter(mesh):
    ch_mesh, ch_index = open3d.geometry.TriangleMesh.compute_convex_hull(mesh)
    points = np.asarray(mesh.vertices)
    ch_points = []
    diameter = 0
    for i in ch_index:
        point = points[i]
        for ch_point in ch_points:
            distance = np.linalg.norm(point - ch_point)
            if (distance > diameter):
                diameter = distance
        ch_points.append(point)
    return diameter


def eccentricity(mesh):
    points_df = pd.DataFrame(np.asarray(mesh.vertices))
    pca = PCA(n_components=3)
    pca.fit(points_df)
    lambdas = pca.explained_variance_
    return lambdas[0] / lambdas[2]


def A3(points, n):
    sample = []

    for i in range(n):
        index = np.random.choice(points.shape[0], 3, replace=False)
        vec1 = points[index[1]] - points[index[0]]
        vec2 = points[index[2]] - points[index[0]]
        arc = math.acos(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        sample.append(arc / math.pi)
    return sample


def D1(points, n):
    sample = []

    for i in range(n):
        index = np.random.randint(points.shape[0])
        distance = np.linalg.norm(points[index])
        sample.append(distance)
    sample = normalize.normalization(sample)
    return sample


def D2(points, n):
    sample = []

    for i in range(n):
        index = np.random.choice(points.shape[0], 2, replace=False)
        vec = points[index[1]] - points[index[0]]
        distance = np.linalg.norm(vec)
        sample.append(distance)
    sample = normalize.normalization(sample)
    return sample


def D3(points, n):
    sample = []
    # max_area = np.sqrt(3) * 0.75

    for i in range(n):
        index = np.random.choice(points.shape[0], 3, replace=False)
        vec1 = points[index[1]] - points[index[0]]
        vec2 = points[index[2]] - points[index[0]]
        area = np.linalg.norm(abs(np.cross(vec1, vec2)) / 2)
        sample.append(area)
    sample = normalize.normalization(sample)
    return sample


def D4(points, n):
    sample = []
    # max_volume = np.sqrt(64 / 243)

    for i in range(n):
        index = np.random.choice(points.shape[0], 4, replace=False)
        row0 = np.append(points[index[0]], 1)
        row1 = np.append(points[index[1]], 1)
        row2 = np.append(points[index[2]], 1)
        row3 = np.append(points[index[3]], 1)
        det = [row0, row1, row2, row3]
        sample.append(abs(np.linalg.det(det)) / 6)
    sample = normalize.normalization(sample)
    return sample


def bin(sample, low, high, n):
    step = (high - low) / n
    bins = []
    for i in range(n):
        bins.append(round(low + step * i, 4))
    bins.append(high)
    labels = bins[:n]
    cut = pd.cut(sample, bins, labels=labels)
    count = pd.value_counts(cut)
    x = labels
    y = [count[i] for i in labels]
    y = normalize.bin_normalization(y, len(sample))

    return x, y


def get_feature(filepath):
    mesh = open3d.io.read_triangle_mesh(filepath)
    data_features = []
    s = surface_area(mesh)
    c = compactness(mesh)
    v = rectangularity(mesh)
    d = diameter(mesh)
    e = eccentricity(mesh)
    p = np.asarray(mesh.vertices)
    x1, a3 = bin(A3(p, 3000), 0, 1, 10)
    x2, d1 = bin(D1(p, 3000), 0, 1, 10)
    x3, d2 = bin(D2(p, 3000), 0, 1, 10)
    x4, d3 = bin(D3(p, 3000), 0, 1, 10)
    x5, d4 = bin(D4(p, 3000), 0, 1, 10)

    data_features.extend([s, c, v, d, e])
    data_features.extend(a3)
    data_features.extend(d1)
    data_features.extend(d2)
    data_features.extend(d3)
    data_features.extend(d4)
    return data_features
