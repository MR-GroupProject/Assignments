import numpy as np
import pymeshlab
import polyscope as ps

ms = pymeshlab.MeshSet()
ms.load_new_mesh("./LabeledDB_new/Ant/82.off")
ms.generate_copy_of_current_mesh()


# Parameters:
#   cur_ms: mesh
#   n: number of remaining dimensions
# Return: [Feature valuse, feature vectors, lower dimensions matrix, rebuilded mesh's matrix]
def pca(cur_ms):
    mesh_np = cur_ms.vertex_matrix()  # get mesh matrix
    mean_val = np.mean(mesh_np, axis=0)  # get mean of mesh's matrix
    new_mesh_np = mesh_np - mean_val  # set the mesh on new origin

    faces = cur_ms.face_matrix()

    cov_np = np.cov(new_mesh_np, rowvar=False)  # calculate the covariance matrix

    feature_val, feature_vect = np.linalg.eig(np.mat(cov_np))

    print(feature_val)
    print(feature_vect)
    feature_val_index = np.argsort(feature_val)
    print(feature_val_index)
    e1 = feature_vect[feature_val_index[2]]
    e2 = feature_vect[feature_val_index[1]]
    e3 = np.cross(e1, e2)
    m = np.array([e1, e2, e3])
    m = np.mat(m)
    # result = np.dot(mesh_np, m.T)
    m = np.insert(m, 3, [0, 0, 0], 0)
    m = np.insert(m, 3, [0, 0, 0, 1], 1)

    ms.set_matrix(transformmatrix=m)
    # ms.save_current_mesh()
    ms.show_polyscope()


pca(ms.current_mesh())
