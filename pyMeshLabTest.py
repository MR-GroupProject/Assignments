import trimesh
import numpy as np
import pymeshlab
import os

from pynput import keyboard

def creat_bounding_box(bbox_max, bbox_min, dim_x, dim_y, dim_z):

    f = open('bounding_box.off', 'w')
    f.write('OFF\n')
    f.write('8 6 0\n')
    # 4 lower vertexs
    f.write(str(bbox_min[0]) + ' '+ str(bbox_min[1]) + ' ' + str(bbox_min[2]) + '\n')                    #0 000 xmin, ymin, zmin
    f.write(str(bbox_min[0] + dim_x) + ' '+ str(bbox_min[1]) + ' ' + str(bbox_min[2]) + '\n')            #1 100 xmin + dimx, ymin, zmin
    f.write(str(bbox_min[0]+ dim_x) + ' '+ str(bbox_min[1] + dim_y) + ' ' + str(bbox_min[2]) + '\n')     #2 110 xmin, ymin + dimy, zmin
    f.write(str(bbox_min[0]) + ' '+ str(bbox_min[1] + dim_y) + ' ' + str(bbox_min[2]) + '\n')            #3 010 xmin = dimx, ymin + dimy, zmin

    # 4 upper vertexs
    f.write(str(bbox_max[0]) + ' '+ str(bbox_max[1]) + ' ' + str(bbox_max[2]) + '\n')                    #4 111 xmax, ymax, zmax
    f.write(str(bbox_max[0] - dim_x) + ' '+ str(bbox_max[1]) + ' ' + str(bbox_max[2]) + '\n')            #5 011 xmax - dimx, ymax, zmax
    f.write(str(bbox_max[0]- dim_x) + ' '+ str(bbox_max[1] - dim_y) + ' ' + str(bbox_max[2]) + '\n')     #6 001 xmax, ymax - dimy, zmax
    f.write(str(bbox_max[0]) + ' '+ str(bbox_max[1] - dim_y) + ' ' + str(bbox_max[2]) + '\n')            #7 101 xmax - dimx, ymax - dimy, zmax
    
    #faces
    f.write('4 0 1 2 3\n') 
    f.write('4 4 5 6 7\n') 
    f.write('4 2 3 5 4\n') 
    f.write('4 0 1 7 6\n') 
    f.write('4 1 2 4 7\n') 
    f.write('4 0 3 5 6\n') 
    f.close()
    return



# create a new MeshSet
ms = pymeshlab.MeshSet()

# load a new mesh in the MeshSet, and sets it as current mesh
# the path of the mesh can be absolute or relative

ms.load_new_mesh("./LabeledDB_new/Ant/81.off")


#display the bounding box of current mesh
dim_x = ms.current_mesh().bounding_box().dim_x()
dim_y = ms.current_mesh().bounding_box().dim_y()
dim_z = ms.current_mesh().bounding_box().dim_z()
bbox_max = ms.current_mesh().bounding_box().max()
bbox_min = ms.current_mesh().bounding_box().min()
creat_bounding_box(bbox_max, bbox_min, dim_x, dim_y, dim_z)
ms.add_mesh("bounding_box.off")



#ms.generate_resampled_uniform_mesh(cellsize = pymeshlab.Percentage(1))
#ms.generate_sampling_montecarlo(samplenum = 100)
# print(ms.number_meshes())

# print the number of vertices and faces of the current mesh
'''
print(ms.current_mesh().face_number())
print(ms.current_mesh().vertex_number())
print(ms.current_mesh().bounding_box().dim_x())
print(ms.current_mesh().bounding_box().dim_y())
print(ms.current_mesh().bounding_box().dim_z())
print(ms.current_mesh().bounding_box().max())
print(ms.current_mesh().bounding_box().min())
print(ms.current_mesh().vertex_normal_matrix())
'''
ms.show_polyscope()

