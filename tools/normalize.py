import pymeshlab
import numpy as np
import trimesh


def normalization(data):
    d_min, d_max = data.min(0), data.max(0)
    norm = (data - d_min) / (d_max - d_min)
    return norm


def bin_normalization(data, n):
    new_list = []
    for i in data:
        new_list.append(round(i / n, 5))
    return new_list


def standardization(data):
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    if std.all() == 0:
        return data
    result = (data - mean) / std
    return result



def re_mesh(bottom_face_num=10000, up_face_num=15000, ms=None):
    if ms is not None:
        loop_count = 1
        while ms.current_mesh().face_number() < bottom_face_num and loop_count < 5:
            ms.meshing_surface_subdivision_loop(loopweight='Loop', iterations=1, threshold=pymeshlab.Percentage(1.0))
            loop_count += 1
        if ms.current_mesh().face_number() > up_face_num:
            ms.meshing_decimation_quadric_edge_collapse(targetfacenum=bottom_face_num, preservenormal=True,
                                                        planarquadric=True)


def pca(ms):
    mesh_np = ms.current_mesh().vertex_matrix()  # get mesh matrix
    # face_matrix = ms.face_matrix()
    cov_np = np.cov(mesh_np, rowvar=False)  # calculate the covariance matrix
    feature_val, feature_vect = np.linalg.eig(np.mat(cov_np))

    feature_val_index = np.argsort(feature_val)
    number_feature_val_index = feature_val_index[-1:-4:-1]
    number_feature_vect = feature_vect[:, number_feature_val_index]
    number_feature_vect = number_feature_vect.T

    e1 = number_feature_vect[0]
    e2 = number_feature_vect[1]
    e3 = np.cross(e1, e2)
    m = np.array([e1, e2, e3])
    m = np.mat(m)
    # result = np.dot(mesh_np, m.T)
    m = np.insert(m, 3, [0, 0, 0], 0)
    m = np.insert(m, 3, [0, 0, 0, 1], 1)

    ms.set_matrix(transformmatrix=m)  # transform the mesh


def flip(ms, file_path):
    flip_mesh = trimesh.load_mesh(file_path)
    tri_center = flip_mesh.triangles_center
    f0, f1, f2 = 0, 0, 0

    for point in tri_center:
        f0 += point[0] * point[0] * np.sign(point[0])
        f1 += point[1] * point[1] * np.sign(point[1])
        f2 += point[2] * point[2] * np.sign(point[2])

    if f0 >= 0 and f1 >= 0 and f2 >= 0:
        return 0
    else:
        if f0 < 0:
            ms.apply_matrix_flip_or_swap_axis(flipx=True)
        if f1 < 0:
            ms.apply_matrix_flip_or_swap_axis(flipy=True)
        if f2 < 0:
            ms.apply_matrix_flip_or_swap_axis(flipz=True)
        if f0 * f1 * f2 < 0:
            ms.meshing_invert_face_orientation()
        return 1


def clean_ms(ms):
    ms.meshing_remove_duplicate_faces()
    ms.meshing_remove_duplicate_vertices()
    ms.meshing_remove_folded_faces()
    ms.meshing_repair_non_manifold_edges()
    ms.meshing_edge_flip_by_planar_optimization()
    ms.meshing_repair_non_manifold_edges()
    ms.meshing_close_holes()
