import numpy as np
import pymeshlab
'''
ms = pymeshlab.MeshSet()
ms.load_new_mesh("./LabeledDB_new/Ant/82.off")

cur_ms = ms.current_mesh()
'''

# Parameters: 
#   cur_ms: mesh
#   n: number of remaining dimensions 
# Return: [feature vectors(this is an array with descending sorted feature vectors) , lower dimensions matrix, new mesh's matrix]
def pca(cur_ms, n):
    mesh_np = cur_ms.vertex_matrix()       # get mesh matrix
    mean_val = np.mean(mesh_np, axis=0)    # get mean of mesh's matrix
    new_mesh_np = mesh_np - mean_val       # set the mesh on new origin

    '''
    print('mesh matrix')
    print(mesh_np)
    print('mean value')
    print(mean_val)
    print('new mash matrix')
    print(new_mesh_np)
    '''

    cov_np = np.cov(new_mesh_np, rowvar=0)    #calculate the covariance matrix


    feature_val, feature_vect = np.linalg.eig(np.mat(cov_np))

    '''
    print('feature value')
    print(feature_val)
    print('feature vectors')
    print(feature_vect)
    '''
    feature_val_index = np.argsort(feature_val)
    number_feature_val_index = feature_val_index[-1:-(n+1):-1]
    number_feature_vect = feature_vect[:,number_feature_val_index]
    lowD_martix = new_mesh_np * number_feature_vect
    #rebuild_matrix = (lowD_martix * number_feature_vect.T) + mean_val

    return [number_feature_vect, lowD_martix, new_mesh_np]

# calculate the rotation matrix by feacture vector and z-axis vector
def find_rotation_matrix(number_feature_vect):
    a = np.array([0, 0, 1])
    b = number_feature_vect[0]
    b = np.squeeze(np.asarray(b))
    v = np.cross(a, b)
    s = np.linalg.norm(v)
    c = np.dot(a, b) 
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]]) 
    r = np.eye(3) + vx + np.dot(vx, vx) * (1-c)/(s**2) 
    return r

# calculate the new mesh matrix after rotation_matri
# Parameters: mesh matrix, feature vector.
def align_to_z (new_mesh_np, number_feature_vect):
    rotation_matrix = find_rotation_matrix(number_feature_vect)
    print(np.shape(rotation_matrix))
    print(np.shape(new_mesh_np))
    new_mesh_np = new_mesh_np.dot(rotation_matrix)

    return new_mesh_np

