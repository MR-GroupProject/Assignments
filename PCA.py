import numpy as np
import pymeshlab

ms = pymeshlab.MeshSet()
ms.load_new_mesh("./LabeledDB_new/Ant/82.off")

cur_ms = ms.current_mesh()


# Parameters: 
#   cur_ms: mesh
#   n: number of remaining dimensions 
# Return: [Feature valuse, feature vectors, lower dimensions matrix, rebuilded mesh's matrix]
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
    rebuild_matrix = (lowD_martix * number_feature_vect.T) + mean_val

    return [feature_val, feature_vect, lowD_martix, rebuild_matrix]
