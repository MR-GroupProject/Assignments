from sklearn.decomposition import PCA

import math
import matplotlib.pyplot as plt
import numpy as np
import open3d
import pandas as pd


def surface_area(mesh):
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
    return area


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


def aabb(mesh):
    return open3d.geometry.AxisAlignedBoundingBox.get_axis_aligned_bounding_box(mesh)


def diameter(mesh):
    ch_mesh, ch_indeces = open3d.geometry.TriangleMesh.compute_convex_hull(mesh)
    points = np.asarray(mesh.vertices)
    ch_points = []
    diameter = 0
    for i in ch_indeces:
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
    l = points.shape[0]

    sample = []

    for i in range(n):
        indeces = np.random.choice(l, 3, replace=False)
        vec1 = points[indeces[1]] - points[indeces[0]]
        vec2 = points[indeces[2]] - points[indeces[0]]
        arc = math.acos(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        sample.append(arc / math.pi)
    return sample


def D1(points, n):
    l = points.shape[0]

    sample = []

    for i in range(n):
        index = np.random.randint(l)
        distance = np.linalg.norm(points[index])
        sample.append(round(distance, 5))
    return sample


def D2(points, n):
    l = points.shape[0]

    sample = []

    for i in range(n):
        indeces = np.random.choice(l, 2, replace=False)
        vec = points[indeces[1]] - points[indeces[0]]
        distance = np.linalg.norm(vec)
        sample.append(round(distance / 2, 5))
    return sample


def D3(points, n):
    l = points.shape[0]

    sample = []

    max_area = np.sqrt(3) * 0.75

    for i in range(n):
        indeces = np.random.choice(l, 3, replace=False)
        vec1 = points[indeces[1]] - points[indeces[0]]
        vec2 = points[indeces[2]] - points[indeces[0]]
        area = np.linalg.norm(abs(np.cross(vec1, vec2)) / 2)
        sample.append(round(area / max_area, 5))
    return sample


def D4(points, n):
    l = points.shape[0]

    sample = []

    max_volume = np.sqrt(64 / 243)

    for i in range(n):
        indeces = np.random.choice(l, 4, replace=False)
        row0 = np.append(points[indeces[0]], 1)
        row1 = np.append(points[indeces[1]], 1)
        row2 = np.append(points[indeces[2]], 1)
        row3 = np.append(points[indeces[3]], 1)
        det = [row0, row1, row2, row3]
        sample.append(round(abs(np.linalg.det(det)) / (6 * max_volume), 5))
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
    plt.plot(x, y)
    return y
